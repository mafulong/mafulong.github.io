---
layout: post
category: Python
title: appleM1的python不兼容问题
tags: Python
---

## appleM1的python不兼容问题

问题: Running JavaScript code in Python via Apple Silicon

错误: 提示某dylib缺失。比如py_mini_racer 这个js运行库就依赖了这个dylib。 





## 解决方式

[参考](https://medium.com/@Stephen.Z/%EF%B8%8Frunning-javascript-code-in-python-via-apple-silicon-ac9da5da39e3)



首先下载dylib

```scala
#1. Found your site-packages
python -m site
>>> /opt/homebrew/Caskroom/miniconda/base/lib/python3.8/site-packages

# 1. 确定 site-packages 位置
python -m site

# 2. 下载并解压 Dylib 文件
wget https://github.com/sqreen/PyMiniRacer/files/7575004/libmini_racer.dylib.zip && unzip libmini_racer.dylib.zip

# 3. 移动 Dylib 文件到 site-packages
mv libmini_racer.dylib $(python -c "import site; print(site.getsitepackages()[0])")/py_mini_racer/.

# 4. 测试导入
python -c "from py_mini_racer import MiniRacer"

cd $(python -c "import site; print(site.getsitepackages()[0])")/py_mini_racer/.
```



对于dylib不可打开的问题类似 “libc10.dylib” can’t be opened because Apple cannot check it for malicious software.，[可以参考](https://github.com/pytorch/pytorch/issues/120606)

```scala
sudo xattr -r -d com.apple.quarantine  /Users/mafulong/.pyenv/versions/3.11.5/lib/python3.11/site-packages/py_mini_racer/libmini_racer.dylib
```

