---
layout: post
category: AI
title: Claude Code：跳过权限（bypassPermissions）完全指南
tags: AI
---

# Claude Code：跳过权限（bypassPermissions）完全指南

> 减少每条命令都弹的 "Allow?" 确认，
> 让 Claude Code 真正进入"放手去干"模式。

---

## 背景

Claude Code 默认对每个 Bash / Edit / Write / WebFetch 等操作都会弹
"Allow this action?" 的确认，团队 / 个人项目里非常打断思路。

Anthropic 实际上给了一整套"跳过确认"的开关，分布在：

1. **命令行标志**
2. **`settings.json` 里的 `permissions` 和若干 `skip*` 开关**
3. **环境变量**
4. **Hooks**

下面按"由浅到深"全部列一遍。

---

## 1. 命令行：一键启动

```bash
# 等价于 permissions.defaultMode = "bypassPermissions"
claude --dangerously-skip-permissions
```

启动后：

- 不会再弹任何 `Allow?` / `Do you want to proceed?`
- 也不会再弹 "dangerous mode" 警告

⚠️ **等同于 `bypassPermissions` 模式**：

- 可执行任意命令（包括 `rm -rf /`、`sudo`、改系统目录）
- 仅在**完全信任的项目目录**下用

---

## 2. settings.json：核心配置

文件位置：

| 作用域 | 路径                       | 是否入 Git |
| ------ | -------------------------- | ---------- |
| 全局   | `~/.claude/settings.json`  | 否         |
| 项目   | `.claude/settings.json`    | 提交       |
| 覆盖   | `.claude/settings.local.json` | Gitignore |

### 2.1 `permissions.defaultMode`

```json
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  }
}
```

可选值：

| 值 | 行为 |
| --- | --- |
| `default` | 每个工具调用都弹确认 |
| `acceptEdits` | Edit/Write 自动通过，Bash 仍询问 |
| `plan` | 只能读 + 计划，不能执行 |
| `bypassPermissions` | **跳过所有确认**（最高权限） |

### 2.2 `skip*` 提示开关

```json
{
  "skipDangerousModePermissionPrompt": true,
  "skipAutoPermissionPrompt": true,
  "spinnerTipsEnabled": false
}
```

| 字段 | 作用 |
| --- | --- |
| `skipDangerousModePermissionPrompt` | 跳过"进入危险模式"的二次确认弹窗 |
| `skipAutoPermissionPrompt` | 跳过"自动确认模式"的提示 |
| `spinnerTipsEnabled` | 关闭底部 spinner 上的小贴士 |

> 配 `bypassPermissions` 时强烈建议同时开前两个，
> 否则你每次启动 Claude 都会被问一次"你确定要危险模式吗？"

### 2.3 细粒度 `allow` / `deny`（推荐方案）

比起直接 `bypassPermissions`，更稳的姿势是**白名单**:

```json
{
  "permissions": {
    "defaultMode": "default",
    "allow": [
      "Read", "Edit", "Write", "Glob", "Grep",
      "Bash(npm:*)", "Bash(npx:*)", "Bash(yarn:*)", "Bash(pnpm:*)",
      "Bash(git:*)", "Bash(make:*)", "Bash(docker:*)",
      "Bash(ls:*)", "Bash(cat:*)", "Bash(mkdir:*)", "Bash(cp:*)",
      "Bash(curl:*)", "Bash(jq:*)"
    ],
    "deny": [
      "Bash(sudo:*)",
      "Bash(rm -rf:*)",
      "Bash(rm -rf /:*)",
      "Bash(chmod 777:*)"
    ]
  }
}
```

规则优先级：**`deny` > `allow` > `defaultMode`**

注意：

- `defaultMode = "bypassPermissions"` 时，`allow` / `deny` 会被忽略
- 想保留 allow/deny 就把 defaultMode 设回 `default`

---

## 3. Hooks：把"自动确认"挂到事件上

如果你不想 `bypassPermissions` 全开，但希望某些命令自动确认，
可以用 `PreToolUse` hook：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r 'if .tool_input.command | test(\"^git \") then \"{}\" else \"{\\\"decision\\\": \\\"ask\\\"}\" end'"
          }
        ]
      }
    ]
  }
}
```

更简单的写法 —— 直接放行所有 Bash（慎用）：

```bash
# ~/.claude/hooks/auto-allow-bash.sh
#!/bin/bash
echo '{"decision": "allow"}'
```

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/auto-allow-bash.sh"
          }
        ]
      }
    ]
  }
}
```

`decision` 可选值：

| 值 | 含义 |
| --- | --- |
| `allow` | 自动通过 |
| `deny` | 直接拒绝 |
| `ask` | 弹确认（等同默认） |

---

## 4. 环境变量：减少打扰

```json
{
  "env": {
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
    "CLAUDE_CODE_ATTRIBUTION_HEADER": "0",
    "DISABLE_TELEMETRY": "1"
  }
}
```

| 变量 | 作用 |
| --- | --- |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | 关掉遥测 / 错误上报等非必要网络流量 |
| `CLAUDE_CODE_ATTRIBUTION_HEADER` | 关闭请求头里的"由 Claude Code 生成"标记 |
| `DISABLE_TELEMETRY` | 老一点的全局遥测开关 |

---

## 5. MCP 一键全开

```json
{
  "enableAllProjectMcpServers": true
}
```

开启后项目 `.mcp.json` 里列的所有 server 默认启用，
不需要逐个确认。

---

## 6. 三档推荐配置

### 🟢 A. 团队项目（保守）

> 默认模式 + 白名单常用命令 + 禁掉高危操作

```json
{
  "permissions": {
    "defaultMode": "default",
    "allow": [
      "Read", "Edit", "Write", "Glob", "Grep",
      "Bash(npm:*)", "Bash(npx:*)", "Bash(yarn:*)", "Bash(pnpm:*)",
      "Bash(git:*)", "Bash(make:*)", "Bash(docker:*)",
      "Bash(ls:*)", "Bash(cat:*)", "Bash(mkdir:*)", "Bash(cp:*)"
    ],
    "deny": [
      "Bash(sudo:*)",
      "Bash(rm -rf:*)"
    ]
  },
  "skipAutoPermissionPrompt": true,
  "spinnerTipsEnabled": false
}
```

### 🟡 B. 个人项目（中等）

> `acceptEdits`：文件操作全过，命令仍问

```json
{
  "permissions": {
    "defaultMode": "acceptEdits"
  },
  "skipDangerousModePermissionPrompt": true,
  "spinnerTipsEnabled": false
}
```

### 🔴 C. 个人本地 / 沙箱（完全 YOLO）

```json
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  },
  "skipDangerousModePermissionPrompt": true,
  "skipAutoPermissionPrompt": true,
  "spinnerTipsEnabled": false,
  "enableAllProjectMcpServers": true
}
```

或命令行：

```bash
claude --dangerously-skip-permissions
```

---

## 7. 一键写入脚本

保存为 `claude-yolo.sh`：

```bash
#!/bin/bash
set -euo pipefail

CFG="$HOME/.claude/settings.json"
mkdir -p "$(dirname "$CFG")"

# 备份
[ -f "$CFG" ] && cp "$CFG" "$CFG.bak.$(date +%Y%m%d_%H%M%S)"

cat > "$CFG" <<'JSON'
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  },
  "skipDangerousModePermissionPrompt": true,
  "skipAutoPermissionPrompt": true,
  "spinnerTipsEnabled": false,
  "enableAllProjectMcpServers": true,
  "env": {
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
    "DISABLE_TELEMETRY": "1"
  }
}
JSON

echo "✅ 已写入 $CFG"
echo "  备份：$CFG.bak.*"
```

---

## 8. 安全注意

`bypassPermissions` 真的就是"无任何拦截"：

- Claude 可以 `sudo rm -rf /`、改 `~/.ssh/`、改 `~/.zshrc`
- 配合 MCP 时尤其危险（任意工具调用都会被自动放行）
- **不要在你不信任的项目目录 / 共享机器 / 公开仓库里开**

如果想要"YOLO 但是带安全网"，推荐：

1. `defaultMode: "acceptEdits"` + `allow` 白名单
2. `deny` 列表里把 `sudo`、`rm -rf`、`chmod 777` 全列上
3. Hooks 里 PreToolUse 二次过滤（自己写 bash 校验脚本）

---

## 9. 与 Cursor 的 YOLO 模式配合

如果同时用 Cursor + Claude Code（通过 MCP 把 Claude Code 作为 MCP server 接进去），
建议**只在一个地方开 YOLO**：

- Cursor 端开 → Claude Code 端保持 `acceptEdits`（避免双层 YOLO）
- Claude Code 端开 → Cursor 端保持默认（避免双层 YOLO）

否则一不留神 `rm -rf` 真的会跑出去。

---

## 10. 速查表

| 想做的事 | 配置 |
| --- | --- |
| 完全无确认（命令行） | `claude --dangerously-skip-permissions` |
| 完全无确认（配置） | `permissions.defaultMode = "bypassPermissions"` |
| 文件自动、命令问 | `permissions.defaultMode = "acceptEdits"` |
| 白名单 | `permissions.allow = [...]` |
| 黑名单 | `permissions.deny = [...]` |
| 关危险模式警告 | `skipDangerousModePermissionPrompt: true` |
| 关自动模式提示 | `skipAutoPermissionPrompt: true` |
| 关底部 tips | `spinnerTipsEnabled: false` |
| 项目 MCP 全开 | `enableAllProjectMcpServers: true` |
| Hook 自动放行 | `hooks.PreToolUse` 返回 `{"decision":"allow"}` |

---

## 参考

- [Claude Code 官方 settings 文档](https://docs.anthropic.com/en/docs/claude-code/settings)
- `permissions.defaultMode` 可选值来自 Claude Code settings schema
- `skipDangerousModePermissionPrompt` / `skipAutoPermissionPrompt` 在 0.2.x 之后稳定