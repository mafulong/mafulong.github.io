---
layout: post
category: C
title: istringstream和ostringstream
---

头文件sstream

当使用getline()函数获取一行的字符串按空格分开时就可以用istringstream>>string了

也可以用于类型转换，>>int就好

```c++
#include<sstream>
#include<iostream>
using namespace std;

int main() {
	istringstream istr;
	istr.str("mafulong wahh");
	string a;
	istr >> a;
	cout << a << endl;;
	istr >> a;
	cout << a;
	istr >> a;
	
	return 0;
}
```