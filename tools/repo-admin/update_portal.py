#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, base64, json, urllib.request, urllib.error, urllib.parse

TOKEN = os.environ["GH_TOKEN"]
REPO = "xiaobaidian/tools"
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
        print("HTTP", e.code, e.read().decode("utf-8")[:400]); raise

def put(path, content, msg):
    b64 = base64.b64encode(content.encode("utf-8")).decode("ascii")
    sha = None
    try:
        info = api("GET", f"/repos/{REPO}/contents/{urllib.parse.quote(path)}")
        sha = info.get("sha")
    except Exception:
        pass
    body = {"message": msg, "content": b64}
    if sha: body["sha"] = sha
    api("PUT", f"/repos/{REPO}/contents/{urllib.parse.quote(path)}", body)
    print("  wrote", path)

# ---------------- 精美门户 ----------------
index_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>小微的工具箱 · Sanfre's Tools</title>
<style>
  :root{
    --bg:#0b0e1a; --bg2:#121732; --card:rgba(28,34,64,.72);
    --fg:#eaf0ff; --muted:#9aa6d4; --acc:#7c8cff; --acc2:#56e1c9;
    --web:#56e1c9; --tool:#ffb86c; --line:rgba(124,140,255,.18);
    --shadow:0 10px 40px rgba(0,0,0,.45);
  }
  *{box-sizing:border-box}
  html,body{margin:0;padding:0}
  body{
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;
    color:var(--fg); min-height:100vh; line-height:1.6;
    background:
      radial-gradient(1100px 600px at 85% -10%, rgba(124,140,255,.22), transparent 60%),
      radial-gradient(900px 500px at 10% 10%, rgba(86,225,201,.16), transparent 55%),
      linear-gradient(160deg, var(--bg), var(--bg2));
    background-attachment:fixed;
  }
  .wrap{max-width:1080px;margin:0 auto;padding:48px 22px 72px}
  header{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:16px;margin-bottom:30px}
  .title{font-size:40px;font-weight:800;letter-spacing:.5px;margin:0;
    background:linear-gradient(90deg,#fff,#aab6ff 60%,var(--acc2));
    -webkit-background-clip:text;background-clip:text;color:transparent}
  .sub{color:var(--muted);margin:6px 0 0;font-size:15px}
  .links a{color:var(--fg);text-decoration:none;font-size:13px;padding:8px 14px;border:1px solid var(--line);
    border-radius:999px;background:rgba(255,255,255,.04);transition:.2s;white-space:nowrap}
  .links a:hover{border-color:var(--acc);color:#fff;transform:translateY(-2px)}
  .links{display:flex;gap:10px;flex-wrap:wrap}
  .controls{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin:8px 0 26px}
  .search{flex:1;min-width:220px;display:flex;align-items:center;gap:8px;background:var(--card);
    border:1px solid var(--line);border-radius:12px;padding:10px 14px;backdrop-filter:blur(8px)}
  .search input{flex:1;background:transparent;border:0;outline:0;color:var(--fg);font-size:14px}
  .search svg{opacity:.6}
  .chips{display:flex;gap:8px;flex-wrap:wrap}
  .chip{cursor:pointer;border:1px solid var(--line);background:rgba(255,255,255,.04);color:var(--muted);
    padding:8px 14px;border-radius:999px;font-size:13px;transition:.2s}
  .chip:hover{color:#fff}
  .chip.active{background:linear-gradient(90deg,var(--acc),#9aa6ff);color:#0b0e1a;border-color:transparent;font-weight:600}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:18px}
  .card{position:relative;background:var(--card);border:1px solid var(--line);border-radius:18px;
    padding:22px;backdrop-filter:blur(10px);box-shadow:var(--shadow);transition:transform .22s,border-color .22s;overflow:hidden}
  .card:before{content:"";position:absolute;inset:0;background:linear-gradient(120deg,transparent,rgba(124,140,255,.08));opacity:0;transition:.22s}
  .card:hover{transform:translateY(-5px);border-color:var(--acc)}
  .card:hover:before{opacity:1}
  .card .top{display:flex;align-items:center;gap:12px;margin-bottom:10px}
  .emoji{font-size:30px;filter:drop-shadow(0 4px 10px rgba(0,0,0,.4))}
  .card h3{margin:0;font-size:19px}
  .badge{margin-left:auto;font-size:11px;font-weight:700;padding:4px 9px;border-radius:999px;letter-spacing:.3px}
  .badge.web{background:rgba(86,225,201,.16);color:var(--web)}
  .badge.tool{background:rgba(255,184,108,.16);color:var(--tool)}
  .card p{margin:0 0 14px;color:var(--muted);font-size:13.5px;min-height:38px}
  .tags{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:16px}
  .tag{font-size:11px;color:var(--muted);background:rgba(255,255,255,.05);border:1px solid var(--line);padding:3px 8px;border-radius:8px}
  .open{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:600;text-decoration:none;
    color:#0b0e1a;background:linear-gradient(90deg,var(--acc),#aab6ff);padding:9px 16px;border-radius:10px;transition:.2s}
  .open:hover{filter:brightness(1.08);transform:translateX(2px)}
  .empty{grid-column:1/-1;text-align:center;color:var(--muted);padding:60px 20px;border:1px dashed var(--line);border-radius:18px}
  .empty .big{font-size:46px;margin-bottom:10px}
  footer{margin-top:54px;color:var(--muted);font-size:12.5px;display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px}
  footer a{color:var(--acc);text-decoration:none}
  @media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div>
      <h1 class="title">🛠️ 小微的工具箱</h1>
      <p class="sub">Sanfre 的个人小工具 & 静态网页集 · 由 WorkBuddy（小微）维护</p>
    </div>
    <div class="links">
      <a href="https://github.com/xiaobaidian/tools" target="_blank" rel="noopener">⭐ GitHub 仓库</a>
      <a href="https://xiaobaidian.github.io/tools/tools.json" target="_blank" rel="noopener">📄 工具清单</a>
    </div>
  </header>

  <div class="controls">
    <label class="search">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
      <input id="q" type="text" placeholder="搜索工具名称 / 描述 / 标签…" autocomplete="off"/>
    </label>
    <div class="chips" id="chips">
      <span class="chip active" data-f="all">全部</span>
      <span class="chip" data-f="web">🌐 网页</span>
      <span class="chip" data-f="tool">⚙️ 工具</span>
    </div>
  </div>

  <div class="grid" id="grid"></div>

  <footer>
    <span>仓库：<a href="https://github.com/xiaobaidian/tools">github.com/xiaobaidian/tools</a></span>
    <span id="meta"></span>
  </footer>
</div>

<script>
const TYPE = {web:{label:"网页",cls:"web"}, tool:{label:"工具",cls:"tool"}};
let TOOLS = [], filter = "all", query = "";

function esc(s){return (s||"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));}

function render(){
  const grid = document.getElementById("grid");
  const q = query.trim().toLowerCase();
  const list = TOOLS.filter(t=>{
    if(filter!=="all" && t.type!==filter) return false;
    if(!q) return true;
    return (t.name+" "+(t.desc||"")+" "+(t.tags||[]).join(" ")).toLowerCase().includes(q);
  });
  if(!list.length){
    grid.innerHTML = '<div class="empty"><div class="big">🔧</div>还没有匹配的工具～ 让小微给你搓一个？</div>';
    return;
  }
  grid.innerHTML = list.map(t=>{
    const ty = TYPE[t.type]||TYPE.tool;
    const link = "./" + t.folder + (t.type==="web" ? "/" : "/");
    const tags = (t.tags||[]).map(x=>'<span class="tag">#'+esc(x)+'</span>').join("");
    return `<div class="card">
      <div class="top">
        <span class="emoji">${esc(t.emoji||"🧰")}</span>
        <h3>${esc(t.name)}</h3>
        <span class="badge ${ty.cls}">${ty.label}</span>
      </div>
      <p>${esc(t.desc)||"——"}</p>
      <div class="tags">${tags}</div>
      <a class="open" href="${link}" target="_blank" rel="noopener">打开 →</a>
    </div>`;
  }).join("");
}

fetch("./tools.json").then(r=>r.json()).then(d=>{
  TOOLS = d.tools||[];
  document.getElementById("meta").textContent = "共 " + TOOLS.length + " 个工具 · 更新于 " + (d.updated||"");
  render();
}).catch(e=>{
  document.getElementById("grid").innerHTML = '<div class="empty"><div class="big">⚠️</div>清单加载失败：'+e+'</div>';
});

document.getElementById("q").addEventListener("input", e=>{query=e.target.value;render();});
document.getElementById("chips").addEventListener("click", e=>{
  const c=e.target.closest(".chip"); if(!c) return;
  document.querySelectorAll(".chip").forEach(x=>x.classList.remove("active"));
  c.classList.add("active"); filter=c.dataset.f; render();
});
</script>
</body>
</html>
"""

# ---------------- 工具清单 ----------------
tools_json = json.dumps({"updated":"2026-08-27","tools":[]}, ensure_ascii=False, indent=2)

# ---------------- 根 README 模板 ----------------
readme = """# tools

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
"""

print("=== 推送门户 / 清单 / README ===")
put("index.html", index_html, "feat: polished manifest-driven portal")
put("tools.json", tools_json, "chore: init empty tools manifest")
put("README.md", readme, "docs: per-tool detailed README template")
print("DONE")
