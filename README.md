# 📬 WorkBuddy 通知中心

这是小微（WorkBuddy）给我的**个人通知渠道**。每当有需要让我知道的进度、总结、提醒，小微会向本仓库**推送一个 commit**（一个 markdown 文件），GitHub 自动往我邮箱发邮件。

## 为什么用 commit 而不是 issue
- 实测：GitHub **不会**给「自己账号开的 issue」发邮件（判定自己已知情）。
- 但 GitHub **会**给「自己账号的 commit」发邮件（通知 reason=author）。
- 所以通知 = 推送文件，而非开 issue。链路稳定可靠。

## 怎么运作
- 每条通知 = `inbox/` 下一个带日期和类型的 markdown 文件，例如 `inbox/2026-08-25_0107_系统_xxx.md`。
- 文件标题/正文含：时间、类型、详情、来源链接。
- 推送动作本身触发 GitHub 邮件，主题大致为 commit message。

## 通知类型（文件名/标题前缀）
- `[进度]` 推进到哪了
- `[总结]` 一段工作汇总
- `[提醒]` 待办 / 截止 / 需注意
- `[警报]` 异常 / 失败 / 需立即处理
- `[系统]` 通知系统自身状态

## 我怎么“已读”
- 邮件端直接处理/归档即可（读状态以邮件客户端为准）。
- 想归档进 `archive/`，告诉小微“标记 X 已读”，小微会 `git mv` 过去（会产生一次归档 commit，可忽略其邮件）。
- 想回复/补充，在 issue 或邮件里说，小微下次会话会看到。

## 约定（给小微自己看的）
- 仓库：`xiaobaidian/workbuddy-notifications`（私有）
- 发通知：在本仓库 `inbox/` 新增一个 markdown 文件并 `git commit && git push`。
- commit author 必须设为 `xiaobaidian`（noreply 邮箱），否则收不到 author 通知。
- 不在此仓库放代码，只放通知。保持干净。

---
> 由 WorkBuddy 于 2026-08-25 自动搭建，机制于同日从 issue 改为 commit（issue 不自邮）。
