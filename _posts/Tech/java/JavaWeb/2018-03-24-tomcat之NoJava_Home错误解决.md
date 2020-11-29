---
layout: post
category: JavaWeb
title: tomcat之没有Java_Home错误解决
tags: JavaWeb
---

## 运行方式
在tomcat的bin目录下右键cmder，运行./startup.bat，这样子就可以查看运行信息了而不是自动关闭

## 错误
Neither the JAVA_HOME nor the JRE_HOME environment variable is defined At least one of these environment variable is needed to run this program

## 解决
先看Tomcat的startup.bat，它调用了catalina.bat,而catalina.bat则调用了setclasspath.bat。

在catalina.bat中增加两行
```shell
rem mfl
set JAVA_HOME=C:\Program Files\Java\jdk1.8.0_161
set JRE_HOME=C:\Program Files\Java\jre1.8.0_161
```

## 修改后
catalina.bat
```shell
rem ----- Execute The Requested Command ---------------------------------------

echo Using CATALINA_BASE:   "%CATALINA_BASE%"
echo Using CATALINA_HOME:   "%CATALINA_HOME%"
echo Using CATALINA_TMPDIR: "%CATALINA_TMPDIR%"
if ""%1"" == ""debug"" goto use_jdk
echo Using JRE_HOME:        "%JRE_HOME%"
goto java_dir_displayed

rem mfl
set JAVA_HOME=C:\Program Files\Java\jdk1.8.0_161
set JRE_HOME=C:\Program Files\Java\jre1.8.0_161

:use_jdk
echo Using JAVA_HOME:       "%JAVA_HOME%"
:java_dir_displayed
echo Using CLASSPATH:       "%CLASSPATH%"
```