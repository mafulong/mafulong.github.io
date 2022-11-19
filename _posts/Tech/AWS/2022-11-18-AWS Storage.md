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
