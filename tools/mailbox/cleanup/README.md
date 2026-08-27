# 🗂️ mailbox-cleanup · INBOX 规则清理

> 按规则清理 INBOX：**只留 疑似人际 / 账单发票 / 公司合同·offer，其余移到归档文件夹（可找回，不硬删）**。

## 功能
- 规则：合同/offer、账单发票 → 保留；安全/验证码、系统 no-reply、社交动态、营销 → 移到 `Cleanup_YYYYMMDD` 文件夹
- 先生成决策清单（保留/移动逐封记录），再执行「移动」（IMAP MOVE，非删除）
- 输出清理前后数量对比报告

## 用法
```bash
python mail_cleanup.py
# 1) 决策清单 out/cleanup_decision_YYYY-MM-DD.txt
# 2) 执行移动，报告 out/cleanup_report_YYYY-MM-DD.md
```

## 依赖
- Python 3.x（标准库）
- QQ 邮箱 IMAP 凭据

## 文件
- `mail_cleanup.py`：主程序

## 注意事项
- **移动而非硬删**：邮件进入 QQ 邮箱 `Cleanup_*` 文件夹，可随时移回 INBOX
- 运行前会自动检测是否有其它 pending `\Deleted` 邮件，规避 EXPUNGE 误删陷阱
- 涉及真实邮件操作，**建议先跑 mailbox-content-audit 看分筐结果、确认规则无误再跑本工具**
