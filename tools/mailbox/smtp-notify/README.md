# 📧 smtp-notify · QQ 邮箱 SMTP 直发通知

> 走 QQ 邮箱 SMTP 直发邮件，不依赖任何连接器。主要用于小微（WorkBuddy）给你的兜底发信。

## 配置
在脚本目录放置 `smtp_notify.json`（**勿提交到公开仓库**），或用环境变量 `SMTP_NOTIFY_CONFIG` 指定路径。格式：
```json
{
  "smtp_host": "smtp.qq.com",
  "smtp_port": 465,
  "smtp_user": "865778357@qq.com",
  "smtp_pass": "你的授权码（非邮箱密码）",
  "default_to": "865778357@qq.com"
}
```
> 仓库内只提供 `smtp_notify.example.json` 模板，真实配置请自行放在本地、不要推送。

## 用法
```bash
python smtp_notify.py -s "邮件标题" -b "邮件正文"
python smtp_notify.py -s "标题" -b "正文" -t "另一个@收件箱.com"
```

## 依赖
- Python 3.x（标准库 smtplib）
- QQ 邮箱 SMTP 服务已开启 + 授权码

## 文件
- `smtp_notify.py`：主程序
- `smtp_notify.example.json`：配置模板

## 注意事项
- 密钥只在本地，绝不入库
- 与 agent-mail 连接器互为兜底：agent-mail 不可用时用本脚本
