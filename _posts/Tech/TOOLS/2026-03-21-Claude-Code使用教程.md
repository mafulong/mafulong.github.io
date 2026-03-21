---
layout: post
category: tools
title: Claude Code使用教程
tags: Claude
---

## 安装

### macOS

```bash
# 安装
brew install anthropic/claude-code/claude

# 或下载安装
# https://github.com/anthropics/claude-code/releases

# 验证
claude --version
```

### 代理设置（可选）

网络有问题时使用代理：

```bash
export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890
```

---

## 配置文件

| 文件 | 作用域 | Git | 用途 |
|------|--------|-----|------|
| `~/.claude/settings.json` | 全局 | 否 | 个人偏好 |
| `.claude/settings.json` | 项目 | 提交 | 团队共享 |
| `.claude/settings.local.json` | 项目 | Gitignore | 个人覆盖 |

---

## 跳过确认

### permissions.defaultMode

```json
{ "permissions": { "defaultMode": "bypassPermissions" } }
```

可选值：`default`（每次询问）、`bypassPermissions`（跳过所有确认⚠️）、`plan`、`acceptEdits`

### 细粒度权限控制（推荐）

```json
{
  "permissions": {
    "defaultMode": "default",
    "allow": ["Bash(git:*)", "Bash(npm:*)", "Read", "Edit", "Glob", "Grep"],
    "deny": ["Bash(sudo:*)", "Bash(rm -rf:*)"]
  }
}
```

规则优先级：`deny > allow > defaultMode`

**注意**：`bypassPermissions` 模式下 `allow` 规则无意义。

### 其他设置

减少打扰的选项：

| 设置 | 作用 |
|------|------|
| `skipDangerousModePermissionPrompt` | 跳过危险模式警告 |
| `skipAutoPermissionPrompt` | 跳过自动模式确认 |
| `spinnerTipsEnabled` | 关闭底部 tips 提示 |

```json
{
  "skipDangerousModePermissionPrompt": true,
  "skipAutoPermissionPrompt": true,
  "spinnerTipsEnabled": false
}
```

### ⚠️ 安全警告

`bypassPermissions` 模式下 Claude 可执行任意命令，包括 `rm -rf /`。仅在完全信任当前项目时使用。

---

## 模型切换

### 切换模型

对话中使用 `/model` 指令：

```bash
/model sonnet
/model opus
/model haiku
/model MiniMax-M2.7
```

### 配置默认模型

在 `~/.claude/settings.json` 中设置：

```json
{
  "env": {
    "ANTHROPIC_MODEL": "MiniMax-M2.7",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "MiniMax-M2.7",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "MiniMax-M2.7",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "MiniMax-M2.7"
  }
}
```

### 使用自定义 API

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "your-api-key",
    "ANTHROPIC_BASE_URL": "https://api.minimax.chat/v1"
  }
}
```

---

## 常用指令

| 指令 | 说明 |
|------|------|
| `/help` | 获取帮助 |
| `/clear` | 清空对话上下文 |
| `/compact` | 压缩上下文 |
| `/resume` | 查看并恢复历史对话 |
| `/init` | 生成 CLAUDE.md |
| `/model <name>` | 切换模型 |
| `/commit` | 创建 git 提交 |
| `/review-pr <number>` | 审查 PR |

---

## Skills vs Agent vs MCP vs Hooks

这四个概念很容易混淆，先解释区别：

| 概念 | 本质 | 类比 |
|------|------|------|
| **Skill** | 一段提示/指令 | 给你一张任务卡片 |
| **Agent** | 完整的 AI 角色 | 雇佣一个专属员工 |
| **MCP** | 外部工具连接 | 给 AI 装插件 |
| **Hook** | 事件触发器 | 设置"当 X 发生时，执行 Y" |

### 一句话总结

- **Skill** - 告诉 Claude "遇到这种情况这样做"
- **Agent** - 让 Claude "变成"某个角色的专家
- **MCP** - 让 Claude "能用"外部工具
- **Hook** - 让系统"自动"在特定时刻做某事

---

## Skills

内置技能，通过 `/skill-name` 调用：

| Skill | 说明 |
|-------|------|
| `/simplify` | 审查代码优化、复用、质量 |
| `/loop` | 定时执行指令（如每 5 分钟检查状态） |
| `/claude-api` | 构建 Claude API 应用 |
| `/update-config` | 修改配置文件 |

### 自定义 Skill

在 `.claude/skills/` 目录下创建 `.md` 文件：

```markdown
# My Custom Skill

## Instructions
当你看到 `/mytool` 时，执行以下操作...

## Commands
- `echo "hello"`
```

---

## Agent

Agent 是预配置的 AI 角色，有自己的系统提示和工具限制。

### 自定义 Agent

在 `settings.json` 中配置：

```json
{
  "agents": {
    "python-dev": {
      "description": "Python 开发者",
      "systemPrompt": "你是一个 Python 专家，擅长 Django、FastAPI...",
      "model": "sonnet"
    }
  }
}
```

### 使用 Agent

```bash
claude --agent python-dev
```

### Agent vs Skill 区别

- **Skill** - 轻量，一次性任务
- **Agent** - 重量级，长期角色扮演

---

## MCP 服务器

MCP (Model Context Protocol) 让 Claude 连接外部工具和 API。

### MCP vs Skill 区别

- **Skill** - 纯提示/指令
- **MCP** - 调用真实外部服务

### 安装 MCP 服务器

```json
{
  "enableAllProjectMcpServers": true,
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}
```

### 常用 MCP 服务器

| 服务器 | 用途 |
|--------|------|
| `server-filesystem` | 文件系统操作 |
| `server-github` | GitHub API |
| `server-brave-search` | 网页搜索 |
| `server-slack` | Slack 消息 |

---

## Hooks

在特定事件发生时自动执行操作。

### Hooks vs Skills 区别

- **Skill** - 需要手动调用
- **Hook** - 自动触发

### 配置示例

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "prettier --write $FILE"
      }]
    }]
  }
}
```

### 常用事件

| 事件 | 时机 |
|------|------|
| `PreToolUse` | 工具执行前 |
| `PostToolUse` | 工具执行后 |
| `Stop` | 对话结束时 |
| `SessionStart` | 会话开始时 |

---

## CLAUDE.md 项目记忆

使用 `/init` 生成，存储项目信息供 Claude 记忆：

```markdown
# 构建
npm run build

# 测试
npm test

# 代码风格
- 下划线命名
- 函数最多 50 行

# 架构
- MVC 结构
- 路由在 routes/
```

---

## 常见问题

**Q: 如何查看历史对话？**
A: `/resume`

**Q: 上下文太长出错？**
A: `/clear` 清空对话

**Q: 如何退出？**
A: `/exit` 或 `Ctrl+C`

**Q: 如何重置配置？**
A: 删除 `~/.claude/settings.json`
