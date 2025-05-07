---
layout: post
category: Others
title: 会话管理session及jwt
tags: Others
---

[参考](https://javaguide.cn/system-design/security/basis-of-authority-certification.html#%E4%B8%BA%E4%BB%80%E4%B9%88-cookie-%E6%97%A0%E6%B3%95%E9%98%B2%E6%AD%A2-csrf-%E6%94%BB%E5%87%BB-%E8%80%8C-token-%E5%8F%AF%E4%BB%A5)

## cookie、session

cookie：cookie中的信息是以键值对的形式储存在浏览器中，而且在浏览器中可以直接看到数据

session：session存储在服务器中，然后发送一个cookie存储在浏览器中，cookie中存储的是session_id，之后每次请求服务器通过session_id可以获取对应的session信息

## 基于session的认证方式

早期互联网以 web 为主，客户端是浏览器 ，所以 Cookie-Session 方式是早期最常用的认证方式，直到现在，一些 web 网站依然用这种方式做认证。

**认证过程大致如下：**

1. 用户输入用户名、密码或者用短信验证码方式登录系统；
2. 服务端验证后，创建一个 Session 信息，并且将 SessionID 存到 cookie，发送回浏览器；
3. 下次客户端再发起请求，自动带上 cookie 信息，服务端通过 cookie 获取 Session 信息进行校验；



缺点: 

1.  Cookie 是不能跨域的，就是不能多域名共享
2. cookie 存在 CSRF（跨站请求伪造）的风险。比如在html里加了script复用你的cookie来搞事情
3. 分布式系统可能要session同步，当然redis可解决。
4. 对于app可能没有cookie，但可以用app数据库



### 改造版 使用local storage



将Session存入redis来解决分布式系统中的Session同步问题。同时提高了Session的获取速度;  Cookie 是基于域名存储的，不能跨域共享。如果你的应用涉及多个子域名或不同的域名，使用 Cookie 会面临跨域访问的问题。



用了redis， 本地不用cookie, 浏览器使用local storage，app使用app数据库

1. 用户输入用户名、密码或者用短信验证码方式登录系统；
2. 服务端经过验证，将认证信息构造好的数据结构存储到 Redis 中，并将 key 值返回给客户端；
3. 客户端拿到返回的 key，存储到 local storage 或本地数据库；
4. 下次客户端再次请求，把 key 值附加到 header 或者 请求体中；
5. 服务端根据获取的 key，到 Redis 中获取认证信息；



## 基于token的认证方式 JWT

近些年SPA, web API, 和IoT(Internet of Things, 物联网)的崛起带动了基于Token的验证, 通常就是指JWT(Json Web Token)

JWT是无状态的(stateless), 后端不必保存有关session的信息. 后端只需要验证每次请求中携带的Token即可验证请求的真实性.

Token通常以`Bearer {JWT}`的形式保存在Authentication header中, 也可以放到POST body或query parameter中.



流程如下:

1. 用户输入登录信息
2. 服务器验证后, 返回一个签名(signed)的token. 该token存储在前端, 通常在localStorage中, sessionStorage或cookie也可以. **(为了不暴露jwt可以使用https)**
3. 接下来的请求中token被加到Authentication Header中, 或者POST body / query parameter中.
4. **后台解码JWT，使用 base64的头部和 base64 的载荷部分，通过HMACSHA256算法计算签名部分，比较计算结果和传来的签名部分是否一致，如果一致，说明此次请求没有问题，如果不一致，说明请求过期或者是非法请求。**
5. 用户登出后, token从前端销毁, 无需与后端交互.



JWT存储在浏览器的storage或者cookie中。由服务器产生加密的json数据包括：header，payload和signature三部分组成。

header中通常来说由token的生成算法和类型组成；payload中则用来保存相关的状态信息；signature部分由header，payload，secret_key三部分加密生成。 注意，不要在JWT的payload或header中放置敏感信息



缺点：  `token`由于自包含信息，因此一般数据量较大，而且每次请求 都需要传递，因此比较占带宽





[为什么 Cookie 无法防止 CSRF 攻击，而 Token 可以？](https://javaguide.cn/system-design/security/basis-of-authority-certification.html#为什么-cookie-无法防止-csrf-攻击-而-token-可以)  

- 在我们登录成功获得 `Token` 之后，一般会选择存放在 `localStorage` （浏览器本地存储）中。然后我们在前端通过某些方式会给每个发到后端的请求加上这个 `Token`,这样就不会出现 CSRF 漏洞的问题。因为，即使你点击了非法链接发送了请求到服务端，这个非法请求是不会携带 `Token` 的，所以这个请求将是非法的。



#### 如何防止 JWT 被篡改？

有了签名之后，即使 JWT 被泄露或者截获，黑客也没办法同时篡改 Signature、Header、Payload。

这是为什么呢？因为服务端拿到 JWT 之后，会解析出其中包含的 Header、Payload 以及 Signature 。服务端会根据 Header、Payload、密钥再次生成一个 Signature。拿新生成的 Signature 和 JWT 中的 Signature 作对比，如果一样就说明 Header 和 Payload 没有被修改。

不过，如果服务端的秘钥也被泄露的话，黑客就可以同时篡改 Signature、Header、Payload 了。黑客直接修改了 Header 和 Payload 之后，再重新生成一个 Signature 就可以了。

**密钥一定保管好，一定不要泄露出去。JWT 安全的核心在于签名，签名安全的核心在密钥。**



如果 **JWT 被截获**，攻击者就可能使用这个 token 伪造请求。JWT 本身是自包含的，包含了用户的认证信息和一些元数据（如有效期），而且默认情况下它是 **无状态** 的，这就意味着服务端通常不保存 JWT 的信息，所有的信息都在 token 本身。因此，如果 JWT 被篡改或盗取，确实会导致 **安全问题**。



## 开放授权 oauth2

有时候，我们登录某个网站，但我们又不想注册该网站的账号，这时我们可以使用第三方账号登录，比如 github、微博、微信、QQ等。



开放授权（OAuth）是一个开放标准，允许用户让第三方应用访问该用户在某一网站上存储的私密的资源（如照片，视频，联系人列表），而无需将用户名和密码提供给第三方应用。



OAuth允许用户提供一个令牌，而不是用户名和密码来访问他们存放在特定服务提供者的数据。每一个令牌授权一个特定的网站（例如，视频编辑网站)在特定的时段（例如，接下来的2小时内）内访问特定的资源（例如仅仅是某一相册中的视频）。这样，OAuth让用户可以授权第三方网站访问他们存储在另外服务提供者的某些特定信息，而非所有内容。

**名词解释：**

- Third-party application：第三方应用程序又称"客户端"（client），比如打开知乎，使用第三方登录，选择 Github 登录，这时候知乎就是客户端。
- Resource Owner：资源所有者，本文中又称"用户"（user）,即登录用户。
- Authorization server：认证服务器，即 Github 专门用来处理认证的服务器。
- Resource server：资源服务器，即 Github 存放用户生成的资源的服务器。它与认证服务器，可以是同一台服务器，也可以是不同的服务器。



![img](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv3/v3/20220106154749.jpg)



- A. A网站让用户跳转到 GitHub，请求授权码；GitHub 要求用户登录，然后询问“知乎网站要求获得 xx 权限，你是否同意？”；
- B. 用户同意，GitHub 就会重定向回 A 网站，同时发回一个授权码；
- C. A 网站使用授权码，向 GitHub 请求令牌；
- D. GitHub 返回令牌；
- E. A 网站使用令牌，向 GitHub 请求用户数据；

## 参考

- https://cloud.tencent.com/developer/news/769106
- https://liuzhenglai.com/post/5bbabecedcd9832abf60c176
