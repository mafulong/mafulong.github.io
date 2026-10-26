---
layout: post
category: Tools
title: 使用github+picGo+typora图床
tags: Tools
---

## 使用 github+picGo+typora 图床

[参考](https://blog.csdn.net/qq_36376089/article/details/107429913)

### token 生成

https://github.com/settings/tokens

第一个 repo 勾选。

### picgo 配置

仓库名: mafulong/mdPic

分支 v7,v8 递增，需要提前创建。

制定存储路径 v7/, 这样

自定义域名如下，不用包含目录，仅包含分支名即可。

```
https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6
```

开启『时间戳重命名』

不要开启：『上传前重命名』





pico也支持命令后上传

```scala
curl -X POST http://127.0.0.1:36677/upload \
  -H "Content-Type: application/json" \
  -d "{\"list\":[\"$HOME/Desktop/wechat_2025-08-30_152700_320.png\"]}"


返回新的图片地址。
```



## Typora 免费版本下载

### Windows 用户

下载地址： https://github.com/iuxt/src/releases/download/2.0/typora-0-11-18.exe

### Mac 用户

下载地址： https://github.com/iuxt/src/releases/download/2.0/typora-0-11-18.dmg

### Ubuntu 用户

下载地址：https://github.com/iuxt/src/releases/download/2.0/Typora_Linux_0.11.18_amd64.deb

[参考](https://zahui.fan/posts/64b52e0d/)
