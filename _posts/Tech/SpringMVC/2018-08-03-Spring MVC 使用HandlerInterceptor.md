---
layout: post
category: SpringMVC
tags: SpringMVC
title: Spring MVC 使用HandlerInterceptor
---

处理器映射处理过程配置的拦截器，必须实现 org.springframework.web.servlet 包下的 HandlerInterceptor 接口。这个接口定义了三个方法： preHandle(..)，它在处理器实际执行 之前 会被执行； postHandle(..)，它在处理器执行 完毕 以后被执行； afterCompletion(..)，它在 整个请求处理完成 之后被执行。这三个方法为各种类型的前处理和后处理需求提供了足够的灵活性。

preHandle(..)方法返回一个 boolean 值。你可以通过这个方法来决定是否继续执行处理链中的部件。当方法返回 true 时，处理器链会继续执行；若方法返回 false， DispatcherServlet 即认为拦截器自身已经完成了对请求的处理（比如说，已经渲染了一个合适的视图），那么其余的拦截器以及执行链中的其他处理器就不会再被执行了。

拦截器可以通过 interceptors 属性来配置，该选项在所有继承了 AbstractHandlerMapping 的处理器映射类 HandlerMapping 都提供了配置的接口。如下面代码样例所示：

```xml
<beans>
    <bean id="handlerMapping" class="org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping">
        <property name="interceptors">
            <list>
                <ref bean="officeHoursInterceptor"/>
            </list>
        </property>
    </bean>

    <bean id="officeHoursInterceptor" class="samples.TimeBasedAccessInterceptor">
        <property name="openingTime" value="9"/>
        <property name="closingTime" value="18"/>
    </bean>
<beans>
```

```java
package samples;

public class TimeBasedAccessInterceptor extends HandlerInterceptorAdapter {

    private int openingTime;
    private int closingTime;

    public void setOpeningTime(int openingTime) {
        this.openingTime = openingTime;
    }

    public void setClosingTime(int closingTime) {
        this.closingTime = closingTime;
    }

    public boolean preHandle(HttpServletRequest request, HttpServletResponse response,
            Object handler) throws Exception {
        Calendar cal = Calendar.getInstance();
        int hour = cal.get(HOUR_OF_DAY);
        if (openingTime <= hour && hour < closingTime) {
            return true;
        }
        response.sendRedirect("http://host.com/outsideOfficeHours.html");
        return false;
    }
}
```

在上面的例子中，所有被此处理器处理的请求都会被 TimeBasedAccessInterceptor 拦截器拦截。如果当前时间在工作时间以外，那么用户就会被重定向到一个 HTML 文件提示用户，比如显示“你只有在工作时间才可以访问本网站”之类的信息。
