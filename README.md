# tools

Sanfre 的个人小工具 & 静态网页集，由 WorkBuddy（小微）维护。公开仓库，在线访问：**[https://xiaobaidian.github.io/tools/](https://xiaobaidian.github.io/tools/)**

## 📁 仓库结构
```
/                      # GitHub Pages 根（门户）
├── index.html         # 精美门户（由 tools.json 驱动渲染卡片）
├── tools.json         # 工具清单（新增工具只需改这里）
├── README.md          # 本文件：每个工具的详细介绍
├── sites/             # 静态网页，每个工具一个文件夹
│   └── <工具名>/index.html
└── tools/             # 脚本/CLI 小工具，每个工具一个文件夹
    └── <工具名>/(脚本 + README.md)
```

## 📋 工具清单（详细介绍）

### 📊 mailbox-audit · 邮箱体检
- **类型**：⚙️ 工具（CLI）
- **一句话**：只读拉取 INBOX 邮件头，统计年份/发件人/域名/类型占比。
- **功能**：年份分布、发件人 Top15、域名 Top15、订阅广告/系统通知粗略占比；输出 `out/report.md`。
- **用法**：`python mail_audit.py`（需先配 `smtp_notify.json`，见 smtp-notify 工具）
- **依赖**：Python 3.x 标准库（imaplib/email/re）
- **注意**：`readonly` 模式，**绝不改动邮件**；输出在脚本同级 `out/`。
- 📂 `tools/mailbox-audit/`

### 📝 mailbox-content-audit · 邮件内容审计
- **类型**：⚙️ 工具（CLI）
- **一句话**：逐封读正文按价值分筐，生成拟删清单（只读）。
- **功能**：分六筐（安全/账单/营销/社交/系统/人际），输出拟删发件人 Top + 每筐抽样预览；报告 `out/content_audit.md`。
- **用法**：`python mail_content_audit.py`
- **依赖**：Python 3.x 标准库
- **注意**：只读，不执行删除，方便你复核判断标准。
- 📂 `tools/mailbox-content-audit/`

### 🧹 mailbox-cleanup-subscribe · 订阅广告清理候选
- **类型**：⚙️ 工具（CLI）
- **一句话**：生成「订阅/广告/营销类」清理候选清单（只读）。
- **功能**：按关键词命中列为候选，按发件人聚合（计数+样例）；清单 `out/cleanup_subscribe.md`。
- **用法**：`python cleanup_subscribe_list.py`
- **依赖**：Python 3.x 标准库
- **注意**：只读生成，需你确认后再执行真正清理。
- 📂 `tools/mailbox-cleanup-subscribe/`

### 🗂️ mailbox-cleanup · INBOX 规则清理
- **类型**：⚙️ 工具（CLI）
- **一句话**：只留人际/账单/合同offer，其余移到归档夹（**可找回，不硬删**）。
- **功能**：合同/offer、账单发票保留；安全/系统/社交/营销移到 `Cleanup_YYYYMMDD`；先出决策清单再执行 MOVE；报告 `out/cleanup_report_*.md`。
- **用法**：`python mail_cleanup.py`
- **依赖**：Python 3.x 标准库
- **注意**：移动非删除，可随时移回；**建议先跑 content-audit 确认规则**。
- 📂 `tools/mailbox-cleanup/`

### 📧 smtp-notify · QQ 邮箱 SMTP 直发
- **类型**：⚙️ 工具（CLI）
- **一句话**：走 QQ 邮箱 SMTP 直发邮件，不依赖任何连接器（小微兜底发信）。
- **功能**：`python smtp_notify.py -s 标题 -b 正文 [-t 收件人]`
- **依赖**：Python 3.x 标准库；QQ 邮箱 SMTP + 授权码
- **注意**：**密钥只在本地 `smtp_notify.json`，绝不入库**（仓库仅 `smtp_notify.example.json` 模板）。
- 📂 `tools/smtp-notify/`

### 🛠️ repo-admin · 仓库维护脚本
- **类型**：⚙️ 工具（CLI）
- **一句话**：维护本仓库自身的脚本（初始化/重建门户）。
- **功能**：`repo_setup.py`（初始化/改名/启用 Pages）、`update_portal.py`（重建门户/清单/README）。
- **用法**：`export GH_TOKEN=xxx && python update_portal.py`
- **依赖**：Python 3.x 标准库；环境变量 `GH_TOKEN`（对仓库有写权限的 PAT）
- **注意**：无密钥，token 走环境变量。
- 📂 `tools/repo-admin/`

## ➕ 如何新增一个工具
1. 在 `sites/<工具名>/`（网页）或 `tools/<工具名>/`（脚本）建文件夹，放入文件（网页需 `index.html`）+ 自身 `README.md`。
2. 在 `tools.json` 的 `tools` 数组加一项：`{"name":..,"emoji":..,"type":"web|tool","folder":"tools/工具名","desc":..,"tags":[..],"updated":"YYYY-MM-DD"}`。
3. 在上方「工具清单」补一段详细介绍。
4. 推送：走 **GitHub REST API 单提交**（沙箱 `git push` 被截断），推到 `main` 后 Pages 自动构建上线。
5. ⚠️ 公开仓库 **禁止入库 token / 授权码 / 敏感信息**。

## 📜 归纳铁律
凡是小微给 Sanfre 开发的「小工具 / 静态网页」，只要没有自己的独立 GitHub 仓库，都必须归纳进本仓库，每个工具独立文件夹 + 根 README 详细介绍 + 门户精美。
