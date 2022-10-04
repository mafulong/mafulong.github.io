---
layout: post
category: AWS
title: AWS network
tags: AWS
---

# AWS network

[参考](https://docs.amazonaws.cn/vpc/latest/userguide/what-is-amazon-vpc.html)

- **Virtual Private Cloud (VPC)**

  [VPC](https://docs.amazonaws.cn/vpc/latest/userguide/configure-your-vpc.html) 是一个虚拟网络，与您在自己的数据中心中运行的传统网络极为相似。创建 VPC 后，您可以添加子网。

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
