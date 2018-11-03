```
layout: post
category: golang
title: Golang RPC 之 Thrift
```

## Thrift 简介：
Thrift 是一款高性能、开源的 RPC 框架，产自 Facebook 后贡献给了 Apache，Thrift 囊括了整个 RPC 的上下游体系，自带序列化编译工具，因为 Thrift 采用的是二进制序列化，并且与 gRPC 一样使用的都是长连接建立 client 与 server 之间的通讯，相比于比传统的使用XML，JSON，SOAP等短连接的解决方案性能要快得多。
本篇只介绍 Golang 关于 Thrift 的基础使用。

## 实践：
下面我们使用 Thrift 定义一个接口，该接口实现对传入的数据进行大写的格式化处理。

**创建 golang 项目 ThriftDemo 工程：**

![](https://upload-images.jianshu.io/upload_images/208550-bcb893005250db84.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/473/format/webp)

- client目录下的 client.go 实现了客户端用于发送数据并打印接收到 server 端处理后的数据
- server 目录下的 server.go 实现了服务端用于接收客户端发送的数据，并对数据进行大写处理后返回给客户端
- thrift_file 用于存放 thrift 的 IDL 文件： *.thrift

**定义 Thrift RPC 接口**
```
example.thrift：

namespace py example

struct Data {
    1: string text
}

service format_data {
    Data do_format(1:Data data),
}
```

**编译 thrift 文件**

进入 thrift_file 目录执行：$ thrift -out .. --gen go example.thrift，就会在 thrift_file 的同级目录下生成 golang 的包：example，其中 format_data-remote 是生成的测试代码可以不用特别关注

![](https://upload-images.jianshu.io/upload_images/208550-03e830dbda815157.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/470/format/webp)

实现 server 端：

```go
package main

import (
    "ThriftDemo/example"
    "strings"
    "git.apache.org/thrift.git/lib/go/thrift"
    "fmt"
    "log"
)

type FormatDataImpl struct {}

func (fdi *FormatDataImpl) DoFormat(data *example.Data) (r *example.Data, err error){
    var rData example.Data
    rData.Text = strings.ToUpper(data.Text)

    return &rData, nil
}

const (
    HOST = "localhost"
    PORT = "8080"
)

func main() {

    handler := &FormatDataImpl{}
    processor := example.NewFormatDataProcessor(handler)
    serverTransport, err := thrift.NewTServerSocket(HOST + ":" + PORT)
    if err != nil {
        log.Fatalln("Error:", err)
    }
    transportFactory := thrift.NewTFramedTransportFactory(thrift.NewTTransportFactory())
    protocolFactory := thrift.NewTBinaryProtocolFactoryDefault()

    server := thrift.NewTSimpleServer4(processor, serverTransport, transportFactory, protocolFactory)
    fmt.Println("Running at:", HOST + ":" + PORT)
    server.Serve()
}

```


实现 client 端

```
package main

import (
    "git.apache.org/thrift.git/lib/go/thrift"
    "net"
    "fmt"
    "ThriftDemo/example"
    "log"
)

const (
    HOST = "localhost"
    PORT = "8080"
)

func main()  {
    tSocket, err := thrift.NewTSocket(net.JoinHostPort(HOST, PORT))
    if err != nil {
        log.Fatalln("tSocket error:", err)
    }
    transportFactory := thrift.NewTFramedTransportFactory(thrift.NewTTransportFactory())
    transport := transportFactory.GetTransport(tSocket)
    protocolFactory := thrift.NewTBinaryProtocolFactoryDefault()

    client := example.NewFormatDataClientFactory(transport, protocolFactory)

    if err := transport.Open(); err != nil {
        log.Fatalln("Error opening:", HOST + ":" + PORT)
    }
    defer transport.Close()


    data := example.Data{Text:"hello,world!"}
    d, err := client.DoFormat(&data)
    fmt.Println(d.Text)
}

```
执行验证结果：

先启动 server，之后再执行 client

client 侧控制台如果打印的结果为： HELLO,WORLD! ，证明 Thrift 的 RPC 接口定义成功
