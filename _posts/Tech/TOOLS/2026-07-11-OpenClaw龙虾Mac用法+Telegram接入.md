---
layout: post
category: Tools
title: OpenClaw（龙虾）Mac 用法 + Telegram 接入
tags: OpenClaw AI Telegram Tools
---

[OpenClaw](https://openclaw.ai/) 是开源的个人 AI 助手，🦞 「龙虾」是它的吉祥物。一套 Gateway 服务跑在本地（Mac/Linux/Windows），通过 channel 接入你已经在用的 IM 应用（Telegram、WhatsApp、Discord、Slack、Signal、iMessage、微信、QQ 等 20+ 渠道）。

特点：
- 本地运行，数据不出机（除非自己接远程模型）
- macOS 配套 app 提供菜单栏、通知、WebChat、语音唤醒、Canvas
- 一套配置多渠道复用

## 安装

运行时：**Node 24（推荐）** 或 **Node 22.19+**。

```bash
npm install -g openclaw@latest
# 或: pnpm add -g openclaw@latest

openclaw onboard --install-daemon
```

`onboard --install-daemon` 会引导你完成 Gateway / workspace / 渠道 / skills 配置，并把 Gateway 注册为 launchd（macOS）用户服务，开机自启。

### 验证

```bash
openclaw gateway status
```

## Mac 配套 App（可选）

CLI + Gateway 已经够用，但官方还提供一个 macOS menu bar 客户端：

[GitHub Releases](https://github.com/openclaw/openclaw/releases) 下载 `OpenClaw-<version>.dmg`。

App 提供：
- 菜单栏状态 / 健康检查 / WebChat
- macOS 权限申请引导（屏幕、麦克风、语音、辅助功能）
- 本地 node 工具（Canvas、camera/screen capture、`system.run`）
- Exec approval 弹窗（防误执行）

只想要 CLI + Gateway 不用装 App。

## Telegram 接入

Telegram 是 OpenClaw 最常用的 channel 之一，基于 [grammY](https://grammy.dev/)。

### 1. 建 Bot 拿 Token

在 Telegram 找 **@BotFather**（注意核对 handle 是否完全一致）：

- 走聊天流：跟 BotFather 发 `/newbot`，按提示填名字和 username，拿到 token
- 走 Web 流：用 BotFather 的 Web App（在 web.telegram.org 里也能开），UI 里建 bot，复制 token

### 2. 写配置

`~/.openclaw/config.json5`（或 onboard 过程中直接填）：

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",          // 你的 bot token
      dmPolicy: "pairing",          // DM 策略，见下
      groups: {
        "*": { requireMention: true }  // 群里必须 @bot 才响应
      }
    }
  }
}
```

Token 解析优先级：`tokenFile` > `botToken` > 环境变量 `TELEGRAM_BOT_TOKEN`。命名账号必须用 `botToken` 或 `tokenFile`。

### 3. 启动 + 配对

```bash
openclaw gateway
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

第一次 DM bot 会拿到一个 pairing code，1 小时内有效。

### 4. 群组接入

把 bot 加到群后，还需要两个 ID：

| ID | 用途 | 怎么拿 |
|----|------|--------|
| 你的 Telegram user ID | `channels.telegram.allowFrom` / `groupAllowFrom` | DM bot 后看 `openclaw logs --follow` 里的 `from.id`；或 `curl "https://api.telegram.org/bot<token>/getUpdates"` |
| 群 chat ID | `channels.telegram.groups` 里的 key | 看 logs / getUpdates / 转发 ID bot |

> 注意：超级群 ID 是负数且 `-100` 开头，**只放在 `channels.telegram.groups`**，不要塞到 `groupAllowFrom`。

### 5. Telegram 侧设置（重要）

Bot 默认开 **Privacy Mode**，群消息只能看到 `/command` 和 @ 提及。两种方法关掉：

- `/setprivacy` → Disable
- 把 bot 设为群管理员（管理员能看到所有消息）

切换隐私模式后要**先把 bot 移出群，再加回来**，Telegram 才生效。

其他 BotFather 命令：

- `/setjoingroups` — 允许/拒绝被加群
- `/setprivacy` — 群可见性

## DM 策略

`channels.telegram.dmPolicy` 四选一：

| 值 | 行为 |
|----|------|
| `pairing`（默认） | 第一次 DM 弹 pairing code，approve 后才通 |
| `allowlist` | 必须在 `allowFrom` 里列 numeric user ID |
| `open` | 任何人都能 DM bot（必须 `allowFrom: ["*"]`） |
| `disabled` | 关 DM |

**单用户 bot 推荐**：`allowlist` + 自己的 numeric user ID；**公网 bot 才用** `open`。

## 常用命令

### 安装 / 配置 / 维护

```bash
# 首次配置（推荐走向导）
openclaw onboard --install-daemon

# 不走向导，只建 baseline 配置
openclaw setup --baseline

# 增量修改：模型 / gateway / channels / plugins / skills
openclaw configure

# 新增 channel 账号
openclaw channels add              # 向导模式
openclaw channels list             # 列已配
openclaw channels login <name>     # 扫码 / 验证登录

# 健康检查 + 自动修复
openclaw doctor
openclaw doctor --fix

# 备份 / 迁移 / 重置 / 卸载
openclaw backup create <path>
openclaw backup verify <path>
openclaw migrate list
openclaw reset
openclaw uninstall
openclaw update
```

### Gateway 服务

```bash
openclaw gateway status            # 状态
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
openclaw gateway --port 18789 --verbose   # 前台 debug
openclaw gateway health
openclaw gateway logs --follow
```

`daemon` 是 `gateway` 的旧 alias，等价。

### 消息 / Agent

```bash
# 发消息（IM 渠道）
openclaw message send --target +1234567890 --message "hello"
openclaw message broadcast --channel telegram --message "hi all"
openclaw message poll "Which day?" --options "Mon,Tue,Wed"

# 调 agent
openclaw agent --message "Ship checklist" --thinking high
openclaw agents list               # 列已注册的 agent
openclaw agents add <name> --binding ...

# ACP / MCP
openclaw acp ...                   # Agent Client Protocol
openclaw mcp serve                 # 起 MCP server
openclaw mcp list
```

### 配对 / 渠道

```bash
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
openclaw pairing approve discord <CODE>
openclaw qr                         # 生成扫码（iOS/Android node 配对）
```

### 节点 / 设备

```bash
openclaw nodes list                 # 列已配对 node
openclaw nodes pending              # 等审批的
openclaw nodes approve <id>
openclaw nodes invoke <id> --tool canvas:snapshot

openclaw devices list               # 同上另一套叫法
openclaw devices pair               # 配对新 device
openclaw devices rotate <id>        # 轮换密钥
openclaw devices revoke <id>        # 撤销
```

### 模型 / 推理

```bash
openclaw models list                # 列可用模型
openclaw models set claude-sonnet   # 设默认
openclaw models aliases add ...     # 别名
openclaw models fallbacks add ...   # 兜底链

# 鉴权（多 provider）
openclaw models auth login                # 通用
openclaw models auth login-github-copilot
openclaw models auth setup-token
openclaw models auth paste-api-key

# 用量
openclaw status --usage            # 各 provider 配额
```

支持的 provider：Anthropic、Gemini CLI、GitHub Copilot、MiniMax、OpenAI Codex、Xiaomi、z.ai。

### 浏览器 / 沙箱 / 执行审批

```bash
openclaw browser start              # 起受控浏览器
openclaw browser open <url>
openclaw browser screenshot <path>
openclaw browser eval "document.title"

openclaw sandbox list               # 列沙箱
openclaw sandbox recreate <id>      # 重建

openclaw approvals get              # 看当前审批策略
openclaw approvals set preset <name>
openclaw approvals allowlist add <pattern>
```

### 自动化 / 定时

```bash
openclaw cron list
openclaw cron add --schedule "*/5 * * * *" --message "check builds"
openclaw cron enable <id>
openclaw cron runs <id>

openclaw tasks list
openclaw webhooks gmail setup       # 接入 gmail 触发
openclaw hooks list
```

### 终端交互

```bash
openclaw tui                        # 启动 TUI（chat / terminal 都是 alias）
openclaw chat                       # 同 tui
```

### Chat 内的斜杠命令

Telegram / 其他渠道对话里直接发：

| 命令 | 作用 |
|------|------|
| `/status` | 快速诊断 |
| `/trace` | 当前 session 的 plugin trace |
| `/config` | 持久化改配置 |
| `/debug` | 运行时覆盖（仅内存，需 `commands.debug: true`） |

### 全局 flag

```bash
openclaw --dev                      # 状态隔离到 ~/.openclaw-dev，端口 19001
openclaw --profile work             # 状态隔离到 ~/.openclaw-work
openclaw --container mybox          # 在已有 docker/podman 容器里跑
openclaw --log-level debug
openclaw --no-color
openclaw --json                     # 干净输出（部分命令支持 --plain）
openclaw -V                         # 打印版本
```

> 完整 command tree 在 [docs.openclaw.ai/reference/cli](https://docs.openclaw.ai/reference/cli)。Plugin 可能加新命令（如 `voicecall`、`workboard`），跑 `<cmd> --help` 拿权威列表。

## 找 Telegram user ID（不用第三方 bot）

最稳的方法：DM 你的 bot → `openclaw logs --follow` → 看 `from.id` 里的数字。

或官方 API：

```bash
curl "https://api.telegram.org/bot<bot_token>/getUpdates"
```

> 不推荐 `@userinfobot` / `@getidsbot` 等第三方，隐私有风险。

## 常见问题

**Q: macOS App 装不上 / 闪退**

检查是否下载了 signed build（[macOS Permissions](https://docs.openclaw.ai/platforms/mac/permissions)）。macOS 权限会随未签名 build 重建而丢失。

**Q: 群里 bot 不响应**

1. 是不是没 @bot？默认 `requireMention: true`
2. Privacy Mode 没关？ `/setprivacy` + 移除重加
3. 群 ID 没加进 `channels.telegram.groups`？

**Q: `openclaw pairing approve` 失败**

Code 1 小时过期。重新 DM bot 拿新 code。

**Q: `dmPolicy: "allowlist"` 不生效**

必须是 numeric user ID，不要填 `@username`。老配置里有 `@username` 的，跑 `openclaw doctor --fix` 自动转 numeric。

**Q: Dashboard Mini App 打不开**

`/dashboard` 在群里只能用 DM 触发，且需要 `gateway.tailscale.mode = "serve"` 或 `"funnel"`。Docker 部署要 `network_mode: host` + 挂 `/var/run/tailscale` socket。

## 参考

- 仓库：<https://github.com/openclaw/openclaw>
- 文档：<https://docs.openclaw.ai/>
- Telegram channel 详细：<https://docs.openclaw.ai/channels/telegram>
- macOS 平台：<https://docs.openclaw.ai/platforms/macos>
- Discord：<https://discord.gg/clawd>