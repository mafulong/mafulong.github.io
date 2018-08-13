---
layout: post
category: offer
title: insertion-sort-list
---

## title
[problem link](https://www.nowcoder.com/practice/152bc6c5b14149e49bf5d8c46f53152b?tpId=46&tqId=29034&rp=1&ru=/ta/leetcode&qru=/ta/leetcode/question-ranking)


Sort a linked list using insertion sort.

对链表插入排序

## solution


```java

/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) {
 *         val = x;
 *         next = null;
 *     }
 * }
 */
public class Solution {
    void insert(ListNode head,ListNode node){
        ListNode pre=head,p=head.next;
        while (p!=null&&p.val<node.val){
            pre=pre.next;
            p=p.next;
        }
        node.next=p;
        pre.next=node;
    }
    public ListNode insertionSortList(ListNode head) {
        ListNode newhead=new ListNode(Integer.MIN_VALUE);
        newhead.next=head;
        ListNode p=head,pre=newhead;
        while (p!=null){
            if(pre.val>p.val){
                pre.next=p.next;
                p.next=null;
                insert(newhead,p);
                p=pre.next;
                
            }else{
                pre=pre.next;
                p=p.next;
            }

        }
        return newhead.next;
    }
}
```