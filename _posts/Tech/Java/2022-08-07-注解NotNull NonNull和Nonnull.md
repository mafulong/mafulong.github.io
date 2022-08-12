---
layout: post
category: Java
title: 注解NotNull NonNull和Nonnull
tags: Java
---

## @NotNull @NonNull和@Nonnull



[参考](https://github.com/giantray/stackoverflow-java-top-qa/blob/master/contents/which-notnull-java-annotation-should-i-use.md)



lombok.NonNull

```
适用Lombok项目中代码生成器。不是一个标准的占位符注解.
```

会生成检查是否为空的code， 如果为空就抛出NPE异常。



javax.annotation.Nonnull

```
只适用FindBugs,JSR-305不适用
```

一个占位符，不生成code，但是代码分析里可以用到，如果是可空然后又直接引用属性，会发现这样。

其中@Nullable也是这样的，只是一个占位符，不生成code。



NotNull倒没用过这个注解。
