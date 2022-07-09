---
layout: post
category: SpringMVC
tags: SpringMVC
title: spinrgMVC运行流程
---

## 详细运行流程图

## 运行原理

1. 客户端请求提交到 DispatcherServlet
2. 由 DispatcherServlet 控制器查询一个或多个 HandlerMapping，找到处理请求的 Controller
3. DispatcherServlet 将请求提交到 Controller
4. Controller 调用业务逻辑处理后，返回 ModelAndView
5. DispatcherServlet 查询一个或多个 ViewResoler 视图解析器，找到 ModelAndView 指定的视图
6. 视图负责将结果显示到客户端
