---
layout: post
category: spring
title: Spring Bean 作用域
---

## Bean 的作用域

当在 Spring 中定义一个 bean 时，你必须声明该 bean 的作用域的选项。例如，为了强制 Spring 在每次需要时都产生一个新的 bean 实例，你应该声明 bean 的作用域的属性为 prototype。同理，如果你想让 Spring 在每次需要时都返回同一个bean实例，你应该声明 bean 的作用域的属性为 singleton。
Spring 框架支持以下五个作用域，如果你使用 web-aware ApplicationContext 时，其中三个是可用的。

1. singleton    在spring IoC容器仅存在一个Bean实例，Bean以单例方式存在，默认值
2. prototype 每次从容器中调用Bean时，都返回一个新的实例，即每次调用getBean()时，相当于执行newXxxBean()
3. request  每次HTTP请求都会创建一个新的Bean，该作用域仅适用于WebApplicationContext环境
4. session  同一个HTTP Session共享一个Bean，不同Session使用不同的Bean，仅适用于WebApplicationContext环境
5. global-session   一般用于Portlet应用环境，改作用于仅适用于WebApplicationContext环境

```xml
<bean id="..." class="..." scope="singleton">
    <!-- collaborators and configuration for this bean go here -->
</bean>
```

