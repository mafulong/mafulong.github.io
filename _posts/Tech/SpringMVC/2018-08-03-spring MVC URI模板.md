---
layout: post
category: SpringMVC
tags: SpringMVC
title: spring MVC URI模板
---

## Apache Ant 的样式路径

    ?    匹配任何单字符
    *    匹配0或者任意数量的字符
    **    匹配0或者更多的目录

## @PathVariable

在 Spring MVC 中你可以在方法参数上使用@PathVariable 注解，将其与 URI 模板中的参数绑定起来：

```java
@RequestMapping(path="/owners/{ownerId}}", method=RequestMethod.GET)
public String findOwner(@PathVariable("ownerId") String theOwner, Model model) {
    // 具体的方法代码…
}
```

```java
@RequestMapping(path="/owners/{ownerId}", method=RequestMethod.GET)
public String findOwner(@PathVariable String ownerId, Model model) {
    Owner owner = ownerService.findOwner(ownerId);
    model.addAttribute("owner", owner);
    return "displayOwner";
}
```
