---
layout: post
category: IDE
title: IDEA之codeNotes
tags: IDE
---

## IDEA之codeNotes

这是一款笔记插件，支持笔记的存储，管理，导入，导出等。支持添加图片作为笔记的附件

- 使用三级目录来存储和管理笔记:
  笔记本 > 章节 > 笔记
- 精简视图: 适合小屏幕
- 完整视图: 适合大屏幕;显示更直观,拖拉操作更方便
- 笔记本工具窗口列表中的条目,支持上下拖动来改变的位置。
- 移动章节: 拖动章节条目到另一个的笔记本条目上。
- 移动笔记: 拖动笔记条目到另一个的章节条目上。
- 在编辑器使用弹出菜单项(上下文菜单项)收藏到笔记本可以把选择的代码或文字存储为笔记。
- 在编辑器使用弹出菜单项(上下文菜单项)插入笔记内容可以把选择的笔记内容插入到编辑器。
- 笔记本的工具窗口上的按钮导出 JSON/导入 JSON支持导入或者导出笔记。
- 笔记本的工具窗口上的按钮导出 Markdown支持把选择的笔记导出为Markdown格式。
- File | Settings | Tools | 笔记本: 支持自定义Markdown模板。

Plugin: [link](https://plugins.jetbrains.com/plugin/16998-notebook)

自己fork了这个，然后稍微改了下。github地址:  [link](https://github.com/mafulong/Notebooks)

## 使用

下载jar包，idea里安装即可。

选择代码然后右键，上面两个选项就是记录到notebook的。

点击toolbar的notebook也可以查看当前的note.

## 插件开发

目前

- java11
- gradle 6.7 不用提前安,idea有

1. git clone
2. idea开发，设置sdk为opensdk java11
3. 点进build.gradle的run-ide进行本地测试。它就是起了个新idea只有你这个插件，然后你手动测试。

## 生成plugin的jar包

intellij里的buildPlugin是不包含的dep jar包的，用不了

run shadowJar这个命令。

