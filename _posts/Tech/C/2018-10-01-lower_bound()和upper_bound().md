---
layout: post
category: C
title: lower_bound()和upper_bound()
tags: C
---

lower_bound()和upper_bound()

lower_bound 和 upper_bound()需要用在一个有序数组或容器中。 

lower_bound(first,last,val) 用来寻找在数组或容器的[first,last)范围内第一个值大于等于 
val元素的位置，如果是数组，返回该位置的指针；若果是容器，返回该位置的迭代器 

upper_bound(first,last,val) 用来寻找在数组或容器的[first,last)范围内第一个值大于 
val元素的位置，如果是数组，返回该位置的指针；若果是容器，返回该位置的迭代器

```c++
#include<stdio.h>
#include<string>
#include<vector>
#include<algorithm>
using namespace std;
int main()
{
    int a[10]={1,2,2,3,3,3,5,5,5,5};
    printf("%d,%d\n",lower_bound(a,a+10,3)-a,upper_bound(a,a+10,3)-a);
    return 0;
}

```