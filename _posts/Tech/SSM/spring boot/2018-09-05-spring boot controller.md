---
layout: post
category: SSM
title: spring boot controller
---

```@Controller```  处理Http请求

```@RestController```  spring4新加注解，就是```@ResponseBody```与```@Contrller```的结合，返回Json

默认没有```@Controller``` 的模板，要引入thymeleaf，然后templates里放

```@PathVariable``` 获取Url中的数据

```java
    @RequestMapping(value = "/hello/{id}",method = RequestMethod.GET)
    public String Hello2(@PathVariable(value = "id")Integer id){
        System.out.println(id);
        return String.valueOf(id);
    }
```

```@RequestParam```获取参数

```java
    @RequestMapping(value = "/hello",method = RequestMethod.GET)
    public String Hello3(@RequestParam(value = "id",defaultValue = "-1") Integer id){
        System.out.println(id);
        return String.valueOf(id);
    }
```

```http://localhost:8080/hello?id=444```

## 简化RequesetMapping

```@RequestMapping(value = "/hello",method = RequestMethod.GET)```
   替换为
```@GetMapping(value = "/hello")```

类似的：

```java
@PostMapping
@PutMapping
@DeleteMapping
```