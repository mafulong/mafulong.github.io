---
layout: post
category: tools
title: Claude Code使用教程
tags: Claude
---

## 安装

```bash
# macOS
brew install anthropic/claude-code/claude

# 验证
claude --version
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
