# 📝 mailbox-content-audit · 邮件内容审计

> 逐封读取 INBOX 正文，按价值分筐，生成拟删清单。**只读，不改动任何邮件。**

## 功能
按关键词把每封邮件分到六筐：
- `KEEP_SECURITY` 安全/账号/验证码（绝不删）
- `KEEP_BILL` 账单/发票/订单/交易（保留）
- `DELETE_PROMO` 营销/促销/广告（拟删）
- `REVIEW_SOCIAL` 社交动态通知（待定）
- `REVIEW_SYSTEM` 系统 no-reply 通知（待定）
- `REVIEW_HUMAN` 疑似人际/其他（待定）

并输出「拟删发件人 Top」与每筐抽样预览，方便你复核小秘的判断标准对不对。

## 用法
```bash
python mail_content_audit.py   # 报告输出到 out/content_audit.md
```

## 依赖
- Python 3.x（标准库）
- QQ 邮箱 IMAP 凭据（同 mailbox-audit）

## 文件
- `mail_content_audit.py`：主程序

## 注意事项
- 只读；正文仅取前 2000 字节用于判定
- 仅生成清单，不执行任何删除
