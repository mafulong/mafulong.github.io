---
layout: post
category: struts2
title: Struts2 Actions动作
---

## Struts2 Actions动作

Actions是Struts2框架的核心，因为它们适用于任何MVC（Model View Controller）框架。 每个URL映射到特定的action，其提供处理来自用户的请求所需的处理逻辑。

但action还有另外两个重要的功能。 首先，action在将数据从请求传递到视图（无论是JSP还是其他类型的结果）方面起着重要作用。 第二，action必须协助框架确定哪个结果应该呈现在响应请求的视图中。

#### 创建Action
Struts2中actions的唯一要求是必须有一个无参数方法返回String或Result对象，并且必须是POJO。如果没有指定no-argument方法，则默认是使用execute()方法。

你还可以扩展ActionSupport类，该类可实现六个接口，包括Action接口。Action的接口如下：
```java
public interface Action {
   public static final String SUCCESS = "success";
   public static final String NONE = "none";
   public static final String ERROR = "error";
   public static final String INPUT = "input";
   public static final String LOGIN = "login";
   public String execute() throws Exception;
}
```

```java
package cn.w3cschool.struts2;

import com.opensymphony.xwork2.ActionSupport;

public class HelloWorldAction extends ActionSupport{
   private String name;

   public String execute() throws Exception {
      if ("SECRET".equals(name))
      {
         return SUCCESS;
      }else{
         return ERROR;  
      }
   }
   
   public String getName() {
      return name;
   }

   public void setName(String name) {
      this.name = name;
   }
}
```

在这个例子中，我们在execute方法中使用一些逻辑来查看name属性。如果属性等于字符串“SECRET”，我们返回SUCCESS作为结果，否则我们返回ERROR作为结果。因为我们已经扩展了ActionSupport，所以我们可以使用String常量、SUCCESS和ERROR。 现在，让我们修改struts.xml文件如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE struts PUBLIC
   "-//Apache Software Foundation//DTD Struts Configuration 2.0//EN"
   "http://struts.apache.org/dtds/struts-2.0.dtd">
   <struts>
      <constant name="struts.devMode" value="true" />
      <package name="helloworld" extends="struts-default">
         <action name="hello" 
            class="cn.w3cschool.struts2.HelloWorldAction"
            method="execute">
            <result name="success">/HelloWorld.jsp</result>
            <result name="error">/AccessDenied.jsp</result>
         </action>
      </package>
</struts>
```

上面这个action name是和form中的action对应的。就像这样
```html
 <form action="hello">
      <label for="name">Please enter your name</label><br/>
      <input type="text" name="name"/>
      <input type="submit" value="Say Hello"/>
   </form>
```

建议您创建一个包含结果的类。 就是包含哪些结果字符串


