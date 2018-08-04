---
layout: post
category: springMVC
title: springMVC @Controller注解定义一个控制器
---

[详情可以参考helloworld](https://mafulong.top/springmvc/2018/08/03/springMVC-helloworld.html)

## @Controller

你需要在配置中加入组件扫描的配置代码来开启框架对注解控制器的自动检测。请使用下面XML代码所示的spring-context schema：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:p="http://www.springframework.org/schema/p"
    xmlns:context="http://www.springframework.org/schema/context"
    xsi:schemaLocation="
        http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/context
        http://www.springframework.org/schema/context/spring-context.xsd">

    <context:component-scan base-package="org.springframework.samples.petclinic.web"/>

    <!-- ... -->

</beans>
```

```java
@Controller
public class HelloWorldController {

    @RequestMapping("/helloWorld")
    public String helloWorld(Model model) {
        model.addAttribute("message", "Hello World!");
        return "helloWorld";
    }
    
    @RequestMapping(path = "/new", method = RequestMethod.GET)
    public AppointmentForm getNewForm() {
        return new AppointmentForm();
    }
}
```

```java
@Controller
@RequestMapping("/owners/{ownerId}")
public class RelativePathUriTemplateController {

    @RequestMapping(path = "/pets/{petId}", method = RequestMethod.GET, params="myParam=myValue")
    public void findPet(@PathVariable String ownerId, @PathVariable String petId, Model model) {
        // 实际实现省略
    }

}
```

## 请求参数与请求头的值
你可以筛选请求参数的条件来缩小请求匹配范围，比如"myParam"、"!myParam"及"myParam=myValue"等。前两个条件用于筛选存在/不存在某些请求参数的请求，第三个条件筛选具有特定参数值的请求。下面有个例子，展示了如何使用请求参数值的筛选条件：

```java
@Controller
@RequestMapping("/owners/{ownerId}")
public class RelativePathUriTemplateController {

    @RequestMapping(path = "/pets/{petId}", method = RequestMethod.GET, params="myParam=myValue")
    public void findPet(@PathVariable String ownerId, @PathVariable String petId, Model model) {
        // 实际实现省略
    }

}
```

同样，你可以用相同的条件来筛选请求头的出现与否，或者筛选出一个具有特定值的请求头：

```java
@Controller
@RequestMapping("/owners/{ownerId}")
public class RelativePathUriTemplateController {

    @RequestMapping(path = "/pets", method = RequestMethod.GET, headers="myHeader=myValue")
    public void findPet(@PathVariable String ownerId, @PathVariable String petId, Model model) {
        // 方法体实现省略
    }

}
```