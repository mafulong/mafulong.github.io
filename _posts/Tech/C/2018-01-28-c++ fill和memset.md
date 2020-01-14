---
layout: post
category: C
title: fill和memset
tags: C
---

## fill函数

在头文件<algorithm>里面

fill(arr, arr + n, 要填入的内容);

array:

    #include <cstdio>
    #include <algorithm>
    using namespace std;
    int main() {
        int arr[10];
        fill(arr, arr + 10, 2);
        return 0;
    }

//二维数组fill
	int e[510][510]
    fill(e[0], e[0] + 510 * 510, inf);

vector:

    #include <algorithm>
    #include <vector>
    #include <iostream>
    using namespace std;
    int main(){
        vector<int> v{0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
        fill(v.begin(), v.end(), -1);
        return 0;
    }

## memset函数

因为memset函数按照字节填充，所以一般memset只能用来填充char型数组，（因为只有char型占一个字节）如果填充int型数组，除了0和-1，其他的不能。因为只有00000000 = 0，-1同理，如果我们把每一位都填充“1”，会导致变成填充入“11111111”

    #include <iostream>
    #include <cstring>
    using namespace std;
    int main(){
        int a[20];
        memset(a, 0, sizeof a);
        return 0;
    }