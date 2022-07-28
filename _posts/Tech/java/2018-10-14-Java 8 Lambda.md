---
layout: post
category: Java
title: Java 8 Lambda
tags: Java
---

# Lambda表达式的组成及使用
## Lambda表达式是什么？
可以把Lambda表达式理解为简洁地表示可传递的匿名函数的一种方式：它没有名称，但它有参数列表、函数主体、返回类型，可能还有一个可以抛出的异常列表。

- 匿名——我们说匿名，是因为它不像普通的方法那样有一个明确的名称：写得少而想得多！
- 函数——我们说它是函数，是因为Lambda函数不像方法那样属于某个特定的类。但和方法一样， Lambda有参数列表、函数主体、返回类型，还可能有可以抛出的异常列表。
- 传递——Lambda表达式可以作为参数传递给方法或存储在变量中。
- 简洁——无需像匿名类那样写很多模板代码。

## Lambda表达式的语法与组成

Lambda表达式由参数、箭头、主体组成。

```ruby
(lambda paramters) -> lambda expression;

小括号()：代表方法签名，当只有一个参数的时候，（）可以省略
lambda paramters：代表具体形参，参数可以指定类型也可以省略类型，因为Lambda表达式会自动推断出参数类型
->：代表lambda操作符
lambda expression：代表lambda表达式body体，具体的函数式接口唯一方法实现逻辑。当body体只有一行代码的时候，{}和return都可以省略
```

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



错误示例

- 参数类型要么全部省略，不能省略部分，如 (x, int y) -> x+y;
- 参数不能使用final修饰，如(final a)->a;
- 函数表达式接口不能返回一个Object对象，如Object obj = () -> "lambda";

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



# 进阶

## 函数式接口


有且只有一个抽象方法（可以包含default或static方法，但Object类除外）的接口是函数式接口。@FunctionlInterface就是用来指定某个接口必须是函数式接口。@FunctionalInterface不是必须的，只是告诉编译器检查这个接口，保证该接口只能包含一个抽象方法，否则就会编译出错。@FunctionalInterface主要是帮助程序员避免一些低级错误，比如多个抽象方法。



例子

![image.png](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202207282325504.png)

常用函数式接口

![image.png](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202207282324717.png)

![image.png](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202207282324583.png)



## 方法引用

**什么是方法引用？**
Lambda还有一个非常重要的功能，就是方法引用。方法引用可以理解为lambda表达式的简便写法。方法引用是用来直接访问类或者实例的已经存在的方法或构造方法（函数），它比lambda表达式更加的简洁，更高的可读性，更好的复用性。



**方法引用的语法**

```autohotkey
类名（或实例）::方法名
```

------

**方法引用的分类**

| 方法引用类型 | 语法                 | Lambda表达式                            |
| ------------ | -------------------- | --------------------------------------- |
| 静态方法引用 | 类名::staticMethod   | (args)->类名.staticMethod(args)         |
| 实例方法引用 | instance::instMethod | (args)->instance::instMethod(args)      |
| 对象方法引用 | 类名::instMethod     | (instance,args)->类名::instMethod(args) |
| 构造方法引用 | 类名::new            | (args)->new 类名(args)                  |



学会了lambda后已经会了如下写法

```java
    Consumer<String> c1 = (name) -> LambdaStaticMethodTest.setName(name);
    Consumer<String> c2 = name -> LambdaStaticMethodTest.setName(name);
    Consumer<String> c3 = (name) -> LambdaStaticMethodTest.queryName(name);
    Consumer<String> c4 = name -> LambdaStaticMethodTest.queryName(name);

```

但还可以再见过做替代，可用如下替代

```java
    Consumer<String> c5 = LambdaStaticMethodTest::setName;
    Consumer<String> c6 = LambdaStaticMethodTest::queryName;
```

原理在于就一个函数，已经知道参数是啥了，反正也是自己新起的名字，这样直接不如不起了。

```java
    Function<String, Integer> f1 = name -> LambdaStaticMethodTest.length(name);
    /**
     * 将f1改写为静态方法引用，只需要写类名和方法名即可，简洁了很多
     */
    Function<String, Integer> f2 = LambdaStaticMethodTest::length;
```

有参数的话，可自动识别，不用管。

有返回值的话，可自动识别，不用管。

[各种情况参考，实际就是不用管](https://segmentfault.com/a/1190000039404435)

# 参考

https://segmentfault.com/a/1190000039393723



https://segmentfault.com/a/1190000039404435