---
layout: post
category: C
title: make工具与Makefile文件
tags: C
---

[Linux工具入门：make工具与Makefile文件](http://www.cnblogs.com/QG-whz/p/5461110.html)

## 1. make工具

利用make工具可以自动完成编译工作，这些工作包括：

- 如果修改了某几个源文件，则只重新编译这几个源文件
- 如果某个头文件被修改了，则重新编译所有包含该头文件的源文件

利用这种自动编译可以大大简化开发工作，避免不必要的重新编译。make工具通过一个称为Makefile的文件来完成并自动维护编译工作，Makefile文件描述了整个工程的编译、连接规则。

## 2. Makefile文件 ##

Makefile描述了整个工程的编译连接规则。Makefile的基本规则为：

```
TARGET...: DEPENDENCIES...
    COMMAND
    ...
```

- TARGER：目标程序产生的文件，如可执行文件和目标文件，目标也可以是要执行的动作，如clean，也称为伪目标。
- DEPENDENCIES:依赖是用来产生目标的输入文件列表，一个目标通常依赖与多个文件。
- COMMAND:命令是make执行的动作（命令是shell命令或是可在shell下执行的程序），注意每个命令行的起始字符必须为TAB字符。
- 如果DEPENDENCIES中有一个或多个文件更新的话，COMMAND就要执行，这就是Makefile最核心的内容。

## 3. Makefile的简单示例
```$ touch add.c add.h sub.c sub.h main.c```

现在有这5个文件add.h 、sub.h中包含了函数声明，add.c、sub.c中包含了函数实现，main.c调用了函数。Makefile的文件：

```
main:main.o add.o sub.o        【目标文件是main，它依赖于main.o,add.o,sub.o这三个文件】
        gcc -Wall -g main.o add.o sub.o -o main    【由依赖文件生成目标文件应该执行的命令】
main.o:main.c
        gcc -Wall -g -c main.c -o main.o
add.o:add.c add.h
        gcc -Wall -g -c add.c -o add.o
sub.o:sub.c sub.h
        gcc -Wall -g -c sub.c -o sub.o
```

保存Makefile文件后执行make命令：

```
$ make
gcc -Wall -g -c main.c -o main.o
gcc -Wall -g -c add.c -o add.o
gcc -Wall -g -c sub.c -o sub.o
gcc -Wall -g main.o add.o sub.o -o main
```

可以看到执行了make之后，由于 目标文件main依赖于 main.o add.o sub.o ，所以是需要先 生成 这三个.o文件，最后才生成main。
如果此时再次输入make，会看到：

```
$ make
make: 'main' is up to date.
```

make的编译规则是根据时间来进行判断，一旦依赖列表中某个文件的更新时间比目标文件晚，则会重新生成目标，否则会出现以上提示。
默认情况下敲击make将生成第一个目标，也就是main。也可以生成指定的目标：

```
$ make add.o   【指定只生成add.o文件】
```


Makefile文件的名字不一定得命名为“Makefile”或"makefile"，使用其他名字也是可以的。例如我们由一个文件叫myMakefile，同样可以使用它：

```make -f myMakefile ```  【-f 选项的作用是把名字"myMakefile"作为makefile来对待。】