---
layout: post
category: PAT
title: 1015 Reversible Primes (20)
tags: PAT
---

## title
[problem link](https://pintia.cn/problem-sets/994805342720868352/problems/994805495863296000)

A reversible prime in any number system is a prime whose "reverse" in that number system is also a prime. For example in the decimal system 73 is a reversible prime because its reverse 37 is also a prime.

Now given any two positive integers N (< 10^5^) and D (1 < D <= 10), you are supposed to tell if N is a reversible prime with radix D.

Input Specification:

The input file consists of several test cases. Each case occupies a line which contains two integers N and D. The input is finished by a negative N.

Output Specification:

For each test case, print in one line "Yes" if N is a reversible prime with radix D, or "No" if not.
	
	Sample Input:
	
	73 10
	23 2
	23 10
	-2
	Sample Output:
	
	Yes
	Yes
	No

## solution
题目大意：判断是否反素数，即：本身是素数，在D进制下的reverser数还是素数

注意以下几点：

1. 判断素数，记得<=1的都是非素数返回false
2. 看题啊！！！

```c++
#include<iostream>
#include<string>
#include<stdio.h>
using namespace std;
bool isPrime2(long long);
bool isPrime(long long a, int radix) {
	string s = "";
	while (a > 0) {
		s += (a%radix+'0');
		a /= radix;
	}
	long long b = 0;
	for (int i = 0; i < s.length(); i++) {
		b = b * radix + (s[i] - '0');
	}
	//cout << "--------" << a<<" --- "<<b << endl;
	return isPrime2(b);
}
bool isPrime2(long long n) {
	if (n <= 1)
		return false;
	for (int i = 2; i*i <= n; i++) {
		if (n%i == 0) {
			return false;
		}
	}
	return true;
}
int main() {
	long long a;
	int radix;
	while (scanf(" %lld", &a)==1&&a>0) {
		scanf(" %d", &radix);
		if (isPrime2(a)&&isPrime(a, radix)) {
			cout << "Yes" << endl;
		}
		else {
			cout << "No" << endl;
		}
	}
}

```