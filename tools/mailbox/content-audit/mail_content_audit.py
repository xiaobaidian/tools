#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""邮件内容审计：逐封读取 INBOX 正文，按价值分筐，生成拟删清单（只读，不改动任何邮件）。"""
import json, imaplib, email, email.header as eh, re, os

def _load_cfg():
    import os
    for _p in [os.environ.get("SMTP_NOTIFY_CONFIG"),
               os.path.join(os.path.dirname(os.path.abspath(__file__)), "smtp_notify.json"),
               r"D:/WorkBuddyData/Tools/smtp_notify.json"]:
        if _p and os.path.exists(_p):
            return json.load(open(_p, encoding="utf-8"))
    raise FileNotFoundError("smtp_notify.json 未找到：请在脚本目录放置，或用环境变量 SMTP_NOTIFY_CONFIG 指定（详见 README）")
cfg = _load_cfg()
USER, PWD = cfg["smtp_user"], cfg["smtp_pass"]

def dec(s):
    if not s: return ""
    out = ""
    for b, enc in eh.decode_header(s):
        if isinstance(b, bytes):
            try: out += b.decode(enc or "utf-8", "ignore")
            except: out += b.decode("latin-1", "ignore")
        else: out += b
    return out

def strip_html(t):
    t = re.sub(r"<style[\s\S]*?</style>", " ", t, flags=re.I)
    t = re.sub(r"<script[\s\S]*?</script>", " ", t, flags=re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t).strip()

EXCLUDE = {"account-security-noreply@accountprotection.microsoft.com", "automated@airbnb.com"}

SEC_KW   = re.compile(r"异常登录|安全中心|account.?security|password|密码|验证码|登录验证|找回密码|security alert|new sign|sign-in attempt|异地登录|device confirmation|authenticator|两步验证|二次验证", re.I)
BILL_KW  = re.compile(r"账单|发票|订单|交易|还款|扣款|对账单|statement|invoice|order #|payment|receipt|还款提醒|信用卡|分期|账单日|月结|余额|明细", re.I)
PROMO_KW = re.compile(r"unsubscribe|退订|优惠|促销|打折|秒杀|coupon|折扣|满减|大促|限时|抢购|新品|特惠|广告|推广|双11|双十一|618|清仓|返现|抽奖|领券|立减|专属福利|会员日|周年庆|秒杀节|回馈|好礼|开抢|爆款", re.I)
SOCIAL_KW= re.compile(r"github|facebook|linkedin|twitter|微博|知乎|点赞|关注|评论|新动态|notification|new followers|有人评论|赞了|新增粉丝", re.I)

def sender_addr(frm):
    from email.utils import getaddresses
    addrs = getaddresses([frm])
    return addrs[0][1].lower() if addrs else frm.lower()

def classify(subj, frm, text):
    addr = sender_addr(frm)
    if addr in EXCLUDE: return "KEEP_SECURITY"
    if SEC_KW.search(subj + " " + frm + " " + text[:500]): return "KEEP_SECURITY"
    if BILL_KW.search(subj + " " + frm + " " + text[:500]): return "KEEP_BILL"
    if PROMO_KW.search(subj + " " + frm + " " + text[:800]): return "DELETE_PROMO"
    if SOCIAL_KW.search(frm.lower() + " " + subj.lower()): return "REVIEW_SOCIAL"
    if any(k in addr for k in ("no-reply", "noreply", "do-not-reply", "donotreply", "mailer-daemon")):
        return "REVIEW_SYSTEM"
    return "REVIEW_HUMAN"

con = imaplib.IMAP4_SSL("imap.qq.com", 993, timeout=120)
con.login(USER, PWD)
con.select("INBOX", readonly=True)
typ, uids = con.uid("search", None, "ALL")
uid_list = uids[0].split()
total = len(uid_list)
print(f"INBOX 总数={total}", flush=True)

headers, texts = {}, {}
for i in range(0, total, 80):
    batch = uid_list[i:i+80]
    typ, data = con.uid("fetch", b",".join(batch), "(UID BODY.PEEK[HEADER])")
    for item in data:
        if not (isinstance(item, tuple) and len(item) > 1): continue
        m = re.search(rb"UID (\d+)", item[0])
        if not m: continue
        uid = int(m.group(1))
        try: msg = email.message_from_bytes(item[1])
        except: continue
        headers[uid] = (dec(msg.get("Subject", "")), dec(msg.get("From", "")), msg.get("Date", ""))

for i in range(0, total, 80):
    batch = uid_list[i:i+80]
    typ, data = con.uid("fetch", b",".join(batch), "(UID BODY.PEEK[TEXT]<0.2000>)")
    for item in data:
        if not (isinstance(item, tuple) and len(item) > 1): continue
        m = re.search(rb"UID (\d+)", item[0])
        if not m: continue
        uid = int(m.group(1))
        raw = item[1]
        try: t = raw.decode("utf-8", "ignore")
        except: t = raw.decode("latin-1", "ignore")
        texts[uid] = strip_html(t)

con.logout()

buckets = {}
by_sender_delete = {}
year_dist = {}
samples = {k: [] for k in ("DELETE_PROMO", "REVIEW_SOCIAL", "REVIEW_SYSTEM", "REVIEW_HUMAN", "KEEP_BILL", "KEEP_SECURITY")}

for uidb in uid_list:
    uid = int(uidb)
    subj, frm, date = headers.get(uid, ("", "", ""))
    text = strip_html(texts.get(uid, ""))
    cat = classify(subj, frm, text)
    buckets[cat] = buckets.get(cat, 0) + 1
    addr = sender_addr(frm)
    ym = (date or "")[:4]
    year_dist[ym] = year_dist.get(ym, 0) + 1
    if cat == "DELETE_PROMO":
        by_sender_delete[addr] = by_sender_delete.get(addr, 0) + 1
    # 抽样（每类最多 12 封）
    if cat in samples and len(samples[cat]) < 12:
        samples[cat].append((frm, date, subj, text[:140]))

os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"), exist_ok=True)
out = r"D:/WorkBuddyData/Workspace/mail_audit/content_audit.md"
with open(out, "w", encoding="utf-8") as f:
    f.write("# 📬 邮箱内容审计（逐封读正文 · 只读）\n\n")
    f.write(f"- 邮箱：`{USER}` · 范围：INBOX · 共 **{total}** 封\n")
    f.write("- 说明：小秘逐封读取正文前 2000 字节，按价值分筐。**未改动任何邮件**。\n\n")
    f.write("## 分筐结果\n\n")
    f.write("| 筐 | 含义 | 数量 | 建议 |\n|---|---|---|---|\n")
    f.write(f"| KEEP_SECURITY | 安全/账号/验证码 | {buckets.get('KEEP_SECURITY',0)} | 绝不删 |\n")
    f.write(f"| KEEP_BILL | 账单/发票/订单/交易 | {buckets.get('KEEP_BILL',0)} | 保留 |\n")
    f.write(f"| DELETE_PROMO | 营销/促销/广告 | {buckets.get('DELETE_PROMO',0)} | 拟删 |\n")
    f.write(f"| REVIEW_SOCIAL | 社交动态通知 | {buckets.get('REVIEW_SOCIAL',0)} | 待定 |\n")
    f.write(f"| REVIEW_SYSTEM | 系统 no-reply 通知 | {buckets.get('REVIEW_SYSTEM',0)} | 待定 |\n")
    f.write(f"| REVIEW_HUMAN | 疑似人际/其他 | {buckets.get('REVIEW_HUMAN',0)} | 待定 |\n\n")
    f.write("## 拟删（营销类）发件人 Top\n\n")
    for a, c in sorted(by_sender_delete.items(), key=lambda x: -x[1])[:30]:
        f.write(f"- {a}: {c}\n")
    f.write("\n## 抽样预览（让你判断小秘的标准对不对）\n\n")
    labels = {"DELETE_PROMO":"拟删·营销","REVIEW_SOCIAL":"待定·社交","REVIEW_SYSTEM":"待定·系统","REVIEW_HUMAN":"待定·人际/其他","KEEP_BILL":"保留·账单","KEEP_SECURITY":"保留·安全"}
    for cat in ("DELETE_PROMO", "REVIEW_SOCIAL", "REVIEW_SYSTEM", "REVIEW_HUMAN", "KEEP_BILL", "KEEP_SECURITY"):
        f.write(f"### {labels[cat]}（{buckets.get(cat,0)} 封，抽样 {len(samples[cat])}）\n\n")
        for frm, date, subj, txt in samples[cat]:
            f.write(f"- **[{date[:16]}] {frm}**\n  - 主题：{subj}\n  - 正文：{txt}…\n")
        f.write("\n")

print("REPORT_WRITTEN", out, flush=True)
print("BUCKETS", json.dumps(buckets, ensure_ascii=False), flush=True)
