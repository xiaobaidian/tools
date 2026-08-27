#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, base64, json, urllib.request, urllib.error

TOKEN = os.environ["GH_TOKEN"]
OLD = "xiaobaidian/workbuddy-notifications"
NEW = "xiaobaidian/tools"
API = "https://api.github.com"

def api(method, path, body=None):
    url = API + path
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + TOKEN)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            txt = r.read().decode("utf-8")
            return json.loads(txt) if txt else {}
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode("utf-8")[:500])
        raise

print("=== 1) 改名 + 公开 + 改描述 ===")
api("PATCH", f"/repos/{OLD}", {
    "name": "tools",
    "private": False,
    "description": "Sanfre 的个人小工具 & 静态网页集（由 WorkBuddy/小微 维护）",
})

print("=== 2) 取旧文件 sha ===")
for p in ["README.md", "inbox/2026-08-25_0107_系统_通知链路修复验证.md",
          "inbox/2026-08-25_0115_系统_订阅生效后邮件验证.md"]:
    try:
        info = api("GET", f"/repos/{NEW}/contents/{urllib.parse.quote(p)}")
        sha = info.get("sha")
        print(f"  删 {p} ({sha[:8]})")
        api("DELETE", f"/repos/{NEW}/contents/{urllib.parse.quote(p)}",
            {"message": f"chore: remove obsolete notification logs ({p})", "sha": sha})
    except Exception as e:
        print("  skip", p, e)

def put(path, content, msg):
    b64 = base64.b64encode(content.encode("utf-8")).decode("ascii")
    # 已存在则取 sha 覆盖
    sha = None
    try:
        info = api("GET", f"/repos/{NEW}/contents/{urllib.parse.quote(path)}")
        sha = info.get("sha")
    except Exception:
        pass
    body = {"message": msg, "content": b64}
    if sha:
        body["sha"] = sha
    api("PUT", f"/repos/{NEW}/contents/{urllib.parse.quote(path)}", body)
    print("  wrote", path)

import urllib.parse

print("=== 3) 写新结构 ===")
readme = """# tools

Sanfre 的个人小工具 & 静态网页集，由 WorkBuddy（小微）维护。

## 结构
- `index.html` —— GitHub Pages 门户（工具索引）
- `sites/` —— 每个静态网页一个子文件夹，访问地址 `https://xiaobaidian.github.io/tools/sites/<站点名>/`
- `tools/` —— 非网页的小工具（Python / CLI 等）

## 在线访问
- 门户：https://xiaobaidian.github.io/tools/
- 新增网页：在 `sites/<站点名>/` 下放 `index.html` 即可，推送到 main 分支后自动上线。

> 本仓库前身为通知归档仓库，已清空改造。
"""
put("README.md", readme, "docs: init tools repo readme")

portal = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>小微的工具箱 · Sanfre's Tools</title>
<style>
  :root{--bg:#0f1220;--card:#1a1f35;--fg:#e8ecff;--muted:#9aa3c7;--acc:#7c8cff}
  *{box-sizing:border-box}
  body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;
       background:radial-gradient(1200px 600px at 80% -10%,#2a2f55 0,var(--bg) 60%);color:var(--fg);min-height:100vh}
  .wrap{max-width:880px;margin:0 auto;padding:64px 24px}
  h1{font-size:34px;margin:0 0 6px}
  .sub{color:var(--muted);margin:0 0 36px}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}
  .card{background:var(--card);border:1px solid #2c335a;border-radius:14px;padding:18px;transition:.2s}
  .card:hover{transform:translateY(-3px);border-color:var(--acc)}
  .card h3{margin:0 0 6px;font-size:17px}
  .card p{margin:0;color:var(--muted);font-size:13px;line-height:1.5}
  .empty{color:var(--muted);font-size:14px;border:1px dashed #2c335a;border-radius:12px;padding:28px;text-align:center}
  footer{margin-top:48px;color:var(--muted);font-size:12px}
  a{color:var(--acc);text-decoration:none}
</style>
</head>
<body>
<div class="wrap">
  <h1>🛠️ 小微的工具箱</h1>
  <p class="sub">Sanfre 的个人小工具 & 静态网页集 · 由 WorkBuddy 维护</p>
  <div class="grid" id="grid">
    <div class="card"><h3>📁 sites/</h3><p>静态网页都放在这里，每个子文件夹是一个独立站点，推送到 main 后自动上线。</p></div>
    <div class="card"><h3>📁 tools/</h3><p>非网页的小工具（Python / CLI 脚本等）。</p></div>
  </div>
  <div class="empty" style="margin-top:24px">🔧 工具陆续建设中 —— 让小微给你搓一个？</div>
  <footer>仓库：<a href="https://github.com/xiaobaidian/tools">github.com/xiaobaidian/tools</a> · 门户即 GitHub Pages 自动构建</footer>
</div>
</body>
</html>
"""
put("index.html", portal, "feat: add Pages portal index.html")

put("sites/README.md",
    "# sites/\n\n每个静态网页一个子文件夹，例如 `sites/my-tool/index.html`。\n访问地址：https://xiaobaidian.github.io/tools/sites/my-tool/\n",
    "docs: add sites folder")
put("tools/README.md",
    "# tools/\n\n非网页的小工具（Python / CLI 等）放这里，每个工具一个子文件夹。\n",
    "docs: add tools folder")

print("=== 4) 启用 GitHub Pages (main /) ===")
try:
    api("POST", f"/repos/{NEW}/pages", {"source": {"branch": "main", "path": "/"}})
    print("  Pages 已触发启用")
except Exception as e:
    print("  Pages 启用可能已存在或延迟，稍后查询")

print("=== 5) 查询 Pages 状态 ===")
try:
    st = api("GET", f"/repos/{NEW}/pages")
    print("  status:", st.get("status"), "| url:", st.get("html_url"))
except Exception as e:
    print("  Pages 状态查询:", e)

print("DONE")
