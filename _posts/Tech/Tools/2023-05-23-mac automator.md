---
layout: post
category: Tools
title: mac automator
tags: Tools
---

# mac automator

Automator允许你选择八中不同类型的行为（Action）：





- 工作流（Workflow）：最简单的形式，是一个在Automator内部运行的文件；
- 应用程序（Application）：比较常用的形式，允许你创建一个单独的App，并且可以将文件拖到其图标上触发相应动作；
- 服务（Service）：在服务菜单中创建一个流程，从当前应用程序或Finder接收文本或文件；
- 打印插件（Print Plugins）：在任何应用程序的打印界面中接收将要被打印文件的PDF文件，并且对其进行工作流处理；
- 文件夹（Folder）：赋给Finder文件夹的工作流程，对文件夹中的文件执行工作流程操作；
- 日历提醒（Calendar Alarms）：由日历中的事件触发相应工作流，不接收任何输入；
- 图像捕捉插件（Image Capture Plug-ins）：在“图像捕捉”中可用的工作流程，它们将图像文件作为输入用来接收；
- 听写命令（Dictation Commands）：可以将一些命令直接“说”给Mac，然后执行相应工作流。

## 工作流编辑

![image-20230523130455587](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202305231305381.png)

左边是一些可以选的action，选中拖拽到右边即可。



工作流操作以主窗口中的排列顺序来线性执行，每一步的输出都是下一步操作的输入，因此你需要确保每一个操作的顺序排列是正确的。在测试的时候，你可以点击工具栏中的“步进”按钮来一步一步的跟踪调试。如果需要执行从头至尾的完整流程，则点击“运行”按钮。



工作流可以在不接收任何输入的条件下运行，当然你也可以创建一个工作流提示需要的输入信息。



## Automator变量

如果以上就是Automator所能够做的，那已经很强大了。但还可以更强大。比如说变量栏，允许你将其中一个步骤的输出保存下来，然后可以往后面的步骤传下去。举个例子，你可以创建一个工作流获取网页上的复制文本，然后保存，继而可以在后续的Email操作步骤中，将复制文本赋给Email中的正文部分。或者可以抓取一个网页的URL地址然后传给文本文件。



## automator删除

默认在这个文件夹

```scala
/System/Volumes/Data/Users/mafulong/Library/Services
```

不知道在哪就 根目录下

```scala
find / -name "*.workflow"
```





# automator例子

## 实现一个截图工具自动上传

创建类型： 快速操作。

输入: no input

选择action: 运行shell

然后shell里就

1. 创建文件

```scala
#!/bin/bash

filename=$(cat /dev/urandom | env LC_CTYPE=C tr -cd 'a-zA-Z0-9' | head -c 10).png
filename=$(date +'%Y-%m-%d_%H-%M-%S')_$filename
# echo $filename
fullname=/tmp/$filename
```

2. 截图, 保存到文件里

```scala
if screencapture -i $fullname; then
	xxx
fi
```



1. curl上传文件
2. 删除创建的随机文件。
3. 设置剪贴板。比如

```scala
echo $url | pbcopy
```



mac系统设置里的快捷键选general然后选中创建好的工作流，设置快捷键。





# mac快捷指令

是新mac系统支持的一个操作。可以在菜单栏显示快捷指令。

可以将automator的导入进来。

[参考](https://www.huxiu.com/article/441978.html)

