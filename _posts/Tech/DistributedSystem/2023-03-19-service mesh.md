---
layout: post
category: DistributedSystem
title: service mesh
tags: DistributedSystem
---

## service mesh

在TCP出现之后，机器之间的网络通信不再是一个难题，以GFS/BigTable/MapReduce为代表的分布式系统得以蓬勃发展。这时，分布式系统特有的通信语义又出现了，如熔断策略、负载均衡、服务发现、认证和授权、quota限制、trace和监控等等，于是服务根据业务需求来实现一部分所需的通信语义。

service mesh就实现了这种通信语义。

![img](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv10/img/202508301533501.webp)

服务网格是一个基础设施层，用于处理服务间通信。云原生应用有着复杂的服务拓扑，服务网格保证请求在这些拓扑中可靠地穿梭。在实际应用当中，服务网格通常是由一系列轻量级的网络代理组成的，它们与应用程序部署在一起，但对应用程序透明。

**`Service Mesh`目的是解决系统架构微服务化后的服务间通信和治理问题。** 服务网格由`Sidecar`节点组成，这个模式的精髓在于实现了数据面（业务逻辑）和控制面的解耦。具体到[微服务](https://so.csdn.net/so/search?q=微服务&spm=1001.2101.3001.7020)架构中，即给每一个微服务实例同步部署一个`Sidecar`。可以sidecar形式和应用程序部署到一起。



Service Mesh具有如下优点：

- 屏蔽分布式系统通信的复杂性(负载均衡、服务发现、认证授权、监控追踪、流量控制等等)，服务只用关注业务逻辑；
- 真正的语言无关，服务可以用任何语言编写，只需和Service Mesh通信即可；
- 对应用透明，Service Mesh组件可以单独升级；





## 参考

- [什么是 Service Mesh](https://zhuanlan.zhihu.com/p/61901608)