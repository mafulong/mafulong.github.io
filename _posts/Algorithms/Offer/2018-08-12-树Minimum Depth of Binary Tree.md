---
layout: post
category: offer
title: 树Minimum Depth of Binary Tree
---

## title
[problem link](https://www.nowcoder.com/practice/e08819cfdeb34985a8de9c4e6562e724?tpId=46&tqId=29030&tPage=1&rp=1&ru=/ta/leetcode&qru=/ta/leetcode/question-ranking)

Given a binary tree, find its minimum depth.The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.

## solution

思路：

- 递归，若为空树返回0；
- 若左子树为空，则返回右子树的最小深度+1；（加1是因为要加上根这一层，下同）
- 若右子树为空，则返回左子树的最小深度+1；
- 若左右子树均不为空，则取左、右子树最小深度的较小值，+1；

```java
/**
 * Definition for binary tree
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */

public class Solution {
    int depth(TreeNode root){
        if(root==null){
            return 0;
        }
        if(root.left==null)
            return depth(root.right)+1;
        else if(root.right==null)
            return depth(root.left)+1;
        else{
            int left=depth(root.left);
            int right=depth(root.right);
       //     return left<right?left+1:right+1;
            return Math.min(left,right)+1;
        }
    }
    public int run(TreeNode root) {
        return depth(root);
    }
}

```