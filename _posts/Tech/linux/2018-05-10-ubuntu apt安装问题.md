---
layout: post
category: Linux
title: ubuntu apt安装问题
tags: Linux
---

[参考])(https://www.zhujiceping.com/28021.html)

解决问题：E: Could not get lock /var/lib/dpkg/lock – open (11: Resource temporarily unavailable)

解决方法

```
sudo rm /var/lib/apt/lists/lock
```