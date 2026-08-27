#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按用户规则清理 INBOX：只留 疑似人际 / 账单发票 / 公司合同·offer，其余移到专门文件夹（可找回，不硬删）。"""
import json, imaplib, email, email.header as eh, re, os, datetime

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
FOLDER = "Cleanup_20260825"
ARCH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(ARCH, exist_ok=True)

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

# ---- 保留规则关键词 ----
BILL_KW = re.compile(r"账单|发票|订单|交易|还款|扣款|对账单|statement|invoice|order #|payment|receipt|还款提醒|信用卡|分期|账单日|月结|余额|明细|缴费|话费|水电", re.I)
CONTRACT_KW = re.compile(r"合同|offer|录用|入职|劳动合同|保密协议|竞业|意向书|聘书|录取通知|签约|拟录用|薪资|薪酬|offer letter|employment|agreement|入职通知|录用通知|聘任|劳动协议|实习协议|派遣|外包协议", re.I)
SEC_KW   = re.compile(r"异常登录|安全中心|account.?security|password|密码|验证码|登录验证|找回密码|security alert|new sign|sign-in attempt|异地登录|device confirmation|authenticator|两步验证|二次验证", re.I)
PROMO_KW = re.compile(r"unsubscribe|退订|优惠|促销|打折|秒杀|coupon|折扣|满减|大促|限时|抢购|新品|特惠|广告|推广|双11|双十一|618|清仓|返现|抽奖|领券|立减|专属福利|会员日|周年庆|秒杀节|回馈|好礼|开抢|爆款", re.I)
SOCIAL_KW= re.compile(r"github|facebook|linkedin|twitter|微博|知乎|点赞|关注|评论|新动态|notification|new followers|有人评论|赞了|新增粉丝", re.I)
EXCLUDE = {"account-security-noreply@accountprotection.microsoft.com", "automated@airbnb.com"}

def sender_addr(frm):
    from email.utils import getaddresses
    addrs = getaddresses([frm])
    return addrs[0][1].lower() if addrs else frm.lower()

def classify(subj, frm, text):
    """返回 ('KEEP'|'MOVE', 理由)。仅保留：合同/offer、账单发票、疑似人际（真人发、非模式命中）。"""
    blob = subj + " " + frm + " " + text
    # 1) 合同/offer 无论被分到哪筐都抢救
    if CONTRACT_KW.search(blob):
        return ("KEEP", "合同/offer")
    # 2) 账单发票
    if BILL_KW.search(blob[:1500]):
        return ("KEEP", "账单/发票")
    # 3) 以下任一命中即移走（非保留项）
    addr = sender_addr(frm)
    if addr in EXCLUDE:
        return ("MOVE", "安全账号排除项")
    if SEC_KW.search(blob[:600]):
        return ("MOVE", "安全/验证码")
    if PROMO_KW.search(blob[:900]):
        return ("MOVE", "营销/广告")
    if SOCIAL_KW.search((frm + " " + subj).lower()):
        return ("MOVE", "社交动态")
    if any(k in addr for k in ("no-reply", "noreply", "do-not-reply", "donotreply", "mailer-daemon", "postmaster")):
        return ("MOVE", "系统no-reply")
    # 4) 其余：真人发的疑似人际，保留
    return ("KEEP", "疑似人际")

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

keep, move = [], []
keep_reason = {}
for uidb in uid_list:
    uid = int(uidb)
    subj, frm, date = headers.get(uid, ("", "", ""))
    text = strip_html(texts.get(uid, ""))
    dec_cat, why = classify(subj, frm, text)
    if dec_cat == "KEEP":
        keep.append(uid); keep_reason[uid] = why
    else:
        move.append(uid)

print(f"PLAN: 保留={len(keep)} 移动={len(move)}", flush=True)

# 备份决策清单
with open(os.path.join(ARCH, "cleanup_decision_2026-08-25.txt"), "w", encoding="utf-8") as f:
    f.write(f"# 清理决策 {datetime.date.today()}\n")
    f.write(f"INBOX 总数={total}  保留={len(keep)}  移动={len(move)}\n")
    f.write("## 保留\n")
    for u in keep:
        subj, frm, date = headers.get(u, ("", "", ""))
        f.write(f"  KEEP[{keep_reason.get(u)}] {u} | {frm} | {subj}\n")
    f.write("## 移动\n")
    for u in move:
        subj, frm, date = headers.get(u, ("", "", ""))
        f.write(f"  MOVE {u} | {frm} | {subj}\n")

# ---- 执行：移到专门文件夹（可找回）----
con = imaplib.IMAP4_SSL("imap.qq.com", 993, timeout=120)
con.login(USER, PWD)
con.select("INBOX")
# 检测 EXPUNGE 陷阱：是否有其他 pending \\Deleted
typ, d = con.uid("search", None, "DELETED")
pending = d[0].split() if d[0] else []
print(f"PENDING_DELETED_BEFORE={len(pending)}", flush=True)
# 创建目标文件夹（若已存在忽略错误）
try:
    con.create(FOLDER)
    print("FOLDER_CREATED", FOLDER, flush=True)
except Exception as e:
    print("FOLDER_EXISTS_OR_ERR", str(e)[:80], flush=True)

con.select("INBOX")
moved = 0
step = 150
for i in range(0, len(move), step):
    chunk = move[i:i+step]
    try:
        typ, resp = con.uid("MOVE", b",".join(str(u).encode() for u in chunk), FOLDER)
        moved += len(chunk)
    except Exception as e:
        print("MOVE_ERR", str(e)[:100], flush=True)
    if i % 600 == 0:
        print(f"  moved {moved}/{len(move)}", flush=True)

# 验证剩余
con.select("INBOX", readonly=True)
typ, u = con.uid("search", None, "ALL")
remaining = len(u[0].split())
con.logout()
print(f"MOVED={moved}  REMAINING_INBOX={remaining}", flush=True)

# 报告
with open(os.path.join(ARCH, "cleanup_report_2026-08-25.md"), "w", encoding="utf-8") as f:
    f.write("# 🧹 INBOX 清理报告（2026-08-25）\n\n")
    f.write(f"- 邮箱：`{USER}`\n")
    f.write(f"- 清理前 INBOX：**{total}** 封\n")
    f.write(f"- **保留：{len(keep)} 封**（疑似人际 / 账单发票 / 公司合同·offer）\n")
    f.write(f"- **移动到文件夹 `{FOLDER}`：{moved} 封**（可找回，非硬删）\n")
    f.write(f"- 清理后 INBOX 剩余：**{remaining}** 封\n\n")
    f.write("## 保留项理由分布\n\n")
    from collections import Counter
    rc = Counter(keep_reason.values())
    for k, v in rc.most_common():
        f.write(f"- {k}: {v} 封\n")
    f.write("\n## 说明\n")
    f.write("- 移动而非硬删：邮件在 QQ 邮箱 `Cleanup_20260825` 文件夹，可随时移回 INBOX。\n")
    f.write("- 安全/验证码、系统 no-reply、社交动态、营销均按规则清理。\n")
    f.write("- 决策清单见 `cleanup_decision_2026-08-25.txt`。\n")

print("DONE", flush=True)
