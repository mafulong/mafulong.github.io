---
layout: post
category: AWS
title: AWS Overall
tags: AWS
---

## Cloud Notes

IaaS、PaaS 和SaaS 的区别： 基础设施即服务(IaaS) 为云服务提供硬件，其中包括服务器、网络和存储。 平台即服务(PaaS) 除了提供IaaS 可提供的所有硬件之外，还提供操作系统和数据库。 软件即服务(SaaS) 提供了最多的支持，即为您的最终用户提供除其数据之外的所有服务。

[参考](https://www.zhihu.com/question/20387284)

如果你是一个网站站长，想要建立一个网站。不采用云服务，你所需要的投入大概是：买服务器，安装服务器软件，编写网站程序。

现在你追随潮流，采用流行的云计算，

如果你采用IaaS服务，那么意味着你就不用自己买服务器了，随便在哪家购买虚拟机，但是还是需要自己装服务器软件

而如果你采用PaaS的服务，那么意味着你既不需要买服务器，也不需要自己装服务器软件，只需要自己开发网站程序

如果你再进一步，购买某些在线论坛或者在线网店的服务,这意味着你也不用自己开发网站程序，只需要使用它们开发好的程序，而且他们会负责程序的升级、维护、增加服务器等，而你只需要专心运营即可，此即为SaaS。



## AWS Overall Notes

云从业者Note: https://github.com/Matthewow/AWS-CLF-StudyNotes



很好overall: https://www.zhihu.com/question/22314873



云的基础是计算、存储、网络，这三部分涵盖了互联网应用的各个方面，所有的云服务也是围绕这三部分去展开。



AWS的服务是按照region来划分的，在部署自己的应用之前，需要选择region，比如美国有us-west, us-east regions, 中国有cn-north, cn-west regions。基本上按照服务用户所在的区域来选择region，服务中国的用户就选择中国的region，服务美国的用户就选择美国的region。否则这个网络传输的成本就非常高，而且中国区其独有的网络环境，导致其他地区的服务是无法访问的。一个region又划分为多个AZ (availability zone), 一般情况下，我们需要把服务器均匀分布在多个AZ，为了避免单点故障，也就是我们所说的灾备多活。



选择好region后，就需要部署自己的[VPC](https://link.zhihu.com/?target=https%3A//console.aws.amazon.com/vpc/home) (virtual private cloud)，一个VPC定义了一个私有隔离的网络环境。在VPC里面，我们部署所有的计算、网络资源。计算资源就是我们的服务器，AWS最出名的就是[EC2](https://link.zhihu.com/?target=https%3A//console.aws.amazon.com/ec2) (elastic compute cloud)。在部署EC2时，我们首先预估应用需要消耗的计算资源(cpu，磁盘，带宽等等)，选择EC2的型号和数量。然后将所有的EC2分割成多个[ASG](https://link.zhihu.com/?target=https%3A//console.aws.amazon.com/ec2autoscaling/home) (auto scaling group), 一个ASG就相当于一个可弹性收缩的机器群，只要定义好扩容和缩容的指标，ASG就可以自己分配机器的数量。比如我们要求在EC2 CPU升到40%就扩容一倍，在CPU降到10%就缩容一倍，这样一个ASG里面机器CPU的消耗就一直均衡地保持在20%左右。具体分割成几个ASG，一般依据这个region有几个AZ来定，比如[us-east-1 region](https://www.zhihu.com/search?q=us-east-1+region&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A2333079486})有3个AZ，就分割成三个ASG，一个AZ部署一个ASG，这三个ASG在接受流量方面没有任何区别。接下来就是网络资源，每个VPC都有自己的ACL(acess control list)，一个ACL定义了inbound rules和outbound rules，分别限制了访问IP的限制和访出IP的限制。VPC的网络资源被划分成多个子网subnets，一个subnet是一组IP地址的集合，前面说到的ASG就部署在[subnet](https://www.zhihu.com/search?q=subnet&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A2333079486})里面。一般来说subnet的数据量跟region AZ的数据成正比，每个AZ分配一个public subnet和一个private subnet，那么us-east-1的VPC就会有6个subnets。我们将ASG部署在private subnet里面，只允许vpc内部的IP访问，用于保护机器资源。因为public subnet是对外的，所以我们在public subnet里面部署ELB (elastic load balancer)，用于接受vpc外的请求。有人会问如果我们想登录到ASG的EC2上面，应该怎么做？解决办法是在public subnet里面launch一个跳板机，我们先登录到跳板机，然后从跳板机里面登录到EC2上面。

接下来就是存储资源，AWS提供多种选择，我们最熟悉的应该就是[S3](https://link.zhihu.com/?target=https%3A//s3.console.aws.amazon.com/s3/home) (simple storage service)。S3是面向对象存储的服务，可以用来做数据归档、备份、恢复，或者作为数据分析、AI、Machine learning的数据湖来使用。通俗的理解就是我们的磁盘，它存储的key就是一个目录路径，相当于磁盘的目录，value是一个object，相当于文件或者子目录。在线的存储根据功能的不同也有很多选择，比较出名的而且是我用过的有三个。第一个是[DynamoDB](https://link.zhihu.com/?target=https%3A//console.aws.amazon.com/dynamodb/home)，它是document-based NoSQL DB。DynamoDB是Amazon内部使用最频繁的数据，几乎90%的存储都会选择DynamoDB，绝对地超过RDS。这个现象的原因在这篇文章[Dynamo: Amazon’s Highly Available Key-value Store](https://link.zhihu.com/?target=https%3A//www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)里面有解释，同时DDIA (Design [data-intensive application](https://www.zhihu.com/search?q=data-intensive+application&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A2333079486})) 这本书也给了同样的解释。总结就是：Amazon内部的存储90%以上都是单对多的关系，DynamoDB作为一个分布式的key-value DB，在可用性、扩展性方面非常适合这种单对多的存储结构。而且DynamoDB是最终一致性，进一步增加了它的可用性。关于DynamoDB我后面会单独出一篇介绍它的blog。而对于多对多的存储，我们就会用[RDS](https://link.zhihu.com/?target=https%3A//console.aws.amazon.com/rds) (relational database service)，RDS字面理解就是[关系型数据库](https://www.zhihu.com/search?q=关系型数据库&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A2333079486})。AWS RDS上面托管了多种关系型数据库，包括mysql、oracle、MS SQL、aurora、MariaDB和PostgreSQL这六种数据库，其中我使用过mysql和aurora。在Amazon内部，[aurora](https://link.zhihu.com/?target=https%3A//docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html)使用的更频繁，它是兼容mysql和PostgreSQL的结合体，具体内容可见这篇文章[Amazon Aurora: Design Considerations for High Throughput Cloud-Native Relational Databases](https://link.zhihu.com/?target=https%3A//www.allthingsdistributed.com/files/p1041-verbitski.pdf)。我使用的最后一种存储是[AWS elasticsearch](https://link.zhihu.com/?target=https%3A//console.aws.amazon.com/esv3/home) ，当时为了实现一个搜索功能，因为涉及到模糊匹配，全文搜索，就采用了[aws es](https://www.zhihu.com/search?q=aws+es&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A2333079486})。aws es跟主流的es已经分道扬镳，目前在aws上面称为openSearch service。

介绍完计算、网络、存储，接下来我想从应用的角度，讲讲在实际应用中，我们应该怎样使用AWS的服务。首先说消息队列，这个广泛应用的基础功能，AWS提供了[SQS](https://link.zhihu.com/?target=https%3A//console.aws.amazon.com/sqs/v2/home)和[SNS](https://link.zhihu.com/?target=https%3A//console.aws.amazon.com/sns/v3/home)。SQS是一个分布式的队列消息service，SNS是一个分布式的发布-订阅消息service。具体有人会问这两者有什么区别，这里给出了回答: [What is the difference between Amazon SNS and Amazon SQS?](https://link.zhihu.com/?target=https%3A//stackoverflow.com/questions/13681213/what-is-the-difference-between-amazon-sns-and-amazon-sqs)。 在我的实践中，SQS和SNS会结合起来使用，首先应用发布消息到SQS的queue里面，然后SNS消费这个queue的消息，放到自身的topic里面持久保存，然后其他的应用订阅这个topic，消费里面的消息。



建设完一个应用，然后就是DevOps。AWS在[托管代码](https://www.zhihu.com/search?q=托管代码&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A2333079486})、编译代码、部署应用、监控应用方面也提供了一整套服务，从前到后，[codeCommit](https://link.zhihu.com/?target=https%3A//console.aws.amazon.com/codesuite/codecommit) -> [codeArtifact](https://link.zhihu.com/?target=https%3A//console.aws.amazon.com/codesuite/codeartifact) -> [codeBuild](https://link.zhihu.com/?target=https%3A//console.aws.amazon.com/codesuite/codebuild) -> [codeDeploy](https://link.zhihu.com/?target=https%3A//console.aws.amazon.com/codesuite/codedeploy) -> [codePipeline](https://link.zhihu.com/?target=https%3A//console.aws.amazon.com/codesuite/codepipeline)。这一套实现了应用的continuous integration和continuous deployment。在监控方面，AWS提供了[cloudWatch](https://link.zhihu.com/?target=https%3A//console.aws.amazon.com/cloudwatch)，可以以应用维度收集日志，视图化监控指标。AWS还提供了一个服务叫cloudFormation，这个服务在应用迁移的过程中，非常有用。Amazon内部很多都是国际化业务，应用需要部署到各个region。cloudFormation以yaml文本的形式记录下一个应用涉及到的各个服务资源配置，放在一个template里面。迁移到不同的region时，只需要一键run coudFormation template, 就可以部署好所有的AWS资源。



Notes:

- region: 包含多个AZ， named by location 用aws需要选个region

- AZ: availability zone. 包含一主多从的cluster，多个data center， 可以有另一个AZ继续保持主从。 region分多个AZ主要是为了容灾。

- region ---> AZ ----> data center 都是一对多。 一般情况下，region之间不会保持同步，互相独立，除非客户允许。

  

![image-20220930233334175](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202209302333289.png)



- 选择region考量: compliance, latency, price, service availability

## 术语

- IAM: identify and access management.  同account也是aws account level, account每月会进行计费，可以任意region里创建资源， work globally.  像s3等存储都是region level. EC2等就是AZ level. 意味着一个ec2不能分布在两个AZ。 IAM可以创建用户，然后授予权限给某个group

- SQS: simple queue service

- SNS: simple notification service. 发一些同事用的，比如发短信等。

- Aws route 53是 aws DNS

- Amazon CouldFront 是CDN

- 对象存储

  - S3: simple storage service

- cloudwatch for monitoring

- ELB: elastic load balancer

- EC2是 virtual machines. 全称: elastic compute cloud. 一共三种compute资源: vm, container services, serverless

- AMI: amazon machine image 就是一堆配置，比如什么系统，安装哪些附加软件。可使用AMI启动一个同配置的实例。 类似docker的image

- AWS Elastic Beanstalk 是一个应用程序管理平台，可以帮助客户轻松部署和扩展 Web 应用程序和服务。它将构建块（例如 EC2、Amazon RDS、Elastic Load Balancing、AWS Auto Scaling 和 Amazon CloudWatch）的预置、应用程序的部署、运行状况监控从用户身上分离出来，让用户可以集中精力编写代码。您只需指定要部署的容器映像、CPU 和内存要求、端口映射和容器链接即可。

  Elastic Beanstalk 将自动处理所有的具体事务，包括预置 Amazon ECS 集群、均衡负载、自动扩展、监控以及在集群中放置容器。如果您希望利用容器的各种优势，但只想通过上传容器映像，在开发到生产等环节部署应用程序时享受到简易性，则 Elastic Beanstalk 非常适合。如果您需要对自定义应用程序架构进行更多精细化的控制，则可以直接使用 Amazon ECS。

- EBS: elastic block store. EC2也需要本地存储，这就是EBS 块存储。例如SSD等。它是外部挂载形式提供的，实例关机了，数据也还在，也可以做备份。适合那种临时数据，而非长期存储。一次只能挂载到一个AZ里的一个实例。 如果想多个实例连一个存储，可以用EFS/FSx， 前者linux，后者windows。



![image-20220930235011369](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202209302350393.png)

![image-20220930234951120](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202209302349145.png)

![image-20220930234939946](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202209302349976.png)

![image-20220930235109632](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202209302351656.png)



## Example: build an application like facebook ,a social media app.  

AWS介绍视频: [youtube](https://www.youtube.com/watch?v=Z3SYDTMP3ME&ab_channel=AWSTrainingCenter)



![image-20221001104944376](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202210011049445.png)



![image-20221001110948079](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202210011109118.png)



![image-20221001144122955](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202210011441985.png)



加一些安全组件，IAM负责每个附件是否可访问，account管理范围等。 KMS负责数据的加密。 ACM负责access certificate management, 比如https证书等，在ELB这块。 WAF是防火墙，比如防止Ddos攻击之类的，在elb之前。Inspectoer负责监控每个service的安全，类似容器里一个agent。 



![image-20221001150745631](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202210011507662.png)



codeCommit类似github这样代码仓库。



## 考证

[参考](https://zhuanlan.zhihu.com/p/138652055)

先考**AWS Certified Solutions Architect - Associate**  AWS 认证助理级解决方案架构师考试，这门考试更注重 AWS 的架构设计。助理级解决方案架构师需要基本了解 AWS 的几个基础的组件，比如 EC2,VPC, IAM, S3, Route53 等，掌握它们分别是什么，使用场景是什么，和传统数据中心的区别和优势等等



云从业者那个可以看这个： https://github.com/Matthewow/AWS-CLF-StudyNotes





## 对象存储: S3及S3 Glacier

> [官网](https://aws.amazon.com/s3/storage-classes/)

Amazon S3 is object-level storage, which means that if you want to change a part of a file, you have to make the change and then re-upload the entire modified file. 对象存储，比较像字节的TOS。 也是以bucket隔离的，然后bucket可设置是否公开，可设置每个文件多版本， 可作为一个静态博客的host。 [对象存储参考](https://mafulong.github.io/2022/10/06/%E5%9D%97%E5%AD%98%E5%82%A8%E5%92%8C%E5%AF%B9%E8%B1%A1%E5%AD%98%E5%82%A8%E5%92%8C%E6%96%87%E4%BB%B6%E5%AD%98%E5%82%A8/)

Amazon S3 Glacier is a great storage choice when low storage cost is paramount, your data is rarely retrieved, and retrieval latency of several hours is acceptable. If your application requires fast or frequent access to your data, consider using Amazon S3. Objects stored in Amazon S3 Glacier are called *archives*. 相比s3，价格便宜，适合平时不太访问的归档数据。



## 计算层：EC2



3种付费方案：

1. on-demand, 运行时收费，按秒计费，价格固定。
2. Reserved instances. (RIs)  预订 选定期的，有折扣。这种情况下即便选择不预付，非运行时也算收费。 它需要绑定一个instance type.
3. Spot instances.  类似出钱，然后aws自己评估这价格可以给几个实例这样。如果不够就掐掉实例。是最便宜的，但需要容忍突然停。

Dedicated hosts: 把物理机控制也给你，贵。和其他公司隔离开。



## 数据库

RDB: Amazon RDS, Redshit, Aurora.

NoSQL: DynamoDB, Nepture, ElastiCache





## IAM



IAM (Identity Access Management) 由这些东西组成：

- Users
- Groups 用户组
- Roles 角色可以分配给AWS服务，让AWS服务有访问其他AWS资源的权限。  举个例子，我们可以赋予EC2实例一个角色，让其有访问S3的读写权限（后面课程会有关于这一点的实操）
- Policy Documents 策略。 策略具体定义了能访问哪些AWS资源，并且能执行哪些操作（比如List, Read, Write等）  策略的文档以JSON的格式展现

```
// An example policy: allowing any access to any resource
{
  "Version": "2012-10-17"
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}
```



IAM 是 Global的，不属于任何一个 region

Root 账号是你第一次配置账号的时候创建的，它拥有完全的 Admin aceess

新 User 刚创建时是没有权限的。



首先要知道, AWS 提供了许许多多种类的服务或者说资源供我们使用, 这些资源挂在我们的 AWS 账户下, 这个账户就是我们第一次用 AWS 时用邮箱和密码申请的, 以后我们所有的资源申请, 账单费用都会挂到这个户头.

那么 IAM 算什么呢? IAM 不是 AWS 的专有名词, 它是一个通用概念, 全称是 Identity and Access Management, 其要解决的两个问题就是身份认证 (Authtication) 和授权 (Authorization). 为此 AWS IAM 设计了用户, 角色, 用户组, 权限策略等概念和机制



场景

1. 自己公司的员工想访问 AWS Console 查看所在项目组的基础设施
2. AWS 账户里的 EC2/Lambda 实例想访问同账户下的一台 RDS
3. 公网里用户的手机想要访问我们的后端存储(借助 API Gateway)



AWS IAM 并不关心你创建的 IAM User 是给人用还是给程序用



AWS 官方建议 root 用户的唯一用途, 就是[用来创建你的第一个 IAM 用户](https://link.zhihu.com/?target=https%3A//docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html%23lock-away-credentials), 把这第一个 IAM 用户设置为管理员, 然后以后的工作都用这个管理员用户来进行.



## SNS vs SQS

AWS提供了[SQS](https://link.zhihu.com/?target=https%3A//console.aws.amazon.com/sqs/v2/home)和[SNS](https://link.zhihu.com/?target=https%3A//console.aws.amazon.com/sns/v3/home)。SQS是一个分布式的队列消息service，SNS是一个分布式的发布-订阅消息service。具体有人会问这两者有什么区别，这里给出了回答: [What is the difference between Amazon SNS and Amazon SQS?](https://link.zhihu.com/?target=https%3A//stackoverflow.com/questions/13681213/what-is-the-difference-between-amazon-sns-and-amazon-sqs)。 在我的实践中，SQS和SNS会结合起来使用，首先应用发布消息到SQS的queue里面，然后SNS消费这个queue的消息，放到自身的topic里面持久保存，然后其他的应用订阅这个topic，消费里面的消息。



sqs是一对一，不能一对多，消息可持久化，不推只能等拉，拉完就删除。

sns可一对多，不能持久化，push模型。

sqs及aws笔记，更全， [link](http://www.cloudbin.cn/?p=2530)
