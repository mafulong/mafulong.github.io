---
layout: post
category: golang
title: golang dep
---

```go
# 初始化
dep init

# 添加一条依赖
dep ensure -add github.com/bitly/go-simplejsondep init
# 建议使用
dep ensure -v
```
