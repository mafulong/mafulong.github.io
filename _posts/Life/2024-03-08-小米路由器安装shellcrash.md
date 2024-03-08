---
layout: post
category: Life
title: 小米路由器安装shellcrash
tags: Life
---

# 小米路由器安装shellcrash

路由器安装了shellcrash后就自带梯子了。然后就可以通过http://192.168.31.1:9999/ui/#/proxies 管理节点切换等。



- [shellcrash介绍](https://github.com/2375399351/ShellCrash/blob/master/README_CN.md)
- [小米路由器后台](http://192.168.31.1/cgi-bin/luci/web)
- [安装shellcrash参考](https://www.gaicas.com/redmi-ax6000.html)
- [参考2](https://beyondkmp.com/2023/03/05/ax6000-ssh/)







你设备的 SSH 密码设置为**admin**，用户名为**root**，并永久开启 SSH；

```scala
ssh -oHostKeyAlgorithms=+ssh-rsa  root@192.168.31.1
```





# ssh解锁

当路由器开启SSH时，可以通过SSH协议连接到路由器并执行一系列的操作，包括但不限于：

1. 远程管理：可以通过SSH连接到路由器并对其进行管理，就像通过Web界面或命令行一样。
2. 文件传输：可以通过SCP或SFTP等协议，在计算机和路由器之间传输文件。
3. 调试和故障排除：通过SSH连接到路由器并查看系统日志、配置文件和其他信息，以帮助调试和解决问题。
4. 安全管理：使用SSH协议进行加密连接，可以更加安全地管理路由器，防止被黑客入侵或监听。

总的来说，开启SSH可以使你更加方便地管理和维护路由器，同时也可以提高安全性。需要注意的是，开启SSH也可能会增加路由器被攻击的风险，因此应该采取一些安全措施，如设置强密码、限制SSH访问等。





## 固件降级

首先，登陆小米路由器的后台。依次点击**常用设置**-**系统状态**，检查路由器的系统版本是否为**1.2.08**版。

若路由器当前版本为其他版本，请先点击**手动升级**，并将路由器 💾 **[稳定版固件](https://www.icloud.com/iclouddrive/006hgOdY5pn3MJ1czZViTDPBA#redmi-ax6000-1.2.8)** 上传至设备，进行手动升级/降级操作。



需要利用老版本的漏洞才能开启ssh, 所以需要手动降级。



## 获取token

登陆小米路由器admin，浏览器地址栏`stok=`后面部分就是token, 这个token是每次登录都会变化，后面都会用到这个token。如果重新登录后，都要重新复制这个token.

![获取token](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv8/v8/202403081125383.png)

## 开启开发者模式

**更改路由器的crash分区，使其进入到开发者模式**

将下面的URL里面的stok=token的token替换成上面获取路由器的token值，然后复制到到浏览器并且按enter打开

```scala
http://192.168.31.1/cgi-bin/luci/;stok=token/api/misystem/set_sys_time?timezone=%20%27%20%3B%20zz%3D%24%28dd%20if%3D%2Fdev%2Fzero%20bs%3D1%20count%3D2%202%3E%2Fdev%2Fnull%29%20%3B%20printf%20%27%A5%5A%25c%25c%27%20%24zz%20%24zz%20%7C%20mtd%20write%20-%20crash%20%3B%20
```

浏览器返回{“code”:0}，表示成功。

**通过浏览器重启路由器**

在浏览器地址栏输入下面的url, 和上面的做法一样，将stok=token的token替换成上面获取路由器的token值

```scala
http://192.168.31.1/cgi-bin/luci/;stok=token/api/misystem/set_sys_time?timezone=%20%27%20%3b%20reboot%20%3b%20
```

## 设置Bdata参数

**设置参数telnet_en、 ssh_en、uart_en**

重启后，要重新获取token, 然后在浏览器地址栏输入下面的url, 将stok=token的token替换成上面获取路由器的token值

```scala
http://192.168.31.1/cgi-bin/luci/;stok=token/api/misystem/set_sys_time?timezone=%20%27%20%3B%20bdata%20set%20telnet_en%3D1%20%3B%20bdata%20set%20ssh_en%3D1%20%3B%20bdata%20set%20uart_en%3D1%20%3B%20bdata%20commit%20%3B%20
```

**重启路由器**

在浏览器地址栏输入下面的url, 和上面的做法一样，将stok=token的token替换成上面获取路由器的token值

```scala
http://192.168.31.1/cgi-bin/luci/;stok=token/api/misystem/set_sys_time?timezone=%20%
```

## 通过telnet开启ssh

在终端输入`telnet 192.168.31.1`, 可以看到Are you ok的界面，就证明telnet成功了。



## 永久开启并固化 ssh

Telnet 登录成功后，将代码复制粘贴并运行。

这将会为你设备的 SSH 密码设置为**admin**，用户名为**root**，并永久开启 SSH；

这一步还会将您的设备从开发模式切换成常规模式，**待最后一个命令reboot即设备重启完成后**，你就可以使用该用户名密码连接设备的 SSH 了。

```shell
echo -e 'admin\nadmin' | passwd root
nvram set ssh_en=1
nvram set telnet_en=1
nvram set uart_en=1
nvram set boot_wait=on
nvram commit
sed -i 's/channel=.*/channel="debug"/g' /etc/init.d/dropbear
/etc/init.d/dropbear restart
mkdir /data/auto_ssh
cd /data/auto_ssh
curl -O https://fastly.jsdelivr.net/gh/lemoeo/AX6S@main/auto_ssh.sh
chmod +x auto_ssh.sh
uci set firewall.auto_ssh=include
uci set firewall.auto_ssh.type='script'
uci set firewall.auto_ssh.path='/data/auto_ssh/auto_ssh.sh'
uci set firewall.auto_ssh.enabled='1'
uci commit firewall
uci set system.@system[0].timezone='CST-8'
uci set system.@system[0].webtimezone='CST-8'
uci set system.@system[0].timezoneindex='2.84'
uci commit
mtd erase crash
reboot

```

## ssh 登录

你设备的 SSH 密码设置为**admin**，用户名为**root**，并永久开启 SSH；

```scala
ssh -oHostKeyAlgorithms=+ssh-rsa  root@192.168.31.1
```

# shellcrash安装

ssh后，在路由器主机里。运行如下代码，如不行，可尝试其它方式见shellcrash主页

```scala
export url='https://fastly.jsdelivr.net/gh/juewuy/ShellClash@master' && sh -c "$(curl -kfsSl $url/install.sh)" && source /etc/profile &> /dev/null

```



- 安装推荐的公测版。

- 安装后运行clash/crash打开软件。

- 路由器安装在/data目录下，另一个可选项是/usrdisk

- 安装yard面板

- 若你的订阅链接为 SS/SSR/VMESS 格式，可以点击下面链接，进行订阅链接转换。[订阅链接转换](https://acl4ssr-sub.github.io/)。 最好直接用clash的订阅链接。

- 如果订阅链接的文件下不下来，就vim创建编辑个yaml文件在tmp目录下，然后手动复制进去。或者curl下载订阅链接的文件。

  ```scala
  curl -o a.yaml "clash订阅链接"
  
  ```

- clash打开后会自动识别当前目录的yaml文件，进而使用这个配置文件。

- CLASH面板管理地址：**http://192.168.31.1:9999/ui**

# 工具

## 路由器文件上传和下载

文件传输：可以通过SCP或SFTP等协议，在计算机和路由器之间传输文件。scp 是 ssh copy 的缩写。



上传文件到指定目录：

> scp myfile.tar.gz root@192.168.1.1:/tmp/temp

下载文件到指定目录：

> scp root@192.168.1.1:/tmp/file.tar.gz  ./





把这个文件拷贝进路由器，格式` scp <local file> <remote user>@<remote machine>:</usr/lib/lua/luci/controller/admin/>`

我路由后台管理地址192.168.3.1为例设置
`scp /Users/jesse/Desktop/xqsystem.lua root@192.168.3.1:/usr/lib/lua/luci/controller/admin/`

测试文件传输效果，直接在路由器ip后面加 /cgi-bin/luci/api/xqsystem/token
如果文件传进去了会这样显示则代表成功

![顺序可能不同，大概内容相似就行](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv8/v8/202403081148181.jpg)

大文件上传下载： https://taoshu.in/transfer-big-file.html