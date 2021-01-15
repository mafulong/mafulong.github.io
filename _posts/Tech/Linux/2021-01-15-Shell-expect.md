---
layout: post
category: Linux
title: Shell-expect
tags: Linux
---

## Shell-expect

有时候我们使用命令行进行交互时，不想频繁的做一些重复的事情，例如：每次ssh远程登录时都需要输入密码。使用spawn和expect可以自动完成一些交互。



## 安装

```shell
sudo apt install expect
```

mac也有expect



## 设置

[参考](http://xstarcd.github.io/wiki/shell/expect.html)

### 举例

```shell
#!/usr/bin/expect

set login_name  "user name"
set login_host  "host's ip"
set password    "guess what"

spawn ssh $login_name@$login_host
expect {
        "(yes/no)" { send "yes\r"; exp_continue }
        "password:" { send "$password\r" }
}
#expect $login_name@*   {send "ls\r" }  ;
interact
```



## 启动

expect expect.sh