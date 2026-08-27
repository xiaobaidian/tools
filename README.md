# tools

Sanfre 的个人小工具 & 静态网页集，由 WorkBuddy（小微）维护。公开仓库，在线访问：**[https://xiaobaidian.github.io/tools/](https://xiaobaidian.github.io/tools/)**

## 📁 仓库结构（按类型归类）
```
/                      # GitHub Pages 根（门户）
├── index.html         # 精美门户（按分类分组，由 tools.json 驱动）
├── tools.json         # 工具清单（新增工具只需改这里）
├── README.md          # 本文件：每个工具的详细介绍
├── sites/             # 静态网页，按类型再分子文件夹
│   ├── image/         #   图片类工具
│   │   └── a4-image-layout/
│   └── document/      #   文档类工具
│       └── outbound-order/
└── tools/             # 脚本/CLI 小工具，按类型再分子文件夹
    ├── mailbox/       #   邮箱管理类（5 个）
    │   ├── audit/
    │   ├── content-audit/
    │   ├── cleanup-subscribe/
    │   ├── cleanup/
    │   └── smtp-notify/
    └── repo-admin/    #   仓库自身维护
```

## 📋 工具清单（按分类）
### 📧 邮箱管理
- **邮箱体检 mailbox-audit** · `tools/mailbox/audit` · 只读统计年份/发件人/域名/类型占比
- **邮件内容审计 mailbox-content-audit** · `tools/mailbox/content-audit` · 逐封分筐生成拟删清单
- **订阅清理候选 mailbox-cleanup-subscribe** · `tools/mailbox/cleanup-subscribe` · 订阅广告清理候选（只读）
- **INBOX 规则清理 mailbox-cleanup** · `tools/mailbox/cleanup` · 只留人际/账单/合同，其余移归档（可找回）
- **SMTP 直发 smtp-notify** · `tools/mailbox/smtp-notify` · QQ 邮箱 SMTP 直发（密钥本地不入仓）

### 🖼️ 图片工具
- **A4 图片排版工具** · [在线打开](https://xiaobaidian.github.io/tools/sites/image/a4-image-layout/) · `sites/image/a4-image-layout` · 多图排版到 A4(300DPI)，本地处理

### 📄 文档工具
- **出库单生成器** · [在线打开](https://xiaobaidian.github.io/tools/sites/document/outbound-order/) · `sites/document/outbound-order` · Excel/粘贴生成出库单，可打印/复制/导出PDF

### 🛠️ 仓库维护
- **仓库维护 repo-admin** · `tools/repo-admin` · 本仓库自身的初始化/重建门户脚本

> 每个工具文件夹内都有独立的 `README.md` 详述功能、用法、依赖与注意点。

## ➕ 如何新增一个工具
1. 在对应类型下建文件夹：`sites/<类型>/<工具名>/`（网页需 `index.html`）或 `tools/<类型>/<工具名>/`（脚本 + 自己的 README.md）。
2. 在 `tools.json` 的 `tools` 数组加一项（含 `category` 归类）：
   ```json
   {"name":"工具名","emoji":"🧰","type":"web|tool","category":"📧 邮箱管理","folder":"sites/类型/工具名","desc":"一句话简介","tags":["标签"],"updated":"YYYY-MM-DD"}
   ```
3. 在该工具文件夹补 `README.md` 详细介绍。
4. 推送：走 **GitHub REST API 单提交**（沙箱 `git push` 被截断），推到 `main` 后 Pages 自动构建上线。
5. ⚠️ 公开仓库 **禁止入库 token / 授权码 / 敏感信息**。

## 📜 归纳铁律
凡是小微给 Sanfre 开发的「小工具 / 静态网页」，只要没有自己的独立 GitHub 仓库，都必须按类型归纳进本仓库对应文件夹，每个工具独立文件夹 + 根 README 详细介绍 + 门户精美。
