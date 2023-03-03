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



## ECS

**Amazon Elastic Container Service (ECS)**是一个有高度扩展性的**容器管理服务**。它可以轻松运行、停止和管理集群上的Docker容器，你可以将容器安装在EC2实例上，或者使用**Fargate**来启动你的服务和任务。

Amazon ECS可以在一个区域内的多个可用区中创建高可用的应用程序容器，你可以定义集群中运行的Docker镜像和服务。而且你可以充分利用AWS内部的**Amazon ECR (Elastic Container Registry)**或者外部的Registry（比如Docker Hub或自建的Registry）来存储和提取容器镜像。



我们可以将标准化的代码、运行环境、系统工具等等打包成一个标准的集装箱，这个集装箱叫做**Docker镜像**（Docker Image）。这个Docker镜像的概念类似于EC2中的AMI (Amazon Machine Image)。

这些镜像文件通常会通过Dockerfile来构建，并且最终存放到**注册表（Registry）**内。这个Registry可以理解为摆放集装箱的码头，我们在需要某个类型的集装箱的时候就到码头去取。这类Registry可以是Amazon的ECR，也可以是公网上的Docker Hub，或者自己私有的Registry。



![img](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202211192204245.png)

### ECS创建举例

![img](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202211192208630.png)



## Lambda

使用**AWS Lambda**，你无需配置和管理任何服务器和应用程序就能运行你的代码。只需要上传代码，Lambda就会处理运行并且根据需要自动进行横向扩展。因此Lambda也被称为**无服务（Serverless）**函数。

要让AWS Lambda的代码执行，需要设定一些触发器（比如CloudWatch Log，CloudWatch Event，API Gateway等），因此Lambda函数被认为是**事件驱动的（Event-Driven）**。

在传统的应用部署过程中，我们往往需要安装操作系统 -> 安装应用程序 -> 配置环境并部署代码，而且往往还需要不定时地为操作系统和应用程序打补丁和进行维护。使用AWS Lambda就方便很多，只需要上传代码，AWS就会在需要的时候帮你运行。我们不再需要（也无法接触）任何操作系统层面的东西，也节省了非常多的部署时间，可以更专心地编写代码。



### AWS Lambda的特点

- 没有服务器/无服务，或者说真实的服务器由AWS管理
- 只需要为运行的代码付费，不需要管理服务器和操作系统
- **持续性/自动的性能伸缩**
- 非常便宜
- AWS只会在代码运行期间收取相应的费用，代码未运行时不产生任何费用
- **代码的最长执行时间是15分钟，如果代码执行时间超过15分钟，则需要将1个代码细分为多个**

### 触发器有哪些

- **API Gateway**
- **AWS IoT**
- **CloudWatch Events** 比如cron job定时任务
- CloudWatch Logs
- CodeCommit
- DynamoDB
- S3
- SNS
- Cognito Sync Trigger
- SQS应该也可以？



## 参考

[参考](http://www.cloudbin.cn/?tag=aws)

## Compute选型

aws提供两种容器编排服务： ECS和EKS, k是kubernetes。 后者适合已经用了k8s的。

AWS fargate就是serverless,  ECS/EKS 可集成在Fargate上或者EC2上。 container hosting platform

Serverless: 允许在服务部署级别而不是服务器部署级别来管理应用部署。类似Faas。无需关注主机管理，服务运维。



ECS vs EC2

- ECS和EKS: aws负责容器管理，但customer依旧需要负责底层的ec2 instances.

Fargate vs Lambda

- Fargate is a Container as a Service (CaaS) offering, AWS Lambda is a Function as a Service (FaaS offering). 

Fargate是类似k8s的工具，可以管理容器，进行编排。

ECS vs Fargate

- ECS delivers more control over the infrastructure, but the trade-off is the added management that comes with it. Fargate is the better option for ease of use as it takes infrastructure management out of the equation allowing you to focus on just the tasks to be run. ECS 提供了对基础设施的更多控制，但代价是随之而来的附加管理。Fargate 是易于使用的更好选择，因为它将基础设施管理排除在外，使您可以专注于要运行的任务。



Serverless vs EC2/ECS:

- If you want to deploy your workloads and applications without having to manage any EC2 instances, you can do that on AWS with serverless compute.
- Serverless includes fargate, lambda.



Serverless vs Lambda

- the latter doesn't need the control of container



两个方面

- 是否要管理主机
  - Yes: ecs, ec2
  - No: fargate, lambda
- 是否要管理容器,类似k8s的活。
  - Yes: fargate, ecs, ec2.
  - No: lambda





虚拟机相比容器好处，重要的是资源隔离。

- 拥有完整操作系统
- 异质环境
- 安全

容器好处：

- 速度和可移植性，启动只有几秒钟，虚拟机要几分钟
- 可扩展性，通过编排器，自动扩展。
- 模块化
- 易于更新。