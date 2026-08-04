---
layout: post
category: AI
title: 9router 安装与对比 cc-switch
tags: AI Tools 9router cc-switch ClaudeCode LLMGateway Proxy
---

最近折腾 AI CLI 工具链，发现 [9router](https://github.com/decolua/9router) 这个项目在 GitHub Trending 上蹿得很快（24.6k⭐，周下载量也在涨）。第一眼以为是 cc-switch 的"另一个桌面端替代品"，但翻完文档 + 实际跑了一下，发现定位完全不同 —— **9router 是 LLM 网关/路由器，cc-switch 是供应商配置管理器**。两个东西不是替代关系，是互补的，但默认值不一样。

本文：先讲 9router 是什么、怎么装、怎么用；再放一张和 cc-switch 的横向对比；最后给一个我自己用的组合方案。

## 1. 9router 是什么

[9router](https://github.com/decolua/9router)（npm 包名 `9router`，`decolua/9router`，MIT）是一个**本地 LLM 网关**：

- 一个 HTTP 代理服务，常驻在 `http://localhost:20128`
- 把请求路由到 40+ AI provider（OpenAI / Anthropic / Gemini / Codex / Bedrock / Qwen / 智谱 / DeepSeek / Ollama …）、100+ 模型
- **核心卖点**：
  - **RTK Token Saver** — 自动压缩 `tool_result`（git diff、grep、ls 这类工具输出），省 20-40% token
  - **3 段式自动降级**：subscription → cheap → free，订阅额度用完自动接便宜模型，再不行接免费
  - **多账号轮询**：同一 provider 配多个 key，自动 round-robin
  - **订阅额度追踪**：实时显示 Claude / Codex / Cursor 剩余配额
- 不是 GUI 桌面应用，本体是 Node.js CLI + Next.js 写的 Web Dashboard
- 配套工具：上游是 Go 写的 [CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI)

跟 cc-switch 的核心区别：**9router 是「请求经过的代理」，cc-switch 是「写配置文件的 GUI」**。下面章节会更细。

## 2. 安装

9router 提供三种形态，按使用场景选：

### 2.1 桌面端最简：npx 一行

```bash
npx 9router
# 或全局装
npm install -g 9router
9router
```

启动后自动开浏览器 → `http://localhost:20128/dashboard`。**默认监听 20128**，跟常用的 3000 / 8080 / 8000 都不冲突。

CLI 选项：

```bash
9router                  # 默认启动 + 自动开浏览器
9router --port 8080      # 换端口
9router --no-browser     # 不自动开浏览器
9router --skip-update    # 跳过自检更新
9router --help           # 所有选项
```

### 2.2 服务器 / VPS：Docker

```bash
docker run -d --name 9router -p 20128:20128 \
  -v "$HOME/.9router:/app/data" -e DATA_DIR=/app/data \
  decolua/9router:latest
```

镜像同时发在 Docker Hub (`decolua/9router`) 和 GHCR，支持 amd64 / arm64。挂 `$HOME/.9router` 是为了**持久化 SQLite 数据**（账号、provider 配置、配额历史都在这），不挂重启就丢。

### 2.3 前置依赖

- Node.js 18+（npx 路线），或 Docker（容器路线）
- 任意一个 CLI 工具作为下游消费者：Claude Code / Codex / OpenClaw / Cursor / Cline / Copilot / Antigravity / Gemini CLI / OpenCode / Qwen Code / Aider … — 凡是支持 OpenAI / Anthropic 兼容 endpoint 的都行

数据落盘位置：

| 平台 | 路径 |
|------|------|
| macOS / Linux | `~/.9router/db/data.sqlite` |
| Windows | `%APPDATA%/9router/db/data.sqlite` |
| Docker | `/app/data/db/data.sqlite`（挂 `$HOME/.9router`） |

## 3. 配置与使用

### 3.1 接 Provider

打开 Dashboard → Providers → 选「Connect」。两类起步最省事：

- **Kiro AI**：免费 Claude 不限量（**注意**：我写博客时这个口子还在，AI 类免费午餐通常寿命不长，先到先得）
- **OpenCode Free**：免认证

需要正经接 Claude / GPT 时，按 Dashboard 提示填 base_url + api_key 即可，跟 cc-switch 里加 Provider 的字段几乎一致。

### 3.2 接下游 CLI（以 Claude Code 为例）

把 Claude Code 的 API endpoint 改成指向 9router：

```
Endpoint:  http://localhost:20128/v1
API Key:   [从 9router Dashboard 复制]
Model:     kr/claude-sonnet-4.5    # 9router 的"虚拟模型名"
```

`kr/` 前缀是 9router 的别名空间，写在请求里表示走它的 router 逻辑（quota 追踪、降级都在这一层做）；不写前缀直接当 passthrough 也有。

**CC Switch 用户切换路径**：如果你已经在用 cc-switch，最简单的迁移/共存方案是让 cc-switch 也指 9router——把 cc-switch 的某个 Provider 的 base_url 改成 `http://localhost:20128/v1`，模型名写 `kr/<model>`，所有走这个 Provider 的 CLI 实际都会先经过 9router。

### 3.3 验证

```bash
# dashboard 应该有请求记录
open http://localhost:20128/dashboard

# Claude Code 端能正常响应即可
claude "echo hi"
```

## 4. 和 cc-switch 的对比

先放硬数据：

| 维度 | 9router | cc-switch |
|------|---------|-----------|
| GitHub stars | 24.6k | **124k** |
| 最新版本 | v0.5.35（2026-07-16） | **v3.19.1**（2026-07-31） |
| 技术栈 | Node.js + Next.js（Web Dashboard） | **Rust + Tauri 2**（原生桌面 GUI） |
| 平台 | 桌面 + Docker（VPS） | **Windows / macOS / Linux 桌面** |
| 安装 | `npx 9router` / Docker | **`.dmg` / `.msi` / `.deb` / Homebrew `brew install --cask cc-switch`** |
| 形态 | 本地 HTTP 代理（`:20128`） | 桌面 GUI + 可选本地代理 |
| 管理 CLI 工具数 | 18+（Claude Code / Codex / Cursor / Cline / Copilot / OpenCode / Hermes …） | **8 个一等公民**（Claude Code / Claude Desktop / Codex / Gemini CLI / Grok Build / OpenCode / OpenClaw / Hermes） |
| 核心能力 | **路由 + 降级 + RTK 压缩** | **配置管理 + MCP + Skills + Prompts + Sessions + 用量统计** |
| 内置 provider 预设 | 40+ | 50+ |
| 多账号 | ✅ round-robin | ✅ 多 profile |
| 自动降级 / 故障转移 | ✅ Subscription → Cheap → Free 三段 | ✅ Circuit breaker + 健康检查（proxy 模式） |
| MCP 管理 | ❌（不管 MCP） | ✅ 跨 6 个 CLI 双向同步 |
| Skills 管理 | ❌ | ✅ GitHub 一键安装 + 双向同步 |
| Prompts / AGENTS.md | ❌ | ✅ 跨 CLI 同步 + 防回填 |
| 会话历史 | ❌ | ✅ 跨 CLI 浏览/搜索/恢复 |
| 用量统计 | ⭕ 仅配额追踪 | ✅ 趋势图 + 模型定价 + 请求日志 |
| Token 压缩 | ✅ **RTK 20-40%** | ❌ |
| 订阅额度追踪 | ✅ Claude / Codex / Cursor | ✅ 多 provider 余额面板 |
| Tray 快速切换 | ❌（走 Dashboard） | ✅ 系统托盘一键切 |
| 云同步（多设备） | ❌ | ✅ Dropbox / OneDrive / iCloud / WebDAV |
| Deep Link | ❌ | ✅ `ccswitch://` 一键导入 |
| 系统级自动更新 | ❌（要 `--skip-update`） | ✅ 内置 auto-updater |

> 数据采集自 GitHub API + 各自 README 主页，2026-08-04。

### 4.1 一句话定位

- **cc-switch**：我是**配置管理员**。你来选 provider，我把配置写到对应 CLI 的配置文件里；额外帮你管 MCP / Skills / Prompts / 会话。
- **9router**：我是**网络代理**。请求经过我，我决定这次走哪家、要不要压缩、要不要降级。

### 4.2 工作模式差异（重点）

cc-switch 有两种工作模式，**默认是写配置模式**：

1. **写配置模式（默认）**：你在 GUI 里点「启用 Provider A」→ cc-switch 把 Provider A 的 base_url / api_key 写进 `~/.claude/settings.json`（或对应 CLI 的配置）→ Claude Code 下次启动就用 A。**CLI 不重启不生效**（Claude Code 例外）。
2. **Proxy 模式（可选）**：cc-switch 启动一个本地代理（类似 9router），CLI 指过来，热切换不重启。配 circuit breaker + failover。

9router **只有 proxy 模式**——它本质上就是个代理，所有路由、降级、压缩逻辑都跑在请求路径上。

### 4.3 各自最强的场景

**用 cc-switch 的场景：**

- 同时管理多个 CLI 工具的配置（Claude Code + Codex + Gemini CLI + OpenClaw + Hermes …）
- 想统一管 **MCP server**、**Skills**、**Prompts（CLAUDE.md / AGENTS.md / GEMINI.md）**
- 想看**用量统计 + 请求日志**
- 想**跨设备同步**配置（iCloud / Dropbox）
- 想用**系统托盘**秒切 provider

**用 9router 的场景：**

- 你**只有 1-2 个 CLI**（比如就 Claude Code + Codex），但想**自动降级** + **省 token**
- 同一 provider 想接**多账号**，自动 round-robin
- 想跑在 **VPS / 服务器**上，给团队共享一个智能路由入口
- 想用 **RTK Token Saver** 把 `git diff` / `grep` / `ls` 这类工具输出压一下
- 想让**订阅额度在月底前自动用完**（9router 会主动调度到还没用满的 provider）

### 4.4 坑 & 注意

**9router 的坑：**

- **0.5.x 版本号**：v0.5.35 说明还在快速迭代，breaking change 概率比 cc-switch 高。生产用钉住版本：`npx 9router@0.5.35`
- **完全没 GUI 桌面**：所有操作走 Web Dashboard + 命令行，习惯 cc-switch 原生窗口的人会别扭
- **不接管 MCP / Skills / Prompts**：这些 9router 完全不管，需要另外的工具
- **Kiro AI 之类的免费口子**：依赖上游第三方，**随时可能挂**，别当生产方案
- **多账号轮询 vs cc-switch**：9router 是同 provider 多 key round-robin；cc-switch 是配置层多 profile，按需手动切

**cc-switch 的坑（这些 9router 反而不踩）：**

- **默认模式要重启 CLI**：除了 Claude Code，其它工具切完 provider 都要重启终端
- **proxy 模式是可选的、配置项多**：想用降级要手动开 proxy service
- **Tauri 应用首启动慢**：Rust 编译产物虽然小，冷启动几百 ms

## 5. 我自己的组合

日常开发机上**两个一起跑**：

- **cc-switch** 做主面板 —— 管 8 个 CLI 的配置、MCP、Skills、Prompts；面板看用量；托盘切主用 provider
- **9router** 跑在 Docker 里（端口 20128）—— 给"想省钱"的 session 当后端：CLI → cc-switch → 9router → 上游，9router 自动压 token + 降级

具体接法：

1. 9router 跑起来，接好所有 provider，Dashboard 里能看到每个 provider 的状态
2. cc-switch 加一个 `9router-pass-through` Provider，base_url 填 `http://localhost:20128/v1`，模型名 `kr/claude-sonnet-4.5`
3. 不在意钱的场景（生产代码 review）直接用 cc-switch 的原生 provider；在意 token 的场景（晚上刷量、跑长任务）切到 `9router-pass-through`

如果是 VPS / 多人协作场景，**9router 单跑就够了**——一个 endpoint 服务所有人，Dashboard 上能看全局用量。

## 6. 选哪个

按人数 / 场景直接给答案：

| 你是谁 | 推荐 |
|--------|------|
| 个人开发者，主要用 Claude Code + Codex | **9router**（一个 endpoint 自动降级省心） |
| 个人重度玩家，5+ 个 CLI 全要管 | **cc-switch**（GUI 写配置 + 统一 MCP/Skills） |
| 小团队，VPS 共享一个 AI 入口 | **9router Docker**（一个 endpoint 服务多人） |
| 想要 100% 本地、可视化、不折腾命令行的 | **cc-switch**（Rust 原生 GUI，开箱即用） |
| Token 敏感、订阅额度月底用不完的 | **9router**（RTK 压 + 自动调度） |
| 已经在用 Claude Code + 一堆 MCP server | **cc-switch**（MCP 双向同步是真刚需） |
| 想两个都要 | 参考上面第 5 节组合方案 |

## 参考

- 9router GitHub：[decolua/9router](https://github.com/decolua/9router)
- 9router npm：[9router on npm](https://www.npmjs.com/package/9router)（v0.5.45 发布日 2026-07-16）
- 9router 官网：[9router.com](https://9router.com)
- cc-switch GitHub：[farion1231/cc-switch](https://github.com/farion1231/cc-switch)（v3.19.1，2026-07-31）
- cc-switch 官网：[ccswitch.io](https://ccswitch.io)
- 上游 Go 实现：[router-for-me/CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI)