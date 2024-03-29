---
layout: post
category: SpringMVC
tags: SpringMVC
title: Spring MVC 注解 @RequestParam解析
---

在 Spring MVC 后台控制层获取参数的方式主要有两种，一种是 requset.getParameter(“name”),另一种是用注解@Resquest.Param 直接获取。

```java
    @RequestMapping("/publisherManage")
    public String publisherManage(ModelMap modelMap,
            @RequestParam(value = "page", required = false, defaultValue = "1") int page,
            @RequestParam(value = "user", required = false, defaultValue = "") String user,
            @RequestParam(value = "name", required = false, defaultValue = "") String name) {

        Integer id = null;
        String appId = null;
        BizQuery pageInfo = new BizQuery();
        pageInfo.setAppId(appId);
        pageInfo.setId(id);
        pageInfo.setPage(page);
        if (!StringUtils.isBlank(user))
            pageInfo.setUserId(user);
        if (!StringUtils.isBlank(name))
            pageInfo.setName(name);
        int num = fundService.getFundsNumByManagerPublisher(pageInfo);
        pageInfo.setNum(num);
        List<BizQuery> queryInfos = fundService.getFundsByManagerPublisher(pageInfo);
        BizQuery statInfo = fundService.getCountByManagerPublisher();
        modelMap.addAttribute("statInfo", statInfo);
        modelMap.addAttribute("queryInfos", queryInfos);
        modelMap.addAttribute("pageInfo", pageInfo);
        return "/manager/publisherManage";
    }
```

以上的 value 值是对传入的参数有所指定，如果传入的参数不是 value 值，会报错。

request=false(ture)表示前端的参数是否一定要传入。

需要注意的是 value=“page”，它是 Int 型的，如果不传入，会报错，于是设置一个默认值 default= 1，因为如果不传入值就会为空值 null，int 为空置是不可以的。
