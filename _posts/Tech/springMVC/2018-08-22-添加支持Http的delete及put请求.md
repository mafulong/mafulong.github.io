---
layout: post
category: springMVC
title: 添加支持Http的delete、put请求
---

浏览器form表单只支持GET与POST请求，而DELETE、PUT等method并不支持，spring3.0添加了一个过滤器，可以将这些请求转换为标准的http方法，使得支持GET、POST、PUT与DELETE请求。

1.配置springmvc配置文件springmvc-servlet.xml

```xml
    <!--　浏览器不支持put,delete等method,由该filter将/blog?_method=delete转换为标准的http　delete方法　-->
    <filter>
        <filter-name>HiddenHttpMethodFilter</filter-name>
        <filter-class>org.springframework.web.filter.HiddenHttpMethodFilter</filter-class>
    </filter>
    <filter-mapping>
        <filter-name>HiddenHttpMethodFilter</filter-name>
        <servlet-name>SpringMVC</servlet-name>
    </filter-mapping>
```

2.在对应的Controller中，添加对应的请求注解

```java
/** 进入新增 */
@RequestMapping(value="/new")

/** 显示 */
@RequestMapping(value="/{id}")

/** 编辑 */
@RequestMapping(value="/{id}/edit")

/** 保存新增 */
@RequestMapping(method=RequestMethod.POST)

/** 保存更新 */
@RequestMapping(value="/{id}",method=RequestMethod.PUT)

/** 删除 */
@RequestMapping(value="/{id}",method=RequestMethod.DELETE)

/** 批量删除 */
@RequestMapping(method=RequestMethod.DELETE)

```
进入新增页面时没有用add而是用new，是因为某些浏览器会将add当做广告拦截掉。


3.页面请求

```html
<form:form action="/xxx/xxx" method="put">

</form:form>
```

生成的页面代码会添加一个hidden的_method=put,并于web.xml中的HiddenHttpMethodFilter配合使用，在服务端将post请求改为put请求

```html
<form id="userInfo" action="/xxx/xxx" method="post">

<input type="hidden" name="_method" value="put"/>

</form>
``
另外也可以用ajax发送delete、put请求