---
layout: post
category: Java
title: Collections工具类
---
[链接](https://www.cnblogs.com/fysola/p/6021134.html)

## 排序
void reverse(List list)：反转

void shuffle(List list),随机排序

void sort(List list),按自然排序的升序排序

void sort(List list, Comparator c);定制排序，由Comparator控制排序逻辑

void swap(List list, int i , int j),交换两个索引位置的元素

void rotate(List list, int distance),旋转。当distance为正数时，将list后distance个元素整体移到前面。当distance为负数时，将 list的前distance个元素整体移到后面。

## 查找，替换操作
int binarySearch(List list, Object key), 对List进行二分查找，返回索引，注意List必须是有序的

int max(Collection coll),根据元素的自然顺序，返回最大的元素。 类比int min(Collection coll)

int max(Collection coll, Comparator c)，根据定制排序，返回最大元素，排序规则由Comparatator类控制。类比int min(Collection coll, Comparator c)

void fill(List list, Object obj),用元素obj填充list中所有元素

int frequency(Collection c, Object o)，统计元素出现次数

int indexOfSubList(List list, List target), 统计targe在list中第一次出现的索引，找不到则返回-1，类比int lastIndexOfSubList(List source, list target).

boolean replaceAll(List list, Object oldVal, Object newVal), 用新元素替换旧元素。

## 同步控制
Collections中几乎对每个集合都定义了同步控制方法，例如 SynchronizedList(), SynchronizedSet()等方法，来将集合包装成线程安全的集合。

## 设置不可变（只读）集合

Collections提供了三类方法返回一个不可变集合，

emptyXXX(),返回一个空的只读集合（这不知用意何在？）

singleXXX()，返回一个只包含指定对象，只有一个元素，只读的集合。

unmodifiablleXXX()，返回指定集合对象的只读视图。
