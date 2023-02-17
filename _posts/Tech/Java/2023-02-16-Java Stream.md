---
layout: post
category: Java
title: Java Stream
tags: Java
---

## Java Stream

Java 8 API添加了一个新的抽象称为流Stream，可以让你以一种声明的方式处理数据。

Stream 使用一种类似用 SQL 语句从数据库查询数据的直观方式来提供一种对 Java 集合运算和表达的高阶抽象。

Stream API可以极大提高Java程序员的生产力，让程序员写出高效率、干净、简洁的代码。

这种风格将要处理的元素集合看作一种流， 流在管道中传输， 并且可以在管道的节点上进行处理， 比如筛选， 排序，聚合等。

元素流在管道中经过中间操作（intermediate operation）的处理，最后由最终操作(terminal operation)得到前面处理的结果。

```
+--------------------+       +------+   +------+   +---+   +-------+
| stream of elements +-----> |filter+-> |sorted+-> |map+-> |collect|
+--------------------+       +------+   +------+   +---+   +-------+
```

以上的流程转换为 Java 代码为：

```java
List<Integer> transactionsIds = 
widgets.stream()
             .filter(b -> b.getColor() == RED)
             .sorted((x,y) -> x.getWeight() - y.getWeight())
             .mapToInt(Widget::getWeight)
             .sum();
```



Stream（流）是一个来自数据源的元素队列并支持聚合操作

- 元素是特定类型的对象，形成一个队列。 Java中的Stream并不会存储元素，而是按需计算。
- **数据源** 流的来源。 可以是集合，数组，I/O channel， 产生器generator 等。
- **聚合操作** 类似SQL语句一样的操作， 比如filter, map, reduce, find, match, sorted等。

和以前的Collection操作不同， Stream操作还有两个基础的特征：

- **Pipelining**: 中间操作都会返回流对象本身。 这样多个操作可以串联成一个管道， 如同流式风格（fluent style）。 这样做可以对操作进行优化， 比如延迟执行(laziness)和短路( short-circuiting)。
- **内部迭代**： 以前对集合遍历都是通过Iterator或者For-Each的方式, 显式的在集合外部进行迭代， 这叫做外部迭代。 Stream提供了内部迭代的方式， 通过访问者模式(Visitor)实现。



## 生成流

在 Java 8 中, 集合接口有两个方法来生成流：

- **stream()** − 为集合创建串行流。
- **parallelStream()** − 为集合创建并行流。

```scala
List<String> strings = Arrays.asList("abc", "", "bc", "efg", "abcd","", "jkl");
List<String> filtered = strings.stream().filter(string -> !string.isEmpty()).collect(Collectors.toList());
```



方法

- forEach 迭代
- map 方法用于映射每个元素到对应的结果
- filter 方法用于通过设置的条件过滤出元素
- limit 方法用于获取指定数量的流
- sorted 方法用于对流进行排序
- collect 终端操作。collect 是一个非常有用的终端操作，它可以将流中的元素转变成另外一个不同的对象，例如一个`List`，`Set`或`Map`。其中Collectors 类实现了很多归约操作，例如将流转换成集合和聚合元素。Collectors 可用于返回列表或字符串。

## Stream 流的处理顺序

当且仅当存在终端操作时，中间操作操作才会被执行。原因是出于性能的考虑。这样设计可以减少对每个元素的实际操作数

区别：

**①**：中间操作会再次返回一个流，所以，我们可以链接多个中间操作，注意这里是不用加分号的。上图中的`filter` 过滤，`map` 对象转换，`sorted` 排序，就属于中间操作。

**②**：终端操作是对流操作的一个结束动作，一般返回 `void` 或者一个非流的结果。 `forEach`循环 就是一个终止操作。



前后位置影响复杂度。比如filter在前面就可以减少大量元素。



 Stream 流是不能被复用的，一旦你调用任何终端操作，流就会关闭

## 操作

### Collect

collect 终端操作。collect 是一个非常有用的终端操作，它可以将流中的元素转变成另外一个不同的对象，例如一个`List`，`Set`或`Map`。其中Collectors 类实现了很多归约操作，例如将流转换成集合和聚合元素。Collectors 可用于返回列表或字符串。collect 接受入参为`Collector`（收集器），它由四个不同的操作组成：供应器（supplier）、累加器（accumulator）、组合器（combiner）和终止器（finisher）。



对于如何将流转换为 `Map`集合，我们必须指定 `Map` 的键和值。这里需要注意，`Map` 的键必须是唯一的，否则会抛出`IllegalStateException` 异常。

```scala
Map<Integer, String> map = persons
    .stream()
    .collect(Collectors.toMap(
        p -> p.age,
        p -> p.name,
        (name1, name2) -> name1 + ";" + name2)); // 对于同样 key 的，将值拼接

System.out.println(map);
// {18=Max, 23=Peter;Pamela, 12=David}

```



构建自定义收集器。 比如说，我们希望将流中的所有人转换成一个字符串，包含所有大写的名称，并以|分割。为了达到这种效果，我们需要通过Collector.of()创建一个新的收集器。同时，我们还需要传入收集器的四个组成部分：供应器、累加器、组合器和终止器。

```java
Collector<Person, StringJoiner, String> personNameCollector =
    Collector.of(
        () -> new StringJoiner(" | "),          // supplier 供应器
        (j, p) -> j.add(p.name.toUpperCase()),  // accumulator 累加器
        (j1, j2) -> j1.merge(j2),               // combiner 组合器
        StringJoiner::toString);                // finisher 终止器

String names = persons
    .stream()
    .collect(personNameCollector); // 传入自定义的收集器

System.out.println(names);  // MAX | PETER | PAMELA | DAVID

```

### FlatMap 平铺

`Map`只能将每个对象映射到另一个对象。

如果说，我们想要将一个对象转换为多个其他对象或者根本不做转换操作呢？这个时候，`flatMap`就派上用场了。



`FlatMap` 能够将流的每个元素, 转换为其他对象的流。因此，每个对象可以被转换为零个，一个或多个其他对象，并以流的方式返回。之后，这些流的内容会被放入`flatMap`返回的流中。



我们创建了包含三个`foo`的集合，每个`foo`中又包含三个 `bar`。

`flatMap` 的入参接受一个返回对象流的函数。为了处理每个`foo`中的`bar`，我们需要传入相应 stream 流：

```java
foos.stream()
    .flatMap(f -> f.bars.stream())
    .forEach(b -> System.out.println(b.name));
```

如上所示，我们已成功将三个 `foo`对象的流转换为九个`bar`对象的流。

### Reduce

归约。连续操作每两个连续的值。

```scala
persons
    .stream()
    .reduce((p1, p2) -> p1.age > p2.age ? p1 : p2)
    .ifPresent(System.out::println);    // Pamela
```



## 参考

- https://juejin.cn/post/6844903830254010381