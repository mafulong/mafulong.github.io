---
layout: post
category: Python
title: python单测pytest
tags: Python
---

## python单测pytest

## 安装

```
pip install -U pytest
```



## 使用

```python
#!/usr/local/bin/python
# -*- coding:utf-8 -*-
def test_one():
    print('我是方法一')
    x = "this"
    assert "h" in x
def test_two():
    print('我是方法二')
    y=5
    assert y > 6
```



执行该目录下所有用例：pytest 文件名/
执行某一个py文件下用例：pytest 脚本名称.py
-k 按关键字匹配：pytest -k “关键字”

```
pytest -q *.py
```

