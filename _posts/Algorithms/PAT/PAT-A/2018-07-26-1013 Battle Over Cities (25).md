---
layout: post
category: PAT
title: 1013 Battle Over Cities (25)
tags: PAT
---

## title
[problem link](https://pintia.cn/problem-sets/994805342720868352/problems/994805500414115840)

It is vitally important to have all the cities connected by highways in a war. If a city is occupied by the enemy, all the highways from/toward that city are closed. We must know immediately if we need to repair any other highways to keep the rest of the cities connected. Given the map of cities which have all the remaining highways marked, you are supposed to tell the number of highways need to be repaired, quickly.

For example, if we have 3 cities and 2 highways connecting city~1~-city~2~ and city~1~-city~3~. Then if city~1~ is occupied by the enemy, we must have 1 highway repaired, that is the highway city~2~-city~3~.

Input

Each input file contains one test case. Each case starts with a line containing 3 numbers N (&lt1000), M and K, which are the total number of cities, the number of remaining highways, and the number of cities to be checked, respectively. Then M lines follow, each describes a highway by 2 integers, which are the numbers of the cities the highway connects. The cities are numbered from 1 to N. Finally there is a line containing K numbers, which represent the cities we concern.

Output

For each of the K cities, output in a line the number of highways need to be repaired if that city is lost.

	Sample Input
	
	3 2 3
	1 2
	1 3
	1 2 3
	Sample Output
	
	1
	0
	0

## solution

dfs
```c++

#include <cstdio>
#include <algorithm>
using namespace std;
int v[1010][1010];
bool visit[1010];
int n;
void dfs(int node) {
    visit[node] = true;
    for(int i = 1; i <= n; i++) {
        if(visit[i] == false && v[node][i] == 1)
            dfs(i);
    }
}
int main() {
    int m, k, a, b;
    scanf("%d%d%d", &n, &m, &k);
    for(int i = 0; i < m; i++) {
        scanf("%d%d", &a, &b);
        v[a][b] = v[b][a] = 1;
    }
    for(int i = 0; i < k; i++) {
        fill(visit, visit + 1010, false);
        scanf("%d", &a);
        int cnt = 0;
        visit[a] = true;
        for(int j = 1; j <= n; j++) {
            if(visit[j] == false) {
                dfs(j);
                cnt++;
            }
        }
        printf("%d\n", cnt - 1);
    }
    return 0;
}
```

并查集 超时
```c++
#include<map>
#include<queue>
#include<cmath>
#include<stack>
#include<cstdio>
#include<vector>
#include<cstring>
#include<iostream>
#include<algorithm>
using namespace std;
typedef long long LL;
#define INF 0x3f3f3f3f
#define CLR(a,b) memset(a,b,sizeof(a))
#define PI acos(-1.0)
#define fi first
#define se second
vector<pair<int, int> > edge;
int f[1005];
int n, m;
int find(int x)
{

	//以下实现查找根节点
	int r = x;
	while (r != f[r])
		r = f[r];

	//以下代码用来实现路径压缩
	int i = x, j;
	while (f[i] != r)
	{
		j = f[i];
		f[i] = r;
		i = j;
	}
	return r;

}
void join(int x, int y)
{
	int fx, fy;
	fx = find(x);
	fy = find(y);
	if (fx != fy)
		f[fx] = fy;
}
void solve(int p)
{
	for (int i = 1; i <= n; i++)      //记得初始化 
		f[i] = i;
	for (int i = 0; i < edge.size(); i++)
	{
		if (edge[i].first == p || edge[i].second == p)
			continue;
		join(edge[i].first, edge[i].second);
	}
	int cnt = 0;
	bool vis[1005] = { false };
	for (int i = 1; i <= n; i++)
	{
		if (i == p)
			continue;
		int fx = find(i);
		if (!vis[fx])
		{
			vis[fx] = true;
			cnt++;
		}
	}
	cout << cnt - 1 << endl;
}
int main()
{
	int k;
	cin >> n >> m >> k;
	edge.resize(m);
	for (int i = 0; i < m; i++)
	{
		int x, y;
		cin >> x >> y;
		edge[i] = make_pair(x, y);
	}
	for (int i = 1; i <= k; i++)
	{
		int q;
		cin >> q;
		solve(q);
	}
	return 0;
}
```