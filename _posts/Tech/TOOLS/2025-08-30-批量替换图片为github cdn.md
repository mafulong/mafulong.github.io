---
layout: post
category: Tools
title: 批量替换图片为 GitHub CDN
tags: [Tools, PicGo, Markdown, Python]
---

## 背景

写博客笔记时，经常会插入大量本地图片或者引用外链。  
但随着时间推移，本地路径容易失效，外链也可能过期，影响文章的可读性。  

一个可行的解决方案是：  
把图片统一上传到 **GitHub 仓库**，然后通过 **jsDelivr CDN** 加速，既免费又稳定。  

这里记录一个方法，使用 **PicGo Server + Python 脚本**，自动批量替换 Markdown 文档里的图片链接。

---

## PicGo Server 配置

1. 安装 PicGo（推荐 Mac/Windows 用 GUI 版本）。  
2. 在 PicGo 设置里配置好图床（比如 GitHub 仓库）。  
3. 启动 PicGo Server：  

   ```bash
   picgo server
   ```

默认监听 `http://127.0.0.1:36677/upload`。

测试上传是否正常：

```
curl -X POST http://127.0.0.1:36677/upload \
  -H "Content-Type: application/json" \
  -d '{"list":["/Users/yourname/Desktop/test.png"]}'
```

如果返回 JSON，带有一个 `https://cdn.jsdelivr.net/...` 链接，就说明配置成功。

------

## Python 脚本

核心功能：

- 递归扫描指定目录下所有 Markdown 文件
- 提取其中的图片链接
- 对不是 jsDelivr 开头的图片，调用 PicGo Server 上传
- 替换 Markdown 文件里的链接，并备份原文件

脚本代码（简化版）：

```
#!/usr/bin/env python3
import os, re, shutil, requests, tempfile
from pathlib import Path

ROOT_DIR = Path("/Users/mafulong/mafulong.github.io/_posts").resolve()
PICGO_SERVER = "http://127.0.0.1:36677/upload"
JSDELIVR_PREFIX = "https://cdn.jsdelivr.net/"

def is_jsdelivr(url: str) -> bool:
    return url.startswith(JSDELIVR_PREFIX)

def run_picgo_upload(local_path: Path) -> str:
    payload = {"list": [str(local_path)]}
    resp = requests.post(PICGO_SERVER, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data["result"][0]

def handle_image(url: str, base_dir: Path) -> str:
    if is_jsdelivr(url):
        return url
    local_path = (base_dir / url).resolve()
    if local_path.exists():
        return run_picgo_upload(local_path)
    return url

def process_file(path: Path):
    text = path.read_text(encoding="utf-8")
    matches = re.finditer(r"!\[[^]]*]\(([^)]+)\)", text)
    new_text = text
    for m in matches:
        old_url = m.group(1)
        new_url = handle_image(old_url, path.parent)
        if new_url != old_url:
            new_text = new_text.replace(old_url, new_url)
    if new_text != text:
        # shutil.copy2(path, path.with_suffix(path.suffix + ".bak"))
        path.write_text(new_text, encoding="utf-8")
        print(f"[OK] {path} 已替换图片链接")

for md in ROOT_DIR.rglob("*.md"):
    process_file(md)
```

------

## 使用步骤

1. 修改脚本里的 `ROOT_DIR` 为你的博客目录

2. 启动 `picgo server`

3. 运行脚本：

   ```
   python3 md_cdn_picgo.py
   ```

4. 所有 Markdown 文件里的图片链接会自动替换为 jsDelivr 地址

## 总结

这样就能把 Markdown 博客里的图片统一迁移到 **GitHub + jsDelivr**，实现免费图床、自动加速和批量替换，非常适合 Jekyll / Hexo 博客用户。