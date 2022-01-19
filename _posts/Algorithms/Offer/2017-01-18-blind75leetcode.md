---
layout: post
category: Offer
title: blind75leetcode
tags: Offer
---

## bind75leetcode


## Array

- [x] [Two Sum](https://leetcode-cn.com/problems/two-sum/) 哈希表
- [x] [Best Time to Buy and Sell Stock](https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock/)
- [x] [Contains Duplicate](https://leetcode-cn.com/problems/contains-duplicate/)  哈希表
- [x] [Product of Array Except Self](https://leetcode-cn.com/problems/product-of-array-except-self/) 可以ans算左边的，然后维护变量R不断乘以右边的。
- [x] [Maximum Subarray](https://leetcode-cn.com/problems/maximum-subarray/)
- [x] [Maximum Product Subarray](https://leetcode-cn.com/problems/maximum-product-subarray/)  两个变量维护当前结尾最大的和最小的
- [x] [Find Minimum in Rotated Sorted Array](https://leetcode-cn.com/problems/find-minimum-in-rotated-sorted-array/) 如果有相等情况，当`a[mid] == a[right]`, `right-=1`
- [x] [Search in Rotated Sorted Array](https://leetcode-cn.com/problems/search-in-rotated-sorted-array/) 当左右中间都相等时， `left+=1, right-=1`
- [x] [3Sum](https://leetcode-cn.com/problems/3sum/) 排序+双指针
- [x] [Container With Most Water](https://leetcode-cn.com/problems/container-with-most-water/) 多个柱子，统计最多能接多少水，双指针，不断缩小两边矮的那个

---

## Binary

- [x] [Sum of Two Integers](https://leetcode-cn.com/problems/sum-of-two-integers/) 不用+做加法，记得python的负数处理，要取负数的补码，需要&0xffffffff。 负数的补码还原到python的负数，如-2， 需要&下0xffffffff,然后取反加一，外面再加个负号。
- [x] [Number of 1 Bits](https://leetcode-cn.com/problems/number-of-1-bits/)
- [x] [Counting Bits](https://leetcode-cn.com/problems/counting-bits/) 统计1-n里每个数字1的个数，动态规划，最低设置位。
- [x] [Missing Number](https://leetcode-cn.com/problems/missing-number/) 异或
- [x] [Reverse Bits](https://leetcode-cn.com/problems/reverse-bits/) 反转位，一个新值，不断从右边增加然后左移

---

## Dynamic Programming

- [x] [Climbing Stairs](https://leetcode-cn.com/problems/climbing-stairs/)
- [x] [Coin Change](https://leetcode-cn.com/problems/coin-change/)
- [x] [Longest Increasing Subsequence](https://leetcode-cn.com/problems/longest-increasing-subsequence/)
- [x] [Longest Common Subsequence](https://leetcode-cn.com/problems/longest-common-subsequence/)
- [x] [Word Break Problem](https://leetcode-cn.com/problems/word-break/)
- [x] [Combination Sum](https://leetcode-cn.com/problems/combination-sum-iv/) 给你一个由 **不同** 整数组成的数组 `nums` ，和一个目标整数 `target` 。请你从 `nums` 中找出并返回总和为 `target` 的元素组合的个数。
- [x] [House Robber](https://leetcode-cn.com/problems/house-robber/)
- [x] [House Robber II](https://leetcode-cn.com/problems/house-robber-ii/)
- [x] [Decode Ways](https://leetcode-cn.com/problems/decode-ways/) Z -> 26的字符串反解码可能性
- [x] [Unique Paths](https://leetcode-cn.com/problems/unique-paths/)
- [x] [Jump Game](https://leetcode-cn.com/problems/jump-game/)  贪心

---

## Graph

- [x] [Clone Graph](https://leetcode-cn.com/problems/clone-graph/)

- [x] [Course Schedule](https://leetcode-cn.com/problems/course-schedule/)

- [x] [Pacific Atlantic Water Flow](https://leetcode-cn.com/problems/pacific-atlantic-water-flow/) 太平洋大西洋水流问题

- [x] [Number of Islands](https://leetcode-cn.com/problems/number-of-islands/)

- [x] [Longest Consecutive Sequence](https://leetcode-cn.com/problems/longest-consecutive-sequence/) 找1，2，3，4这样连续，并查集map. 

- [x]  [Alien Dictionary (Leetcode Premium)](https://www.lintcode.com/problem/892/) 有一种新的使用拉丁字母的外来语言。但是，你不知道字母之间的顺序。你会从词典中收到一个**非空的**单词列表，其中的单词**在这种新语言的规则下按字典顺序排序**。请推导出这种语言的字母顺序。

  ```
  输入：["wrt","wrf","er","ett","rftt"]
  输出："wertf"
  解释：
  从 "wrt"和"wrf" ,我们可以得到 't'<'f'
  从 "wrt"和"er" ,我们可以得到'w'<'e'
  从 "er"和"ett" ,我们可以得到 get 'r'<'t'
  从 "ett"和"rftt" ,我们可以得到 'e'<'r'
  所以返回 "wertf"
  ```

  解答: 每连续两个单词可以得到字母和字母顺序，然后拓扑排序即可。

  

- [x] [Graph Valid Tree (Leetcode Premium)](https://www.lintcode.com/problem/graph-valid-tree/note/157655) 判断图是否是树，即无环。可以dfs, bfs, unionfind

- [x] [Number of Connected Components in an Undirected Graph (Leetcode Premium)](https://leetcode-cn.com/problems/number-of-connected-components-in-an-undirected-graph/) 无向图里连通数量，可以并查集。

---

## Interval

贪心的可以按end排序，否则涉及插入、合并的都是按start排序

[秒懂力扣区间题目：重叠区间、合并区间、插入区间](https://mp.weixin.qq.com/s/ioUlNa4ZToCrun3qb4y4Ow)   

[找最多不重合的数量，按end排序](https://leetcode-cn.com/problems/non-overlapping-intervals/solution/qu-jian-wen-ti-de-tan-xin-jie-fa-de-tong-hzy3/)

- [x] [Insert Interval](https://leetcode-cn.com/problems/insert-interval/)  按start排序，遇到重叠就合并,start = min(start, left), right= max(right, end)

- [x] [Merge Intervals](https://leetcode-cn.com/problems/merge-intervals/) 合并区间，按start排序

- [x] [Non-overlapping Intervals](https://leetcode-cn.com/problems/non-overlapping-intervals/)

- [x] [Meeting Rooms (Leetcode Premium)](https://leetcode-cn.com/problems/meeting-rooms/) Given an array of meeting time intervals consisting of start and end times`[[s1,e1],[s2,e2],...]`(si< ei), determine if a person could attend all meetings.

  解答: 按start排序，看有无重合区间

- [x] [Meeting Rooms II (Leetcode Premium)](https://leetcode-cn.com/problems/meeting-rooms-ii/) Given an array of meeting time intervals consisting of start and end times`[[s1,e1],[s2,e2],...]`(si< ei), find the minimum number of conference rooms required.

  可以用heap弹出，复杂度高。最佳是扫描线算法。遇到start则+1, end则-1.  [参考](https://www.jiuzhang.com/solution/meeting-rooms-ii/)

---

## Linked List

- [x] [Reverse a Linked List](https://leetcode-cn.com/problems/reverse-linked-list/)
- [x] [Detect Cycle in a Linked List](https://leetcode-cn.com/problems/linked-list-cycle/)
- [x] [Merge Two Sorted Lists](https://leetcode-cn.com/problems/merge-two-sorted-lists/)
- [x] [Merge K Sorted Lists](https://leetcode-cn.com/problems/merge-k-sorted-lists/)
- [x] [Remove Nth Node From End Of List](https://leetcode-cn.com/problems/remove-nth-node-from-end-of-list/)  分治合并 和 heap取最小合并复杂度相同
- [x] [Reorder List](https://leetcode-cn.com/problems/reorder-list/)

---

## Matrix

- [x] [Set Matrix Zeroes](https://leetcode-cn.com/problems/set-matrix-zeroes/) 有0的位置横和竖都变0，可以利用第一行和第一列来记录
- [x] [Spiral Matrix](https://leetcode-cn.com/problems/spiral-matrix/) 螺旋遍历
- [x] [Rotate Image](https://leetcode-cn.com/problems/rotate-image/)
- [x] [Word Search](https://leetcode-cn.com/problems/word-search/)

---

## String

- [x] [Longest Substring Without Repeating Characters](https://leetcode-cn.com/problems/longest-substring-without-repeating-characters/)

- [x] [Longest Repeating Character Replacement](https://leetcode-cn.com/problems/longest-repeating-character-replacement/) 给你一个仅由大写英文字母组成的字符串，你可以将任意位置上的字符替换成另外的字符，总共可最多替换 k 次。在执行上述操作后，找到包含重复字母的最长子串的长度。

  解答: 双指针

- [x] [Minimum Window Substring](https://leetcode-cn.com/problems/minimum-window-substring/) 滑动窗口

- [x] [Valid Anagram](https://leetcode-cn.com/problems/valid-anagram/) 判断 `*t*` 是否是 `*s*` 的字母异位词。 hash表

- [x] [Group Anagrams](https://leetcode-cn.com/problems/group-anagrams/) 按频次统计分组，hash表

- [x] [Valid Parentheses](https://leetcode-cn.com/problems/valid-parentheses/)

- [x] [Valid Palindrome](https://leetcode-cn.com/problems/valid-palindrome/)

- [x] [Longest Palindromic Substring](https://leetcode-cn.com/problems/longest-palindromic-substring/)

- [x] [Palindromic Substrings](https://leetcode-cn.com/problems/palindromic-substrings/)                       解答: [回文子串的数目](https://leetcode-cn.com/submissions/detail/249689602/)

- [x] [Encode and Decode Strings (Leetcode Premium)](https://www.lintcode.com/problem/encode-and-decode-strings/note/79209)

---

## Tree
- [x] [Maximum Depth of Binary Tree](https://leetcode-cn.com/problems/maximum-depth-of-binary-tree/)
- [x] [Same Tree](https://leetcode-cn.com/problems/same-tree/)
- [x] [Invert/Flip Binary Tree](https://leetcode-cn.com/problems/invert-binary-tree/)
- [x] [Binary Tree Maximum Path Sum](https://leetcode-cn.com/problems/binary-tree-maximum-path-sum/)
- [x] [Binary Tree Level Order Traversal](https://leetcode-cn.com/problems/binary-tree-level-order-traversal/)
- [x] [Serialize and Deserialize Binary Tree](https://leetcode-cn.com/problems/serialize-and-deserialize-binary-tree/)
- [x] [Subtree of Another Tree](https://leetcode-cn.com/problems/subtree-of-another-tree/)
- [x] [Construct Binary Tree from Preorder and Inorder Traversal](https://leetcode-cn.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)
- [x] [Validate Binary Search Tree](https://leetcode-cn.com/problems/validate-binary-search-tree/)
- [x] [Kth Smallest Element in a BST](https://leetcode-cn.com/problems/kth-smallest-element-in-a-bst/)
- [x] [Lowest Common Ancestor of BST](https://leetcode-cn.com/problems/lowest-common-ancestor-of-a-binary-search-tree/)
- [x] [Implement Trie (Prefix Tree)](https://leetcode-cn.com/problems/implement-trie-prefix-tree/)
- [x] [Add and Search Word](https://leetcode-cn.com/problems/add-and-search-word-data-structure-design/)
- [x] [Word Search II](https://leetcode-cn.com/problems/word-search-ii/)

---

## Heap

- [x] [Merge K Sorted Lists](https://leetcode-cn.com/problems/merge-k-sorted-lists/)
- [x] [Top K Frequent Elements](https://leetcode-cn.com/problems/top-k-frequent-elements/)
- [x] [Find Median from Data Stream](https://leetcode-cn.com/problems/find-median-from-data-stream/)

## Important Link:
[14 Patterns to Ace Any Coding Interview Question](https://hackernoon.com/14-patterns-to-ace-any-coding-interview-question-c5bb3357f6ed)
