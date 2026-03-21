---
layout: post
category: tools
title: Claude Code使用教程
tags: Claude
---

## 安装

### macOS
```bash
# 使用 Homebrew 安装
brew install anthropic/claude-code/claude

# 或下载安装
# https://github.com/anthropics/claude-code/releases
```

### 验证安装
```bash
claude --version
```

---

## 配置

### 配置文件位置
- 全局配置: `~/.claude/settings.json`
- 项目配置: `.claude/settings.json`

### 常用配置项

```json
{
  "permissions": {
    "allow": ["Read", "Write", "Bash"],
    "deny": []
  },
  "model": "sonnet-4-6-20250514",
  "maxTokens": 8000
}
```

### 配置权限

```bash
# 允许执行 npm 命令
claude settings allow npm

# 允许所有 bash 命令
claude settings allow bash

# 允许读写项目文件
claude settings allow Read Write
```

---

## 跳过确认

### 配置文件层级

Claude Code 有 3 层配置文件，后面的会覆盖前面的：

| 文件 | 作用域 | Git | 用途 |
|------|--------|-----|------|
| `~/.claude/settings.json` | 全局 | 否 | 个人偏好 |
| `.claude/settings.json` | 项目 | 提交 | 团队共享 |
| `.claude/settings.local.json` | 项目 | Gitignore | 个人覆盖 |

### permissions.defaultMode

跳过确认的核心配置：

```json
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  }
}
```

可选值：
- `default` - 每次询问（安全）
- `bypassPermissions` - 跳过所有确认（危险⚠️）
- `plan` - 进入 plan 模式前询问
- `acceptEdits` - 接受编辑，跳过执行确认

### 细粒度权限控制（推荐）

```json
{
  "permissions": {
    "defaultMode": "default",
    "allow": ["Bash(git:*)", "Bash(npm:*)", "Bash(node:*)", "Read", "Edit", "Glob", "Grep"],
    "deny": ["Bash(sudo:*)", "Bash(rm -rf:*)"],
    "ask": ["Write(/etc/*)"]
  }
}
```

规则优先级：`deny > allow > defaultMode`

**注意**：`bypassPermissions` 模式下，所有非 deny 操作直接执行，`allow` 规则无意义。

### 其他跳过确认的设置

```json
{
  "skipDangerousModePermissionPrompt": true,
  "skipAutoPermissionPrompt": true,
  "spinnerTipsEnabled": false,
  "feedbackSurveyRate": 0
}
```

### 环境变量

```bash
export CLAUDE_SKIP_CONFIRM=true
export API_TIMEOUT_MS=3000000  # API 超时 3 秒
```

### ⚠️ 安全警告

`bypassPermissions` 模式下 Claude 可以执行任意命令，包括：
- `rm -rf /` 之类的删除操作
- 修改系统文件
- 执行未知脚本

**仅在完全信任当前项目代码时使用**。日常使用建议保持 `default` + 细粒度 `allow` 规则。

---

## 常用命令

### 基础命令

| 命令 | 说明 |
|------|------|
| `claude` | 启动对话 |
| `claude --help` | 显示帮助 |
| `claude --version` | 查看版本 |

### 对话中常用指令

| 指令 | 说明 |
|------|------|
| `/help` | 获取帮助 |
| `/clear` | 清空对话 |
| `/compact` | 压缩上下文 |
| `/model <name>` | 切换模型 |
| `/commit` | 创建 git 提交 |
| `/review-pr <number>` | 审查 PR |

---

## 常用工具

### Read - 读取文件

```bash
Read /path/to/file
Read /path/to/file offset=10 limit=50
```

### Write - 写入文件

```bash
Write /path/to/file content="文件内容"
```

### Edit - 编辑文件

```bash
Edit /path/to/file old_string="旧内容" new_string="新内容"
```

### Glob - 文件搜索

```bash
Glob **/*.js
Glob src/**/*.ts
```

### Grep - 内容搜索

```bash
Grep "functionName" type=js
Grep "error" output_mode=content -C 3
```

### Bash - 执行命令

```bash
Bash command="ls -la" timeout=30000
```

---

## 最佳实践

1. **安全第一**: 敏感操作（如 `rm -rf`、`git push --force`）不要添加到白名单
2. **项目隔离**: 建议在项目级别配置权限，而不是全局配置
3. **定期审查**: 定期检查 `.claude/settings.json` 确保配置合理
4. **使用 Task 工具**: 复杂任务使用 TaskCreate/TaskUpdate 跟踪进度

---

## 常见问题

**Q: 如何退出 Claude?**
A: 输入 `/exit` 或按 `Ctrl+C`

**Q: 如何中断正在执行的命令?**
A: 按 `Ctrl+C`

**Q: 如何查看当前配置?**
A: `claude settings list`

**Q: 如何重置配置?**
A: 删除 `~/.claude/settings.json` 或使用 `claude settings reset`
