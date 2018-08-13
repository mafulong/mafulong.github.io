---
layout: post
category: 算法知识
title: permutaion
---

## 前言
C++中有permutaion的函数[the link](http://mafulong.top/c%E8%AF%AD%E8%A8%80/2018/01/28/c++-next_permutation.html)

那个也可以begin(vector)的哈哈哈

关于permutation取下一个要参考[the link](http://mafulong.top/leetcode/2018/05/08/leetcode31.html)

至于自己实现permutaion的完整代码，如下

## Problem
Given a collection of numbers, return all possible permutations.
For example,

[1,2,3] have the following permutations:

[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], and [3,2,1].

有一些例子的[the link](https://leetcode.com/problems/permutations/)

## Recursive Solution
DFS解法

Basic idea: permutation of A[1..n] equals to

A[1] + permutation of (A[1..n] - A[1])

A[2] + permutation of (A[1..n] - A[2])

...

A[n] + permutation of (A[1..n] - A[n]).

```c++
class Solution {
public:
    vector<vector<int> > permute(vector<int> &num) {
        vector<vector<int> > result;
 
        permuteRecursive(num, 0, result);
        return result;
    }
 
    // permute num[begin..end]
    // invariant: num[0..begin-1] have been fixed/permuted
    void permuteRecursive(vector<int> &num, int begin, vector<vector<int> > &result)    {
        if (begin >= num.size()) {
            // one permutation instance
            result.push_back(num);
            return;
        }
 
        for (int i = begin; i < num.size(); i++) {
            swap(num[begin], num[i]);
            permuteRecursive(num, begin + 1, result);
            // reset
            swap(num[begin], num[i]);
        }
    }
};
```

## permutation 2
对于有重复的就是duplicate的数组，permutation时

注意有duplicate的是不同通过swap() 而 reset的，因为，比较的是与Pos位置，还会重复，只能值传递到下一个解，不要reset

[the problem link](https://leetcode.com/problems/permutations-ii/description/)

需要加一步

[参考](https://leetcode.com/problems/permutations-ii/discuss/18613/13-lines-C++-backtracking)

Solution for Permutations II is similar to Permutations I, the only difference is that we CAN'T swap back after each permutation, cause we want to pick a new different number for position i in each loop.

For example, suppose array nums = [1, 1, 2, 2, 3], first we swap nums[0] = 1 with the first different number nums[2] = 2, after first swap, nums = [2, 1, 1, 2, 3], then if we swap back 1 with 2, nums = [1, 1, 2, 2, 3].

Now, we want to pick nums[4] = 3 as a new number for position 0, but nums[3] = 2 would be considered the new different number because we swaped the number '1' back to position 0, so we will swap nums[0] with nums[3], nums = [2, 1, 2, 1, 3], so the same number '2' appears twice at position 0, which caused the repeated outcomes.

```c++
class Solution {
public:
    vector<vector<int>> permuteUnique(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        vector<vector<int>>res;
        DFS(res, nums, 0);
        return res;
   }
    
    void DFS(vector<vector<int>>& res, vector<int> nums, int pos){
        if(pos == nums.size() - 1){
            res.push_back(nums);
            return;
        }
        for(int i = pos; i < nums.size(); i++){
            if(i != pos && nums[i] == nums[pos]) continue;
            swap(nums[pos], nums[i]);
            DFS(res, nums, pos + 1);
        }
    }
};
```

类似的牛客网题目[link](https://www.nowcoder.com/practice/fe6b651b66ae47d7acce78ffdd9a96c7?tpId=13&tqId=11180&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking)

```c++
class Solution {
public:
    void f(vector<string> &res,string s,int begin){
        if(begin==s.length()-1){
            res.push_back(s);
            return ;
        }
        for(int i=begin;i<s.length();i++){
            if(i!=begin&&s[i]==s[begin]) continue;
            swap(s[begin],s[i]);
            f(res,s,begin+1);
            //swap(s[begin],s[i]);
        }
    }
    vector<string> Permutation(string str) {
        sort(str.begin(),str.end());
        vector<string> res;
        if(str.length()==0)
            return res;
        f(res,str,0);
        return res;
    }
};
```

## 下一个排列

[参考链接](http://mafulong.top/leetcode/2018/05/08/leetcode31.html)

My idea is for an array:

Start from its last element, traverse backward to find the first one with index i that satisfy num[i-1] < num[i]. So, elements from num[i] to num[n-1] is reversely sorted.

To find the next permutation, we have to swap some numbers at different positions, to minimize the increased amount, we have to make the highest changed position as high as possible. Notice that index larger than or equal to i is not possible as num[i,n-1] is reversely sorted. So, we want to increase the number at index i-1, clearly, swap it with the smallest number between num[i,n-1] that is larger than num[i-1]. For example, original number is 121543321, we want to swap the ‘1’ at position 2 with ‘2’ at position 7.

The last step is to make the remaining higher position part as small as possible, we just have to reversely sort the num[i,n-1]

```c++
class Solution {
public:
	void nextPermutation(vector<int>& nums) {
		int n = nums.size();
		int k = n - 1;
		while (k > 0 && nums[k] <= nums[k - 1]) {
			k--;
		}
		if (k == 0) {
			reverse(nums.begin(), nums.end());
			return;
		}
		k--;
		int index,t = INT_MAX;
		for (int i = k + 1; i < n; i++) {
			if (nums[i] > nums[k]) {
				if (nums[i] < t) {
					t = nums[i];
					index = i;
				}
			}
		}
		swap(nums[k], nums[index]);
		reverse(nums.begin() + index, nums.end());
	}
};
```