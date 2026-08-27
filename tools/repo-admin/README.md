# 🛠️ repo-admin · 本仓库维护脚本

> 维护 `xiaobaidian/tools` 这个仓库自身的小工具（无外部依赖，仅用 GitHub REST API + 环境变量 token）。

## 文件
- `repo_setup.py`：初始化/改名/清理旧文件/启用 GitHub Pages 的一次性脚本（已用过，留作参考）
- `update_portal.py`：重建门户 `index.html`、清单 `tools.json`、根 `README.md` 的脚本（改版门户时用）

## 用法
```bash
# 需要 GitHub PAT（repo+workflow），从环境变量传入
export GH_TOKEN=ghp_xxx
python update_portal.py
```

## 依赖
- Python 3.x（标准库 urllib）
- 环境变量 `GH_TOKEN`：对 `xiaobaidian/tools` 有写权限的 PAT

## 注意事项
- 这两个脚本是「造仓库的工具」，不是给你的日常小工具；归档在此便于下次维护复用
- 不含任何密钥，token 一律走环境变量
