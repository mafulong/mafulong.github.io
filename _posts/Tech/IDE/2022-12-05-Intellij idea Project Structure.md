---
layout: post
category: IDE
title: Intellij idea Project Structure
tags: IDE
---

## Intellij idea Project Structure

mac上cmd+; 快捷键唤醒。File菜单栏也可以唤醒。

## Project和Module区别

一个Project代表一个完整的APP，Module表示APP中的一些依赖库或独立开发的模块。比如可以新建一个library做为module。

一个模块为一个Module。





## Language level和sdk区别

> 限定项目编译检查时最低要求的 JDK 特性。 Language level <= sdk。

当我们使用 JDK 8 的时候，我们只能向下兼容 JDK 8 及其以下的特性，所以只能选择 8 及其以下的 `language level`。所以当我们项目使用的是 JDK 8，但是代码却没有使用 JDK 8 的新特性，最多使用了 JDK 7 的特性的时候我们可以选择 `7 - Diamonds，ARM，multi-catch etc.`。

对此我们总结 `language level`：限定项目编译检查时最低要求的 JDK 特性。

现在假设我们有一个项目代码使用的 JDK 8 新特性：`lambda` 语法，但是 JDK 选择的却是 JDK 7，即使 `language level` 选择了 `8 - Lambdas，type annotation etc.`，也是没有多大意义的，一样会编译报错。



## Project Structure设置

![img](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202212052232428.png)

Project 项目级别的，下面每个Module还可以自己有

- Project Name
- SDK
- Language level
- 编译输出路径



Modules

![img](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202212052235310.png)

- Souces：这里对Module的开发目录进行文件夹分类，就是说这个module里有什么内容，说明了不同性质的内容放在哪里。
  注意，这些不同内容的标记代表了一个标准Java工程的各项内容，IntelliJ就是根据这些标记来识别一个Java工程的各项内容的，比如，它会用javac去编译标记为Sources的源码，打包的时候会把标记为Resources的资源拷贝到jar包中，并且忽略标记为Exluded的内容。左边显示的是在选中内容的预览。
- Paths：为模块配置编译器输出路径，还可以指定与模块关联的外部JavaDocs和外部注释的位置。
- Dependencies：在此选项卡上，您可以定义模块的SDK并形成模块依赖关系列表。要将项目SDK与模块相关联，请选择Project SDK。请注意，如果稍后更改了项目SDK，模块SDK将相应更改。**需要保证Dependencies下Add Library时为空，如果有就都Add selected.**



Library

- 项目级别的类库，这里先加好，然后Module里加jar的话就可以直接选了，相当于统一管理。



Facets

![img](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202212052245804.png)

- 表示这个 module 有什么特征，比如 Web，Spring 和 Hibernate 等； 





Artifact

![img](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202212052248695.png)

- Artifact 是 maven 中的一个概念，表示某个 module 要如何打包，例如 war exploded、war、jar、ear 等等这种打包形式；
  一个 module 有了 Artifacts 就可以部署到应用服务器中了！
  在给项目配置 Artifacts 的时候有好多个 type 的选项，exploed 是什么意思？
  explode 在这里你可以理解为展开，不压缩的意思。也就是 war、jar 等产出物没压缩前的目录结构。建议在开发的时候使用这种模式，便于修改了文件的效果立刻显现出来。默认情况下，IDEA 的 Modules 和 Artifacts 的 output 目录 已经设置好了，不需要更改，
  打成 war 包 的时候会自动在 WEB-INF 目录 下生产 classes 目录 ，然后把编译后的文件放进去。

**最上面的截图下面Platform Settings和Project, Module都无关！**



添加一个Lib方法

1. 方法1： 更推荐。在project structure的Libraries加入lib，然后再走方法2，选择Project Lib即可。
2. 方法2： 在Modules的Dependencies下添加lib

