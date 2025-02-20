---
layout: post
category: Python
title: libmini_racer的mac不兼容问题
tags: Python
---

## appleM1的python不兼容问题

问题: Running JavaScript code in Python via Apple Silicon

错误: 提示某dylib缺失。比如py_mini_racer 这个js运行库就依赖了这个dylib。 

其他类似问题

```
  File "/Users/mafulong/.pyenv/versions/3.11.10/lib/python3.11/site-packages/py_mini_racer/py_mini_racer.py", line 178, in __init__
    self.__class__.ext = _build_ext_handle()
                         ^^^^^^^^^^^^^^^^^^^
  File "/Users/mafulong/.pyenv/versions/3.11.10/lib/python3.11/site-packages/py_mini_racer/py_mini_racer.py", line 132, in _build_ext_handle
    _ext_handle.mr_eval_context.argtypes = [
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/mafulong/.pyenv/versions/3.11.10/lib/python3.11/ctypes/__init__.py", line 389, in __getattr__
    func = self.__getitem__(name)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/mafulong/.pyenv/versions/3.11.10/lib/python3.11/ctypes/__init__.py", line 394, in __getitem__
    func = self._FuncPtr((name_or_ordinal, self))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: dlsym(0x6d2e0e10, mr_eval_context): symbol not found. Did you mean: 'mr_init_context'?
Exception ignored in: <function MiniRacer.__del__ at 0x12584b420>
Traceback (most recent call last):
  File "/Users/mafulong/.pyenv/versions/3.11.10/lib/python3.11/site-packages/py_mini_racer/py_mini_racer.py", line 315, in __del__
    self.ext.mr_free_context(getattr(self, "ctx", None))
    ^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'mr_free_context'
```



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

