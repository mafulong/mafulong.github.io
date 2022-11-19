---
layout: post
category: AWS
title: AWS Compute
tags: AWS
---

## AWS Compute

## AMI

AMI: amazon machine image 就是一堆配置，比如什么系统，安装哪些附加软件。可使用AMI启动一个同配置的实例。 类似docker的image

**Amazon Machine Image (AMI)** 是亚马逊AWS提供的系统镜像，这个AMI包含了如下的信息：

- 由实例的操作系统、应用程序和应用程序相关的配置组成的模板
- 一个指定的需要在实例启动时附加到实例的卷的信息（比方说定义了使用8 GB的General Purpose SSD卷）

下图所示的是AMI的生命周期，你可以创建并注册一个AMI，并且可以使用这个AMI来创建一个EC2实例。同时你也可以将这个AMI复制到同一个AWS区域或者不同的AWS区域。你同样也可以注销这个AMI镜像。

![img](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202211182358363.png)

- **AMI是区域化的**，只能使用本区域的AMI来创建实例；但你可以将AMI从一个区域复制到另一个区域





## 弹性伸缩（Auto Scaling）

**亚马逊弹性伸缩（Auto Scaling）**能**自动地**增加/减少EC2实例的数量，从而让你的应用程序一直能保持可用的状态。

你可以预定义Auto Scaling，使其在需求高峰期自动增加EC2实例，而在需求低谷自动减少EC2实例。这样不仅能让你的应用程序一直保持健康的状态，而且也节省了你为EC2实例所付出的费用。

Auto Scaling 适用于那些需求稳定的应用程序，同时也适用于在每小时、每天、甚至每周都有需求变化的应用程序。

- Auto Scaling能保证你一直拥有一定数量的EC2实例来分担应用程序的负载
- Auto Scaling能带来更高的容错性、更好的可用性和更高的性价比
- 你可以控制伸缩的策略来决定在什么时候终止和创建EC2实例，以处理动态变化的需求
- 默认情况下，Auto Scaling能控制每一个可用区内所运行的实例数量尽量平均
  - 为了达到这个目标，Auto Scaling在需要启动新实例的时候，会选择一个目前拥有运行实例最少的可用区

Auto Scaling的构成组件：

![img](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202211190006430.png)

### 启动配置（Launch Configuration）

- 启动配置是弹性伸缩组用来启动EC2实例的时候所使用的模板
- 启动配置包含了镜像文件（AMI），实例类型、密钥对、安全组和挂载的存储设备
- 一个启动配置可以关联多个Auto Scaling组
- **启动配置一经创建不能被更改，只能删除重建**
- 启动配置中可以使用CloudWatch的基础监控（Basic Monitoring）或者详细监控（Detail Monitoring）
- Auto Scaling automatically creates a launch configuration directly from an EC2 instance.

### 弹性伸缩组（Auto Scaling Group）

- 弹性伸缩组（ASG）是弹性伸缩的核心，它包含了多个拥有类似配置/类型的EC2实例，这些实例被逻辑上认为是一样的
- 弹性伸缩组需要的几个参数：
  - **启动配置（Launch Configuration）**：它决定了EC2使用什么模板，模板内容包括了镜像文件（AMI），实例类型、密钥对、安全组和挂载的存储设备
  - **最小和最大的性能**：决定了在弹性伸缩的情况下，EC2实例数量的浮动范围
  - **所需的性能**：决定了这个弹性伸缩组要保持的运作所需要的基本的EC2实例数量；如果没有填写，则默认为其数值等同于最小的性能
  - **可用区和子网**：定义EC2实例启动时候所在的可用区和子网信息
  - **参数和健康检查**：参数定义了何时启动新实例，何时终止旧实例；健康检查决定了实例的健康状态。
- **如果一个EC2实例的健康状态变成“不健康”，那么ASG会终止这个EC2实例，并且自动启动一个新的EC2实例**
- 弹性伸缩组（ASG）只能在某一个AWS区域内运行，不能跨越多个区域
- 如果启动配置（Launch Configuration）有更新，那么之后启动的新EC2实例会使用新的启动配置，而旧的EC2实例不受影响
- 从AWS管理平台你可以直接删除一个弹性伸缩组（ASG）；从AWS CLI你只能先将最小的性能和需求的性能两个参数设置为0，才能删除这个弹性伸缩组。
