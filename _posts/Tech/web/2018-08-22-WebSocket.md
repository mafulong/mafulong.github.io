---
layout: post
category: web
title: WebSocket
---

WebSocket 是 HTML5 开始提供的一种在单个 TCP 连接上进行全双工通讯的协议。

## 为什么需要 WebSocket ？
了解计算机网络协议的人，应该都知道：HTTP 协议是一种无状态的、无连接的、单向的应用层协议。它采用了请求/响应模型。通信请求只能由客户端发起，服务端对请求做出应答处理。

这种通信模型有一个弊端：HTTP 协议无法实现服务器主动向客户端发起消息。

这种单向请求的特点，注定了如果服务器有连续的状态变化，客户端要获知就非常麻烦。大多数 Web 应用程序将通过频繁的异步JavaScript和XML（AJAX）请求实现长轮询。轮询的效率低，非常浪费资源（因为必须不停连接，或者 HTTP 连接始终打开）。

![](http://oyz7npk35.bkt.clouddn.com/image/spring/web/ajax-long-polling.png)

因此，工程师们一直在思考，有没有更好的方法。WebSocket 就是这样发明的。WebSocket 连接允许客户端和服务器之间进行全双工通信，以便任一方都可以通过建立的连接将数据推送到另一端。WebSocket 只需要建立一次连接，就可以一直保持连接状态。这相比于轮询方式的不停建立连接显然效率要大大提高。

## WebSocket 如何工作？
Web浏览器和服务器都必须实现 WebSockets 协议来建立和维护连接。由于 WebSockets 连接长期存在，与典型的HTTP连接不同，对服务器有重要的影响。

基于多线程或多进程的服务器无法适用于 WebSockets，因为它旨在打开连接，尽可能快地处理请求，然后关闭连接。任何实际的 WebSockets 服务器端实现都需要一个异步服务器。

## WebSocket 客户端
在客户端，没有必要为 WebSockets 使用 JavaScript 库。实现 WebSockets 的 Web 浏览器将通过 WebSockets 对象公开所有必需的客户端功能（主要指支持 Html5 的浏览器）。

```javascript
// 初始化一个 WebSocket 对象
var ws = new WebSocket("ws://localhost:9998/echo");

// 建立 web socket 连接成功触发事件
ws.onopen = function () {
  // 使用 send() 方法发送数据
  ws.send("发送数据");
  alert("数据发送中...");
};

// 接收服务端数据时触发事件
ws.onmessage = function (evt) {
  var received_msg = evt.data;
  alert("数据已接收...");
};

// 断开 web socket 连接成功触发事件
ws.onclose = function () {
  alert("连接已关闭...");
};
```

## WebSocket 服务端
WebSocket 在服务端的实现非常丰富。Node.js、Java、C++、Python 等多种语言都有自己的解决方案。

以下，介绍我在学习 WebSocket 过程中接触过的 WebSocket 服务端解决方案。

### Java
Java 的 web 一般都依托于 servlet 容器。

我使用过的 servlet 容器有：Tomcat、Jetty、Resin。其中Tomcat7、Jetty7及以上版本均开始支持 WebSocket（推荐较新的版本，因为随着版本的更迭，对 WebSocket 的支持可能有变更）。

此外，Spring 框架对 WebSocket 也提供了支持。

虽然，以上应用对于 WebSocket 都有各自的实现。但是，它们都遵循RFC6455 的通信标准，并且 Java API 统一遵循 JSR 356 - JavaTM API for WebSocket 规范。所以，在实际编码中，API 差异不大。

### Spring
Spring 对于 WebSocket 的支持基于下面的 jar 包：
```xml
<dependency>
  <groupId>org.springframework</groupId>
  <artifactId>spring-websocket</artifactId>
  <version>${spring.version}</version>
</dependency>
```

### javax.websocket
如果不想使用 Spring 框架的 WebSocket API，你也可以选择基本的 javax.websocket。

首先，需要引入 API jar 包。

```xml
<!-- To write basic javax.websocket against -->
<dependency>
  <groupId>javax.websocket</groupId>
  <artifactId>javax.websocket-api</artifactId>
  <version>1.0</version>
</dependency>
```

@ServerEndpoint

这个注解用来标记一个类是 WebSocket 的处理器。

然后，你可以在这个类中使用下面的注解来表明所修饰的方法是触发事件的回调

```java
// 收到消息触发事件
@OnMessage
public void onMessage(String message, Session session) throws IOException, InterruptedException {
    ...
}

// 打开连接触发事件
@OnOpen
public void onOpen(Session session, EndpointConfig config, @PathParam("id") String id) {
    ...
}

// 关闭连接触发事件
@OnClose
public void onClose(Session session, CloseReason closeReason) {
    ...
}

// 传输消息错误触发事件
@OnError
public void onError(Throwable error) {
    ...
}
```

ServerEndpointConfig.Configurator

编写完处理器，你需要扩展 ServerEndpointConfig.Configurator 类完成配置：

```java
public class WebSocketServerConfigurator extends ServerEndpointConfig.Configurator {
    @Override
    public void modifyHandshake(ServerEndpointConfig sec, HandshakeRequest request, HandshakeResponse response) {
        HttpSession httpSession = (HttpSession) request.getHttpSession();
        sec.getUserProperties().put(HttpSession.class.getName(), httpSession);
    }
}
```