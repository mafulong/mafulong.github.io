---
layout: post
category: Java
title: java String
tags: Java
---

## String.format
String类有个格式化方法format()，返回一个String对象
```java
String fs;
fs=String.format("%d is 3",3);
```

String format()方法的语法为：

```
String.format(String format, Object... args)
```

### 格式说明符

以下是常用的格式说明符：

| 说明符 | 描述                        |
| :----- | :-------------------------- |
| %b, %B | 根据参数为“ true”或“ false” |
| %s, %S | 一个字符串, 也可以是其他，万能匹配 |
| %c, %C | Unicode字符                 |
| %d     | 十进制整数（仅用于整数）    |
| %f   | 用于十进制数字（用于浮点数） |

不知道用啥就用%s



### 十进制数的格式

示例

```java
class Main {
  public static void main(String[] args) {

    float n1 = -452.534f;
    double n2 = -345.766d;

    //按原样格式化浮点数
    System.out.println(String.format("n1 = %f", n1)); // -452.533997
    System.out.println(String.format("n2 = %f", n2)); // -345.766000

    //显示到小数点后两位
    System.out.println(String.format("n1 = %.2f", n1)); // -452.53
    System.out.println(String.format("n2 = %.2f", n2)); // -345.77
  }
}
```



## String, StringBuffer and StringBuilder

**1. 是否可变** 

- String 不可变
- StringBuffer 和 StringBuilder 可变

**2. 是否线程安全** 

- String 不可变，因此是线程安全的
- StringBuilder 不是线程安全的
- StringBuffer 是线程安全的，内部使用 synchronized 来同步

**StringBuffer 和 StringBuilder 类**

当对字符串进行修改的时候，需要使用 StringBuffer 和 StringBuilder 类。

和 String 类不同的是，StringBuffer 和 StringBuilder 类的对象能够被多次的修改，并且不产生新的未使用对象。

StringBuilder 类在 Java 5 中被提出，它和 StringBuffer 之间的最大不同在于 StringBuilder 的方法不是线程安全的（不能同步访问）。

由于 StringBuilder 相较于 StringBuffer 有速度优势，所以多数情况下建议使用 StringBuilder 类。然而在应用程序要求线程安全的情况下，则必须使用 StringBuffer 类。

比较

- String 长度大小不可变
- StringBuffer 和 StringBuilder 长度可变
- StringBuffer 线程安全 StringBuilder 线程不安全
- StringBuilder 速度快

## String和基本类型的转换

### 基本类型转换String
String.valueOf()函数转为字符串
```java
String s=String.valueOf(3);
```

### String转换基本类型
```java
int intValue = Integer.parseInt(s);
```

## String 不可变的原因

**1. 可以缓存 hash 值** 

因为 String 的 hash 值经常被使用，例如 String 用做 HashMap 的 key。不可变的特性可以使得 hash 值也不可变，因此只需要进行一次计算。

**2. String Pool 的需要** 

如果一个 String 对象已经被创建过了，那么就会从 String Pool 中取得引用。只有 String 是不可变的，才可能使用 String Pool。

**3. 安全性** 

String 经常作为参数，String 不可变性可以保证参数不可变。例如在作为网络连接参数的情况下如果 String 是可变的，那么在网络连接过程中，String 被改变，改变 String 对象的那一方以为现在连接的是其它主机，而实际情况却不一定是。

**4. 线程安全** 

String 不可变性天生具备线程安全，可以在多个线程中安全地使用。

## String.intern()

使用 String.intern() 可以保证相同内容的字符串实例引用相同的内存对象。

下面示例中，s1 和 s2 采用 new String() 的方式新建了两个不同对象，而 s3 是通过 s1.intern() 方法取得一个对象引用，这个方法首先把 s1 引用的对象放到 String Poll（字符串常量池）中，然后返回这个对象引用。因此 s3 和 s1 引用的是同一个字符串常量池的对象。

```java
String s1 = new String("aaa");
String s2 = new String("aaa");
System.out.println(s1 == s2);           // false
String s3 = s1.intern();
System.out.println(s1.intern() == s3);  // true
```

如果是采用 "bbb" 这种使用双引号的形式创建字符串实例，会自动地将新建的对象放入 String Poll 中。

```java
String s4 = "bbb";
String s5 = "bbb";
System.out.println(s4 == s5);  // true
```

在 Java 7 之前，字符串常量池被放在运行时常量池中，它属于永久代。而在 Java 7，字符串常量池被放在堆中。这是因为永久代的空间有限，在大量使用字符串的场景下会导致 OutOfMemoryError 错误。