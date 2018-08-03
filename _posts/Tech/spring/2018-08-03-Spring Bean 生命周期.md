---
layout: post
category: spring
title: Spring Bean 生命周期
---

理解 Spring bean 的生命周期很容易。当一个 bean 被实例化时，它可能需要执行一些初始化使它转换成可用状态。同样，当 bean 不再需要，并且从容器中移除时，可能需要做一些清除工作。

只要声明带有 init-method 和/或 destroy-method 参数的 。init-method 属性指定一个方法，在实例化 bean 时，立即调用该方法。同样，destroy-method 指定一个方法，只有从容器中移除 bean 之后，才能调用该方法。

## 初始化回调

org.springframework.beans.factory.InitializingBean 接口指定一个单一的方法：

```java
void afterPropertiesSet() throws Exception;
```

因此，你可以简单地实现上述接口和初始化工作可以在 afterPropertiesSet() 方法中执行，如下所示：

```java

public class ExampleBean implements InitializingBean {
   public void afterPropertiesSet() {
      // do some initialization work
   }
}
```

在基于 XML 的配置元数据的情况下，你可以使用 init-method 属性来指定带有 void 无参数方法的名称。例如：

```xml
<bean id="exampleBean" 
         class="examples.ExampleBean" init-method="init"/>
```

下面是类的定义：

```java

public class ExampleBean {
   public void init() {
      // do some initialization work
   }
}
```

## 销毁回调

org.springframework.beans.factory.DisposableBean 接口指定一个单一的方法：

你可以简单地实现上述接口并且结束工作可以在 destroy() 方法中执行，如下所示：
```java
public class ExampleBean implements DisposableBean {
   public void destroy() {
      // do some destruction work
   }
}
```

```xml
<bean id="exampleBean"
         class="examples.ExampleBean" destroy-method="destroy"/>
```
```xml
   <bean id="helloWorld" 
       class="com.tutorialspoint.HelloWorld"
       init-method="init" destroy-method="destroy">
       <property name="message" value="Hello World!"/>
   </bean>
```

## 默认的初始化和销毁方法

如果你有太多具有相同名称的初始化或者销毁方法的 Bean，那么你不需要在每一个 bean 上声明初始化方法和销毁方法。框架使用 元素中的 default-init-method 和 default-destroy-method 属性提供了灵活地配置这种情况，如下所示：

```java
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.springframework.org/schema/beans
    http://www.springframework.org/schema/beans/spring-beans-3.0.xsd"
    default-init-method="init" 
    default-destroy-method="destroy">

   <bean id="..." class="...">
       <!-- collaborators and configuration for this bean go here -->
   </bean>

</beans>
```