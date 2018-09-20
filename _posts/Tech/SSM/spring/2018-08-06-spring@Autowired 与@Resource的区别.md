---
layout: post
category: SSM
title: spring@Autowired 与@Resource的区别
---

@Resource的作用相当于@Autowired，只不过@Autowired按byType自动注入，而@Resource默认按 byName自动注入罢了。@Resource有两个属性是比较重要的，分是name和type，Spring将@Resource注解的name属性解析为bean的名字，而type属性则解析为bean的类型。所以如果使用name属性，则使用byName的自动注入策略，而使用type属性时则使用byType自动注入策略。如果既不指定name也不指定type属性，这时将通过反射机制使用byName自动注入策略。

@Autowired与@Resource都可以用来装配bean. 都可以写在字段上,或写在setter方法上。

[link](https://blog.csdn.net/weixin_40423597/article/details/80643990)