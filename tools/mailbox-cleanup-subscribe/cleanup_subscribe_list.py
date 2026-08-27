#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成「订阅/广告/营销类」清理候选清单（只读，不移动/不删除任何邮件）。
输出：D:/WorkBuddyData/Workspace/mail_audit/cleanup_subscribe.md
判定：标题/发件人含促销、退订、newsletter、优惠、活动、订阅等关键词。
"""
import json
import imaplib
import email
import email.header as eh
import re
from email.utils import getaddresses
from collections import defaultdict
import os

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
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)


def dec(s):
    if not s:
        return ""
    out = ""
    for b, enc in eh.decode_header(s):
        if isinstance(b, bytes):
            try:
                out += b.decode(enc or "utf-8", "ignore")
            except Exception:
                out += b.decode("latin-1", "ignore")
        else:
            out += b
    return out


promo_kw = re.compile(
    r"退订|unsubscribe|广告|促销|优惠|活动|订阅|newsletter|marketing|推广|打折|秒杀|coupon|双11|双十一|618|特惠|限时|抢购|满减|折扣|大促|新品|推荐",
    re.I)

con = imaplib.IMAP4_SSL("imap.qq.com", 993, timeout=40)
con.login(USER, PWD)
con.select("INBOX", readonly=True)
typ, uids = con.uid("search", None, "ALL")
uid_list = uids[0].split()

cands = []            # (uid, from_addr, subject)
by_sender = defaultdict(list)

for i in range(0, len(uid_list), 200):
    batch = uid_list[i:i + 200]
    typ, data = con.uid("fetch", b",".join(batch), "(UID BODY.PEEK[HEADER])")
    for item in data:
        if not (isinstance(item, tuple) and len(item) > 1):
            continue
        meta, hdr = item[0], item[1]
        m = re.search(rb"UID (\d+)", meta)
        if not m:
            continue
        uid = int(m.group(1))
        try:
            msg = email.message_from_bytes(hdr)
        except Exception:
            continue
        subj = dec(msg.get("Subject", ""))
        frm = dec(msg.get("From", ""))
        blob = subj + " " + frm
        if promo_kw.search(blob):
            addrs = getaddresses([frm])
            addr = addrs[0][1] if addrs else frm
            cands.append((uid, addr, subj))
            by_sender[addr].append((uid, subj))
con.logout()

# 输出 markdown 清单
lines = []
lines.append("# 🧹 订阅/广告类清理候选清单（待确认）")
lines.append("")
lines.append(f"> 候选总数：**{len(cands)} 封** ｜ 判定：标题/发件人含促销/退订/订阅等关键词 ｜ **只读生成，未移动/未删除任何邮件**")
lines.append("")
lines.append("## 按发件人聚合（计数 / 样例主题）")
lines.append("")
for addr, lst in sorted(by_sender.items(), key=lambda x: -len(x[1])):
    lines.append(f"### `{addr}` — {len(lst)} 封")
    for uid, subj in lst[:3]:
        s = subj if len(subj) < 50 else subj[:47] + "..."
        lines.append(f"- #{uid} · {s}")
    if len(lst) > 3:
        lines.append(f"- …（其余 {len(lst)-3} 封略）")
    lines.append("")
lines.append("---")
lines.append("_由 WorkBuddy 小秘于 2026-08-25 生成 · 待 Sanfre 确认后执行「移动到归档文件夹」（不删，可恢复）_")

report = "\n".join(lines)
with open(os.path.join(OUT, "cleanup_subscribe.md"), "w", encoding="utf-8") as f:
    f.write(report)
print(f"CANDIDATES={len(cands)}")
print(report)
