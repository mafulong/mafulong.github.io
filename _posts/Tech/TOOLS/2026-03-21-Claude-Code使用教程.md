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

如果网络有问题，使用代理：

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

## Skills

内置的自动化技能，通过 `/skill-name` 调用：

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

## Hooks

Hooks 让你在特定事件发生时自动执行操作。

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
    }],
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "echo 'Bash: $COMMAND' >> ~/.claude/bash-log.txt"
      }]
    }]
  }
}
```

### 常用 Hook 事件

| 事件 | 时机 |
|------|------|
| `PreToolUse` | 工具执行前 |
| `PostToolUse` | 工具执行后 |
| `Stop` | 对话结束时 |
| `SessionStart` | 会话开始时 |

---

## MCP 服务器

Model Context Protocol 服务器，扩展 Claude 的能力。

### 安装 MCP 服务器

在 `.claude/settings.json` 中配置：

```json
{
  "enableAllProjectMcpServers": true,
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
    }
  }
}
```

### 常用 MCP 服务器

| 服务器 | 用途 |
|--------|------|
| `server-filesystem` | 文件系统操作 |
| `server-github` | GitHub API 操作 |
| `server-brave-search` | 网页搜索 |

---

## Agent 自定义

创建自定义 Agent 改变 Claude 的行为。

### 配置 Agent

```json
{
  "agent": "my-agent",
  "agents": {
    "my-agent": {
      "description": "我的自定义 Agent",
      "systemPrompt": "你是一个专注于 Python 的开发者...",
      "model": "sonnet"
    }
  }
}
```

### 使用 Agent

```bash
claude --agent my-agent
```

或在对话中用 `/agent` 指令切换。

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
