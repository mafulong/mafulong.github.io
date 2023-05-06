---
layout: post
category: IDE
title: Intellij idea 远程调试
tags: IDE
---

## Intellij idea 远程调试

> [详述 IntelliJ IDEA 远程调试 Tomcat 的方法 attch形式](https://github.com/guobinhit/intellij-idea-tutorial/blob/master/articles/practical-skills/the-method-of-remote-debugging-with-idea.md)

远程debug的意思是启动一个Java进程，启动一个debugger进程，将两者连接起来，利用debugger来debug Java进程。

事实上目前所有的IDE的debug功能都是通过远程debug方式来实现的，它们都利用了一个叫做JDPA（Java Platform Debugger Architecture）的技术。



场景：本地有代码，然后远程debug 某server/开发机的里的Java代码(java代码无法本地启动，只能远程调试)

不仅运行的服务可以debug，单测也可以。因为单测其实也是基于jvm的Java程序。

实际是个jvm的java调试。



## Debug attach形式

此种模式下，调试服务端（被调试远程运行的机器）启动一个端口等待我们（调试客户端）去连接;

### 本地intellij idea配置

Edit Configurations新建一个Remote JVM debug.

传输方式，默认为`Socket`；

- `Socket`：macOS 及 Linux 系统使用此种传输方式；
- `Shared memory`： Windows 系统使用此种传输方式。

调试模式，默认为`Attach`；

- `Attach`：此种模式下，调试服务端（被调试远程运行的机器）启动一个端口等待我们（调试客户端）去连接；

- `Listen`： 此种模式下，是我们（调试客户端）去监听一个端口，当调试服务端准备好了，就会进行连接。

服务器 IP 地址，默认为`localhost`，需要修改为目标服务器的真实 IP 地址；如果目标服务器限制了随便访问，则可以ssh tunnel映射到本地某个端口。比如

```scala
 ssh -N -L 5090:localhost:5090 {host}
```

服务器端口号，默认为`5005`，需要修改为目标服务器的真实端口号； 我的是5090

### 设置remote的启动参数

这个就需要上个步骤里的idea的运行远程 JVM 的命令行参数， Command line arguments for remote JVM。

其实就是让当前remote启动时以debug方式启动，同时对外开放一个debug port，这个debug port应该上个步骤的idea监听到。



Command line arguments for remote JVM例子

```scala
-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5090
```



这个文本框你是不能修改的，它告诉了你如果要这个Java进程能够被远程Debug，那么必须添加这些参数才可以。 所以你要把这里的参数复制出来。导入到tomcat或者build的xml里文件里。

### 开始debug

1. remote程序启动，会阻塞并输出以下内容 ` [junit] Listening for transport dt_socket at address: 5090` 如果没有就是设置remote的启动参数设置错了，重新进行。
2. idea debug启动。 先idea加上必要的断点，然后点击debug，idea出现Connected to the target VM, address: 'localhost:5090', transport: 'socket'。
3. 此时开发机和本地都在断点那停止了！就可以从断点开始往下debug了！

## Debug listen形式

Command line arguments for remote JVM里的server=y: 开启调试 server。若是 **Attach to remote JVM**，则值为 `y`，若是 **Listen to remote JVM**，则远程服务器为 client，值应该为 `n`



所以就是一个先后和参数区别问题。推荐attach形式，更人性化。

## 参考

- [Intellij IDEA远程debug线上项目记录](https://www.cnblogs.com/fengyun2050/p/15357075.html) attach形式