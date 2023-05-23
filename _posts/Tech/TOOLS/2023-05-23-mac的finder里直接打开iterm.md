---
layout: post
category: Tools
title: mac的finder里直接打开iterm
tags: Tools
---

## mac的finder里直接打开iterm

github repo: https://github.com/mafulong/openWithIterm



在mac finder里使用iterm打开当前目录

- 打开Script Editor
- 新建文件
- 输入以下内容

```scala

tell application "Finder"
	set pathList to (quoted form of POSIX path of (folder of the front window as alias))
end tell

tell application "System Events"
	if not (exists (processes where name is "iTerm2")) then
		do shell script "open -a iTerm " & pathList
	else
		tell application "iTerm"
			do shell script "open -a iTerm "
			activate
			tell current session of current window
				write text "cd " & pathList
			end tell
			
		end tell
	end if
end tell
```

- 文件 -> 导出。选择应用程序，勾选仅运行。

![image-20230523145416151](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202305231508359.png)


然后

- finder里cmd+鼠标选中创建的app，拖拽到工具栏。 如果要删除，也是cmd+鼠标拖拽出来进行删除。
- 设置图标和重命名，不需要重新拖拽。设置图标的话，右键->显示简洁。然后用新图拖拽到图标上即可。细节请看参考2。
