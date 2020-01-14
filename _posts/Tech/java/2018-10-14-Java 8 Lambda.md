---
layout: post
category: Java
title: Java 8 Lambda
tags: Java
---

## Lambda表达式的组成及使用
### Lambda表达式是什么？
可以把Lambda表达式理解为简洁地表示可传递的匿名函数的一种方式：它没有名称，但它有参数列表、函数主体、返回类型，可能还有一个可以抛出的异常列表。

- 匿名——我们说匿名，是因为它不像普通的方法那样有一个明确的名称：写得少而想得多！
- 函数——我们说它是函数，是因为Lambda函数不像方法那样属于某个特定的类。但和方法一样， Lambda有参数列表、函数主体、返回类型，还可能有可以抛出的异常列表。
- 传递——Lambda表达式可以作为参数传递给方法或存储在变量中。
- 简洁——无需像匿名类那样写很多模板代码。

### Lambda表达式的语法与组成

Lambda表达式由参数、箭头、主体组成。如下图：

![](http://img.hao124.net/c25961a4a7f8330c30c9774689d32bce.PNG)

- 参数列表——这里它采用了Comparator中compare方法的参数，两个Apple。
- 箭头——箭头->把参数列表与Lambda主体分隔开。
- Lambda主体——比较两个Apple的重量。表达式就是Lambda的返回值了。

所以,Lambda表达式的基本语法可以总结为:
```(parameters) -> expression 或 (parameters) -> { statements; }```

使用案例	Lambda示例

- 布尔表达式	```(List list) -> list.isEmpty()```
- 创建对象	```() -> new Apple(10)```
- 消费一个对象	```(Apple a) -> {System.out.println(a.getWeight());}```
- 从一个对象中选择/抽取	(```String s) -> s.length()```
- 组合两个值	``(int a, int b) -> a * b``
- 比较两个对象	```(Apple a1, Apple a2) ->a1.getWeight().compareTo(a2.getWeight())```

也许你已经想到了，能够使用Lambda的依据是必须有相应的函数接口（函数接口，是指内部只有一个抽象方法的接口）。这一点跟Java是强类型语言吻合，也就是说你并不能在代码的任何地方任性的写Lambda表达式。实际上Lambda的类型就是对应函数接口的类型。Lambda表达式另一个依据是类型推断机制，在上下文信息足够的情况下，编译器可以推断出参数表的类型，而不需要显式指名。Lambda表达更多合法的书写形式如下：

```java
// Lambda表达式的书写形式
Runnable run = () -> System.out.println("Hello World");// 1
ActionListener listener = event -> System.out.println("button clicked");// 2
Runnable multiLine = () -> {// 3 代码块
    System.out.print("Hello");
    System.out.println(" Hoolee");
};
BinaryOperator<Long> add = (Long x, Long y) -> x + y;// 4
BinaryOperator<Long> addImplicit = (x, y) -> x + y;// 5 类型推断
```

## 1.替代匿名内部类

毫无疑问，lambda表达式用得最多的场合就是替代匿名内部类，而实现Runnable接口是匿名内部类的经典例子。lambda表达式的功能相当强大，用()->就可以代替整个匿名内部类！


```java
    @Test
    public void oldRunable() {
        new Thread(new Runnable() {
            @Override
            public void run() {
                System.out.println("The old runable now is using!");
            }
        }).start();
    }
//lambada
    @Test
    public void runable() {
        new Thread(() -> System.out.println("It's a lambda function!")).start();
    }
```

## 2.使用lambda表达式对集合进行迭代
Java的集合类是日常开发中经常用到的，甚至说没有哪个java代码中没有使用到集合类。。。而对集合类最常见的操作就是进行迭代遍历了。请看对比：

```java
    @Test
    public void iterTest() {
        List<String> languages = Arrays.asList("java","scala","python");
        //before java8
        for(String each:languages) {
            System.out.println(each);
        }
        //after java8
        languages.forEach(x -> System.out.println(x));
        languages.forEach(System.out::println);
    }
```


## 3.用lambda表达式实现map
一提到函数式编程，一提到lambda表达式，怎么能不提map。。。没错，java8肯定也是支持的。请看示例代码：

```java
    @Test
    public void mapTest() {
        List<Double> cost = Arrays.asList(10.0, 20.0,30.0);
        cost.stream().map(x -> x + x*0.05).forEach(x -> System.out.println(x));
    }
```

## 4.用lambda表达式实现map与reduce

既然提到了map，又怎能不提到reduce。reduce与map一样，也是函数式编程里最重要的几个方法之一。。。map的作用是将一个对象变为另外一个，而reduce实现的则是将所有值合并为一个，请看：

```java
    @Test
    public void mapReduceTest() {
        List<Double> cost = Arrays.asList(10.0, 20.0,30.0);
        double allCost = cost.stream().map(x -> x+x*0.05).reduce((sum,x) -> sum + x).get();
        System.out.println(allCost);
    }
```

## 5.filter操作

filter也是我们经常使用的一个操作。在操作集合的时候，经常需要从原始的集合中过滤掉一部分元素。
```java
    @Test
    public void filterTest() {
        List<Double> cost = Arrays.asList(10.0, 20.0,30.0,40.0);
        List<Double> filteredCost = cost.stream().filter(x -> x > 25.0).collect(Collectors.toList());
        filteredCost.forEach(x -> System.out.println(x));

    }
```

## 6.与函数式接口Predicate配合
除了在语言层面支持函数式编程风格，Java 8也添加了一个包，叫做 java.util.function。它包含了很多类，用来支持Java的函数式编程。其中一个便是Predicate，使用 java.util.function.Predicate 函数式接口以及lambda表达式，可以向API方法添加逻辑，用更少的代码支持更多的动态行为。Predicate接口非常适用于做过滤。

```java
   public static void filterTest(List<String> languages, Predicate<String> condition) {
        languages.stream().filter(x -> condition.test(x)).forEach(x -> System.out.println(x + " "));
    }

    public static void main(String[] args) {
        List<String> languages = Arrays.asList("Java","Python","scala","Shell","R");
        System.out.println("Language starts with J: ");
        filterTest(languages,x -> x.startsWith("J"));
        System.out.println("\nLanguage ends with a: ");
        filterTest(languages,x -> x.endsWith("a"));
        System.out.println("\nAll languages: ");
        filterTest(languages,x -> true);
        System.out.println("\nNo languages: ");
        filterTest(languages,x -> false);
        System.out.println("\nLanguage length bigger three: ");
        filterTest(languages,x -> x.length() > 4);
    }
```