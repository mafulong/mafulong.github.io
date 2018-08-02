---
layout: post
category: leetcode
title: leetcodeAC
---

## 单词整理
```
exclusive 唯一性的
convention 约定

```

## 题目集
Array easy:

![](https://i.imgur.com/R6xw2wg.png)

1	Two Sum    返回一个数组里两个数为target的对应两个数的索引，用哈希表

26  Remove Duplicates from Sorted Array    	返回一个有序数组不冗余的元素，两个指针。注意破坏原来数组没有关系

27	Remove Element    删除一个元素，不能用其他内容，方法1是两个指针，方法二是交换，返回新的长度

35  Search Insert Position  给个有序数组，找插入位置，就是二分法的改造嘛，到最后就是right-value-left的模式，然后返回的直接就是left了

53	Maximum Subarray        最大连续子序列和，注意为-1时，要返回—1，所以要sum=nums[0]

66  Plus One    大整数运算，就是一个int数组加1后，模拟大整数加1

88  Merge Sorted Array  将两个有序数组归并到第一个数组里，和归并排序的两个数组归并是不太一样的，归并排序的有序数组归并是两个归并到一个数组里。这个是不需要第三个数组的，所以两个指针的思想还是特别有用的。要注意当第二个数组的所有元素都小的时候，是需要把第二数组加进来的，当第一个数组小的时候就没关系啦，因为本来位置就是对的。

118	 Pascal's Triangle     就是构造这个数组嘛，注意构建vector的方式哈   

119  Pascal's Triangle II   就是二项式那个表，其实吧，可以用二项式定理做的，这个要再看下

121	 Best Time to Buy and Sell Stock        题目大意：给一个数组，表示每天的物品价格，你要做的就是选一天买这个物品，再之后找一天卖这个物品，计算这个最大利润

122	 Best Time to Buy and Sell Stock II    题目大意： 数组是每天的价格，买一个卖一个，计算最大收益，可以多次买卖。第一个是峰谷峰值法，找个波谷，找个波峰来计算。第二种就是不管波峰波谷了

167	 Two Sum II - Input array is sorted    问题大意： 对于一个有序数组找到两个位置索引，对应的两个数字和为target.有序嘛，就可以用二分法了。

169	 Majority Element    找出现次数超过n/2的数字，因此就是找第n/2大的数字嘛，因为超过n/2了，肯定是有序的中间的那个位置有这个数字呀！！！利用快速排序O(n)找第k个数字的方法，找第n/2个，不过看leetcode的Solution的解放还是挺多的，记得一会得去看下！！

189	 Rotate Array    题目大意，把数组循环右移k个

217  Contains Duplicate    判断数组元素是否有冗余，就是有重复的，可以用hash表也可以排序后比较相邻两个元素是否相同

219  Contains Duplicate II   判断是否冗余，这个冗余是相邻索引差小于等于K的。首先想到了hash表嘛。第一次写的ac。不是最优的，用undered_set做的，但做的代码太多了，zz,第一次写的。hashmap其实这种最好用hashmap,一旦出现啥要求的话，比如索引呀

268	 Missing Number    题目大意: 就是一个数组找缺失的那个数。首先想到可以用set，要hash的，其次也可以用总和减去每个数字，那差不就是嘛！但可能溢出，可以用Longlong，看int也能ac的。看solution还可以用异或的，就是^操作符，所有数组元素和数组size异或结果就是所求结果

283	 Move Zeroes  题目意思就是把一个数组的非零元素移动到左边，零都移动到右边。第一个方法用另一个vector存储非零元素，再放和原vector零元素相同数量的0。第二个方法就是用指针的思想，in-place    

414	 Third Maximum Number    维护一个有序堆，3个大小，用set就好了这个不就是有序的嘛！！！

448	 Find All Numbers Disappeared in an Array    	题目大意：找失去的数字，两个  用的hashset，可以用O(1)的内存的，这个我没细看，有时间去看下！！

485	 Max Consecutive Ones    