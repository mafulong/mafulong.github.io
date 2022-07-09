---
layout: post
category: SpringMVC
tags: SpringMVC
title: springMVC helloworld
---

# springMVChelloworld

springMVChelloworld

## 注意点

一定要 war 部署

# 关键代码

## 在 web.xml 文件中配置 DispatcherServlet

本质上就是一个 servlet，将请求转发到{servelt-name}-servlet.xml，同文件下，就是 WEB-INF 目录下

- Spring mvc 需要一个配置文件：
- 位置：默认情况下在 WEB-INF 下
- 命名规则：servlet 的名称 + “-”+ servlet.xml

```xml
    <servlet>
        <servlet-name>dispatcher</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <load-on-startup>1</load-on-startup>
    </servlet>
    <servlet-mapping>
        <servlet-name>dispatcher</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>
```

## Controller 配置

```java
@Controller
public class testController1 {
    @RequestMapping("/hello")
    public String hello(){
        System.out.println("testController1");
        return "hello";
    }
}

```

## dispatcher-servlet.xml

注意：

1. base-package 是自己代码 Controller 配置的包
2. 这个 value="/jsp/"是根目录下的，其实就是字符串拼接，前缀/jsp/，后缀.jsp，返回的字符串是 hello，那就是访问/jsp/hello.jsp 了

```xml
    <!-- mvc的注解驱动 -->
    <mvc:annotation-driven/>
    <!-- 一旦有扫描器的定义mvc:annotation-driven不需要，扫描器已经有了注解驱动的功能 -->
    <context:component-scan base-package="com.mfl"/>


    <!-- 前缀+ viewName +后缀 -->
    <bean class="org.springframework.web.servlet.view.InternalResourceViewResolver">
        <!-- webroot到某一指定的文件夹的路径 -->
        <property name="prefix" value="/jsp/"></property>
        <!-- 视图名称的后缀 -->
        <property name="suffix" value=".jsp"></property>
    </bean>

```

## 关于 Controller 使用

1. @RequestMapping("/test") controller 的唯一标识或者命名空间,当加在类上时
2. 方法的返回值可以是 ModelAndView 中的 viewName
3. HttpServletRequest 可以直接定义在参数的列表，可以使用
4. 在参数列表上直接定义要接收的参数名称，只要参数名称能匹配的上就能接收所传过来的数据,可以自动转换成参数列表里面的类型，注意的是值与类型之间是可以转换的
5. 也可以传递对象，在参数列表上直接定义要接收的参数名称，只要参数名称能匹配的上就能接收所传过来的数据，可以自动转换成参数列表里面的类型，注意的是值与类型之间是可以转换的
6. 对数组的接收，比如传来的参数有 name=1&name2
7. 方法的返回值采用 ModelAndView， new ModelAndView("index", map);相当于把结果数据放到 request 里面,其实就是 new ModelAndView("index", map);
8. 在参数列表中直接定义 Model，model.addAttribute("p", person);把参数值放到 request 类里面去，建议使用
9. ajax 的请求返回值类型应该是 void,直接在参数的列表上定义 PrintWriter，out.write(result);把结果写到页面，建议使用的
10. controller 内部重定向，redirect:加上同一个 controller 中的 requestMapping 的值
11. controller 之间的重定向：必须要指定好 controller 的命名空间再指定 requestMapping 的值，redirect：后必须要加/,是从根目录开始
12. @RequestMapping( method=RequestMethod.POST )可以指定请求方式，前台页面就必须要以它制定好的方式来访问，否则出现 405 错误，即方法错误

对于时间传递，Date 做参数，需要进行自己转换，即注册时间类型的属性编辑器

```java

	@InitBinder
	public void initBinder(ServletRequestDataBinder binder){
		binder.registerCustomEditor(Date.class,
				new CustomDateEditor(new SimpleDateFormat("yyyy-MM-dd"), true));
	}
```
