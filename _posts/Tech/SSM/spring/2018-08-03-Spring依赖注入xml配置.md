---
layout: post
category: SSM 
tags: Spring
title: Spring依赖注入xml配置
---

DI（Depandency Injection），也叫“依赖注入”，与人也称其为“控制反转（IOC）”，而我更喜欢把它称之为DI。传统的Java对象，对其本身及关联的对象（Bean），都是自主创建和管理的，这样就导致高度耦合和难以测试的问题。而Spring框架则意识到这个问题，其提供的DI功能，可以完美的解决Bean及其依赖的Bean的创建、装配及生命周期等管理工作，这个管理机制称为“Spring容器”，也是Spring框架的核心模块。

## Spring 基于构造函数的依赖注入

当容器调用带有一组参数的类构造函数时，基于构造函数的 DI 就完成了，其中每个参数代表一个对其他类的依赖。

```xml
   <bean id="textEditor" class="com.tutorialspoint.TextEditor">
      <constructor-arg ref="spellChecker"/>
   </bean>
```

## 构造函数参数解析:

如果存在不止一个参数时，当把参数传递给构造函数时，可能会存在歧义。要解决这个问题，那么构造函数的参数在 bean 定义中的顺序就是把这些参数提供给适当的构造函数的顺序就可以了。考虑下面的类:

```java
package x.y;
public class Foo {
   public Foo(Bar bar, Baz baz) {
      // ...
   }
}
```

下述配置文件工作顺利：
```xml
<beans>
   <bean id="foo" class="x.y.Foo">
      <constructor-arg ref="bar"/>
      <constructor-arg ref="baz"/>
   </bean>

   <bean id="bar" class="x.y.Bar"/>
   <bean id="baz" class="x.y.Baz"/>
</beans>
```

让我们再检查一下我们传递给构造函数不同类型的位置。考虑下面的类：
```java
package x.y;
public class Foo {
   public Foo(int year, String name) {
      // ...
   }
}
```

如果你使用 type 属性显式的指定了构造函数参数的类型，容器也可以使用与简单类型匹配的类型。例如：
```xml
<beans>

   <bean id="exampleBean" class="examples.ExampleBean">
      <constructor-arg type="int" value="2001"/>
      <constructor-arg type="java.lang.String" value="Zara"/>
   </bean>

</beans>
```

最后并且也是最好的传递构造函数参数的方式，使用 index 属性来显式的指定构造函数参数的索引。下面是基于索引为 0 的例子，如下所示：
```xml
<beans>

   <bean id="exampleBean" class="examples.ExampleBean">
      <constructor-arg index="0" value="2001"/>
      <constructor-arg index="1" value="Zara"/>
   </bean>

</beans>
```

最后，如果你想要向一个对象传递一个引用，你需要使用 标签的 ref 属性，如果你想要直接传递值，那么你应该使用如上所示的 value 属性。

## Spring 基于设值函数的依赖注入

当容器调用一个无参的构造函数或一个无参的静态 factory 方法来初始化你的 bean 后，通过容器在你的 bean 上调用设值函数，基于设值函数的 DI 就完成了。
```xml
   <bean id="textEditor" class="com.tutorialspoint.TextEditor">
      <property name="spellChecker" ref="spellChecker"/>
   </bean>

   <!-- Definition for spellChecker bean -->
   <bean id="spellChecker" class="com.tutorialspoint.SpellChecker">
   </bean>
```

如果你要把一个引用传递给一个对象，那么你需要使用 标签的 ref 属性，而如果你要直接传递一个值，那么你应该使用 value 属性。

## 注入内部 Beans

正如你所知道的 Java 内部类是在其他类的范围内被定义的，同理，inner beans 是在其他 bean 的范围内定义的 bean。因此在 或 元素内 元素被称为内部bean，如下所示。

```xml
   <bean id="textEditor" class="com.tutorialspoint.TextEditor">
      <property name="spellChecker">
         <bean id="spellChecker" class="com.tutorialspoint.SpellChecker"/>
       </property>
   </bean>
```

## 注入集合

你已经看到了如何使用 value 属性来配置基本数据类型和在你的 bean 配置文件中使用<property>标签的 ref 属性来配置对象引用。这两种情况下处理奇异值传递给一个 bean。

现在如果你想传递多个值，如 Java Collection 类型 List、Set、Map 和 Properties，应该怎么做呢。为了处理这种情况，Spring 提供了四种类型的集合的配置元素，如下所示：

```xml
   <bean id="javaCollection" class="com.tutorialspoint.JavaCollection">

      <!-- results in a setAddressList(java.util.List) call -->
      <property name="addressList">
         <list>
            <value>INDIA</value>
            <value>Pakistan</value>
            <value>USA</value>
            <value>USA</value>
         </list>
      </property>

      <!-- results in a setAddressSet(java.util.Set) call -->
      <property name="addressSet">
         <set>
            <value>INDIA</value>
            <value>Pakistan</value>
            <value>USA</value>
            <value>USA</value>
        </set>
      </property>

      <!-- results in a setAddressMap(java.util.Map) call -->
      <property name="addressMap">
         <map>
            <entry key="1" value="INDIA"/>
            <entry key="2" value="Pakistan"/>
            <entry key="3" value="USA"/>
            <entry key="4" value="USA"/>
         </map>
      </property>

      <!-- results in a setAddressProp(java.util.Properties) call -->
      <property name="addressProp">
         <props>
            <prop key="one">INDIA</prop>
            <prop key="two">Pakistan</prop>
            <prop key="three">USA</prop>
            <prop key="four">USA</prop>
         </props>
      </property>

   </bean>
```

## 注入 null 和空字符串的值

如果你需要传递一个空字符串作为值，那么你可以传递它，如下所示：
```xml
<bean id="..." class="exampleBean">
   <property name="email" value=""/>
</bean>
```