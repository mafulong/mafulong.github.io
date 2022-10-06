---
layout: post
category: AWS
title: AWS network
tags: AWS
---

# AWS network

[参考](https://docs.amazonaws.cn/vpc/latest/userguide/what-is-amazon-vpc.html)

- **Virtual Private Cloud (VPC)**

  [VPC](https://docs.amazonaws.cn/vpc/latest/userguide/configure-your-vpc.html) 是一个虚拟网络，与您在自己的数据中心中运行的传统网络极为相似。创建 VPC 后，您可以添加子网。翻译成中文是虚拟私有云。

- **子网**

  [子网](https://docs.amazonaws.cn/vpc/latest/userguide/configure-subnets.html)是您的 VPC 内的 IP 地址范围。子网必须位于单个可用区中。在添加子网后，您可以在 VPC 中部署 Amazon 资源。

- **IP 寻址**

  您可以将 IPv4 地址和 IPv6 地址分配到 VPC 和子网。您还可以将您的公有 IPv4 和 IPv6 GUA 地址带到 Amazon 并将其分配到 VPC 中的资源，例如 EC2 实例、NAT 网关和网络负载均衡器。创建 VPC 时，需要为其分配一个 IPv4 CIDR 块（一系列私有 IPv4 地址）、一个 IPv6 CIDR 块或同时分配两种 CIDR 块（双堆栈）。

  私有 IPv4 地址无法通过 Internet 访问。IPv6 地址具有全球唯一性，可以配置为保持私有或通过互联网进行访问。

- **路由选择**

  使用[路由表](https://docs.amazonaws.cn/vpc/latest/userguide/VPC_Route_Tables.html)决定将来自您的子网或网关的网络流量定向到何处。

- **网关和端点**

  [网关](https://docs.amazonaws.cn/vpc/latest/userguide/extend-intro.html)将您的 VPC 连到其他网络。例如，使用[互联网网关](https://docs.amazonaws.cn/vpc/latest/userguide/VPC_Internet_Gateway.html)将您的 VPC 连接到网络。使用 [VPC 端点](https://docs.amazonaws.cn/vpc/latest/privatelink/privatelink-access-aws-services.html)私下连接到 Amazon Web Services，无需使用互联网网关或 NAT 设备。

- **对等连接**

  使用 [VPC 对等连接](https://docs.amazonaws.cn/vpc/latest/peering/)在两个 VPC 中的资源之间路由流量。

- **流量镜像**

  从网络接口[复制网络流量](https://docs.amazonaws.cn/vpc/latest/mirroring/)，然后将其发送到安全和监控设备进行深度数据包检查。

- **中转网关**

  将[中转网关](https://docs.amazonaws.cn/vpc/latest/userguide/extend-tgw.html)用作中央枢纽，以在 VPC、VPN 连接和 Amazon Direct Connect 连接之间路由流量。

- **VPC 流日志**

  [流日志](https://docs.amazonaws.cn/vpc/latest/userguide/flow-logs.html)捕获有关在 VPC 中传入和传出网络接口的 IP 流量的信息。

- **VPN 连接**

  使用 [Amazon Virtual Private Network (Amazon VPN)](https://docs.amazonaws.cn/vpc/latest/userguide/vpn-connections.html) 将 VPC 连接到您的本地网络。





# 工作原理

[参考](https://docs.amazonaws.cn/vpc/latest/userguide/how-it-works.html)

## IP 寻址
创建 VPC 时，需要为其分配一个 IPv4 CIDR 块（一系列私有 IPv4 地址）、一个 IPv6 CIDR 块或同时分配两种 CIDR 块（双堆栈）。

私有 IPv4 地址无法通过 Internet 访问。IPv6 地址具有全球唯一性，可以配置为保持私有或通过互联网进行访问。

公有 IP 地址将从 Amazon 的公有 IP 地址池分配，它不与您的账户关联。在公有 IP 地址与您的实例取消关联后，该地址即释放回该池，并且不再可供您使用。您不能手动关联或取消关联公有 IP 地址。而是在某些情况下，我们从您的实例释放该公有 IP 地址，或向其分配新地址。有关更多信息，请参阅适用于 Linux 实例的 Amazon EC2 用户指南 中的公有 IP 地址。

## 访问 Internet

> 私有网络不能访问互联网，需要互联网网关，私有网络内部之间可通信。

原定设置 VPC 包含一个互联网网关，而且每个原定设置子网都是公有子网。您在默认子网中启动的每个实例都有一个私有 IPv4 地址和一个公有 IPv4 地址。这些实例可以通过 Internet 网关与 Internet 通信。通过互联网网关，您的实例可通过 Amazon EC2 网络边界连接到 Internet。

默认情况下，您启动到非默认子网中的每个实例都有一个私有 IPv4 地址，但没有公有 IPv4 地址，除非您在启动时特意指定一个，或者修改子网的公有 IP 地址属性。这些实例可以相互通信，但无法访问 Internet。

您可以通过以下方式为在非默认子网中启动的实例启用 Internet 访问：将一个互联网网关附加到该实例的 VPC（如果其 VPC 不是默认 VPC），然后将一个弹性 IP 地址与该实例相关联。

或者，您还可以使用网络地址转换 (NAT) 设备，以允许 VPC 中的实例发起到互联网的出站连接，但阻止来自互联网的未经请求的入站连接。NAT 将多个私有 IPv4 地址映射到一个公有 IPv4 地址。您可以使用弹性 IP 地址配置 NAT 设备，并通过互联网网关将其与互联网相连。您可以通过 NAT 设备将私有子网中的实例连接到互联网，NAT 设备会将来自实例的流量路由到互联网网关，并将所有响应路由到该实例。

如果您将 IPv6 CIDR 块与 VPC 关联并为实例分配 IPv6 地址，则实例可以通过互联网网关通过 IPv6 连接到互联网。或者，实例也可以使用仅出口互联网网关经由 IPv6 发起到互联网的出站连接。IPv6 流量独立于 IPv4 流量；您的路由表必须包含单独的 IPv6 流量路由。

# 连接 VPC 和网络

您可以在两个 VPC 之间创建一个 *VPC 对等连接*，然后通过此连接不公开地在这两个 VPC 之间路由流量。这两个 VPC 中的实例可以彼此通信，就像它们在同一网络中一样。



默认情况下，默认子网为公有子网，因为主路由表会将指定发往 Internet 的子网流量发送到 Internet 网关。



# 场景

**带单个公有子网的 VPC**： 此场景的配置包含一个有单一公有子网的 Virtual Private Cloud (VPC)，以及一个 Internet 网关以启用 Internet 通信。如果您要运行单一层级且面向公众的 Web 应用程序，如博客或简单的网站，则我们建议您使用此配置。

**带有公有和私有子网的 VPC (NAT)**：这个场景的配置包括一个有公有子网和私有子网的 Virtual Private Cloud (VPC)。如果您希望运行面向公众的 Web 应用程序，并同时保留不可公开访问的后端服务器，我们建议您使用此场景。常用例子是一个多层网站，其 Web 服务器位于公有子网之内，数据库服务器则位于私有子网之内。您可以设置安全性和路由，以使 Web 服务器能够与数据库服务器建立通信。

公有子网中的实例可直接将出站流量发往 Internet，而私有子网中的实例不能这样做。但是，私有子网中的实例可使用位于公有子网中的网络地址转换 (NAT) 网关访问 Internet。数据库服务器可以使用 NAT 网关连接到 Internet 进行软件更新，但 Internet 不能建立到数据库服务器的连接。

# **Security Groups（安全组）**

[参考](https://zhuanlan.zhihu.com/p/151419823)

VPC 网络安全组标志 VPC 中的哪些流量可以发往 EC2 实例或从 EC2 发出。安全组指定具体的入向和出向流量规则，并精确到源地址（入向）和目的地址（出向）。这些安全组是与 EC2 实例而非子网关联的。
默认情况下，流量只允许出，不允许入。



Security Group（SG）通过控制IP和端口来控制出站入站规则，可以用于EC2，RDS及下面将要用到的VPC Endpoint。



# Difference between Internet Gateway and NAT Gateway

<img src="https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202210041648324.png" style="zoom:67%;" />

参考

- Internet Gateway (IGW) allows instances with public IPs to access the internet.
- NAT Gateway (NGW) allows instances with no public IPs to access the internet.

# 参考Note 基础概念

[参考](https://juejin.cn/post/6949072638145003556)

大部分 AWS 服务都需要以 VPC 为基础进行构建，比如最常用的 EC2，ALB，及无服务器服务 ECS Fargate。 vb

当我们在一个 VPC 中创建 Subnet 时需要给 Subnet 选择一个 AZ（Availability Zone），一个 Subnet 只能选择建在一个 AZ 中。



**选择region**

因为国内政策法规原因，AWS 在中国的服务与 AWS Global 服务略有不同。

AWS Global 的 Region 之间是通过主干网相连的，AWS 中国区的服务没有通过主干网与 AWS Global 相连，只有中国区内部两个 Region，北京和宁夏是相连接的。

在创建 VPC 时并不需要添写 AZ（Availability Zone）信息，VPC 只与 Region 有关。



Subnet 是最终承载大部分 AWS 服务的组件，比如 EC2， ECS Fargate，RDS。

Subnet 分为两种 Private Subnet 和 Public Subnet。

简单来说，不能直接访问 internet 的 Subnet 就是 Private Subnet，能直接访问 internet 的就是 Public Subnet。



Security Group（SG）通过控制IP和端口来控制出站入站规则，可以用于EC2，RDS及下面将要用到的VPC Endpoint。



VPC Endpoint用来直接连接VPC与AWS相关服务，比如RDS AIP,S3。

当系统安全要求比较高时，EC2处于的Subnet可能被限制，无法访问internet，这时EC2就无法访问AWS的一些服务，比如SSM。

这时我们可以利用VPC Endpoint把VPC和所需要访问的服务连接起来，然后EC2就可以不经internet访问到所需的服务。



[参考](https://juejin.cn/post/6954169148318433288)

RT（Route Table）与Subnet相关连，用来描述网络路由。IGW: Internet gateway IGW是一个独立的组件配置在VPC上，使得VPC可以访问internet

我们给VPC加了IGW之后，需要修改Subnet相关的路由，确保访问Internet的请求发送到IGW。

每个VPC中有一个默认的主RT，自动关联VPC内的每一个Subnet。我们现在为Subnet “ts-public-1”单独创建一个新的RT。



- 新建的Subnet就是Private Subnet
- 在Private Subnet中配置了到IGW的路由后，就变成Public Subnet
- Public Subnet中的EC2还要再配置一个Public IP或者EIP就可以访问Internet
- 如果EC2可以访问internet，其关联的Security Group入站规则如果允许从internet访问，那么这个EC2就可以从internet中直接访问到。



1. 实践中我们把应用程序，数据库放在Private Subnet中，阻止从internet访问。把堡垒机和ALB（Application Load balancer）放在Public Subnet，允许从internet访问。

2. 一般我们会建两套Public Subnet和Private Subnet，分别放在不同的AZ中，防止其中一个AZ出问题。这时如果配置NAT，也需要在两个Public Subnet中各配置一个NAT。



# 总结

VPN里多个AZ, 每个AZ都需要至少一个子网，默认是公有子网。但如果有internet访问不到的实例或者数据库，则需建个私有子网，私有子网默认不能访问internet，internet也不能访问私有子网。

要走互联网必须走internet gateway，它对整个vpc生效, public subnet可直接通过IGW与互联网互联，私有子网再通过NAT走公有子网是可以访问internet的，反向不能。 

和互联网连接时都需要有个公网ip，这个是从amazon分配的。
