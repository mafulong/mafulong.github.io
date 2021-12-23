---
layout: post
category: Mysql
title: linux的mysql配置及连接
---

# linux的mysql配置及连接

## 安装
[How To Install MySQL on Debian 9 ](https://tecadmin.net/install-mysql-server-on-debian9-stretch/)

```shell
sudo apt update 
sudo apt upgrade

wget http://repo.mysql.com/mysql-apt-config_0.8.9-1_all.deb
sudo dpkg -i mysql-apt-config_0.8.9-1_all.deb

sudo apt update 
sudo apt install mysql-server

sudo systemctl restart mysql

mysql -u root -p
```

## mysql更改密码和创建用户
```shell
UPDATE user SET Password = PASSWORD('newpass') WHERE user = 'root';
FLUSH PRIVILEGES;
select host,user,password from user ;
# 创建admin用户可远程也可本地访问，超级用户
CREATE USER 'admin'@'localhost' IDENTIFIED BY '1234';
CREATE USER 'admin'@'%' IDENTIFIED BY '1234';
GRANT ALL ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;
GRANT ALL ON *.* TO 'admin'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

[grant](https://www.yiibai.com/mysql/grant.html)

## 查看默认端口号
[查看并修改默认端口号](https://www.cnblogs.com/tianlangshu/p/5665290.html)

```shell
show global variables like 'port';
```

## mysql远程连接
```shell
mysql -h 192.168.5.116 -P 3306 -u root -p123456
```

## 配置可远程连接
[配置mysql允许远程链接](https://www.cnblogs.com/skyWings/p/5952795.html)
```shell
update user set host = '%' where user = 'root';
select host, user from user;
```
还需要修改bind-address
在/etc/mysql/mysql.conf.d目录下的mysqld.cnf文件
```
bind-address=0.0.0.0
```

## mysql重启或关闭
[mysql重启或关闭](https://www.cnblogs.com/linjiqin/p/3544472.html)
```shell
service mysqld restart 
service mysqld stop
```

