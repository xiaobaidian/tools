# 📊 mailbox-audit · 邮箱体检

> 只读拉取 QQ 邮箱 INBOX 全部邮件头，统计年份分布 / 发件人 Top / 域名 Top / 订阅广告·系统通知粗略占比。**不改动任何邮件。**

## 功能
- 年份分布、发件人 Top15、发件域名 Top15
- 按标题/发件人关键词粗略判定「订阅/广告/营销类」与「系统/通知/账单类」占比
- 输出 Markdown 报告

## 用法
```bash
# 1) 准备配置（见同仓库 smtp-notify 工具）：在脚本目录放 smtp_notify.json，或设环境变量 SMTP_NOTIFY_CONFIG 指向它
python mail_audit.py
# 报告输出到脚本所在 out/report.md
```

## 依赖
- Python 3.x（仅标准库：imaplib / email / re / collections）
- QQ 邮箱 IMAP 凭据（smtp_notify.json 里的 smtp_user / smtp_pass）

## 文件
- `mail_audit.py`：主程序

## 注意事项
- 全程 `readonly` 模式，绝不会删除/移动邮件
- 输出目录为脚本同级 `out/`，可随意删除
