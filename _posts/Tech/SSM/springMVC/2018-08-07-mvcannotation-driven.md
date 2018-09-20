---
layout: post
category: SSM
title: mvc:annotation-driven
---

特别是下面那段英文很重要，我就曾经遇到过加入了jackson的core和mapper包之后竟然不写配置文件也能自动转换成json，我当时很费解。原来是

<mvc:annotation-driven />这个东西在起作用。

<mvc:annotation-driven /> 是一种简写形式，完全可以手动配置替代这种简写形式，简写形式可以让初学都快速应用默认配置方案。
<mvc:annotation-driven /> 会自动注册DefaultAnnotationHandlerMapping与AnnotationMethodHandlerAdapter 两个bean,是spring MVC为@Controllers分发请求所必须的。

并提供了：数据绑定支持，@NumberFormatannotation支持，@DateTimeFormat支持，@Valid支持，读写XML的支持（JAXB），读写JSON的支持（Jackson）。

后面，我们处理响应ajax请求时，就使用到了对json的支持。

后面，对action写JUnit单元测试时，要从spring IOC容器中取DefaultAnnotationHandlerMapping与AnnotationMethodHandlerAdapter 两个bean，来完成测试，取的时候要知道是<mvc:annotation-driven />这一句注册的这两个bean。

<context:annotation-config> declares support for general annotations such as @Required, @Autowired, @PostConstruct, and so on.

<mvc:annotation-driven /> is actually rather pointless. It declares explicit support for annotation-driven MVC controllers (i.e.@RequestMapping, @Controller, etc), even though support for those is the default behaviour.

My advice is to always declare <context:annotation-config>, but don't bother with <mvc:annotation-driven /> unless you want JSON support via Jackson.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns:context="http://www.springframework.org/schema/context"
	xmlns:mvc="http://www.springframework.org/schema/mvc" 
	xsi:schemaLocation="http://www.springframework.org/schema/beans
	http://www.springframework.org/schema/beans/spring-beans.xsd
	http://www.springframework.org/schema/context
	http://www.springframework.org/schema/context/spring-context.xsd
	http://www.springframework.org/schema/mvc
	http://www.springframework.org/schema/mvc/spring-mvc-3.0.xsd">
	<!-- 配置SpringMVC -->
	<!-- 1.开启SpringMVC注解模式 -->
	<!-- 简化配置： 
		(1)自动注册DefaultAnootationHandlerMapping,AnotationMethodHandlerAdapter 
		(2)提供一些列：数据绑定，数字和日期的format @NumberFormat, @DateTimeFormat, xml,json默认读写支持 
	-->
	<mvc:annotation-driven />
	
	<!-- 2.静态资源默认servlet配置
		(1)加入对静态资源的处理：js,gif,png
		(2)允许使用"/"做整体映射
	 -->
	 <mvc:default-servlet-handler/>
	 
	 <!-- 3.配置jsp 显示ViewResolver -->
	 <bean class="org.springframework.web.servlet.view.InternalResourceViewResolver">
	 	<property name="viewClass" value="org.springframework.web.servlet.view.JstlView" />
	 	<property name="prefix" value="/WEB-INF/jsp/" />
	 	<property name="suffix" value=".jsp" />
	 </bean>
	 
	 <!-- 4.扫描web相关的bean -->
	 <context:component-scan base-package="com.soecode.lyf.web" />
</beans>
```