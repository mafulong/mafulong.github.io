---
layout: post
category: Others
title: 浏览器书签 + WebSocket 桥接（通用模式）
tags: Others
---

一套**不依赖具体业务平台**的本地遥控模式：用浏览器书签把脚本注入到「已登录」的网页，经本机 WebSocket 接收命令，再在页面里用 `fetch`（带 cookie）调用目标站 API。

适用场景：目标系统只有浏览器登录态、不便导出 cookie / Token，又希望用 curl / Agent / 脚本自动化操作。

---

## 1. 原理（一句话）

> 本地服务发命令 → WebSocket 推到浏览器 → 浏览器带着当前登录 cookie 去调目标站。

```
curl / Agent / 脚本
        │  HTTP  REST
        ▼
┌───────────────────┐
│  本地 Node 服务    │  REST 端口（例：9100）
│  + WebSocket 服务  │  WS 端口（例：9101）
└─────────┬─────────┘
          │  WebSocket 长连接
          ▼
┌───────────────────┐
│ 目标站点已打开的页 │  已登录，有 cookie
│ + 书签注入的 bridge.js │
└─────────┬─────────┘
          │  fetch(..., { credentials: 'include' })
          ▼
     目标站点同源 API
```

不是「把 cookie 拷出来」；是「遥控已登录的浏览器页」。

---

## 2. 三个组件

| 组件 | 是什么 | 职责 |
|------|--------|------|
| 书签 / Bookmarklet | 浏览器书签栏里的一段 `javascript:...` | 往当前页插入 `<script src="http://localhost:REST/bridge.js">` |
| 本地服务 | 本机 Node（HTTP + WebSocket） | 对外提供 REST；对内把命令推给浏览器；等结果返回 |
| 桥接脚本 `bridge.js` | 注入到目标页的 JS | 连本机 WS；收命令；用 `fetch` 调目标站；回传结果 |

可选：页面右下角小 UI（状态灯、手动按钮、日志），方便人眼确认「已连接」。

---

## 3. 怎么用（操作步骤）

### 3.1 准备

1. 本机安装 Node.js，项目目录里有 `server.js` + `bridge.js`（见下文最小模板）。
2. 安装依赖并启动：

```bash
cd /path/to/your-bridge-tool
npm install ws
node server.js
```

看到类似输出即成功：

```
REST  http://localhost:9100
WS    ws://localhost:9101
```

3. 健康检查：

```bash
curl -sf http://localhost:9100/api/status
# 期望: {"ok":true,"browser":false}   ← 此时还没连浏览器
```

### 3.2 添加书签

新建书签，**名称**随意（如 `Inject Bridge`），**地址**填（整行）：

```javascript
javascript:(function(){var s=document.createElement('script');s.src='http://localhost:9100/bridge.js?t='+Date.now();document.head.appendChild(s)})()
```

> 注意：URL 必须以 `javascript:` 开头，且要保存为**书签的「网址」字段**，不是放在注释或描述里。
> 一些 Jekyll / Markdown 渲染器会把 `javascript:` 自动转成 `<a href>`，拷贝时留意：**整段当一行**贴进去，不要拆行。

说明：

- `javascript:` 前缀让浏览器执行这段代码，而不是打开网址。
- `s.src = ...`：从本机下载真正的桥接脚本。
- `?t=Date.now()`：防缓存，每次点书签都拉最新 JS。

### 3.3 注入

1. 用浏览器打开**目标站点**并**登录成功**。
2. 点击刚才的书签。
3. 页面右下角若出现状态 UI，或控制台出现 `Bridge connected`，即注入成功。
4. 再查状态：

```bash
curl -sf http://localhost:9100/api/status
# 期望: {"ok":true,"browser":true}
```

### 3.4 发命令

```bash
# 探活
curl -sf http://localhost:9100/api/ping

# 业务命令（按你实现的 REST 定制）
curl -sf "http://localhost:9100/api/do?action=example"
curl -s -X POST http://localhost:9100/api/do \
  -H 'Content-Type: application/json' \
  -d '{"command":"example","params":{"foo":"bar"}}'
```

断线 / 换标签 / 登出后：`browser` 变 `false`，需重新打开目标页并点书签。

---

## 4. 通信协议（约定）

### 4.1 服务 → 浏览器（命令）

```json
{ "id": 1, "command": "ping", "params": {} }
```

| 字段 | 含义 |
|------|------|
| `id` | 请求序号，用于配对结果 |
| `command` | 命令名（白名单，脚本里 `switch`） |
| `params` | 参数对象 |

### 4.2 浏览器 → 服务（结果）

成功：

```json
{ "id": 1, "type": "result", "status": "ok", "result": { "pong": true } }
```

失败：

```json
{ "id": 1, "type": "result", "status": "error", "error": "原因说明" }
```

### 4.3 建议内置命令

| command | 用途 |
|---------|------|
| `ping` | 探活；可返回 `portal: location.origin` |
| 业务命令 | 只实现你需要的，**不要**做成任意 JS 执行 |

安全原则：**命令白名单**。不要接收 eval / 任意 URL 请求。

---

## 5. 最小可跑模板

### 5.1 `server.js`（本地服务）

```javascript
const http = require('http');
const fs = require('fs');
const path = require('path');
const WebSocket = require('ws');

const REST_PORT = 9100;
const WS_PORT = 9101;

let browserWs = null;
let cmdId = 0;
const pending = new Map();

const wss = new WebSocket.Server({ port: WS_PORT });
wss.on('connection', (ws) => {
  browserWs = ws;
  console.log('browser connected');
  ws.on('message', (raw) => {
    try {
      const msg = JSON.parse(raw.toString());
      if (msg.type === 'result' && pending.has(msg.id)) {
        const { resolve, reject, timer } = pending.get(msg.id);
        clearTimeout(timer);
        pending.delete(msg.id);
        msg.status === 'error'
          ? reject(new Error(msg.error || 'unknown'))
          : resolve(msg.result);
      }
    } catch {}
  });
  ws.on('close', () => {
    if (ws === browserWs) browserWs = null;
  });
});

function sendCommand(command, params = {}, timeout = 60000) {
  return new Promise((resolve, reject) => {
    if (!browserWs || browserWs.readyState !== WebSocket.OPEN) {
      return reject(new Error('NO_BROWSER: 请打开目标页并点击书签'));
    }
    const id = ++cmdId;
    const timer = setTimeout(() => {
      pending.delete(id);
      reject(new Error('TIMEOUT'));
    }, timeout);
    pending.set(id, { resolve, reject, timer });
    browserWs.send(JSON.stringify({ id, command, params }));
  });
}

function json(res, data, status = 200) {
  res.writeHead(status, {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
  });
  res.end(JSON.stringify(data));
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${REST_PORT}`);
  const p = url.pathname;

  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    });
    return res.end();
  }

  try {
    if (p === '/api/status') {
      return json(res, { ok: true, browser: browserWs !== null });
    }
    if (p === '/api/ping') {
      return json(res, await sendCommand('ping', {}));
    }
    // 在此按业务加 REST → sendCommand(...)
  } catch (e) {
    return json(
      res,
      { error: e.message },
      e.message.startsWith('NO_BROWSER') ? 503 : 500
    );
  }

  // 静态提供 bridge.js
  const file = path.join(__dirname, p === '/' ? 'bridge.js' : p.split('?')[0]);
  try {
    const data = fs.readFileSync(file);
    res.writeHead(200, {
      'Content-Type': 'application/javascript',
      'Access-Control-Allow-Origin': '*',
    });
    res.end(data);
  } catch {
    res.writeHead(404);
    res.end('Not found');
  }
});

server.listen(REST_PORT, () => {
  console.log(`REST  http://localhost:${REST_PORT}`);
  console.log(`WS    ws://localhost:${WS_PORT}`);
});
```

### 5.2 `bridge.js`（注入到目标页）

```javascript
;(function () {
  'use strict';
  if (window.__genericBridgeReady) return;
  window.__genericBridgeReady = true;

  const BASE = location.origin; // 目标站同源
  const WS_URL = 'ws://localhost:9101';

  async function api(path, opts = {}) {
    const res = await fetch(BASE + path, {
      credentials: 'include', // 带上当前登录 cookie
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
        ...(opts.headers || {}),
      },
      ...opts,
    });
    if (res.status === 401 || res.status === 403) {
      throw new Error('认证失败，请重新登录目标站');
    }
    if (!res.ok) {
      const text = await res.text().catch(() => '');
      throw new Error(`HTTP ${res.status}: ${text.slice(0, 200)}`);
    }
    const text = await res.text().catch(() => '');
    if (!text) return {};
    try {
      return JSON.parse(text);
    } catch {
      return { raw: text };
    }
  }

  function connect() {
    const ws = new WebSocket(WS_URL);
    ws.onopen = () => console.log('[bridge] connected');
    ws.onclose = () => setTimeout(connect, 3000); // 断线重连
    ws.onmessage = async (e) => {
      try {
        const { id, command, params } = JSON.parse(e.data);
        let result;
        try {
          switch (command) {
            case 'ping':
              result = { pong: true, portal: location.origin };
              break;
            // case 'yourCommand':
            //   result = await api('/your/api/path', { method: 'GET' });
            //   break;
            default:
              throw new Error('Unknown command: ' + command);
          }
          ws.send(JSON.stringify({ id, type: 'result', status: 'ok', result }));
        } catch (err) {
          ws.send(
            JSON.stringify({
              id,
              type: 'result',
              status: 'error',
              error: err.message,
            })
          );
        }
      } catch {}
    };
  }

  connect();
})();
```

### 5.3 `package.json`

```json
{
  "name": "browser-ws-bridge",
  "private": true,
  "dependencies": {
    "ws": "^8.18.0"
  }
}
```

---

## 6. 关键概念速查

| 名词 | 含义 |
|------|------|
| 书签 / Bookmarklet | 地址以 `javascript:` 开头的书签，点击即在当前页执行 JS |
| `script.src` | 告诉浏览器「从这个 URL 下载并执行脚本」 |
| WebSocket | 浏览器与本机服务之间的长连接，两边可随时推消息 |
| `fetch` | 浏览器发 HTTP 请求的 API |
| `credentials: 'include'` | 发请求时带上该域名下的 cookie（沿用登录态） |
| 同源 | 协议 + 域名 + 端口与当前页一致；桥接脚本应只打当前站 API |

---

## 7. 能力边界（做不到什么）

- 只能执行 `bridge.js` 白名单命令，**不是任意控制浏览器**。
- 没有注入 / 未登录 → `NO_BROWSER` 或 401。
- 账号没权限的操作，桥接也过不去。
- 默认**不能**跨站操作；换域名要另开标签并再点书签（或另写桥）。
- 本机 REST 未鉴权时，**本机其他进程也能调**；勿在不可信环境裸奔生产写操作。

---

## 8. 排障

| 现象 | 排查 |
|------|------|
| `browser: false` | 目标页是否打开、是否点过书签、WS 端口是否通 |
| `NO_BROWSER` | 同上；确认只保留一个有效连接 |
| 401 / 403 | 目标站登录过期，重新登录后再点书签 |
| 书签点了没反应 | 地址是否以 `javascript:` 开头；部分浏览器需允许书签脚本 |
| `bridge.js` 加载失败 | 本机服务是否在跑；页面是否拦截混合内容（目标站若是 https，localhost http 脚本可能被拦，需同源策略或本地 https） |
| TIMEOUT | 命令执行过久或 bridge 卡死；看控制台报错 |

**混合内容提示**：若目标站是 `https://`，从页面加载 `http://localhost/...` 可能被浏览器拦截。常见做法：

- 开发机用本地自签 HTTPS 提供 `bridge.js`；或
- 仅在允许的测试环境使用；或
- 用浏览器扩展注入（超出本文书签方案）。

---

## 9. 落地检查清单

- [ ] 选定 REST / WS 端口，避免与已有工具冲突
- [ ] `server.js` 提供 `/api/status`、`/api/ping`、静态 `bridge.js`
- [ ] `bridge.js` 只实现白名单 `command` + `credentials: 'include'`
- [ ] 书签 URL 指向本机 `bridge.js`
- [ ] 先登录目标站，再点书签，确认 `browser: true`
- [ ] 用 curl 验证 ping → 再接业务命令
- [ ] 写操作务必二次确认（尤其生产环境）

---

## 10. 和「导出 Cookie」方案对比

| | 书签 + WebSocket | 导出 Cookie 文件 |
|--|------------------|------------------|
| 登录态 | 跟浏览器会话走 | 需定期刷新文件 |
| 安全 | cookie 不出浏览器 | cookie 落盘，易泄露 |
| 依赖 | 必须开着目标页 | 可无头脚本直打 API |
| 适合 | SSO / 复杂登录 / 短期自动化 | 长期 CI、无 UI 环境 |

本模式的取舍：**用「必须开浏览器」换「不存 cookie、跟登录态自动同步」**。
