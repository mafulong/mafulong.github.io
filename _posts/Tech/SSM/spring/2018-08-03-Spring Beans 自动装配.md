---
layout: post
category: Spring 
tags: Spring
title: Spring Beans 自动装配xml
---

## Beans 自动装配

你已经学会如何使用<bean>元素来声明 bean 和通过使用 XML 配置文件中的<constructor-arg>和<property>元素来注入 。
Spring 容器可以在不使用<constructor-arg>和<property> 元素的情况下自动装配相互协作的 bean 之间的关系，这有助于减少编写一个大的基于 Spring 的应用程序的 XML 配置的数量。

```xml
   <bean id="textEditor" class="com.tutorialspoint.TextEditor" 
      autowire="byName">
      <property name="name" value="Generic Text Editor" />
   </bean>

   <!-- Definition for spellChecker bean -->
   <bean id="spellChecker" class="com.tutorialspoint.SpellChecker">
   </bean>
```

```xml
   <bean id="textEditor" class="com.tutorialspoint.TextEditor" 
      autowire="byType">
      <property name="name" value="Generic Text Editor" />
   </bean>

   <!-- Definition for spellChecker bean -->
   <bean id="SpellChecker" class="com.tutorialspoint.SpellChecker">
   </bean>
```

Spring 由构造函数自动装配

这种模式与 byType 非常相似，但它应用于构造器参数。

```xml
   <bean id="textEditor" class="com.tutorialspoint.TextEditor" 
      autowire="constructor">
      <constructor-arg value="Generic Text Editor"/>
   </bean>

   <!-- Definition for spellChecker bean -->
   <bean id="SpellChecker" class="com.tutorialspoint.SpellChecker">
   </bean>
```