---
layout: post
category: Mybatis
title: Mybatis之typeAliases
tags: Mybatis
---

- 自定义别名 
- 单个别名定义
- 批量定义别名（常用）

UserMapper.xml

```xml
<!-- 别名定义 -->
<typeAliases>

    <!-- 针对单个别名定义
    type：类型的路径
    alias：别名
     -->
    <!-- <typeAlias type="cn.itcast.mybatis.po.User" alias="user"/> -->
    <!-- 批量别名定义
    指定包名，mybatis自动扫描包中的po类，自动定义别名，别名就是类名（首字母大写或小写都可以）
    -->
    <package name="com.iot.mybatis.po"/>

</typeAliases>
```