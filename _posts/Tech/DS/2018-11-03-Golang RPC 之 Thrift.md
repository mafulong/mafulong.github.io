```
layout: post
category: 服务端
title: Thrift
```

## Thrift 简介：

目前流行的服务调用方式有很多种，例如基于 SOAP 消息格式的 Web Service，基于 JSON 消息格式的 RESTful 服务等。其中所用到的数据传输方式包括 XML，JSON 等，然而 XML 相对体积太大，传输效率低，JSON 体积较小，新颖，但还不够完善。本文将介绍由 Facebook 开发的远程服务调用框架 Apache Thrift，它采用接口描述语言定义并创建服务，支持可扩展的跨语言服务开发，所包含的代码生成引擎可以在多种语言中，如 C++, Java, Python, PHP, Ruby, Erlang, Perl, Haskell, C#, Cocoa, Smalltalk 等创建高效的、无缝的服务，其传输数据采用二进制格式，相对 XML 和 JSON 体积更小，对于高并发、大数据量和多语言的环境更有优势。本文将详细介绍 Thrift 的使用，并且提供丰富的实例代码加以解释说明，帮助使用者快速构建服务。

[thrift参考文档](https://www.ibm.com/developerworks/cn/java/j-lo-apachethrift/index.html)

Thrift 是一款高性能、开源的 RPC 框架，产自 Facebook 后贡献给了 Apache，Thrift 囊括了整个 RPC 的上下游体系，自带序列化编译工具，因为 Thrift 采用的是二进制序列化，并且与 gRPC 一样使用的都是长连接建立 client 与 server 之间的通讯，相比于比传统的使用XML，JSON，SOAP等短连接的解决方案性能要快得多。
本篇只介绍 Golang 关于 Thrift 的基础使用。

Thrift实际上是实现了C/S模式，通过代码生成工具将thrift文生成服务器端和客户端代码（可以为不同语言），从而实现服务端和客户端跨语言的支持。用户在Thirft文件中声明自己的服务，这些服务经过编译后会生成相应语言的代码文件，然后客户端调用服务，服务器端提服务便可以了。

一般将服务放到一个.thrift文件中，服务的编写语法与C语言语法基本一致，在.thrift文件中有主要有以下几个内容：变量声明（variable）、数据声明（struct）和服务接口声明（service, 可以继承其他接口）。

在client端，用户自定义CalculatorClient类型的对象（用户在.thrift文件中声明的服务名称是Calculator， 则生成的中间代码中的主类为CalculatorClient）， 该对象中封装了各种服务，可以直接调用（如client.ping()）, 然后thrift会通过封装的rpc调用server端同名的函数。

在server端，需要实现在.thrift文件中声明的服务中的所有功能，以便处理client发过来的请求。

 

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
