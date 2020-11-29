---
layout: post
category: JavaLib
tags: JavaLib
title: SpringBean作用域和生命周期
---

## Bean 的作用域

当在 Spring 中定义一个 bean 时，你必须声明该 bean 的作用域的选项。例如，为了强制 Spring 在每次需要时都产生一个新的 bean 实例，你应该声明 bean 的作用域的属性为 prototype。同理，如果你想让 Spring 在每次需要时都返回同一个bean实例，你应该声明 bean 的作用域的属性为 singleton。
Spring 框架支持以下五个作用域，如果你使用 web-aware ApplicationContext 时，其中三个是可用的。

1. singleton    在spring IoC容器仅存在一个Bean实例，Bean以单例方式存在，默认值
2. prototype 每次从容器中调用Bean时，都返回一个新的实例，即每次调用getBean()时，相当于执行newXxxBean()
3. request  每次HTTP请求都会创建一个新的Bean，该作用域仅适用于WebApplicationContext环境
4. session  同一个HTTP Session共享一个Bean，不同Session使用不同的Bean，仅适用于WebApplicationContext环境
5. global-session   一般用于Portlet应用环境，改作用于仅适用于WebApplicationContext环境

```xml
<bean id="..." class="..." scope="singleton">
    <!-- collaborators and configuration for this bean go here -->
</bean>
```

# Bean的声明周期

理解 Spring bean 的生命周期很容易。当一个 bean 被实例化时，它可能需要执行一些初始化使它转换成可用状态。同样，当 bean 不再需要，并且从容器中移除时，可能需要做一些清除工作。

只要声明带有 init-method 和/或 destroy-method 参数的 。init-method 属性指定一个方法，在实例化 bean 时，立即调用该方法。同样，destroy-method 指定一个方法，只有从容器中移除 bean 之后，才能调用该方法。

## 初始化销毁回调
### 初始化回调

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

### 销毁回调

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

## 生命周期

![](https://i.imgur.com/INF4UhB.png)

![](https://upload-images.jianshu.io/upload_images/4638441-05bf2b9b2f2a01d4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1. Spring容器 从XML 文件中读取bean的定义，并实例化bean。
1. Spring根据bean的定义填充所有的属性。
1. 如果bean实现了BeanNameAware 接口，Spring 传递bean 的ID 到 setBeanName方法。
1. 如果Bean 实现了 BeanFactoryAware 接口， Spring传递beanfactory 给setBeanFactory 方法。
1. 如果有任何与bean相关联的BeanPostProcessors，Spring会在postProcesserBeforeInitialization()方法内调用它们。
1. 如果bean实现IntializingBean了，调用它的afterPropertySet方法，如果bean声明了初始化方法，调用此初始化方法。
1. 如果有BeanPostProcessors 和bean 关联，这些bean的postProcessAfterInitialization() 方法将被调用。
1. 如果bean实现了 DisposableBean，它将调用destroy()方法。