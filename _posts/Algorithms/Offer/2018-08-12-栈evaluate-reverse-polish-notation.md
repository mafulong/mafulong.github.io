---
layout: post
category: offer
title: 栈evaluate-reverse-polish-notation
---

## title
[problem link](https://www.nowcoder.com/practice/22f9d7dd89374b6c8289e44237c70447?tpId=46&tqId=29031&tPage=1&rp=1&ru=/ta/leetcode&qru=/ta/leetcode/question-ranking)

Evaluate the value of an arithmetic expression in Reverse Polish Notation.

Valid operators are+,-,*,/. Each operand may be an integer or another expression.

Some examples:

	  ["2", "1", "+", "3", "*"] -> ((2 + 1) * 3) -> 9
	  ["4", "13", "5", "/", "+"] -> (4 + (13 / 5)) -> 6

## solution


```java

import java.util.ArrayDeque;

public class Solution {
    public int evalRPN(String[] tokens) {
        ArrayDeque<Integer> s=new ArrayDeque<>();
        for(int i=0;i<tokens.length;i++){
            try{
                int num=Integer.parseInt(tokens[i]);
                s.push(num);
            }
            catch (Exception e){
                int b=s.pop();
                int a=s.pop();
                s.push(get(a,b,tokens[i]));
            }
        }
        return s.pop();

    }
    int get(int a,int b,String operator){
        switch (operator){
            case "+":
                return a+b;
            case "-":
                return a-b;
            case "*":
                return a*b;
            case "/":
                return a/b;
            default:
                return 0;
        }
    }
}
```