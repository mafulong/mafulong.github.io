---
layout: post
category: JavaLib
tags: JavaLib
title: spring使用bean入门xml配置
---

idea新建spring项目

## 目录结构


## 代码
HelloWorld.java
```java
package com.mfl.spring.model;

public class HelloWorld {
    private String message;

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    @Override
    public String toString() {
        return "HelloWorld{" +
                "message='" + message + '\'' +
                '}';
    }
}

```

App
```java
package com.mfl.spring;

import com.mfl.spring.model.HelloWorld;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class App {
    public static void main(String[] args){

        ApplicationContext context =
                new ClassPathXmlApplicationContext("Beans.xml");
        HelloWorld obj = (HelloWorld) context.getBean("helloWorld");
        obj.getMessage();
        System.out.println(obj.getMessage());

    }
}

```

Beans.xml，是根目录src下的
```xml
<?xml version="1.0" encoding="UTF-8"?>

<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
    http://www.springframework.org/schema/beans/spring-beans-3.0.xsd">

    <bean id="helloWorld" class="com.mfl.spring.model.HelloWorld">
        <property name="message" value="Hello World!"/>
    </bean>

</beans>
```
