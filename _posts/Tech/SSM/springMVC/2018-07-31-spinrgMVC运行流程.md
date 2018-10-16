---
layout: post
category: SSM
tags: Spring MVC
title: spinrgMVC运行流程
---

## 详细运行流程图
![](https://i.imgur.com/fb03ryP.png)

## 运行原理

1. 客户端请求提交到DispatcherServlet
2. 由DispatcherServlet控制器查询一个或多个HandlerMapping，找到处理请求的Controller
3. DispatcherServlet将请求提交到Controller
4. Controller调用业务逻辑处理后，返回ModelAndView
5. DispatcherServlet查询一个或多个ViewResoler视图解析器，找到ModelAndView指定的视图
6. 视图负责将结果显示到客户端