---
layout: post
category: PAT-A
title: 1009 Product of Polynomials (25)
---

## title
[problem link](https://pintia.cn/problem-sets/994805342720868352/problems/994805509540921344)

This time, you are supposed to find A*B where A and B are two polynomials.

Input Specification:

Each input file contains one test case. Each case occupies 2 lines, and each line contains the information of a polynomial: K N1 a~N1~ N2 a~N2~ ... NK a~NK~, where K is the number of nonzero terms in the polynomial, Ni and a~Ni~ (i=1, 2, ..., K) are the exponents and coefficients, respectively. It is given that 1 <= K <= 10, 0 <= NK < ... < N2 < N1 <=1000.

Output Specification:

For each test case you should output the product of A and B in one line, with the same format as the input. Notice that there must be NO extra space at the end of each line. Please be accurate up to 1 decimal place.

	Sample Input
	
	2 1 2.4 0 3.2
	2 2 1.5 1 0.5
	Sample Output
	
	3 3 3.6 2 6.0 1 1.6

## solution


```c++

#include<stdio.h>
#include<string>
#include<iostream>
#include<unordered_map>
#include<algorithm>
#include<utility>
#include<functional>
#include<queue>
#include<sstream>
using namespace std;

#define N 2001
#define inf 99999
double a[N], b[N], ans[N];

int main() {
	int n;
	cin >> n;
	int t;
	for (int i = 0; i < n; i++) {
		scanf("%d", &t);
		scanf("%lf", &a[t]);
	}

	cin >> n;
	for (int i = 0; i < n; i++) {
		scanf("%d", &t);
		scanf("%lf", &b[t]);
		for (int j = 0; j < 1001; j++) {
			ans[t + j] += b[t] * a[j];
		}
	}
	int num = 0;
	for (int i = 2000; i >= 0; i--) {
		if (ans[i] != 0.0) {
			num++;
		}
	}
	cout << num;
	for (int i = 2000; i >= 0; i--) {
		if (ans[i] != 0.0) {
			printf(" %d %.1f", i, ans[i]);
		}
	}

	return 0;
}
```