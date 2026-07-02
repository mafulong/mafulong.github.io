---
layout: post
category: AI
title: Cursor 配置 YOLO 模式（Run Everything）
tags: AI
---

# Cursor 配置 YOLO 模式（Run Everything）

> 开启后，Agent 会自动执行 Shell / Edit / MCP / Web Search / 图片生成等工具，
> **不再每步都弹确认**，让 Agent 真正"放手去干"。

---

## 背景

Cursor UI 里的 "Run Everything" 按钮只放开了一部分 Composer 的确认，
对于 Agent 模式调用工具，仍会按风险评估逐条弹窗。

如果想真正无人值守，可以直接改 Cursor 的本地数据库 `state.vscdb`，
把 UI 没暴露出来的开关一次性全部打开。

> ⚠️ **适用版本**：Cursor 1.x。
> 老版本控制 Run Everything 的字段是 `useYoloMode`，
> **新版已经改成 `yoloEnableRunEverything`**。

---

## 配置文件位置

| 系统    | 路径                                                                                |
| ------- | ----------------------------------------------------------------------------------- |
| macOS   | `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb`               |
| Linux   | `~/.config/Cursor/User/globalStorage/state.vscdb`                                   |
| Windows | `%APPDATA%\Cursor\User\globalStorage\state.vscdb`                                   |

要修改的记录 `key`：

```
src.vs.platform.reactivestorage.browser.reactiveStorageServiceImpl.persistentStorage.applicationUser
```

`value` 是一个 JSON，所有 `composerState.*` 都是 Agent 行为开关。

---

## 字段说明

| 字段                                          | 含义                                | 目标值  |
| --------------------------------------------- | ----------------------------------- | ------- |
| `composerState.yoloEnableRunEverything`      | 开启 Run Everything（YOLO 模式）    | `true`  |
| `composerState.modes4[0].autoRun`            | Agent 自动运行                      | `true`  |
| `composerState.modes4[0].fullAutoRun`        | Agent 全自动执行工具（不只规划）    | `true`  |
| `composerState.yoloMcpToolsDisabled`         | 是否禁用 MCP（`false` = 自动调用）  | `false` |
| `composerState.yoloDeleteFileDisabled`       | 是否禁用文件删除（`false` = 允许）  | `false` |
| `composerState.yoloOutsideWorkspaceDisabled` | 是否禁止工作区外访问                | `false` |
| `composerState.autoAcceptWebSearchTool`      | 自动接受 Web Search                 | `true`  |
| `composerState.autoAcceptGenerateImageTool`  | 自动接受图片生成                    | `true`  |
| `composerState.autoApproveModeTransitions`   | 自动批准 Agent 模式切换             | `true`  |
| `composerState.enableSmartAuto`              | Smart Auto（保持关闭，更可控）      | `false` |

---

## 一键脚本

### ⚠️ 操作前请：

1. **完全退出 Cursor**（macOS 是 `Cmd + Q`，不是关窗口）
2. 确保系统装了 `sqlite3`（macOS 自带，Linux 通常也有，Windows 需安装）

保存为 `cursor-yolo.sh`：

```bash
#!/bin/bash
set -euo pipefail

DB="$HOME/Library/Application Support/Cursor/User/globalStorage/state.vscdb"
KEY="src.vs.platform.reactivestorage.browser.reactiveStorageServiceImpl.persistentStorage.applicationUser"

if [ ! -f "$DB" ]; then
  echo "❌ 找不到数据库：$DB"
  exit 1
fi

# 备份
cp "$DB" "$DB.bak.$(date +%Y%m%d_%H%M%S)"
echo "✅ 已备份到 $DB.bak.*"

sqlite3 "$DB" <<SQL
UPDATE ItemTable
SET value = json_set(
  value,
  -- Run Everything
  '\$.composerState.yoloEnableRunEverything', json('true'),
  -- Agent
  '\$.composerState.modes4[0].autoRun', json('true'),
  '\$.composerState.modes4[0].fullAutoRun', json('true'),
  -- MCP
  '\$.composerState.yoloMcpToolsDisabled', json('false'),
  -- 文件权限
  '\$.composerState.yoloDeleteFileDisabled', json('false'),
  '\$.composerState.yoloOutsideWorkspaceDisabled', json('false'),
  -- 自动接受工具
  '\$.composerState.autoAcceptWebSearchTool', json('true'),
  '\$.composerState.autoAcceptGenerateImageTool', json('true'),
  -- 自动批准模式切换
  '\$.composerState.autoApproveModeTransitions', json('true'),
  -- 保持 Smart Auto 关闭
  '\$.composerState.enableSmartAuto', json('false')
)
WHERE key='$KEY';
SQL

echo
echo "========== 当前配置 =========="

sqlite3 -header -column "$DB" "
SELECT
  json_extract(value,'\$.composerState.yoloEnableRunEverything') AS runEverything,
  json_extract(value,'\$.composerState.modes4[0].fullAutoRun')     AS fullAutoRun,
  json_extract(value,'\$.composerState.modes4[0].autoRun')         AS autoRun,
  json_extract(value,'\$.composerState.yoloMcpToolsDisabled')      AS mcpDisabled,
  json_extract(value,'\$.composerState.yoloDeleteFileDisabled')    AS deleteDisabled,
  json_extract(value,'\$.composerState.yoloOutsideWorkspaceDisabled') AS outsideWorkspaceDisabled,
  json_extract(value,'\$.composerState.autoAcceptWebSearchTool')   AS autoWebSearch,
  json_extract(value,'\$.composerState.autoAcceptGenerateImageTool') AS autoImage,
  json_extract(value,'\$.composerState.autoApproveModeTransitions') AS autoModeTransition
FROM ItemTable
WHERE key='$KEY';
"

echo
echo "✅ 完成，请重新启动 Cursor。"
```

执行：

```bash
chmod +x cursor-yolo.sh
./cursor-yolo.sh
```

成功后应该看到：

```
runEverything  fullAutoRun  autoRun  mcpDisabled  deleteDisabled  outsideWorkspaceDisabled  autoWebSearch  autoImage  autoModeTransition
-------------  -----------  -------  -----------  --------------  ------------------------  -------------  ---------  ------------------
1              1            1        0            0               0                         1              1          1
```

说明：

- `runEverything = 1`：YOLO 模式开启
- `fullAutoRun = 1`：Agent 全自动执行
- `autoRun = 1`：Agent 自动运行
- `mcpDisabled = 0`：MCP 没禁用
- `deleteDisabled = 0`：允许删除文件
- `outsideWorkspaceDisabled = 0`：允许工作区外访问
- `autoWebSearch = 1`：Web Search 自动接受
- `autoImage = 1`：图片生成自动接受
- `autoModeTransition = 1`：Agent 模式自动切换

---

## 还原

需要回退时把备份还原即可：

```bash
DB="$HOME/Library/Application Support/Cursor/User/globalStorage/state.vscdb"
LATEST_BAK=$(ls -1t "$DB".bak.* | head -1)
cp "$LATEST_BAK" "$DB"
```

或者直接在 Cursor UI 里手动关闭 Run Everything。

---

## 为什么偶尔还是会弹确认？

即使上面所有字段都打开了，Cursor 仍然可能在以下情况弹确认：

- **MCP Server 自身要求确认**：部分 MCP Server 在声明工具时强制要用户确认，
  这由 Server 而不是 Cursor 控制。
- **高风险 Shell 操作**：例如 `sudo`、系统目录、`rm -rf /` 等，
  Cursor 内置了硬编码的安全策略，不在 `state.vscdb` 里。
- **企业策略**：如果 Cursor 受企业管理，部分开关可能被锁定。

如果你 99% 的场景都不弹，但偶尔还会弹——这是正常的，
说明 Cursor 内置的安全逻辑在工作，而不是配置没生效。

---

## 平台路径速查

如果你想把这个脚本发到 Linux / Windows 上用，只改路径就行：

```bash
# Linux
DB="$HOME/.config/Cursor/User/globalStorage/state.vscdb"

# Windows (Git Bash / WSL)
DB="$APPDATA/Cursor/User/globalStorage/state.vscdb"
```

其他逻辑完全一致。

---

## 参考

- 控制 Run Everything 的字段在 Cursor 1.x 是 `yoloEnableRunEverything`，
  不是老版本的 `useYoloMode`
- 上面脚本已经覆盖 `state.vscdb` 里所有和 YOLO 相关的用户可配置开关