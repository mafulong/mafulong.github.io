---
layout: post
category: Mybatis
title: Mybatis之db.properties文件
tags: Mybatis
---

## Mybatis之db.properties文件
db.properties
```java
jdbc.driver=com.mysql.jdbc.Driver
jdbc.url=jdbc:mysql://localhost:3306/mybatis
jdbc.username=root
jdbc.password=123456
```

## 配置引用
在mybatis-config.xml中配置
```xml
    <properties resource="db.properties">
        <!--properties中还可以配置一些属性名和属性值  -->
        <!-- <property name="jdbc.driver" value=""/> -->
    </properties>
```

```xml
    <property name="driver" value="${jdbc.driver}" />
    <property name="url" value="${jdbc.url}" />
    <property name="username" value="${jdbc.username}" />
    <property name="password" value="${jdbc.password}" />
```

完整的xml
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <properties resource="db.properties">
        <!--properties中还可以配置一些属性名和属性值  -->
        <!-- <property name="jdbc.driver" value=""/> -->
    </properties>

    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="${jdbc.driver}" />
                <property name="url" value="${jdbc.url}" />
                <property name="username" value="${jdbc.username}" />
                <property name="password" value="${jdbc.password}" />
                <!--<property name="driver" value="com.mysql.jdbc.Driver"/>-->
                <!--<property name="url" value="jdbc:mysql://localhost:3306/mybatis"/>-->
                <!--<property name="username" value="root"/>-->
                <!--<property name="password" value="123456"/>-->
            </dataSource>
        </environment>
    </environments>
    <mappers>
        <mapper resource="UserMapper.xml"/>
        <mapper resource="UserMapper2.xml"/>
    </mappers>
</configuration>
```