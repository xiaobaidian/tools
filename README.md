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
    └── <工具名>/(脚本 + 自己的 README.md)
```

## 📋 工具清单
> 新增工具后，在下方复制一个 `###` 小节补详细介绍；同时更新 `tools.json` 让门户出卡片。

### <工具名>（示例模板，照抄）
- **类型**：🌐 网页 / ⚙️ 工具
- **一句话**：这个工具是干嘛的
- **访问 / 下载**：`https://xiaobaidian.github.io/tools/sites/<工具名>/`
- **功能详解**：
  1. 功能点一
  2. 功能点二
- **用法**：怎么用（网页直接打开 / 命令行怎么跑）
- **依赖**：需要什么环境（如 Python 3.x、无第三方库）
- **文件**：该工具文件夹里有哪些文件、各自作用
- **注意事项**：坑点、边界、敏感信息说明

## ➕ 如何新增一个工具
1. 在 `sites/<工具名>/` 或 `tools/<工具名>/` 建文件夹，放入文件（网页需 `index.html`）。
2. 在 `tools.json` 的 `tools` 数组加一项：
   ```json
   {"name":"工具名","emoji":"🧰","type":"web|tool","folder":"sites/工具名","desc":"一句话简介","tags":["标签"],"updated":"YYYY-MM-DD"}
   ```
3. 在上方「工具清单」补一段详细介绍。
4. 推送：走 **GitHub REST API 单提交**（沙箱 `git push` 被截断），推到 `main` 后 Pages 自动构建上线。
5. ⚠️ 公开仓库 **禁止入库 token / 授权码 / 敏感信息**。

## 📜 归纳铁律
凡是小微给 Sanfre 开发的「小工具 / 静态网页」，只要没有自己的独立 GitHub 仓库，都必须归纳进本仓库，每个工具独立文件夹 + 根 README 详细介绍 + 门户精美。
