---
layout: post
category: SpringMVC
tags: SpringMVC
title: Spring MVC 静态资源访问
---

我们怎么让 servlet 来处理项目中的静态资源呢？这里有两种方法。

1. 另外使用一个 servlet 来处理静态资源。若我们的资源放置在 webapps 文件夹下的 resources 文件夹中，那么我们可以用名字为 default 的 servlet 来处理静态资源。因此我们还需要在上述配置的基础上加上以下配置：

```xml
<servlet-mapping>
<servlet-name>default</servlet-name>
<url-pattern>resources/*</url-pattern>
</servlet-mapping>
```

这表示 default 的 servlet 会处理 url 中为 resources/\*的对应的请求。这样，当你把你的 image，css 已经其他文件放在 resources 文件中时，spring 就可以找到它啦。

2. 采用 spring 自带`<mvc:resources>`方法。首先找到你定义的那个 servlet 的 xml 文件，如本例子中，servlet 的名字叫 mvc-dispatcher，因此需要找到 mvc-dispatcher-servlet.xml 文件，并在该文件中插入以下配置：

```xml
<!-- 扩充了注解驱动，可以将请求参数绑定到控制器参数 -->
<mvc:annotation-driven/>
<mvc:resources mapping="/resources/**/" location="/resources/"/>
```

如此就不必另外添加一个 mvc 来处理静态资源。而 mvc 知道静态资源所处的位置为 resources 文件夹。
两种方法都可以将 spring mvc 配置处理静态资源。

在 SpringMVC3.0 之后推荐使用一

```xml
 <mvc:annotation-driven />
 <mvc:resources location="/img/" mapping="/img/**"/>
 <mvc:resources location="/js/" mapping="/js/**"/>
 <mvc:resources location="/css/" mapping="/css/**"/>
```

说明：

location 元素表示 webapp 目录下的 static 包下的所有文件；

mapping 元素表示以/static 开头的所有请求路径，如/static/a 或者/static/a/b；

该配置的作用是：DispatcherServlet 不会拦截以/static 开头的所有请求路径，并当作静态资源交由 Servlet 处理。

```java
    <!--静态资源映射-->
    <!--
    http://perfy315.iteye.com/blog/2008763
    mapping="/js/**"
    表示当浏览器有静态资源请求的时候，并且请求url路径中带有：/js/，则这个资源跑到webapp目录下的/WEB-INF/statics/js/去找
    比如我们在 JSP 中引入一个 js 文件：src="${webRoot}/js/jQuery-core/jquery-1.6.1.min.js
    -->
    <mvc:resources mapping="/css/**" location="/WEB-INF/statics/css/"/>
    <mvc:resources mapping="/js/**" location="/WEB-INF/statics/js/"/>
    <mvc:resources mapping="/images/**" location="/WEB-INF/statics/images/"/>
```
