#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小秘 SMTP 通知脚本 —— 走 QQ 邮箱 SMTP 直发，不依赖任何连接器。
用法：
  python3 smtp_notify.py -s "邮件标题" -b "邮件正文"
  python3 smtp_notify.py -s "标题" -b "正文" -t "另一个@收件箱.com"
凭据从同目录 smtp_notify.json 读取（不在脚本里硬编码）。
"""
import json
import sys
import argparse
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def _cfg_path():
    import os
    for _p in [os.environ.get("SMTP_NOTIFY_CONFIG"),
               os.path.join(os.path.dirname(os.path.abspath(__file__)), "smtp_notify.json"),
               r"D:/WorkBuddyData/Tools/smtp_notify.json"]:
        if _p and os.path.exists(_p):
            return _p
    return r"D:/WorkBuddyData/Tools/smtp_notify.json"
CONFIG_PATH = _cfg_path()


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def send(subject, body, to=None):
    cfg = load_config()
    host = cfg["smtp_host"]
    port = cfg["smtp_port"]
    user = cfg["smtp_user"]
    pwd = cfg["smtp_pass"]
    sender = cfg["smtp_user"]
    receivers = [to] if to else [cfg["default_to"]]

    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = sender
    msg["To"] = ", ".join(receivers)
    msg["Subject"] = Header(subject, "utf-8")

    with smtplib.SMTP_SSL(host, port, timeout=15) as s:
        s.login(user, pwd)
        s.sendmail(sender, receivers, msg.as_string())
    print("SENT OK ->", ", ".join(receivers), "|", subject)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="小秘 SMTP 通知")
    p.add_argument("-s", "--subject", required=True, help="邮件标题")
    p.add_argument("-b", "--body", required=True, help="邮件正文")
    p.add_argument("-t", "--to", default=None, help="收件人（默认走配置里的 default_to）")
    args = p.parse_args()
    send(args.subject, args.body, args.to)
