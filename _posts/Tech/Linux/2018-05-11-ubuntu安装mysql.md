---
layout: post
category: Linux
title: ubuntu18.04安装mysql
tags: Linux
---

## 删除mysql
	sudo apt-get autoremove --purge mysql-server-5.0
	sudo apt-get remove mysql-server
	sudo apt-get autoremove mysql-server
	sudo apt-get remove mysql-common (非常重要)

## 清理残留数据
	dpkg -l |grep ^rc|awk '{print $2}' |sudo xargs dpkg -P

## 安装 mysql
	sudo apt-get install mysql-server
	sudo apt-get install mysql-client
	sudo apt-get install php5-mysql(安装php5-mysql是将php和mysql连接起来 )
	sudo apt-get install libmysqlclient-dev

一旦安装完成，MySQL服务器应该自动启动。您可以在终端提示符后运行以下命令来检查 MySQL 服务器是否正在运行：

##  检查Mysql是否正在运行
	sudo netstat -tap | grep mysql

当您运行该命令时，您可以看到类似下面的行：

	root@ubuntu:~# sudo netstat -tap | grep mysql
	tcp        0      0 localhost.localdo:mysql *:* LISTEN 870/mysqld 

如果服务器不能正常运行，您可以通过下列命令启动它：

	sudo /etc/init.d/mysql restart

如下命令来检查是否安装成功：

	sudo netstat -tap | grep mysql

通过上述命令检查之后，如果看到有mysql 的socket处于 listen 状态则表示安装成功。

登陆mysql数据库可以通过如下命令：

	mysql -u root -p 

-u 表示选择登陆的用户名， -p 表示登陆的用户密码，上面命令输入之后会提示输入密码，此时输入密码就可以登录到mysql。

## Ubuntu中安装MySQL的时候初始化密码

当在Ubuntu中执行命令sudo apt-get install mysql-server5.1安装的时候居然没有提示我输入mysql的密码之类的信息，但是当安装好之后再终端中直接输入mysql的时候又能直接进入mysql中，虽然可以进入mysql中但是我对mysql的密码一点都不知道，所以这个时候安装的mysql就相当于没有安装，因为不能用程序进行操作mysql数据库（因为操作数据库都需要mysql数据的密码的），为了解决ubuntu中mysql密码初始化的方法有一下两种：

（1）打开/etc/mysql/debian.cnf文件，在这个文件中有系统默认给我们分配的用户名和密码，通过这个密码就可以直接对mysql进行操作了。但是一般这个密码都比较怪，很长很长。

（2）当进入mysql之后修改mysql的密码：这个方法比较好，具体的操作如下用命令：set password for 'root'@'localhost' = password('yourpass');当修改之后就可应正常对mysql进行操作了。

## 新建用户
	show grants for 'root'@'localhost';

	GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION

	GRANT ALL PRIVILEGES ON *.* TO 'test1'@'127.0.0.1' WITH GRANT OPTION

	mysql> GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP
	    -> ON TUTORIALS.*
	    -> TO 'zara'@'localhost'
	    -> IDENTIFIED BY 'zara123';


