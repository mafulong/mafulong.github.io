---
layout: post
category: Life
title: 小米路由器安装shellcrash
tags: Life
---

## 小米路由器安装shellcrash

路由器安装了shellcrash后就自带梯子了。然后就可以通过http://192.168.31.1:9999/ui/#/proxies 管理节点切换等。



- [shellcrash介绍](https://github.com/2375399351/ShellCrash/blob/master/README_CN.md)
- [小米路由器后台](http://192.168.31.1/cgi-bin/luci/web)
- [安装shellcrash参考](https://www.gaicas.com/redmi-ax6000.html)
- [参考2](https://beyondkmp.com/2023/03/05/ax6000-ssh/)





```scala
curl -o a.yaml "clash订阅链接"

```

然后crash本地导入。不能下载，会timeout.



你设备的 SSH 密码设置为**admin**，用户名为**root**，并永久开启 SSH；

```scala
ssh -oHostKeyAlgorithms=+ssh-rsa  root@192.168.31.1
```

