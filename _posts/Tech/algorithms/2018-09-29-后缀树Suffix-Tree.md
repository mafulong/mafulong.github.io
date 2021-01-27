---
layout: post
category: Algorithms
title: 后缀树Suffix-Tree
tags: Algorithms
---

[参考1](https://blog.csdn.net/u013949069/article/details/78056102)

[参考2](https://blog.csdn.net/v_july_v/article/details/6897097)

#### 简介

后缀树，它描述了给定字符串的所有后缀，许多重要的字符串操作都能够在后缀树上快速地实现。

一个长度为n的字符串S，它的后缀树定义为一棵满足如下条件的树：

1. 从根到树叶的路径与S的后缀一一对应。即每条路径惟一代表了S的一个后缀；
2. 每条边都代表一个非空的字符串；
3. 所有内部节点（根节点除外）都有至少两个子节点。

由于并非所有的字符串都存在这样的树，因此S通常使用一个终止符号进行填充（通常使用$）。

![](https://cdn.jsdelivr.net/gh/mafulong/mdPic@master/images/cbc0942c49766bad09ba134b41e81295.gif)

#### 优点
匹配快。对于长度为m的模式串，只需花费至多O(m)的时间进行匹配。

空间省。Suffix tree的空间耗费要低于Suffix trie，因为Suffix tree除根节点外不允许其内部节点只含单个子节点，因此它是Suffix trie的压缩表示。

![](https://cdn.jsdelivr.net/gh/mafulong/mdPic@master/images/7a75afe1c22113474dc0cf803ae94d71.gif)

![](https://cdn.jsdelivr.net/gh/mafulong/mdPic@master/images/dda895e1efbf5f4cca68f520d6b6a263.gif)

![](https://cdn.jsdelivr.net/gh/mafulong/mdPic@master/images/5a5d8cc3d02d8e1e11b7bb793c0d105d.jpeg)



#### 应用

后缀树（Suffix tree）是一种树形数据结构，能快速解决很多关于字符串的问题。后缀樹的概念最早由Weiner 於1973年提出，既而由McCreight 在1976年和Ukkonen在1992年和1995年加以改進完善。

总结起来，它主要可以解决类似如下的一些问题：

- 查找字符串o是否在字符串S中
- 指定字符串T在字符串S中的重复次数
- 字符串S中的最长重复子串
- 两个字符串S1，S2的最长公共部分

这些问题如何解决，我们最后再谈。


查找字符串o是否在字符串S中  
解法：如果S存在于o中，那么S必然是o的某一个后缀的前缀，按照Trie树搜索前缀的方法，遍历后缀树即可。复杂度为O(M)，其中M为字符串S的长度。
原理：若o在S中，则o必然是S的某个后缀的前缀。 
例如S: leconte，查找o: con是否在S中,则o(con)必然是S(leconte)的后缀之一conte的前缀.有了这个前提，采用trie搜索的方法就不难理解了。

指定字符串T在字符串S中的重复次数  
解法：在字符串S后追加$构造包含所有后缀的完整后缀树，在其中找到T子川，的最后一个节点，该节点拥有的叶子节点个数几位重复次数，复杂度为O(M)，M为T的长度。
原理：如果T在S中重复了两次，则S应有两个后缀以T为前缀，重复次数就自然统计出来了。

字符串S中的最长重复子串  
解法：遍历整个后缀树，找到深度最大的非叶子节点，复杂度为O(N)，N为字符串的长度。
这个深是指从root所经历过的字符个数，最深非叶节点所经历的字符串起来就是最长重复子串。 
为什么要非叶节点呢?因为既然是要重复，当然叶节点个数要>=2。 

两个字符串S1，S2的最长公共部分  
解法：分别 为S1、S2追加#、$作为末尾，把他们压入同一个后缀树，然后找到最深的非叶子节点，该节点的叶子节点中，既有#又有$。复杂度为构造两颗后缀树的复杂度之和，取最大即可max(O(N),O(M))，其中N、M为S1、S2的长度，假设我们以线性时间构造了后缀树，下位讲解构造方法。
方案：将S1#S2$作为字符串压入后缀树，找到最深的非叶节点，且该节点的叶节点既有#也有$(无#)。 

#### 后缀树的构造方法-Ukkonen
