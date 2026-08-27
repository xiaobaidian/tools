# 🧹 mailbox-cleanup-subscribe · 订阅广告清理候选

> 生成「订阅/广告/营销类」清理候选清单（只读，不移动/不删除任何邮件）。

## 功能
- 扫描 INBOX 全部邮件头，命中「退订 / unsubscribe / 广告 / 促销 / 优惠 / 活动 / 订阅 / newsletter / 双11 / 618 …」等关键词即列为候选
- 按发件人聚合（计数 + 样例主题），方便你一眼识别可批量清理的源头

## 用法
```bash
python cleanup_subscribe_list.py   # 清单输出到 out/cleanup_subscribe.md
```

## 依赖
- Python 3.x（标准库）
- QQ 邮箱 IMAP 凭据

## 文件
- `cleanup_subscribe_list.py`：主程序

## 注意事项
- 只读生成，需你确认后再执行真正的清理（见 mailbox-cleanup）
