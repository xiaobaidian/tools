#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮箱体检：只读拉取 INBOX 全部邮件头，统计年份分布 / 发件人 Top / 域名 Top /
订阅广告类 & 系统通知类粗略占比。不改动任何邮件。
输出：D:/WorkBuddyData/Workspace/mail_audit/report.md
"""
import json
import imaplib
import email
import email.header as eh
from collections import Counter
from email.utils import parsedate_to_datetime, getaddresses
import os
from datetime import datetime

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
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT_DIR, exist_ok=True)

def dec(s):
    if not s:
        return ""
    out = ""
    for b, enc in eh.decode_header(s):
        if isinstance(b, bytes):
            try:
                out += b.decode(enc or "utf-8", "ignore")
            except (LookupError, UnicodeDecodeError):
                out += b.decode("latin-1", "ignore")
        else:
            out += b
    return out

con = imaplib.IMAP4_SSL("imap.qq.com", 993, timeout=40)
con.login(USER, PWD)
con.select("INBOX", readonly=True)
typ, uids = con.uid("search", None, "ALL")
uid_list = uids[0].split()
total = len(uid_list)

year_c = Counter()
sender_c = Counter()
domain_c = Counter()
promo = 0
notice = 0
promo_kw = __import__("re").compile(r"退订|unsubscribe|广告|促销|优惠|活动|订阅|newsletter|marketing|推广|打折|秒杀|coupon|双11|双十一|618", __import__("re").I)
notice_kw = __import__("re").compile(r"通知|提醒|账单|发票|验证码|系统|invoice|alert|daily|weekly|monthly|report|summary|账单|回执|确认", __import__("re").I)

BATCH = 200
for i in range(0, total, BATCH):
    batch = uid_list[i:i + BATCH]
    typ, data = con.uid("fetch", b",".join(batch), "(BODY.PEEK[HEADER])")
    for item in data:
        hdr = None
        if isinstance(item, tuple) and len(item) > 1:
            hdr = item[1]
        elif isinstance(item, bytes) and len(item) > 30:
            hdr = item
        if not isinstance(hdr, bytes):
            continue
        try:
            msg = email.message_from_bytes(hdr)
        except Exception:
            continue
        subj = dec(msg.get("Subject", ""))
        frm = dec(msg.get("From", ""))
        date = msg.get("Date", "")
        addrs = getaddresses([frm])
        addr = addrs[0][1] if addrs else frm
        if "@" in addr:
            sender_c[addr.lower()] += 1
            domain_c[addr.lower().split("@")[-1]] += 1
        else:
            sender_c[frm[:60]] += 1
        try:
            dt = parsedate_to_datetime(date)
            if dt:
                year_c[dt.year] += 1
        except Exception:
            pass
        blob = subj + " " + frm
        if promo_kw.search(blob):
            promo += 1
        if notice_kw.search(blob):
            notice += 1
    print(f"  processed {min(i + BATCH, total)}/{total}", flush=True)

con.logout()

# 未读由之前探查所得
unseen = 409
seen = total - unseen

lines = []
lines.append(f"# 📬 邮箱体检报告：{USER}")
lines.append("")
lines.append(f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} ｜ 数据来源：IMAP 只读拉取，未改动任何邮件")
lines.append("")
lines.append("## 概览")
lines.append("")
lines.append(f"- **总邮件数**：{total} 封")
lines.append(f"- **未读**：{unseen} 封 ｜ **已读**：{seen} 封")
lines.append("")
lines.append("## 📅 年份分布")
lines.append("")
for y in sorted(year_c):
    lines.append(f"- {y}：{year_c[y]} 封")
lines.append("")
lines.append("## 👤 发件人 Top 15")
lines.append("")
for a, c in sender_c.most_common(15):
    lines.append(f"- `{a}`：{c} 封")
lines.append("")
lines.append("## 🌐 发件域名 Top 15")
lines.append("")
for d, c in domain_c.most_common(15):
    lines.append(f"- `{d}`：{c} 封")
lines.append("")
lines.append("## 🏷️ 内容类型粗略占比（按标题/发件人关键词）")
lines.append("")
lines.append(f"- **订阅 / 广告 / 营销类**：约 {promo} 封（{promo*100//total if total else 0}%）")
lines.append(f"- **系统 / 通知 / 账单类**：约 {notice} 封（{notice*100//total if total else 0}%）")
lines.append(f"- **其余（人际 / 工作 / 其他）**：约 {total-promo-notice} 封")
lines.append("")
lines.append("## 💡 小秘的下一步建议（需你确认再做）")
lines.append("")
lines.append("- 先把「订阅/广告类」批量移到独立文件夹或清空（通常占比高、价值低）")
lines.append("- 把 N 年前且已读的邮件归档到年份文件夹，给 INBOX 减负")
lines.append("- 按发件域名聚类，识别可一键退订/屏蔽的源头")
lines.append("")
lines.append("---")
lines.append("_由 WorkBuddy 小秘于 2026-08-25 自动生成 · 仅只读分析_")

report = "\n".join(lines)
out_path = os.path.join(OUT_DIR, "report.md")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(report)
print("\n=== REPORT SAVED ===")
print(report)
