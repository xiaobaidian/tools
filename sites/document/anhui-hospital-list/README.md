# 安徽省医院名单 · 三级浏览与星标

安徽省 16 个地级市 / 105 个县区 / **530 家医院**的单文件离线名单，按「地级市 → 县/区 → 医院」三级树浏览，支持展开折叠、搜索、类型筛选、统计概览、星标与备注，并可导出/导入你自己的标记做备份。

- **在线访问**：https://xiaobaidian.github.io/tools/sites/document/anhui-hospital-list/
- **数据来源**：安徽省卫生健康委员会及各市卫健委官方医疗机构信息公开栏目（数据截至 2026 年 9 月）
- **依赖**：零依赖单文件，离线可用，**无任何网络请求**（打开即用，不需要联网）

## 功能

| 区域 | 能力 |
|---|---|
| 左侧树 | 逐级展开/折叠；全部展开 / 全部折叠 / 展开到区县 / 仅地级市 / 重置 |
| 搜索 | 输入即搜，自动展开命中路径并高亮，显示命中数量；清空后还原展开状态 |
| 概览页 | 医院类型分布、各地市医院数量柱状图、按类型筛选 |
| 统计页 | 各地市「区县数 / 医院数」明细表 |
| 星标 | 悬停医院节点点 ☆ 标记；右侧「星标」页汇总，点击可定位并闪烁提示 |
| 备注 | 悬停医院节点点 ✎ 编辑；右侧「备注」页汇总 |
| **备份** | 控制条右侧「⇩ 导出我的标记 / ⇧ 导入标记」——把你的标记存成 JSON 文件，换电脑或清浏览器数据后可恢复 |
| 键盘 | 树节点 `Tab` 可达，`Enter` / `空格` 展开折叠；`Esc` 关闭弹窗（有未保存内容时会确认） |
| **手机** | 顶部分段切换（医院树 / 星标 / 备注 / 统计 / 概览），树改「下钻式」逐层进入，搜索框常驻，操作按钮常显、触摸目标放大（详见下节） |

## 数据模型（两层，重要）

```
      页面文件（index.html）
      ├── <script id="default-marks">   ← 默认层：团队深度合作医院（21 家）
      │                                    随文件分发，所有访客看到同一套
      └── localStorage                  ← 用户层：你自己的增删改，仅存本机
                    ↓ 合并规则
        用户层覆盖默认层；与默认完全一致时不落盘（自动瘦身）
```

- **默认层**由文件本身携带，任何人打开都能看到同样的星标——这就是「每个人看到同一套」的实现方式，不需要后端。
- **用户层**记录你对星标/备注的增删改，只保存在你自己的浏览器里，**不会上传**。
- 右侧「星标」页顶部的**恢复默认**按钮：清除本机所有修改，回到文件内置状态。

## 备份与迁移：导出 / 导入我的标记

`localStorage` 没有过期时间，正常用就一直有效。但**清理浏览数据、换电脑、换浏览器**会让它消失，所以提供了导出备份。

| 操作 | 说明 |
|---|---|
| **⇩ 导出我的标记** | 只导出**你相对默认层的改动**（不是全量 530 家），生成 `安徽省医院名单-我的标记-YYYYMMDD-HHmm.json`；本机没有改动时会提示无需导出 |
| **⇧ 导入标记** | 选择之前导出的 JSON，**按医院合并**：同一家以文件为准，本机其他标记保留；无法识别的记录会跳过并在提示里报数 |
| 导入后 | 如果某条恰好与默认层一致（例如你只是把取消的默认星标恢复回来），该条会**自动从浏览器存储中剔除**，不留无差异的垃圾记录 |

导出文件长这样（也兼容裸对象格式 `{"h_xxx":{"star":true,"note":""}}`，以及 `localStorage` 原始内容）：

```json
{
  "format": "anhui-hospital-marks",
  "version": 1,
  "exportedAt": "2026-09-16T06:22:11.482Z",
  "count": 2,
  "marks": [
    { "hid": "h_24d014373c", "name": "合肥市 / 瑶海区 / 合肥市第二人民医院", "star": true, "note": "重点跟进" }
  ]
}
```

> [!tip] 为什么只导出「我的标记」而不是全部
> 默认层是写在文件里、对所有访客可见的公共数据，导出它没有意义；真正需要备份的只有你自己在浏览器里做的那部分改动。这样文件通常只有几百字节到几 KB。

> [!note] 技术实现（刻意为之）
> 导出用 `Blob` + `URL.createObjectURL` + `<a download>`，导入用 `<input type="file">` + `FileReader`。
> **全程不碰 `fetch` / `XMLHttpRequest`，也不改写 HTML 本体** —— 因为 `file://` 下 `fetch` 必然失败，而回写 HTML 有 `</script>` 截断风险（原版就死在这两条路上，`verify.js` 里已把「前端无 fetch / 无 XHR」设为红线检查）。

> [!warning] 两个必须知道的限制
> 1. **本地文件版和网页版的数据是分开的**：`file://`（双击打开）与 `https://`（GitHub Pages）属于不同来源，各自有独立的 localStorage。建议固定用其中一个入口，别混着标。
> 2. **个人修改不跨设备**：在公司电脑标的星标，回家看不到（那是各自浏览器本地的）。要让所有人看到，必须改默认层的文件。

## 手机端适配（2026-09-16 三）

桌面是「左树 + 右面板」双栏，390px 手机上放不下。改造前实测：树容器被 690px 定宽侧栏挤到只剩 **40px**；`.hospital-actions` 靠 `:hover` 显形，触摸设备上**永远点不到星标**；控制条 7 个按钮换行堆成 855px 高一列。

现在的做法（断点 `820px`，桌面行为完全不变）：

| 变化 | 说明 |
|---|---|
| **单列 + 顶部切换器** | 一次只显示一个视图，切换器带星标/备注实时计数 |
| **树改「下钻式」** | 点地市 → 该市区县 → 该区县医院；顶部面包屑可逐级返回，**手机返回键也能退回上一层**；去掉全部横向缩进与连线，宽度全给内容 |
| **操作按钮常显** | `@media (hover: none)` —— 星标/备注按钮不再依赖悬停 |
| **搜索框常驻** | 从侧栏移到切换器下方，两个视图都能用；搜索时只保留「命中医院 → 其区县 → 其城市」这条链 |
| **触摸目标放大** | 星标/备注/移除等按钮 ≥ 42px，切换器 40px，弹窗按钮 46px |
| **防 iOS 聚焦放大** | 搜索框与备注输入框字号提到 16px（<16px 时 Safari 会强制放大整页） |
| **备注弹窗底部弹出** | 全宽、圆角在上，按钮撑满；适配 `env(safe-area-inset-bottom)` |
| **其他** | `100dvh` 适配地址栏收放、去掉点击高亮、隐藏滚动条、控制条只留「导出/导入」 |

> [!note] 为什么手机上砍掉「展开/折叠」那一排按钮
> 下钻模式下没有「展开」这个概念（一次只看一层），保留反而误导。地市/区县卡片的 `▼` 点击即进入下一层。

> [!tip] 手机端怎么验收的
> 用 CDP `Emulation.setDeviceMetricsOverride(mobile=true)` 切真机视口 —— **只有带 `mobile=true` 才会让 `@media (hover: none)` 生效**，单纯缩窗口测不出触摸端的差异。工具：`D:\WorkBuddyData\Tools\ChromeAutomation\mobile_shot.py`。

## 如何更新「默认星标」（团队深度合作医院）

默认星标由构建脚本写入，**不要手改 `index.html`**（手改会在下次构建时被覆盖）：

1. 编辑 `build.js` 里的 `DEFAULT_STARS` 数据表，每条形如：
   ```js
   { hid: 'h_a37f24ae27', name: '首都医科大学附属北京安贞医院安徽医院' }
   ```
   `hid` 是医院节点 `<li id="h_xxxxxxxxxx">` 的 id，**不是医院名**。构建时会校验每个 hid 在源名单里恰好出现 1 次。
2. 重跑构建（会自动做 12 组校验、写回 `index.html`，并同步一份到 `D:\Tools\安徽省医院名单.html`）：
   ```bash
   "C:/Users/xiaob/.workbuddy/binaries/node/versions/22.22.2-3/node.exe" \
     "D:/WorkBuddyData/Workspace/anhui-hospital-list/build.js"
   ```
3. 推送上线：
   ```bash
   "C:/Users/xiaob/.workbuddy/binaries/node/versions/22.22.2-3/node.exe" \
     "D:/WorkBuddyData/Workspace/anhui-hospital-list/push-repo.js"
   ```
   GitHub Pages 自动重建，所有访客刷新即见。

> [!caution] 构建的输入是 `backup/` 里的原版快照，不是 `D:\Tools\安徽省医院名单.html`
> 后者现在放的是**构建产物**（已被覆盖），拿它当输入会找不到 `<script id="embedded-marks">` 数据槽、构建必然失败。`build.js` 已内置这条检查并给出明确报错。

> 每次新增/删除医院会使现有 `hid` 变化，需要同步更新 `DEFAULT_STARS`。

## 维护与构建

```
build.js                 从原始名单生成 index.html（12 组自动校验 + 写回 D:\Tools + 同步仓库前检查）
app.js                   前端逻辑（注入到 index.html 的 <script> 块）
verify.js                产物静态自检（语法 / 内嵌数据 / 结构 / 导出导入实现 / 移动端就位 / 红线：无 fetch·XHR·document.write）

io-check.js              导出导入闭环（Chrome）：
                         干净起步 → 真实点击加星标+写备注 → 导出(拦截下载并读回 Blob) →
                         清空本机 → 导入恢复 → 非法JSON / 无匹配 / 混合有效无效 / 裸对象格式 /
                         取消默认星标后导入恢复→本机记录自动剔除
io-reload-a.js / -b.js   同实例内 location.reload() 后的持久化比对（等价于点浏览器刷新）
storage-check.py         本地数据层闭环（file://，每步 reload 后断言）
mobile-probe.js          移动端问题探针（改造前量化取证：溢出 / 容器宽度 / 按钮 opacity / 触摸目标 / iOS 字号）
mobile-check.js          移动端功能验证（iPhone 视口）：切换器 / 三层下钻 / 面包屑返回 /
                         触摸星标可点可存 / 视图切换 / 列表定位回树 / 搜索过滤 / 触摸目标尺寸 / 底部弹窗
mobile-diag.js / -diag2  下钻状态与盒模型诊断（排障用）
desktop-regress.js       桌面回归：确认改造后仍是双栏、hover 才显示按钮、点市仍是展开折叠而非下钻
online-check.js          线上结构验证（https，查默认星标数 / 按钮 / JS 错误）
online-storage-check.py  线上数据层闭环（真实托管 origin 上跑同一套场景）
push-repo.js             幂等推送：同步 index.html + README.md 到 xiaobaidian/tools 并校验 local == remote
backup/                  改造前的原版快照（构建的输入源，勿删）
```

移动端验证跑法（`mobile_shot.py` 在 `D:\WorkBuddyData\Tools\ChromeAutomation\`）：

```bash
python mobile_shot.py --url "file:///D:/WorkBuddyData/Workspace/anhui-hospital-list/index.html" \
  --device iphone-14 --js-file "D:/WorkBuddyData/Workspace/anhui-hospital-list/mobile-check.js" \
  --shot "D:/WorkBuddyData/Workspace/anhui-hospital-list/mobile-after.png"
```

一次性脚本（`git-tools.js` / `push-to-tools.js` / `sync-readme.js` / `fix-readme.js` / `fix-tree-push.js`）是搭建期的历史遗留，已被 `push-repo.js` 取代，可清理。

> 数据层改动**必须跑 `io-check.js` 与 `io-reload-a/b.js`**。
> 「改 → 刷新 → 看有没有保住」这类问题手工点击几乎发现不了，只有场景化自动化能抓到（本项目就靠它抓出过一次"用户改动被静默丢弃"的致命缺陷）。

## 验收结论（2026-09-16，线上 `https:` 实测）

| 检查项 | 结果 |
|---|---|
| 协议 / 医院 / 地市 / 区县 | `https:` · 530 · 16 · 105 ✅ |
| **默认星标数** | **21**（所有访客一致）✅ |
| 控制条 | 展开类 5 个 + 导出/导入 2 个 ✅ |
| 旧「保存到HTML」残留 | 0 ✅ |
| JS 错误 | 0 ✅ |
| 数据层闭环 | 干净 21 → 加星 23 → 清空回 21 → 导入恢复 23（`matchCleanState`）✅ |
| 导出链路 | blob 下载可读回，format/version/count/hint 完整 ✅ |
| 异常输入 | 非法 JSON / 无匹配 hid 均报错且**数据不变** ✅ |
| 混合导入 | 1 有效 + 2 无效 → `imported:1, invalid:2` ✅ |
| 无差异清理 | 取消默认星标再导入恢复 → 本机记录自动消失 ✅ |
| 刷新持久化 | `location.reload()` 后 23/2 与刷新前一致，备注完好 ✅ |
| **手机端**（iPhone 390×844，`mobile=true`） | 无横向溢出 · 树容器 96% 宽（改造前 10%）· 下钻 16市→9区县→11家 · 面包屑返回 · 星标按钮 42×42 且常显、点击可存 ✅ |
| **桌面回归** | 仍是双栏（树 758 + 侧栏 690）· 按钮仍 `hover` 才显示 · 点「市」仍是展开/折叠（非下钻）· 文案未变 ✅ |

## 变更记录

- **2026-09-16（三）** 手机端 UI 适配（桌面行为完全不变）：
  - 移动端断点 `820px`：单列布局 + 顶部视图切换器（医院树 / 星标 / 备注 / 统计 / 概览），切换器带实时计数
  - 树改「下钻式」：一次一层 + 面包屑返回 + `history.pushState` 支持手机返回键；去掉横向缩进与连线（原树容器在手机上只剩 40px）
  - **修复触摸端致命问题**：`.hospital-actions` / `.item-actions` 原为 `opacity:0` 且只在 `:hover` 显示 → 触摸设备上星标/备注**永远点不到**；现由 `@media (hover: none), (pointer: coarse)` 常显
  - 搜索框常驻切换器下方；手机搜索只保留「命中医院 → 区县 → 城市」链路
  - iOS：搜索框/备注框字号提至 16px（防聚焦强制放大）、`100dvh`、底部安全区
  - 触摸目标放大（按钮 ≥42px）、备注弹窗改底部弹出、手机端隐藏「展开/折叠」类按钮并缩短「导出/导入」文案
  - `build.js` 新增第 12 组移动端就位校验；新增 `mobile_shot.py`（CDP 真机视口）与 4 个移动端验证/诊断脚本

- **2026-09-16（二）** 加回「我的标记」备份能力：
  - 新增「⇩ 导出我的标记 / ⇧ 导入标记」（`Blob` 下载 + `FileReader` 读取，**不用 fetch、不改写 HTML**，绕开原版致命问题）
  - 导入支持四种格式：本工具导出 / `{marks:[...]}` / `{marks:{hid:{...}}}` / 裸对象；按 hid 合并、无效记录跳过并报数
  - 修复构建脚本输入源问题：`D:\Tools\安徽省医院名单.html` 已被产物覆盖导致 `build.js` 无法重跑，改为固定用 `backup/` 原版快照，并新增明确报错
  - 构建成功后自动同步一份到 `D:\Tools\安徽省医院名单.html`
  - 侧栏默认星标条增加「本机改动 N 条」计数
  - `verify.js` 新增导出/导入实现检查与三条红线（前端无 `fetch` / `XMLHttpRequest` / `document.write`）

- **2026-09-16（一）** 代码审查整改 + 接入默认星标：
  - 移除「导出 / 导入 / 保存到HTML」三个按钮（保存到HTML 在 `file://` 下必然失败，且存在 `</script>` 截断风险）
  - 新增内嵌默认星标（21 家深度合作医院），所有访客可见
  - 存储层重做：版本化 key + 只认带时间戳的用户编辑，避免历史脏数据覆盖默认星标
  - 修复：`getMark()` 读操作的写副作用（曾给全部 530 家写入空记录）、控件按钮索引耦合、空数据除零、枚举查表兜底
  - 改进：`重置` 现在全量复位（含筛选与搜索）、搜索框常驻侧栏、搜索清空还原展开、列表按城市顺序稳定排序、ESC 关闭备注弹窗二次确认、行内提示命中数量
  - 可访问性：树 `role=tree`、节点 `tabindex` + 键盘操作、`aria-expanded`、图标按钮 `aria-label`、`:focus-visible` 焦点态、`prefers-reduced-motion` 适配
  - 其余：去重 favicon、补 `meta description` 与 `<noscript>`、统计数字改为从 DOM 单一来源计算

---

> 归属：本页由小微为 Sanfre 开发，归档于 `xiaobaidian/tools`。
