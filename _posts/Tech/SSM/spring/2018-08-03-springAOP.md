---
layout: post
category: Spring 
tags: Spring
title: SpringAOP
---

[link](https://www.cnblogs.com/liuruowang/p/5711563.html)

AOP称为面向切面编程，在程序开发中主要用来解决一些系统层面上的问题，比如日志，事务，权限等待，Struts2的拦截器设计就是基于AOP的思想，是个比较经典的例子。

## 一 AOP的基本概念

(1)Aspect(切面):通常是一个类，里面可以定义切入点和通知

(2)JointPoint(连接点):程序执行过程中明确的点，一般是方法的调用

(3)Advice(通知):AOP在特定的切入点上执行的增强处理，有before,after,afterReturning,afterThrowing,around 	这是实际行动之前或之后执行的方法。这是在程序执行期间通过 Spring AOP 框架实际被调用的代码。

(4)Pointcut(切入点):就是带有通知的连接点，在程序中主要体现为书写切入点表达式

(5)AOP代理：AOP框架创建的对象，代理就是目标对象的加强。Spring中的AOP代理可以使JDK动态代理，也可以是CGLIB代理，前者基于接口，后者基于子类


## 二 Spring AOP

Spring中的AOP代理还是离不开Spring的IOC容器，代理的生成，管理及其依赖关系都是由IOC容器负责，Spring默认使用JDK动态代理，在需要代理类而不是代理接口的时候，Spring会自动切换为使用CGLIB代理，不过现在的项目都是面向接口编程，所以JDK动态代理相对来说用的还是多一些。

Spring AOP 模块提供拦截器来拦截一个应用程序，例如，当执行一个方法时，你可以在方法执行之前或之后添加额外的功能。


## 三 基于注解的AOP配置方式

### 基于注解的AOP配置方式
1.启用@AsjectJ支持

在applicationContext.xml中配置下面一句:
```xml
<aop:aspectj-autoproxy />
```

2.通知类型介绍

(1)Before:在一个方法执行之前，执行通知。在目标方法被调用之前做增强处理,@Before只需要指定切入点表达式即可

(2)AfterReturning:在目标方法正常完成后做增强,@AfterReturning除了指定切入点表达式后，还可以指定一个返回值形参名returning,代表目标方法的返回值

(3)AfterThrowing:主要用来处理程序中未处理的异常,@AfterThrowing除了指定切入点表达式后，还可以指定一个throwing的返回值形参名,可以通过该形参名

来访问目标方法中所抛出的异常对象

(4)After:在目标方法完成之后做增强，无论目标方法时候成功完成。@After可以指定一个切入点表达式

(5)Around:在建议方法调用之前和之后，执行通知。环绕通知,在目标方法完成前后做增强处理,环绕通知是最重要的通知类型,像事务,日志等都是环绕通知,注意编程中核心是一个ProceedingJoinPoint

3.例子：

![](https://images2015.cnblogs.com/blog/760279/201607/760279-20160727152818888-1665005413.png)

(1)Operator.java --> 切面类

```java
@Component
@Aspect
public class Operator {
    
    @Pointcut("execution(* com.aijava.springcode.service..*.*(..))")
    public void pointCut(){}
    
    @Before("pointCut()")
    public void doBefore(JoinPoint joinPoint){
        System.out.println("AOP Before Advice...");
    }
    
    @After("pointCut()")
    public void doAfter(JoinPoint joinPoint){
        System.out.println("AOP After Advice...");
    }
    
    @AfterReturning(pointcut="pointCut()",returning="returnVal")
    public void afterReturn(JoinPoint joinPoint,Object returnVal){
        System.out.println("AOP AfterReturning Advice:" + returnVal);
    }
    
    @AfterThrowing(pointcut="pointCut()",throwing="error")
    public void afterThrowing(JoinPoint joinPoint,Throwable error){
        System.out.println("AOP AfterThrowing Advice..." + error);
        System.out.println("AfterThrowing...");
    }
    
    @Around("pointCut()")
    public void around(ProceedingJoinPoint pjp){
        System.out.println("AOP Aronud before...");
        try {
            pjp.proceed();
        } catch (Throwable e) {
            e.printStackTrace();
        }
        System.out.println("AOP Aronud after...");
    }
    
}
```

(2)UserService.java --> 定义一些目标方法

```java
@Service
public class UserService {
    
    public void add(){
        System.out.println("UserService add()");
    }
    
    public boolean delete(){
        System.out.println("UserService delete()");
        return true;
    }
    
    public void edit(){
        System.out.println("UserService edit()");
        int i = 5/0;
    }
    
    
}
```

(3).applicationContext.xml

```xml
<context:component-scan base-package="com.aijava.springcode"/>
    
<aop:aspectj-autoproxy />
```
(4).Test.java
```java
public class Test {
    public static void main(String[] args) {
        ApplicationContext ctx = new ClassPathXmlApplicationContext("classpath:applicationContext.xml");
        UserService userService = (UserService) ctx.getBean("userService");
        userService.add();
    }
}
```

上面是一个比较简单的测试，基本涵盖了各种增强定义。注意:做环绕通知的时候，调用ProceedingJoinPoint的proceed()方法才会执行目标方法。

4.通知执行的优先级

进入目标方法时,先织入Around,再织入Before，退出目标方法时，先织入Around,再织入AfterReturning,最后才织入After。

注意:Spring AOP的环绕通知会影响到AfterThrowing通知的运行,不要同时使用!同时使用也没啥意义。

5.切入点的定义和表达式

切入点表达式的定义算是整个AOP中的核心，有一套自己的规范

Spring AOP支持的切入点指示符：

(1)execution:用来匹配执行方法的连接点

    A:@Pointcut("execution(* com.aijava.springcode.service..*.*(..))")

第一个*表示匹配任意的方法返回值，..(两个点)表示零个或多个，上面的第一个..表示service包及其子包,第二个*表示所有类,第三个*表示所有方法，第二个..表示

方法的任意参数个数

    B:@Pointcut("within(com.aijava.springcode.service.*)")

within限定匹配方法的连接点,上面的就是表示匹配service包下的任意连接点

    C:@Pointcut("this(com.aijava.springcode.service.UserService)")

this用来限定AOP代理必须是指定类型的实例，如上，指定了一个特定的实例，就是UserService

    D:@Pointcut("bean(userService)")

bean也是非常常用的,bean可以指定IOC容器中的bean的名称

6.基于XML形式的配置方式

开发中如果选用XML配置方式，通常就是POJO+XML来开发AOP,大同小异，无非就是在XML文件中写切入点表达式和通知类型

### execution切入点表达式

Spring AOP 用户可能会经常使用 execution切入点指示符。执行表达式的格式如下：

execution（modifiers-pattern? ret-type-pattern declaring-type-pattern? name-pattern（param-pattern）throws-pattern?）

除了返回类型模式（上面代码片断中的ret-type-pattern），名字模式和参数模式以外， 所有的部分都是可选的。返回类型模式决定了方法的返回类型必须依次匹配一个连接点。 

使用的最频繁的返回类型模式是*，它代表了匹配任意的返回类型。 一个全限定的类型名将只会匹配返回给定类型的方法。名字模式匹配的是方法名。 

使用*通配符作为所有或者部分命名模式。 

类型匹配模式：

1. *：匹配任何数量字符；比如模式 (*,String) 匹配了一个接受两个参数的方法，第一个可以是任意类型，第二个则必须是String类型
2. ..：匹配任何数量字符的重复，如在类型模式中匹配任何数量子包；而在方法参数模式中匹配任何数量参数，可以使零到多个。
3. +：匹配指定类型的子类型；仅能作为后缀放在类型模式后边。

参数匹配模式：

    ()匹配了一个不接受任何参数的方法，
    (..)匹配了一个接受任意数量参数的方法（零或者更多）。 
    (*)匹配了一个接受一个任何类型的参数的方法。 
    (*,String)匹配了一个接受两个参数的方法，第一个可以是任意类型， 第二个则必须是String类型。

## 四 Spring 中基于 AOP 的 XML架构
为了在本节的描述中使用 aop 命名空间标签，你需要导入 spring-aop j架构，如下所述：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xmlns:aop="http://www.springframework.org/schema/aop"
    xsi:schemaLocation="http://www.springframework.org/schema/beans
    http://www.springframework.org/schema/beans/spring-beans-3.0.xsd 
    http://www.springframework.org/schema/aop 
    http://www.springframework.org/schema/aop/spring-aop-3.0.xsd ">

   <!-- bean definition & AOP specific configuration -->

</beans>
```

你还需要在你的应用程序的 CLASSPATH 中使用以下 AspectJ 库文件
```
aspectjrt.jar
aspectjweaver.jar
aspectj.jar
aopalliance.jar
```

### 声明一个 aspect

一个 aspect 是使用 元素声明的，支持的 bean 是使用 ref 属性引用的，如下所示：
```xml
<aop:config>
   <aop:aspect id="myAspect" ref="aBean">
   ...
   </aop:aspect>
</aop:config>
<bean id="aBean" class="...">
...
</bean>
```

这里，“aBean” 将被配置和依赖注入，就像前面的章节中你看到的其他的 Spring bean 一样。

### 声明一个切入点

一个切入点有助于确定使用不同建议执行的感兴趣的连接点（即方法）。在处理基于配置的 XML 架构时，切入点将会按照如下所示定义：
```xml
<aop:config>
   <aop:aspect id="myAspect" ref="aBean">
   <aop:pointcut id="businessService"
      expression="execution(* com.xyz.myapp.service.*.*(..))"/>
   ...
   </aop:aspect>
</aop:config>
<bean id="aBean" class="...">
...
</bean>

```

下面的示例定义了一个名为 “businessService” 的切入点，该切入点将与 com.tutorialspoint 包下的 Student 类中的 getName() 方法相匹配：
```xml
<aop:config>
   <aop:aspect id="myAspect" ref="aBean">
   <aop:pointcut id="businessService"
      expression="execution(* com.tutorialspoint.Student.getName(..))"/>
   ...
   </aop:aspect>
</aop:config>
<bean id="aBean" class="...">
...
</bean>
```

注意，aop的ref指向的bean是aspect啊！！！就是有切入点和advice的那个类

```xml
你可以使用 <aop:{ADVICE NAME}> 元素在一个 中声明五个建议中的任何一个，如下所示：
<aop:config>
   <aop:aspect id="myAspect" ref="aBean">
      <aop:pointcut id="businessService"
         expression="execution(* com.xyz.myapp.service.*.*(..))"/>
      <!-- a before advice definition -->
      <aop:before pointcut-ref="businessService" 
         method="doRequiredTask"/>
      <!-- an after advice definition -->
      <aop:after pointcut-ref="businessService" 
         method="doRequiredTask"/>
      <!-- an after-returning advice definition -->
      <!--The doRequiredTask method must have parameter named retVal -->
      <aop:after-returning pointcut-ref="businessService"
         returning="retVal"
         method="doRequiredTask"/>
      <!-- an after-throwing advice definition -->
      <!--The doRequiredTask method must have parameter named ex -->
      <aop:after-throwing pointcut-ref="businessService"
         throwing="ex"
         method="doRequiredTask"/>
      <!-- an around advice definition -->
      <aop:around pointcut-ref="businessService" 
         method="doRequiredTask"/>
   ...
   </aop:aspect>
</aop:config>
<bean id="aBean" class="...">
...
</bean>
```

## AOP实现
AOP实现的关键在于AOP框架自动创建的AOP代理，AOP代理主要分为静态代理和动态代理，静态代理的代表为AspectJ；而动态代理则以Spring AOP为代表。

AspectJ是静态代理的增强，所谓的静态代理就是AOP框架会在编译阶段生成AOP代理类，因此也称为编译时增强。

AspectJ的静态代理，它会在编译阶段将Aspect织入Java字节码中， 运行的时候就是经过增强之后的AOP对象。

与AspectJ的静态代理不同，Spring AOP使用的动态代理，所谓的动态代理就是说AOP框架不会去修改字节码，而是在内存中临时为方法生成一个AOP对象，这个AOP对象包含了目标对象的全部方法，并且在特定的切点做了增强处理，并回调原对象的方法。

Spring AOP中的动态代理主要有两种方式，JDK动态代理和CGLIB动态代理。JDK动态代理通过反射来接收被代理的类，并且要求被代理的类必须实现一个接口。JDK动态代理的核心是InvocationHandler接口和Proxy类。

如果目标类没有实现接口，那么Spring AOP会选择使用CGLIB来动态代理目标类。CGLIB（Code Generation Library），是一个代码生成的类库，可以在运行时动态的生成某个类的子类，注意，CGLIB是通过继承的方式做的动态代理，因此如果某个类被标记为final，那么它是无法使用CGLIB做动态代理的。