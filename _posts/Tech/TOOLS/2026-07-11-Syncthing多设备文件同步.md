---
layout: post
category: Tools
title: Syncthing 多设备文件同步（2 台 Mac + 多台 Android）
tags: Syncthing P2P Tools
---

## 概述

[Syncthing](https://syncthing.net/) 是开源的 P2P 连续文件同步工具，没有中心服务器，设备之间直接交换数据。适合：

- 2 台 Mac + 多台 Android 互相同步
- 数据敏感，不想走第三方网盘
- 不想付费 / 不被网盘限速

跨 NAT 默认走 relay 服务器（中继），LAN 下直接通。

## 安装

### macOS

```bash
brew install syncthing
```

启动：

```bash
# 前台启动，自动开 web UI
syncthing

# 后台常驻（launchd 托管）
brew services start syncthing
brew services stop syncthing
```

Web UI 入口：http://127.0.0.1:8384

> 配置目录：macOS 默认 `~/Library/Application Support/Syncthing/`，Linux 默认 `~/.config/syncthing/`。可用 `syncthing -home=DIR` 覆盖。

### Android

社区维护版 [Syncthing-Fork](https://github.com/Catfriend1/syncthing-android)：

- F-Droid 搜「Syncthing-Fork」
- 或 GitHub Releases 下载 APK 安装

> 原 `com.github.catfriend1.syncthing.android` 已停更，换 Fork 版本即可。

## 初始化

### 1. 拿到本机 Device ID

```bash
syncthing --device-id
```

或在 web UI 右上角 **Actions → Show ID**。形如：

```
MFZWI3D-BONSGYC-YLTMRWG-C43ENR5-QXGZDMM-FZWI3DP-BONSGYC-YLTMRWH
```

### 2. 互相添加设备

每台设备都要把对方的 Device ID 加进来，单向加不会建立连接：

- web UI：**Actions → Add Device** → 粘贴对方 ID → Save
- Android app：「设备」页 → 右上角 + → 填对方 ID

> Address 字段留空即可，跨网会走 relay。

### 3. 添加共享文件夹

web UI：**Add Folder**：

| 字段 | 填写 |
|------|------|
| Folder ID | 唯一标识，如 `photos`、`docs` |
| Folder Path | 本机要同步的目录（不存在会自动创建） |
| Sharing | 勾选要共享给的设备 |
| File Versioning | 按需，保留历史版本可防误删 |
| Folder Type | Send & Receive / Send Only / Receive Only |

第一次同步前先在一台设备上放文件，其他设备会拉过来。

## 同步模式（Folder Type）

| 模式 | 行为 |
|------|------|
| **Send & Receive** | 双向，默认 |
| **Send Only** | 只推不拉，本地删除不影响远端 |
| **Receive Only** | 只拉不推，适合备份 |

多设备常见配置：

| 场景 | 配置 |
|------|------|
| 两台 Mac 都要编辑 | 都选 Send & Receive |
| Mac 是「源」，Android 只读 | Mac Send Only / Android Receive Only |
| 多台 Android 互相同步照片 | 都选 Send & Receive |

## CLI 速查

```bash
# 前台启动
syncthing

# 后台常驻（macOS）
brew services start syncthing

# 打印 Device ID 并退出
syncthing --device-id

# 生成默认配置（默认路径）
syncthing -generate

# 生成配置到指定路径
syncthing -generate="$HOME/.config/syncthing"

# 用指定配置目录启动
syncthing -home="$HOME/.config/syncthing"

# 重置所有配置和数据库
syncthing -reset
```

## REST API（脚本化）

Web UI 背后是 REST API，可以用 `curl` 改配置。先在 **Settings → GUI → API Key** 拿到 key：

```bash
API=http://127.0.0.1:8384
KEY=<your-api-key>

# 列出所有文件夹
curl -s -H "X-API-Key: $KEY" $API/rest/config/folders | jq

# 新建文件夹
curl -X POST -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  $API/rest/config/folders -d '{
    "id": "photos",
    "path": "/Users/me/Pictures/Shared",
    "devices": [{"deviceID": "MFZWI3D-..."}]
  }'
```

## 常见问题

**Q: 连不上？**

- 先看 LAN 通不通：同 WiFi 下应秒连，不通常是 macOS 防火墙挡了 `syncthing` 进程，去「系统设置 → 网络 → 防火墙」放行。
- Android 要把 Syncthing-Fork 加电池优化白名单，否则后台被回收会断连。
- 跨 NAT 走 relay 速度受限，自建 relay / introducer 可解决。

**Q: 配置文件备份？**

配置文件 `config.xml` + 同级证书目录整个拷走即可：

| 平台 | 路径 |
|------|------|
| macOS | `~/Library/Application Support/Syncthing/` |
| Linux | `~/.config/syncthing/` |
| Android | app 设置里导出，或 root 后 `/data/data/.../files/` |

**Q: 文件冲突？**

Syncthing 默认策略：两边都保留，另一份改名为 `xxx~syncting~<id>.dat`，需手动决定保留哪份。**避免冲突最好的办法是单一来源（Send Only / Receive Only）**。