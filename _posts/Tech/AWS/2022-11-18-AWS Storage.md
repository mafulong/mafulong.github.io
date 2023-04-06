---
layout: post
category: AWS
title: AWS Storage
tags: AWS
---

## AWS Storage

## dynamoDB

[论文讲解](http://systemdesigns.blogspot.com/2016/01/dynamodb.html)

[深入探讨 Amazon DynamoDB 的设计模 式、流复制和全局表](https://sides-share.s3.cn-north-1.amazonaws.com.cn/AWS+Webinar+2019/PDF/Amazon+DynamoDB+webinar.pdf)

[官网](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Programming.LowLevelAPI.html#Programming.LowLevelAPI.DataTypeDescriptors)

[AWS 如何实现数据跨区域同步](https://techsummit.ctrip.com/pdf/songye.pdf)

[MongoDB 与 DynamoDB 正面交锋](https://www.modb.pro/db/432414)



## EBS

### EBS的特点

- 亚马逊EBS卷提供了**高可用、可靠、持续性的块存储**，EBS可以依附到一个正在运行的EC2实例上
- 如果你的EC2实例需要使用数据库或者文件系统，那么建议使用EBS作为首选的存储设备
- EBS卷的存活可以脱离EC2实例的存活状态。也就是说在终止一个实例的时候，你可以选择保留该实例所绑定的EBS卷
- EBS卷可以依附到**同一个可用区（AZ）**内的任何实例上
- EBS卷可以被加密，如果进行了加密那么它存有的所有已有数据，传输的数据，以及制造的镜像都会被加密
- **EBS卷可以通过快照（Snapshot）来进行（增量）备份，这个快照会保存在S3 (Simple Storage System)上**
- 你可以使用任何快照来创建一个基于该快照的EBS卷，并且随时将这个EBS卷应用到**该区域**的任何实例上
- EBS卷创建的时候已经固定了可用区，并且**只能给该可用区的实例使用**。如果需要在其他可用区使用该EBS，那么可以创建快照，并且使用该快照创建一个在其他可用区的新的EBS卷
- **快照还可以复制到其他的AWS区域**

### EBS (Elastic Block Storage)小结

- EBS的不同类型，需要了解不同类型的EBS主要的使用场景
  - 通用型SSD – GP2 (高达10,000 IOPS)，适用于启动盘，低延迟的应用程序等
  - 预配置型SSD – IO1 (超过10,000 IOPS)，适用于IO密集型的数据库
  - 吞吐量优化型HDD -ST1，适用于数据仓库，日志处理
  - HDD Cold – SC1 – 适合较少使用的冷数据
  - HDD, Magnetic
- 不能将EBS挂载到多个EC2实例上，一个EBS只能挂载到1个EC2实例上。
  - 如果有共享数据盘的需求，请使用EFS (Elastic File System)
- 根EBS卷默认是不能进行加密的，但可以使用第三方的加密工具（例如BitLocker）对其进行加密
  - *除了根磁盘外的其他卷是可以加密的*

### EBS快照（Snapshot）小结

- *EBS的快照会被保存到S3（Simple Storage System）上*

- *你可以对一个EBS卷创建一个快照，这个快照会被保存到S3上*

- 快照实际上是

  增量备份

  ，只有在上次进行快照之后更改的数据才会被添加的S3上

  - 因此第一次快照所花费的时间比较长
  - 而第二次以后的快照所花费的时间相对短很多

- 对加密的EBS卷创建快照，创建后的快照也会是加密的

- 从加密的快照恢复的EBS卷也会是加密的

- 你可以分享快照给其他账户或AWS市场，但仅限于这个快照是没有进行过加密的

- 要为一个作为根设备的EBS卷创建快照的话，建议停止这个实例再做快照

### 实例存储（Instance Store）

- 实例存储也叫做**短暂性存储（Ephemeral Storage）**
- 实例存储的实例不能被停止（只能重启或终止），如果这个实例出现故障，那么在上面的所有数据将会丢失
- 使用EBS的实例可以被停止，停止后EBS上的数据不会丢失
- 重启使用实例存储的实例或者重启使用EBS的实例都不会导致数据丢失



## AWS EBS, S3和EFS的区别

- AWS S3对于静态页面的托管、多媒体分发、版本管理、大数据分析、数据存档来说都非常有用。S3可以和AWS CloudFront结合使用而达到更快的上传和下载速度。
- AWS EBS是可以用来做数据库或托管应用程序的持续性文件系统，EBS具有很高的IO读写速度并且即插即用。 只能被单个EC2实例访问
- 相比前面两种存储，AWS EFS是比较新的一项服务。它提供了可以在多个EC2实例之间共享的网络文件系统，功能类似于NAS设备。可以用EFS来处理大数据分析、多媒体处理和内容管理。

## S3

Amazon **Simple Storage Service (S3)** 是互联网存储解决方案，它提供了一个简单的Web接口，让其存储的数据和文件在互联网的任何地方给任何人访问。

文件对象存储。



### S3基本特性

- S3是**对象存储**，可以在S3上存储各种类型的文件，它不是**块存储**（EBS是块存储）
- 文件大小可以从0 字节到5 TB
  - 使用Single Operation上传只能上传*最大5 GB*的文件
  - 使用分段上传（Multipart Upload）可以对文件进行分段上传，最大支持上传*5 TB*的文件
- S3的总存储空间是**无限大**的
- 文件存储在**存储桶（Bucket）**内，可以理解存储桶就是一个文件夹
- S3的名字是需要**全球唯一**的，不能与任何区域的任何人拥有的S3重名
- 存储桶创建之后会生成一个URL，命名类似于https://s3-ap-northeast-1.amazonaws.com/aws_xiaopeiqing_com
  - **S3是以HTTPS的形式展现的，而非HTTP**
  - ap-northeast-1表示了当前桶所在的区域
  - aws_xiaopeiqing_com表示了S3存储桶的名字，全球唯一
- S3拥有99.99%（4个9）的可用性（Availability）
  - 可用性可以理解为系统的uptime时间，即在一个自然年内（365天）有52.56分钟系统不可用
- S3拥有99.999999999%（11个9）的持久性（Durability）
  - 持久性可以认为是数据完整性/数据安全性，即在一千亿个存储在S3上的文件会有大概 1 个文件是不可读的
- S3的存储桶创建的时候可以选择所在区域（Region），但不能选择可用区（AZ），AWS会负责S3的高可用、容灾问题
  - S3创建的时候可以选择某个AWS区域，一旦选择了就不能更改
  - 如果要在其他区域使用该S3的内容，可以使用**跨区域复制**
- S3拥有不同的等级（Standard, Stantard-IA, Onezone-IA, RRS, Glacier）
- 启用了**版本控制（Version Control）**你可以恢复S3内的文件到之前的版本
- S3可以开启生命周期管理，对文件在不同的生命周期进行不同的操作
  - 比如，文件在创建30天后迁移到便宜的S3等级（S3-IA），再经过30天进行归档（迁移到Glacier），再过30天就进行删除
- 要启用生命周期管理需要先启用版本控制功能
- S3支持加密功能
- 使用访问控制列表（Access Control Lists）和桶策略（Bucket Policy）可以控制S3的访问安全
- 在S3上成功上传了文件，你将会得到一个**HTTP 200**的状态反馈

### 不同的S3存储类型

- **Standard – 默认的存储类：**如果上传对象时未注明则S3会分配这个类型的存储
- **Standard – IA（Infrequently Accessed）：**用于保存不经常访问的数据，但是需要访问的时候也能很快地访问到。存储的价格比标准S3便宜，但是读取的费用比标准的S3高，也因为如此才要把不经常访问的数据放到这种类型的S3上。并且数据跨了多个AWS地理位置。
- **Intelligent_Tiering** 智能分层（S3 智能分层）: 这种储存类别将对象存储在两个访问层中，一个是频繁访问的层，一个是不频繁访问的层；如果对象`30`天内未访问，则会被移动至不频繁访问的层，如果不频繁访问层中的对象被访问，则会被移动至频繁访问的层；频繁访问的层的存储费用与`STANDARD`一样，不频繁访问层的存储费用与`STANDARD_IA`一样，该储存类别的请求费用与`STANDARD`一样，**该储存类别有额外的监控费用**；
- **Onezone – IA：**同上，但数据只保存到一个AWS可用区内
- **Glacier：**非常便宜，仅用于做归档。从Glacier读取数据需要花费3-5个小时。
- **Glacier Deep Archive:** S3 Glacier Deep Archive 是 Amazon S3 成本最低的存储类，支持每年可能访问一两次的数据的长期保留和数字预留。它是为客户设计的 – 特别是那些监管严格的行业，如金融服务、医疗保健和公共部门 – 为了满足监管合规要求，将数据集保留 7-10 年或更长时间。S3 Glacier Deep Archive 还可用于备份和灾难恢复使用案例，是成本效益高、易于管理的磁带系统替代，无论磁带系统是本地库还是非本地服务都是如此。S3 Glacier Deep Archive 是 Amazon S3 Glacier 的补充，后者适合存档，其中会定期检索数据并且每隔几分钟可能需要一些数据。存储在 S3 Glacier Deep Archive 中的所有对象都将接受复制并存储在至少三个地理分散的可用区中，受 99.999999999% 的持久性保护，并且可在 12 小时内恢复。

## CloudFront CDN

**Amazon CloudFront**是一种全球**内容分发网络（CDN）**服务，可以安全地以低延迟和高传输速度向浏览者分发数据、视频、应用程序和API。



- **边缘站点（Edge Location）**：边缘站点是内容缓存的地方，它存在于多个网络服务提供商的机房，它和AWS区域和可用区是完全不一样的概念。截至2018年中，AWS目前一共有100多个边缘站点。
- **源（Origin）**：这是CDN缓存的内容所使用的源，源可以是一个S3存储桶，可以是一个EC2实例，一个弹性负载均衡器（ELB）或Route53，甚至可以是AWS之外的资源。
- **分配（Distribution）**：AWS CloudFront创建后的名字
- 分配分为两种类型，分别是
  - **Web Distribution**：一般的网站应用
  - **RTMP (Real-Time Messaging Protocol)**：媒体流
- 你不只是可以从边缘站点读取数据，你还可以往边缘站点写入数据（比如上传一个文件），边缘站点会将你写入的数据同步到源上
- 在CloudFront上的文件会被缓存在边缘节点，缓存的时间是**TTL（Time To Live）**。文件存在超过这个时间，缓存会被自动清除
- 如果在到达TTL时间之前，你希望更新文件，那么你也可以**手动清除缓存**，但你将会被AWS**收取一定的费用**

## ES

AWS ES有两种node

1. decicated master node 数量只能3-5。Dedicated Master 节点不太可能成为性能瓶颈，因为它们主要负责管理集群状态和协调分片分配等任务，并不会直接处理客户端的读写请求。相反，数据节点才是 AWS ES 集群中的性能瓶颈，因为它们需要实际检索和处理文档数据，对系统资源的消耗较大。
2. 普通node，和es一样。

每个node都有存储的一个限制。node数量增加，则性能增加。

## Multi-AZ高可用

是多个AZ里配置一个主，其它从，类似同城多机房架构。



我们可以把AWS RDS数据库部署在多个**可用区（AZ）**内，以提供高可用性和故障转移支持。

使用Multi-AZ部署模式，RDS会在不同的可用区内配置和维护一个主数据库和一个备用数据库，主数据库的数据会自动复制到备用数据库中。

使用这种部署模式，可以为我们提供数据冗余，减少在系统备份期间的I/O冻结（上面有提到）。同时，更重要的是可以防止数据库实例的故障和单个可用区的故障。

如下图所示，我们可以在两个可用区内分别部署主数据库和备用数据库。

![img](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202211192338177.png)

目前Multi-AZ支持以下数据库：

- Oracle
- PostgreSQL
- MySQL
- MariaDB
- SQL Server

值得注意的是，Aurora数据库本身就支持多可用区部署的高可用设置，因此不需要为Aurora数据库特别开启这个功能。

在上次实验中我们有讲到，创建了RDS数据库之后我们会得到一个数据库的URL Endpoint。在开启Multi-AZ的情况下，这个URL Endpoints会根据主/备数据库的健康状态自动解析到IP地址。对于应用程序来说，我们只需要连接这个URL地址即可。

**高可用的设置只是用来解决灾备的问题，并不能解决读取性能的问题；要提升数据库读取性能，我们需要用到Read Replicas。**



### 只读副本（Read Replicas）

我们可以在源数据库实例的基础上，复制一种新类型的数据库实例，称之为**只读副本（Read Replicas）**。我们对源数据库的任何更新，都会**异步**更新到只读副本中。

因此，我们可以将应用程序的数据库读取功能转移到Read Replicas上，来减轻源数据库的负载。

对于有大量读取需求的数据库，我们可以使用这种方式来进行灵活的数据库扩展，同时突破单个数据库实例的性能限制。

Read Replicas还有如下的特点：

- Read Replicas是用来提高读取性能的，不是用来做灾备的
- 要创建Read Replicas需要源RDS实例开启了自动备份的功能
- 可以为数据库创建最多**5个**Read Replicas
- 可以为Read Replicas创建Read Replicas（如下图所示）
- 每一个Read Replicas都有自己的URL Endpoint
- 可以为一个启用了Multi-AZ的数据库创建Read Replicas
- Read Replicas可以提升成为独立的数据库
- 可以创建位于另一个区域（Region）的Read Replicas

![img](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202211192340392.png)

目前Read Replicas支持以下数据库：

- Aurora
- PostgreSQL
- MySQL
- MariaDB
- Oracle

https://amazonaws-china.com/cn/rds/details/read-replicas/

## 参考

[参考](http://www.cloudbin.cn/?p=1968)
