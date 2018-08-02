---
layout: post
category: JAVA
title: RandomAccess接口
---

## 介绍
根据javadoc上面的的解释是：

RandomAccess 是一个标记接口，用于标明实现该接口的List支持快速随机访问，主要目的是使算法能够在随机和顺序访问的list中表现的更加高效。

我们可以简单的看下Collections下的binarySearch方法的源码:

```java
public static <T>  
    int binarySearch(List<? extends Comparable<? super T>> list, T key) {  
        if (list instanceof RandomAccess || list.size()<BINARYSEARCH_THRESHOLD)  
            return Collections.indexedBinarySearch(list, key);  
        else  
            return Collections.iteratorBinarySearch(list, key);  
    }  
```

从源码中我们可以看到，在进行二分查找的时候，list会先判断是否是RandomAccess也即是否实现了RandomAccess接口，接着在调用想用的二分查找算法来进行，（其中: BINARYSEARCH_THRESHOLD Collections的一个常量（5000），它是二分查找的阀值。）如果实现了RandomAccess接口的List，执行indexedBinarySearch方法，否则执行 iteratorBinarySearch方法。

分别看下这两个方法的实现:

indexedBinarySearch 方法:

```java
private static <T>  
    int indexedBinarySearch(List<? extends Comparable<? super T>> list, T key) {  
        int low = 0;  
        int high = list.size()-1;  
  
        while (low <= high) {  
            int mid = (low + high) >>> 1;  
            Comparable<? super T> midVal = list.get(mid);  
            int cmp = midVal.compareTo(key);  
  
            if (cmp < 0)  
                low = mid + 1;  
            else if (cmp > 0)  
                high = mid - 1;  
            else  
                return mid; // key found  
        }  
        return -(low + 1);  // key not found  
    }  
```


indexedBinarySearch 方法是直接通过get来访问元素


iteratorBinarySearch方法:

```java
private static <T>  
    int iteratorBinarySearch(List<? extends Comparable<? super T>> list, T key)  
    {  
        int low = 0;  
        int high = list.size()-1;  
        ListIterator<? extends Comparable<? super T>> i = list.listIterator();  
  
        while (low <= high) {  
            int mid = (low + high) >>> 1;  
            Comparable<? super T> midVal = get(i, mid);  
            int cmp = midVal.compareTo(key);  
  
            if (cmp < 0)  
                low = mid + 1;  
            else if (cmp > 0)  
                high = mid - 1;  
            else  
                return mid; // key found  
        }  
        return -(low + 1);  // key not found  
    }  
```

iteratorBinarySearch中ListIterator来查找相应的元素

## 总结
实现RandomAccess接口的的List可以通过简单的for循环来访问数据比使用iterator访问来的高效快速。