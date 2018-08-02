---
layout: post
category: 算法知识
title: 图之Floyd-Warshall
---


## Floyd-Warshall

求多源、无负权边的最短路。用矩阵记录图。时效性较差，时间复杂度O(V^3)。

Floyd-Warshall算法（Floyd-Warshall algorithm）是解决任意两点间的最短路径的一种算法，可以正确处理有向图或负权的最短路径问题。

Floyd-Warshall算法的时间复杂度为O(N^3)，空间复杂度为O(N^2)。

```c++
template <class T>
void ShortestPathFloyd(Graph<T> G, PathMatrix &Path, DistanceMatrix& A)
{
    int n = G.NumberOfVertices();
    int i, j, k, t;
    T u, v, w;
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)  {
             A[i][j] = Edge[i][j];
             if (i <> j && A[i][j] < MAXINT)  Path[i][j] = i;	 
             else Path[i][j] = 0;	
        }
    for (k = 0; k < n; k++)
        for (i = 0; i < n; i++)
            for (j = 0; j < n; j++)
                if (A[i][k] + A[k][j] < A[i][j])  {
                    A[i][j] = A[i][k] + A[k][j];
                    Path[i][j] = Path[k][j];
                } 
}
```