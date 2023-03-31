---
layout: post
category: AWS
title: AWS Network
tags: AWS
---

# AWS VPC

## 名词解释

[参考](https://docs.amazonaws.cn/vpc/latest/userguide/what-is-amazon-vpc.html)

- **Virtual Private Cloud (VPC)**

  [VPC](https://docs.amazonaws.cn/vpc/latest/userguide/configure-your-vpc.html) 是一个虚拟网络，与您在自己的数据中心中运行的传统网络极为相似。创建 VPC 后，您可以添加子网。翻译成中文是虚拟私有云。

- **子网** **Subnets**

  [子网](https://docs.amazonaws.cn/vpc/latest/userguide/configure-subnets.html)是您的 VPC 内的 IP 地址范围。子网必须位于单个可用区中。在添加子网后，您可以在 VPC 中部署 Amazon 资源。

- **IP 寻址**

  您可以将 IPv4 地址和 IPv6 地址分配到 VPC 和子网。您还可以将您的公有 IPv4 和 IPv6 GUA 地址带到 Amazon 并将其分配到 VPC 中的资源，例如 EC2 实例、NAT 网关和网络负载均衡器。创建 VPC 时，需要为其分配一个 IPv4 CIDR 块（一系列私有 IPv4 地址）、一个 IPv6 CIDR 块或同时分配两种 CIDR 块（双堆栈）。

  私有 IPv4 地址无法通过 Internet 访问。IPv6 地址具有全球唯一性，可以配置为保持私有或通过互联网进行访问。

- **路由选择** 

  使用[路由表](https://docs.amazonaws.cn/vpc/latest/userguide/VPC_Route_Tables.html)决定将来自您的子网或网关的网络流量定向到何处。

- **网关和端点 ** **Gateways and endpoints**

  [网关](https://docs.amazonaws.cn/vpc/latest/userguide/extend-intro.html)将您的 VPC 连到其他网络。例如，使用[互联网网关](https://docs.amazonaws.cn/vpc/latest/userguide/VPC_Internet_Gateway.html)将您的 VPC 连接到网络。使用 [VPC 端点](https://docs.amazonaws.cn/vpc/latest/privatelink/privatelink-access-aws-services.html)私下连接到 Amazon Web Services，无需使用互联网网关或 NAT 设备。

- **对等连接** **Peering connections**

  使用 [VPC 对等连接](https://docs.amazonaws.cn/vpc/latest/peering/)在两个 VPC 中的资源之间路由流量。

- **流量镜像** **Traffic Mirroring**

  从网络接口[复制网络流量](https://docs.amazonaws.cn/vpc/latest/mirroring/)，然后将其发送到安全和监控设备进行深度数据包检查。

- **中转网关 ** **Transit gateways**

  将[中转网关](https://docs.amazonaws.cn/vpc/latest/userguide/extend-tgw.html)用作中央枢纽，以在 VPC、VPN 连接和 Amazon Direct Connect 连接之间路由流量。

- **VPC 流日志**  **VPC Flow Logs**

  [流日志](https://docs.amazonaws.cn/vpc/latest/userguide/flow-logs.html)捕获有关在 VPC 中传入和传出网络接口的 IP 流量的信息。

- **VPN 连接**

  使用 [Amazon Virtual Private Network (Amazon VPN)](https://docs.amazonaws.cn/vpc/latest/userguide/vpn-connections.html) 将 VPC 连接到您的本地网络。

## VPC

**Amazon Virtual Private Cloud (Amazon VPC)**允许你在已定义的虚拟网络内启动AWS资源。这个虚拟网络与你在数据中心中运行的传统网络极其相似，并会为你提供使用AWS的可扩展基础设施的优势。

简单来说，VPC就是一个AWS用来隔离你的网络与其他客户网络的虚拟网络服务。在一个VPC里面，用户的数据会逻辑上地与其他AWS租户分离，用以保障数据安全。

**可以简单地理解为一个VPC就是一个虚拟的数据中心**，在这个虚拟数据中心内我们可以创建不同的子网（公有网络和私有网络），搭建我们的网页服务器，应用服务器，数据库服务器等等服务。

### VPC有如下特点

- VPC内可以创建多个子网

- 可以在选择的子网上启动EC2实例

- 在每一个子网上分配自己规划的IP地址

- 每一个子网配置自己的路由表

- 创建一个Internet Gateway并且绑定到VPC上，让EC2实例可以访问互联网

- VPC对你的AWS资源有更安全的保护

- 部署针对实例的安全组（Security Group）

- 部署针对子网的**网络控制列表（Network Access Control List）**

- 一个VPC可以跨越多个可用区（AZ）

- **一个子网只能在一个可用区（AZ）内**

- 安全组（Security Group）是有状态的，而网络控制列表（Network Access Control List）是无状态的

  - 有状态：如果入向流量被允许，则出向的响应流量会被自动允许
- 无状态：入向规则和出向规则需要分别单独配置，互不影响
  - 具体的区别挨踢小茶会在后续的章节详细讲解

- VPC的子网掩码范围是从/28到/16，不能设置在这个范围外的子网掩码

- VPC可以通过Virtual Private Gateway (VGW) 来与企业本地的数据中心相连

- VPC可以通过AWS PrivateLink访问其他AWS账户托管的服务（VPC终端节点服务）



### VPC Peering

**VPC Peering**可是两个VPC之间的网络连接，通过此连接，你可以使用IPv4地址在两个VPC之间传输流量。这两个VPC内的实例会和如果在同一个网络一样彼此通信。

- 可以通过AWS内网将一个VPC与另一个VPC相连
- 同一个AWS账号内的2个VPC可以进行VPC Peering
- 不同AWS账号内的VPC也可以进行VPC Peering
- 不支持VPC Transitive Peering 不支持传递
  - 如果VPC A和VPC B做了Peering
  - 而且VPC B和VPC C做了Peering
  - 那么VPC A是**不能**和VPC C进行通信的
  - 要通信，只能将VPC A和VPC C进行Peering

### 默认VPC

- 在每一个区域（Region），AWS都有一个默认的VPC
- 在这个VPC里面所有子网都绑定了一个路由表，其中有默认路由（目的地址 0.0.0.0/0）到互联网
- 所有在默认VPC内启动的EC2实例都可以直接访问互联网
- 在默认VPC内启动的EC2实例都会被分配公网地址和私有地址

如下图所示，我们在某一个区域内有一个VPC，这个VPC的网络是172.31.0.0/16

在这个VPC内有2个子网，分别是172.31.0.0/20 和 172.31.16.0/20。这两个子网内都有一个EC2实例，每一个实例拥有一个该子网的私有地址（172.31.x.x）以及一个AWS分配的公网IP地址（203.0.113.x）。

这两个实例关联了一个主路由表，该路由表拥有一个访问172.31.0.0/16 VPC内流量的路由条目；还有一个目的为 0.0.0.0/0 的默认路由条目，指向Internet网关。

因此这两个实例都可以通过Internet网关访问外网。

![img](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202211192248477.png)

### VPC终端节点（VPC Endpoints）PrivateLink

在一般的情况下，如果你需要访问S3服务，EC2实例或者DynamoDB的资源，你需要通过Internet公网来访问这些服务。有没有更快速、更安全的访问方式呢？

**VPC终端节点（VPC Endpoints）**提供了这种可能性。

VPC终端节点能建立VPC和一些AWS服务之间的高速、私密的“专线”。这个专线叫做PrivateLink，使用了这个技术，你无需再使用Internet网关、NAT网关、VPN或AWS Direct Connect连接就可以访问到一些AWS资源了！



## 工作原理

[参考](https://docs.amazonaws.cn/vpc/latest/userguide/how-it-works.html)

### IP 寻址
创建 VPC 时，需要为其分配一个 IPv4 CIDR 块（一系列私有 IPv4 地址）、一个 IPv6 CIDR 块或同时分配两种 CIDR 块（双堆栈）。

私有 IPv4 地址无法通过 Internet 访问。IPv6 地址具有全球唯一性，可以配置为保持私有或通过互联网进行访问。

公有 IP 地址将从 Amazon 的公有 IP 地址池分配，它不与您的账户关联。在公有 IP 地址与您的实例取消关联后，该地址即释放回该池，并且不再可供您使用。您不能手动关联或取消关联公有 IP 地址。而是在某些情况下，我们从您的实例释放该公有 IP 地址，或向其分配新地址。有关更多信息，请参阅适用于 Linux 实例的 Amazon EC2 用户指南 中的公有 IP 地址。

### 访问 Internet

> 私有网络不能访问互联网，需要互联网网关，私有网络内部之间可通信。

原定设置 VPC 包含一个互联网网关，而且每个原定设置子网都是公有子网。您在默认子网中启动的每个实例都有一个私有 IPv4 地址和一个公有 IPv4 地址。这些实例可以通过 Internet 网关与 Internet 通信。通过互联网网关，您的实例可通过 Amazon EC2 网络边界连接到 Internet。

默认情况下，您启动到非默认子网中的每个实例都有一个私有 IPv4 地址，但没有公有 IPv4 地址，除非您在启动时特意指定一个，或者修改子网的公有 IP 地址属性。这些实例可以相互通信，但无法访问 Internet。

您可以通过以下方式为在非默认子网中启动的实例启用 Internet 访问：将一个互联网网关附加到该实例的 VPC（如果其 VPC 不是默认 VPC），然后将一个弹性 IP 地址与该实例相关联。

或者，您还可以使用网络地址转换 (NAT) 设备，以允许 VPC 中的实例发起到互联网的出站连接，但阻止来自互联网的未经请求的入站连接。NAT 将多个私有 IPv4 地址映射到一个公有 IPv4 地址。您可以使用弹性 IP 地址配置 NAT 设备，并通过互联网网关将其与互联网相连。您可以通过 NAT 设备将私有子网中的实例连接到互联网，NAT 设备会将来自实例的流量路由到互联网网关，并将所有响应路由到该实例。

如果您将 IPv6 CIDR 块与 VPC 关联并为实例分配 IPv6 地址，则实例可以通过互联网网关通过 IPv6 连接到互联网。或者，实例也可以使用仅出口互联网网关经由 IPv6 发起到互联网的出站连接。IPv6 流量独立于 IPv4 流量；您的路由表必须包含单独的 IPv6 流量路由。



默认情况下，默认子网为公有子网，因为主路由表会将指定发往 Internet 的子网流量发送到 Internet 网关。



### NAT

NAT的全程是“**Network Address Translation**”，中文解释是“**网络地址转换**”，它可以让整个机构只使用一个公有的IP地址出现在Internet上。

NAT是一种把内部私有地址（192.168.1.x，10.x.x.x等）转换为Internet公有地址的协议，它一定程度上解决了公网地址不足的问题。

- NAT实例需要创建在公有子网内





**堡垒机（Bastion Host）**又叫做跳板机（Jump Box），主要用于运维人员远程登陆服务器的集中管理。运维人员首先登陆到这台堡垒机（公网），然后再通过堡垒机管理位于内网的所有服务器。

堡垒机可以对运维人员的操作行为进行控制和审计，同时可以结合Token等技术达到更加安全的效果。

## VPC场景

**带单个公有子网的 VPC**： 此场景的配置包含一个有单一公有子网的 Virtual Private Cloud (VPC)，以及一个 Internet 网关以启用 Internet 通信。如果您要运行单一层级且面向公众的 Web 应用程序，如博客或简单的网站，则我们建议您使用此配置。

**带有公有和私有子网的 VPC (NAT)**：这个场景的配置包括一个有公有子网和私有子网的 Virtual Private Cloud (VPC)。如果您希望运行面向公众的 Web 应用程序，并同时保留不可公开访问的后端服务器，我们建议您使用此场景。常用例子是一个多层网站，其 Web 服务器位于公有子网之内，数据库服务器则位于私有子网之内。您可以设置安全性和路由，以使 Web 服务器能够与数据库服务器建立通信。

公有子网中的实例可直接将出站流量发往 Internet，而私有子网中的实例不能这样做。但是，私有子网中的实例可使用位于公有子网中的网络地址转换 (NAT) 网关访问 Internet。数据库服务器可以使用 NAT 网关连接到 Internet 进行软件更新，但 Internet 不能建立到数据库服务器的连接。

## Security Groups（安全组）

[参考](https://zhuanlan.zhihu.com/p/151419823)

VPC 网络安全组标志 VPC 中的哪些流量可以发往 EC2 实例或从 EC2 发出。安全组指定具体的入向和出向流量规则，并精确到源地址（入向）和目的地址（出向）。这些安全组是与 EC2 实例而非子网关联的。
默认情况下，流量只允许出，不允许入。



Security Group（SG）通过控制IP和端口来控制出站入站规则，可以用于EC2，RDS及下面将要用到的VPC Endpoint。



## 网络ACL（NACL）

**网络访问控制列表（NACL）**与安全组（Security Group）类似，它能在子网的层面控制所有入站和出站的流量，为VPC提供更加安全的保障。



- 在你的**默认VPC**内会有一个默认的网络ACL（NACL），它会**允许**所有入向和出向的流量
- 你可以创建一个自定义的网络ACL，在创建之初所有的入向和出向的流量都会被**拒绝**，除非进行手动更改
- 对于所有VPC内的子网，每一个子网都需要关联一个网络ACL。如果没有关联任何网络ACL，那么子网会关联默认的网络ACL
- 一个网络ACL可以关联多个子网，但一个子网只能关联一个网络ACL
- 网络ACL包含了一系列（允许或拒绝）的规则，网络ACL会按顺序执行，一旦匹配就结束，不会再继续往下匹配
- 网络ACL有入向和出向的规则，每一条规则都可以配置允许或者拒绝
- 网络ACL是无状态的（安全组是有状态的）
  - 被允许的入向流量的响应流量必须被精准的出向规则所允许（反之亦然）
  - 一般至少需要允许临时端口（TCP 1024-65535）
  - 关于临时端口的知识，可以参见[这里](https://docs.aws.amazon.com/zh_cn/AmazonVPC/latest/UserGuide/VPC_ACLs.html#VPC_ACLs_Ephemeral_Ports)

## Difference between Internet Gateway and NAT Gateway

<img src="https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202210041648324.png" style="zoom:67%;" />

参考

- Internet Gateway (IGW) allows instances with public IPs to access the internet.
- NAT Gateway (NGW) allows instances with no public IPs to access the internet.

## 参考

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



[参考](http://www.cloudbin.cn/?tag=aws) 暂无Note

## 总结

VPC里多个AZ, 每个AZ都需要至少一个子网，默认是公有子网。但如果有internet访问不到的实例或者数据库，则需建个私有子网，私有子网默认不能访问internet，internet也不能访问私有子网。

要走互联网必须走internet gateway，它对整个vpc生效, public subnet可直接通过IGW与互联网互联，私有子网再通过NAT走公有子网是可以访问internet的，反向不能。 

和互联网连接时都需要有个公网ip，这个是从amazon分配的。



# Route 53

**Amazon Route 53**是一种高可用、高扩展性的云DNS服务。

Amazon Route 53 是一种托管域名系统 (DNS) 服务，它可帮助您为您的域名注册和管理 DNS 记录。您可以使用 Route 53 将您的域名映射到您的 VPC 内的资源，如 ELB 和 Amazon S3。

不同的DNS记录：

- **CNAME** – CNAME （Canonical Name）可以将一个域名指向另一个域名。比如将aws.xiaopeiqing.com指向xiaopeiqing.com
- Alias记录 – 和CNAME类似，又叫做别名记录，可以将一个域名指向另一个域名。
  - **和CNAME最大的区别是，Alias可以应用在根域（Zone Apex）。即可以为xiaopeiqing.com的根域创建Alias记录，而不能创建CNAME**
  - 别名记录可以节省你的时间，因为Route53会自动识别别名记录所指的记录中的更改。例如，假设example.com的一个别名记录指向位于lb1-1234.us-east-2.elb.amazonaws.com上的一个ELB负载均衡器。如果该负载均衡器的IP地址发生更改，Route53将在example.com的DNS应答中自动反映这些更改，而无需对包含example.com的记录的托管区域做出任何更改。 弹性负载均衡器（ELB）没有固定的IPv4地址，在使用ELB的时候永远使用它的DNS名字。很多场景下我们需要绑定DNS记录到ELB的endpoint地址，而不绑定任何IP

# AWS Direct Connect

AWS Direct Connect 是一种专用网络连接服务，它允许您通过私有连接连接到 AWS 服务。您可以使用 Direct Connect 将您的本地数据中心与您的 VPC 直接连接起来，实现更安全、更高带宽的网络连接。





AWS Direct Connect 是一种联网服务，提供了通过互联网连接到AWS 的替代方案。 使用AWS Direct Connect ，以前通过Internet 传输的数据将可以借助您的设施和AWS 之间的私有网络连接进行传输。

**不再需要通过网络提供商。** 描述的是本地IT数据中心和VPC连接。通过物理专线连接。

AWS Direct Connect 通过标准的以太网光纤电缆将您的内部网络链接到 AWS Direct Connect 位置。电缆的一端接到您的路由器，另一端接到 AWS Direct Connect 路由器。有了这个连接，你可以创建*虚拟接口*直接公有公有访问AWS服务（例如，到 Amazon S3）或 Amazon VPC，绕过您的网络路径中的互联网服务提供商。网络 ACL 和安全组都允许 (因此可到达您的实例) 的发起 ping 的AWS Direct Connect位置提供访问AWS在与之关联的区域中。您可以将单个连接用于公有区域或AWS GovCloud (US)公有访问AWS所有其他公有区域中的服务。

[参考](https://docs.aws.amazon.com/zh_cn/directconnect/latest/UserGuide/Welcome.html)

