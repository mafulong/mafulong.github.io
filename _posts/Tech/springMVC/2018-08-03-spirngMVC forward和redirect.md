---
layout: post
category: springMVC
title: spirngMVC forward和redirect
---

## forward
请求转发，在服务器内部完成，客户端不参与，地址栏不改变

共享请求参数

而且只能转发到本应用的其他路径上。比如
```java
return "forward: /hello"
```

## redirect
重定向，客户端参与，地址栏变，可以重定向到任意url地址

不共享参数

```java
return "redirect: /hello"
```