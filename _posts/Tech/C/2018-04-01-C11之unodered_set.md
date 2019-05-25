---
layout: post
category: C
title: C++11之unordered_set介绍
---

C++ 11中出现了两种新的关联容器:unordered_set和unordered_map，其内部实现与set和map大有不同，set和map内部实现是基于RB-Tree，而unordered_set和unordered_map内部实现是基于哈希表(hashtable)，由于unordered_set和unordered_map内部实现的公共接口大致相同，所以本文以unordered_set为例。

包含头文件```#include<undered_set>```

undered_set采用链地址法解决冲突，也叫做拉链法，和java的hashmap类似，虽然无序，但也拥有集合最大特点：不允许重复

C++标准库已经提供了基本数据类型的hash函数

因此，对于自定义类型，我们需要自定义比较函数。这里有两种方法:重载==操作符和使用函数对象

## 举例

```c++
// unordered_set::find  
#include <iostream>  
#include <string>  
#include <unordered_set>  
  
int main ()  
{  
  std::unordered_set<std::string> myset = { "red","green","blue" };  
  
  std::string input;  
  std::cout << "color? ";  
  getline (std::cin,input);  
  
  std::unordered_set<std::string>::const_iterator got = myset.find (input);  
  
  if ( got == myset.end() )  
    std::cout << "not found in myset";  
  else  
    std::cout << *got << " is in myset";  
  
  std::cout << std::endl;  
  
  return 0;  
}  
```

```c++
#include<iostream>
#include<string>
#include<algorithm>
#include<unordered_set>
using namespace std;
int main()
{
	unordered_set<int> hs;
	hs.insert(3);
	hs.insert(4);
	hs.insert(3);
	for (auto e : hs) {
		cout << e << endl;
	}
	if (hs.find(4) != hs.end()) {
		cout << "hhh" << endl;
	}
	cout << hs.size() << endl;
	hs.erase(3);
	cout << hs.size() << endl;
	return 0;
}

```


```c++
bool containsNearbyDuplicate(vector<int>& nums, int k) {
    
    unordered_map<int,int> nmap;
    for (int i = 0; i <nums.size();i++)
    {
        if (nmap.count(nums[i]) == 0)
            nmap[nums[i]] = i;
        else if (i - nmap[nums[i]] <=k)
            return true;
        else
            nmap[nums[i]] = i;
    }
    
    return false;
    
}
```

```c++
class Solution {
public:
	int findPairs(vector<int>& nums, int k) {
		int ans = 0;
		if (k < 0) return 0;
		unordered_map<int, int> umap;
		for (int n : nums) {
			umap[n]++;
		}
		for (auto p : umap) {
			if ((!k&&p.second > 1) || (k&&umap.count(p.first + k))) {
				ans++;
			}
		}
		return ans;
	}
};
```

```c++
class Solution {
public:
	int thirdMax(vector<int>& nums) {
		set<int,less<int>> s;
		for (int i = 0; i < nums.size(); i++) {
			s.insert(nums[i]);
			if (s.size() > 3) {
				s.erase(s.begin());
			}
		}
		if (s.size() == 3)
			return *s.begin();
		else
			return *s.rbegin();
	}
};
```