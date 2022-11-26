---
layout: post
category: AWS
title: AWS DynamoDB
tags: AWS
---

## AWS DynamoDB

[论文讲解](http://systemdesigns.blogspot.com/2016/01/dynamodb.html)

Dynamo在某些故障的场景中将牺牲一致性。

Dynamo的系统假设和要求：
1）query model：对数据项简单的读，写是通过一个主键唯一性标识。状态存储为一个由唯一性键确定二进制对象。没有横跨多个数据项的操作，也不需要关系方案(relational schema)。这项规定是基于观察相当一部分Amazon的服务可以使用这个简单的查询模型，并不需要任何关系模式。Dynamo的目标应用程序需要存储的对象都比较小(通常小于1MB)。

2）ACID属性：ACID是一种保证数据库事务可靠地处理的属性。在数据库方面的，对数据的单一的逻辑操作被称作所谓的交易。Amazon的经验表明，在保证ACID的数据存储提往往有很差的可用性。Dynamo的目标应用程序是高可用性，弱一致性(ACID“中的C”)。Dynamo不提供任何数据隔离(Isolation)保证，只允许单一的关键更新。

3）efficiency：系统需运作在一般的commodity hardware上。Amazon平台的服务都有着严格的延时要求, 鉴于对状态的访问在服务操作中起着至关重要的作用，存储系统必须能够满足那些严格的SLA，服务必须能够通过配置Dynamo，使他们不断达到延时和吞吐量的要求。因此，必须在成本效率，可用性和耐用性保证之间做权衡。



提供get, put操作。



最终一致性。



按key做partition, 一致性Hash。

replica, 复制，用了NWR，让用户做一致性的选择。读数据时如果有不同版本，会所有版本数据都返回回去。

多版本。Vector Clock 一个Vector Clock可以理解为一个<节点编号，计数器>对的列表。每一个版本的数据都会带上一个Vector Clock。Dynamo中，最重要的是要保证写操作的高可用性，即“Always Writeable”，这样就不可避免的牺牲掉数据的一致性。如上所述，Dynamo中并没有对数据做强一致性要求，而是采用的最终一致性(eventual consistency)。若不保证各个副本的强一致性，则用户在读取数据的时候很可能读到的不是最新的数据。Dynamo中将数据的增加或删除这种操作都视为一种增加操作，即每一次操作的结果都作为一份全新的数据保存，这样也就造成了一份数据会存在多个版本，分布在不同的节点上。这种情况类似于版本管理中的多份副本同时有多人在修改。多数情况下，系统会自动合并这些版本，一旦合并尝试失败，那么冲突的解决就交给应用层来解决。这时系统表现出来的现象就是，一个GET(KEY)操作，返回的不是单一的数据，而是一个多版本的数据列表，由用户决定如何合并。这其中的关键技术就是Vector Clock。



为防止要写入节点宕机导致操作失败，采用提示移交机制将操作相关数据写入到随机节点，宕机节点恢复后可根据这些数据进行重放，最终获得数据一致性。



[深入探讨 Amazon DynamoDB 的设计模 式、流复制和全局表](https://sides-share.s3.cn-north-1.amazonaws.com.cn/AWS+Webinar+2019/PDF/Amazon+DynamoDB+webinar.pdf)

[官网](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Programming.LowLevelAPI.html#Programming.LowLevelAPI.DataTypeDescriptors)

[AWS 如何实现数据跨区域同步](https://techsummit.ctrip.com/pdf/songye.pdf)

[MongoDB 与 DynamoDB 正面交锋](https://www.modb.pro/db/432414)
