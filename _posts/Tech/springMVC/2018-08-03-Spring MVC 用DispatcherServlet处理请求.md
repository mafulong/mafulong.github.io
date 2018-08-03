---
layout: post
category: springMVC
title: Spring MVC 用DispatcherServlet处理请求
---

pring MVC框架，与其他很多web的MVC框架一样：请求驱动；所有设计都围绕着一个中央Servlet来展开，它负责把所有请求分发到控制器；同时提供其他web应用开发所需要的功能。不过Spring的中央处理器，DispatcherServlet，能做的比这更多。它与Spring IoC容器做到了无缝集成，这意味着，Spring提供的任何特性，在Spring MVC中你都可以使用。

![](https://i.imgur.com/aoh43Xp.jpg)


DispatcherServlet其实就是个Servlet（它继承自HttpServlet基类），同样也需要在你web应用的web.xml配置文件下声明。你需要在web.xml文件中把你希望DispatcherServlet处理的请求映射到对应的URL上去。这就是标准的Java EE Servlet配置；下面的代码就展示了对DispatcherServlet和路径映射的声明：

```java
<web-app>
    <servlet>
        <servlet-name>example</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <load-on-startup>1</load-on-startup>
    </servlet>

    <servlet-mapping>
        <servlet-name>example</servlet-name>
        <url-pattern>/example/*</url-pattern>
    </servlet-mapping>
</web-app>
```

你可以定制DispatcherServlet的配置

contextConfigLocation. 	一个指定了上下文配置文件路径的字符串，该值会被传入给contextClass所指定的上下文实例对象。该字符串内可以包含多个字符串，字符串之间以逗号分隔，以此支持你进行多个上下文的配置。在多个上下文中重复定义的bean，以最后加载的bean定义为准

namespace	WebApplicationContext的命名空间。默认是[servlet-name]-servlet

```xml
<web-app>
    <context-param>
        <param-name>contextConfigLocation</param-name>
        <param-value>/WEB-INF/root-context.xml</param-value>
    </context-param>
    <servlet>
        <servlet-name>dispatcher</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value></param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>
    <servlet-mapping>
        <servlet-name>dispatcher</servlet-name>
        <url-pattern>/*</url-pattern>
    </servlet-mapping>
    <listener>
        <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
    </listener>
</web-app>
```

在MVC XML命名空间下，则使用<mvc:interceptors>元素：

```xml
<mvc:interceptors>
    <bean class="org.springframework.web.servlet.i18n.LocaleChangeInterceptor"/>
    <mvc:interceptor>
        <mvc:mapping path="/**"/>
        <mvc:exclude-mapping path="/admin/**"/>
        <bean class="org.springframework.web.servlet.theme.ThemeChangeInterceptor"/>
    </mvc:interceptor>
    <mvc:interceptor>
        <mvc:mapping path="/secure/*"/>
        <bean class="org.example.SecurityInterceptor"/>
    </mvc:interceptor>
</mvc:interceptors>
```

```xml
    <mvc:interceptors>
        <!-- 登陆拦截器,负责拦截未登录的操作 -->
        <mvc:interceptor>
            <!-- 需要拦截的地址 -->
            <mvc:mapping path="/**"/>
            <!-- 需要排除拦截的地址 -->
            <mvc:exclude-mapping path="/static/**"/>
            <bean id="loginInterceptor" class="com.amayadream.webchat.interceptor.LoginInterceptor">
                <property name="IGNORE_URI">
                    <list>
                        <value>/user/login</value>
                        <value>/user/logout</value>
                    </list>
                </property>
            </bean>
        </mvc:interceptor>
    </mvc:interceptors>
```