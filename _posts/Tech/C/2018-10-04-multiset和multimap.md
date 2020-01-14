---
layout: post
category: C
title: multiset和multimap
tags: C
---

和set,map一样都是红黑树的，从小到大排序。

可以多值插入的，就是multiset和multimap了

```c++
vector<int> advantageCount(vector<int>& A, vector<int>& B) {
  multiset<int> s(begin(A), end(A));
  for (auto i = 0; i < B.size(); ++i) {
    auto p = *s.rbegin() <= B[i] ? s.begin() : s.upper_bound(B[i]);
    A[i] = *p;
    s.erase(p);
  }
  return A;
}
```

