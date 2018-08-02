---
layout: post
category: C语言
title: string、char*和int转换
---

对于string与int的转换, 刷题用stoi(string)函数和to_string(int)函数

对于char数组和int的转换，刷题用sscanf和sprintf函数

char数组可以直接赋值给string, string转换为char数组需要借助strcpy()函数和string.c_str()函数

```c++
#include<iostream>
#include<string>
#include<cstring>
using namespace std;
int main() {
	string a = "feafhh";
	char p[100];//这里必须为数组，不能是*p
	strcpy(p, a.c_str());
	printf("%s", p);
	cout << strlen(p) << endl;
	string b = p;
	cout << b << endl;
	string c(p);
	cout << c << endl;
}
```