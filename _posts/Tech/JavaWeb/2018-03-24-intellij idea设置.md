---
layout: post
category: JavaWeb
title: idea的web开发设置
---

## tomcat运行
把.war后缀的war包放到tomcat的webapps目录下，然后进入tomcat的bin目录下右键cmder输入./startup.bat开启tomcat，在网址中输入“localhost:8080/war包名”

## Project Structure

### library库配置
1. 在project structure的Libraries加入lib
2. 在Modules的Dependencies下添加lib

### Facets配置
表示这个module有什么特征，比如 Web，Spring和Hibernate等

Name：输入该Web Facet的名称,上图用的是Web作为名称，也是默认的名称。

Deployment Descriptors：在这部分，管理应用的部署描述符。

---- Type：只读字段，展示部署描述符类型。各自依赖的facet类型有：Web Module Deployment Descriptor、EJB Module Deployment Descriptor、 Application Module Deployment Descriptor

---- Path：只读字段，展示部署描述符的位置。各自部署描述符有：web.xml,ejb.xml, or application.xml

Web Resource Directories：在这部分，我们将第三方或未分类资源路径映射到部署根目录。

---- Web Resource Directory ：只读字段，展示所需的Web Resource位置的本地目录。Web Resource目录包含Web开发所需的文件：JSP、HTML、XML等。Web Resource目录下的内容会被拷贝到由Relative Path所指定的Web模块部署目录。

---- Path Relative to Deployment Root：只读字段，展示Web Resource相对于Web部署的根目录的相对路径。
![](https://i.imgur.com/ORR3pIf.png)

### Artifacts
在给项目配置Artifacts的时候有好多个type的选项，exploed是什么意思：

explode 在这里你可以理解为展开，不压缩的意思。也就是war、jar等产出物没压缩前的目录结构。建议在开发的时候使用这种模式，便于修改了文件的效果立刻显现出来。

默认情况下，IDEA的 Modules 和 Artifacts 的 output目录 已经设置好了，不需要更改，打成 war包 的时候会自动在 WEB-INF目录 下生产 classes目录，然后把编译后的文件放进去。

![](https://i.imgur.com/DiLnx7B.png)

### Modules

![](https://i.imgur.com/kecXB8e.png)


## 参考链接
[理解 IntelliJ IDEA 的项目配置和Web部署](https://www.cnblogs.com/deng-cc/p/6416332.html)

[IDEA里面的facets和artifacts的讲解](https://www.cnblogs.com/poilk/p/6529347.html)