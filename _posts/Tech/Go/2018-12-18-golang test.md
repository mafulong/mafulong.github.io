---
layout: post
category: Go
title: go test
tags: Go
---

## 编写测试用例

同一目录下，Test开头

```go
func TestFunctionName(t *testing.T){
    t.Log()
    t.Logf()
    t.Error()
    t.Errorf()
}
```

## 运行命令

当前目录所有测试，则
```go
go test -v
```

指定文件测试和指定函数名测试

指定文件名时注意需要指定被测试的文件名

```go
go test -v  wechat_test.go wechat.go 
go test -v wechat_test.go -test.run TestRefreshAccessToken
```

当代码无修改时，重复go test会引起缓存，此时需要设置字段

```go
go test -count=1 -v 
```