---
layout: post
category: Linux
title: ubuntu安装java环境
tags: Linux
---

## ubuntu安装java环境


1.ubuntu使用的是openjdk，所以我们需要先找到合适的jdk版本。在命令行中输入命令：```$apt-cache search openjdk```

2.从搜索的列表里找到我们需要安装的jdk版本```openjdk-11-jdk - OpenJDK Development Kit (JDK)```

3.输入安装命令，进行安装：```$sudo apt-get install openjdk-11-jdk```等待命令行显示“done”，即安装成功过。

4.查看安装结果。输入命令：```$java -version```显示结果如下： ```openjdk version “10.0.1” 2018-04-17 OpenJDK Runtime Environment (build 10.0.1+10-Ubuntu-3ubuntu1)OpenJDK 64-Bit Server VM (build 10.0.1+10-Ubuntu-3ubuntu1, mixed mode)```则说明安装成功。

5.安装成功后，还需要配置```java_home```变量：

1)输入命令：```echo $java_home``` 返回空行；

2）```which javac``` 返回：```/usr/bin/javac```

3）```file /usr/bin/javac ```返回：```/usr/bin/javac: symbolic link to /etc/alternatives/javac```

4）```file /etc/alternatives/javac``` 返回：```/etc/alternatives/javac: symbolic link to /usr/lib/jvm/java-11-openjdk-amd64/bin/javac5）file /usr/lib/jvm/java-11-openjdk/bin/javac``` 返回：```/usr/lib/jvm/java-11-openjdk/bin/javac: cannot open `/usr/lib/jvm/java-11-openjdk-amd64/bin/javac' (No such file or directory)```

6）```sudo echo export JAVA_HOME=”/usr/lib/jvm/java-11-openjdk-amd64/bin”>>~/.bashrc``` 输入密码；

7）```source ~/.bashrc```

8）测试命令：```gedit ~/.bashrc``` 查看打开的文件末尾是否成功加入```java_home```

---------------------

本文来自 yzj_xiaoyue 的CSDN 博客 ，全文地址请点击：https://blog.csdn.net/yzj_xiaoyue/article/details/80107055?utm_source=copy 