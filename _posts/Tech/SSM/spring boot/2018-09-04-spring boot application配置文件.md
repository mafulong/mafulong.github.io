---
layout: post
category: SSM
title: spring boot application配置文件
---

[参考](https://www.cnblogs.com/lixuwu/p/6376194.html)

## YAML文件

properties文件在面对有层次关系的数据时，就有点不合适。YAML 支持一种类似JSON的格式，可以表现具有层次的数据。详细说明看这里.
YAML的内容会转换为properties格式

application.yml

Spring Boot 也支持Profile特性，Profile相关的配置文件命名为:application-{profile}.properties,可以用spring.profiles.active激活Profile:

```java -jar target/demo-0.0.1-SNAPSHOT.jar --spring.profiles.active=test```

虽然可以通过@Value("${property}")注入属性值,如果有多项需要注入，就有点麻烦了。@ConfigurationProperties可以直接把多个属性值绑定到Bean上。

```@Value("${connection.remoteAddress}") private String address;```

```xml
# application.yml

connection:
    username: admin
    remoteAddress: 192.168.1.1
```

```java
@Component
@ConfigurationProperties(prefix="connection")
public class ConnectionSettings {
    private String username;
    private InetAddress remoteAddress;
    // ... getters and setters
}
```