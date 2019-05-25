---
layout: post
category: Java
title: Arrays工具类
---

java.util.Arrays类：常用方法如下

```java
public static:
    int binarySearch(Object[] a,Object key); 
    void fill(int[] a,int val);
    void sort(Object[] a);
```

## equals比较
对比两个数组是否相等
```java

    @Test
    public void equals(){
        String[] array2 = new String[]{"a","c","2","1","b"};

        //1 对比引用是否相同
        //2 对比是否存在null
        //3 对比长度是否相同
        //4 挨个元素对比
        System.out.println(Arrays.equals(array,array2));
    }
```

## fill
基于目标元素填充数组
```java

    @Test
    public void fill(){
        Arrays.fill(array,"test");
        System.out.println(Arrays.deepToString(array));//[test, test, test, test, test]
    }
```

## toString
打印数组元素
```java

    @Test
    public void string(){
        System.out.println(Arrays.toString(array));//[a, c, 2, 1, b]
    }
```

## copyOf
拷贝数组，第一种用法，如果目标长度不够，会使用0进行补位。第二种用法，支持拷贝目标起始位置到结束为止的数组。
```java

    @Test
    public void copyOf(){
        //如果位数不够，需要补位
        Integer[] result = Arrays.copyOf(ints,10);
        for(int i : result){
            System.out.println(i);
        }
        System.out.println("----------------------------------------->");
        //如果位数够，就取最小的数组
        result = Arrays.copyOf(ints,3);
        for(int i : result){
            System.out.println(i);
        }
        System.out.println("----------------------------------------->");
        //
        result = Arrays.copyOfRange(ints,2,4);
        for(int i : result){
            System.out.println(i);
        }
    }
```

## binarySearch
查找目标元素所在的位置，注意需要先进行排序。
```java

    @Test
    public void binarySearch(){
        //binarySearch需要保证是排好序的
        System.out.println(Arrays.binarySearch(array,"c"));//-6
        Arrays.sort(array);
        System.out.println(Arrays.binarySearch(array,"c"));//4
    }
```
    
## asList
这个方法可以把数组转换成List,List提供了很多的操作方法，更便于使用。
```java

    @Test
    public void test1(){
        List<String> lists = Arrays.asList(array);
    }
```

## sort排序和parallelSort并行排序
sort比较常用了，根据元素按照自然排序规则排序，也可以设置排序元素的起始位置。
```java

    @Test
    public void sort(){
       /* Arrays.sort(array);
        for(String str : array){
            System.out.println(str);
        }*/
        Arrays.sort(array,2,5);
        System.out.println(Arrays.deepToString(array));//[a, c, 1, 2, b]
    }
```

parallelSort则采用并行的排序算法排序.但是我自己测试，可能数据量太小，速度上并没有明显的变化。