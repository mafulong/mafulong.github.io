---
layout: post
category: AI
title: Hermes-Agent + MiniMax + Telegram 实战记录
tags: AI, Hermes, MiniMax, Telegram, GFW, Claude-Code
---

## 背景

想让 Telegram bot 接 LLM，跑一个"手机随时跟 Claude 聊天"的本地 agent。

我日常 Claude Code 走的是 minimaxi（[minimaxi](https://www.minimax.io)）第三方 Anthropic-compatible 代理（`ANTHROPIC_BASE_URL=https://api.minimaxi.com/anthropic`），所以"用 Claude Code 一行命令搞定"的官方方案对我无效。

目标：找一条能在 macOS（上海，Clash 翻墙）+ minimaxi 代理 + Telegram bot 的组合下跑通的链路。

## 排除：Claude Code `--channels`

试了一下：

```
claude --channels plugin:telegram@claude-plugins-official
# ▎ --channels ignored (plugin:telegram@claude-plugins-official)
# ▎ Channels are not currently available
```

CLI 显式忽略了 `--channels`。翻 [anthropics/claude-plugins-official#783](https://github.com/anthropics/claude-plugins-official/issues/783)，跟我撞到的报错一字不差。两个常见触发条件：

1. `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` 在 env 里 —— 删了，无效
2. `ANTHROPIC_BASE_URL` 指向第三方（minimaxi 这种） —— **命中**

官方文档原文：channels "require Anthropic authentication through claude.ai or a Console API key, and are not available on Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry"。第三方 base URL 走同样的排除路径。Issue 783 的反馈也证实了。

**结论**：Claude Code 跑 minimaxi 是 OK 的，但 channels 拒绝走 minimaxi。要么换一方 Claude 账号专门跑 bot（多一个账单），要么换工具栈。

## 选定：hermes-agent（Nous Research）

调研了一圈，能同时覆盖 MiniMax + Telegram 的成熟方案不多：

| 方案 | MiniMax | Telegram | 备注 |
|------|---------|----------|------|
| Claude Code --channels | ✓ 但 channels 拒第三方 | ✓ | 不可行 |
| [hermes-agent](https://github.com/NousResearch/hermes-agent) | ✓ 一等公民（`minimax`/`minimax-cn` provider）| ✓ 6 个内置 gateway 之一 | 180k stars，LiteLLM 自动覆盖 MiniMax |
| 直写 python-telegram-bot | 自己拼 | 自己拼 | 接触面最小但全靠手撸 |
| n8n | 走 OpenAI 兼容节点 | ✓ Trigger 节点 | 工作流友好但流式分块有延迟 |
| Dify | OpenAI 兼容 provider | ✓ webhook | 偏 RAG/agent 风 |

hermes-agent 胜在一体化：装好就能跑，Telegram 内置，LiteLLM 把 MiniMax 的 `/v1/chat/completions` 翻译成 OpenAI 协议。我写一篇调研而不是详细对比是因为后面 hermes 自己也有坑（见下），但**架构选型这一步是对的**。

## 安装 + 配置

```bash
brew install uv                                  # 安装脚本依赖
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash -s -- --non-interactive --skip-setup --no-skills
```

`--non-interactive` 跳过 setup 向导，`--no-skills` 不下载 73 个 bundled skills（节省时间）。装完路径：

- 配置：`~/.hermes/config.yaml`
- 密钥：`~/.hermes/.env`
- 代码：`~/.hermes/hermes-agent/`

改 `~/.hermes/config.yaml` 锁定模型：

```yaml
model:
  default: "MiniMax-M3"
  provider: "minimax-cn"
```

填 `~/.hermes/.env`：

```bash
MINIMAX_CN_API_KEY=sk-cp-...
MINIMAX_CN_BASE_URL=https://api.minimaxi.com/v1
TELEGRAM_BOT_TOKEN=<BotFather 给的>
TELEGRAM_ALLOWED_USERS=<你的 Telegram 数字 ID，从 @userinfobot 查>
```

**验证 LLM 通**：

```bash
curl -sS -X POST "https://api.minimaxi.com/v1/chat/completions" \
  -H "Authorization: Bearer $MINIMAX_CN_API_KEY" \
  -d '{"model":"MiniMax-M3","max_tokens":50,"messages":[{"role":"user","content":"1+1=?"}]}'
# → "1+1=2。" ✓
```

## GFW 这一关

`api.telegram.org` 在国内不通，bot 永远连不上。Clash Verge 在 `127.0.0.1:33331`（dashboard 端口，不是代理端口）跑，实际 mixed proxy 在：

```bash
mixed-port: 7897   # HTTP + SOCKS 都在这
socks-port: 7898
```

裸 curl 验证：

```bash
curl -x "http://127.0.0.1:7897" "https://api.telegram.org/bot<TOKEN>/getMe"
# → {"ok":true,"result":{"username":"claudeCodeMflBot",...}}
```

✓ Telegram API 通过代理可达。

hermes-agent 的 Telegram 插件支持环境变量代理：

| 变量 | 优先级 |
|------|--------|
| `TELEGRAM_PROXY` | 最高 |
| `HTTPS_PROXY` / `HTTP_PROXY` / `ALL_PROXY` | 中 |
| macOS 系统代理（`scutil --proxy`） | 兜底 |

但 `~/.hermes/.env` 里设 `TELEGRAM_PROXY` 不够 —— 启动后会卡在：

```
WARNING [Telegram] Discovering Telegram API fallback IPs via DNS-over-HTTPS…
WARNING [Telegram] Connecting to Telegram (attempt 1/8)…
```

**两个问题**：

1. **DoH discovery 卡死**：插件默认会通过 dns.google / cloudflare-dns.com 查询 `api.telegram.org` 的 A 记录。这两个 DoH endpoint 在国内不通，httpx client 没配代理，会一直 hang 到 30 秒超时。

2. **fallback-IP 分支被绕开**：读源码 `plugins/platforms/telegram/adapter.py` 发现一个反直觉的判断：

```python
# line 3454 原始
if fallback_ips and not proxy_url and not disable_fallback:
    # 用 TelegramFallbackTransport（自动重试 fallback IP）
elif proxy_url:
    # 用 HTTPXRequest + proxy 直连，不走 fallback IP
else:
    # 无 proxy 也无 fallback：直连
```

设了 `TELEGRAM_PROXY` → `proxy_url` 非空 → **永远走 elif 分支** → DoH discovery 之前虽然因为 `TELEGRAM_FALLBACK_IPS` 跳过了，但 transport 没用到 fallback IP，只用直连 + proxy。**预期 fallback IP 是为了在 DoH 失败时还能连上 Telegram，结果 fallback IP 分支要 proxy_url 为空才进**，逻辑反了。

## 打的补丁

最小修改：去掉 `not proxy_url` 这个限制：

```diff
- if fallback_ips and not proxy_url and not disable_fallback:
+ if fallback_ips and not disable_fallback:
```

这样 `TELEGRAM_FALLBACK_IPS=149.154.166.110,149.154.167.220`（Telegram Bot API 的稳定 IP，来自 OpenClaw 的 seed 列表）就会**始终**生效，无论 proxy 是否配置。TelegramFallbackTransport 内部还是会 `_resolve_proxy_url("TELEGRAM_PROXY", ...)` 拿代理，自己内部 AsyncHTTPTransport 用上。

启动命令：

```bash
export TELEGRAM_PROXY="http://127.0.0.1:7897"
export TELEGRAM_FALLBACK_IPS="149.154.166.110,149.154.167.220"
hermes gateway run
```

**补丁之外还要清 `__pycache__`**：

```bash
find ~/.hermes/hermes-agent -name __pycache__ -type d -exec rm -rf {} +
```

否则 `pip` 装的 `.pyc` 会盖过 `.py` 源码。

## 仍未解决的 hang

打了补丁 + 清缓存后，gateway 仍然卡在：

```
WARNING [Telegram] Connecting to Telegram (attempt 1/8)…
```

应用层 `app.initialize()` 内 hang，重试间隔 30 秒一轮，8 轮跑完才退出。但**standalone 验证都通过**：

```python
# 这个跑得通，3 秒内完成
from telegram import Bot
from telegram.request import HTTPXRequest
bot = Bot(token=TOKEN, request=HTTPXRequest(proxy='http://127.0.0.1:7897'))
await bot.get_me()             # ✓
await bot.delete_webhook()     # ✓
```

把同样的参数喂给 `ApplicationBuilder().request(...)` + `app.initialize()` 也正常：

```python
app = ApplicationBuilder().token(TOKEN).request(request).get_updates_request(request).build()
await asyncio.wait_for(app.initialize(), timeout=20)  # ✓
```

所以问题**不在网络、不在 python-telegram-bot、不在 proxy**，是 hermes-agent 的 adapter.py 在构造 `Application` 时混了什么进去导致 `initialize()` 内的某个 await 卡住。具体点没继续追 —— 调试 hermes-agent 0.10.0 的源码很容易陷入补丁越来越多但不确定哪个版本会修的循环。

## 当前状态

| 步骤 | 状态 |
|------|------|
| hermes-agent 安装 | ✓ |
| MiniMax API 接入 | ✓（curl 实测通过，模型 `MiniMax-M3`）|
| Telegram bot token | ✓（BotFather 拿到，claudeCodeMflBot）|
| Telegram 代理配置 | ✓（Clash mixed-port 7897 + TELEGRAM_FALLBACK_IPS）|
| hermes gateway 端到端启动 | ✗（hang 在 `app.initialize()`，独立测试都过，疑 hermes 上游 bug）|
| fallback IP 分支修复 | ✓（adapter.py 一行补丁 + 清缓存）|

## 备选：直写 python-telegram-bot

如果完全不要 hermes-agent，~80 行 Python 就够了：

```python
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from openai import AsyncOpenAI   # OpenAI 兼容客户端

MINIMAX_KEY = "sk-cp-..."
TELEGRAM_TOKEN = "..."
PROXY = "http://127.0.0.1:7897"

llm = AsyncOpenAI(api_key=MINIMAX_KEY, base_url="https://api.minimaxi.com/v1")

async def reply(update: Update, ctx):
    r = await llm.chat.completions.create(
        model="MiniMax-M3",
        messages=[{"role": "user", "content": update.message.text}],
    )
    await update.message.reply_text(r.choices[0].message.content)

app = (
    ApplicationBuilder()
    .token(TELEGRAM_TOKEN)
    .proxy(PROXY)   # python-telegram-bot 内置代理支持
    .build()
)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
app.run_polling()
```

装 `python-telegram-bot` 和 `openai` 之后直接 `python bot.py`。不依赖 hermes，不依赖 LiteLLM，bug surface 小一截。代价是没有 hermes 的 memory/skills/sessions 体系 —— 纯聊天场景够用，要 tool/agent 还得用 hermes。

## 给 minimaxi 用户的速查表

```
Claude Code --channels     拒第三方 base URL，放弃
hermes-agent                架构对，但 0.10.0 上游有 hang bug，
                            要打 adapter.py 补丁 + 等修复
直写 python-telegram-bot    最稳，~80 行，绕过所有框架问题
```

后两者都过同一组环境：minimaxi 中国端点 + Telegram bot + Clash `127.0.0.1:7897` 代理 + `MiniMax-M3` 模型。

## 参考

- [anthropics/claude-plugins-official#783](https://github.com/anthropics/claude-plugins-official/issues/783) — `--channels ignored` 同款报错
- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) — 仓库 + 安装脚本
- [LiteLLM minimax provider](https://docs.litellm.ai/docs/providers/minimax) — provider 注册表
- [python-telegram-bot 文档](https://docs.python-telegram-bot.org/) — `ApplicationBuilder().proxy()`