---
layout: post
category: DistributedSystem
title: zookeeper
tags: DistributedSystem
---

## zookeeper



了解zk： [参考](https://segmentfault.com/a/1190000022431516)

zk有序树形节点实现分布式锁： [参考](http://www.cyc2018.xyz/%E5%85%B6%E5%AE%83/%E7%B3%BB%E7%BB%9F%E8%AE%BE%E8%AE%A1/%E5%88%86%E5%B8%83%E5%BC%8F.html#zookeeper-%E7%9A%84%E6%9C%89%E5%BA%8F%E8%8A%82%E7%82%B9) 

- Kafka 选举就用的这个。leader选举。

paxos执行过程： [参考](http://www.cyc2018.xyz/%E5%85%B6%E5%AE%83/%E7%B3%BB%E7%BB%9F%E8%AE%BE%E8%AE%A1/%E5%88%86%E5%B8%83%E5%BC%8F.html#%E6%9C%80%E7%BB%88%E4%B8%80%E8%87%B4%E6%80%A7)

zk基于zab协议，是个paxos的变种。

zk的所有副本都可以提供读服务，与此相对应的，只有主节点可以提供写服务。

选举原则：数据最新or ID最大的节点作为主。

## QA

### zk会脑裂吗

不会脑裂。默认 **只有获得超过半数节点的投票, 才能选举出leader.** 因此只会有一个leader存在。可能会有部分节点没有follow leader。这些节点已经挂了。

### zk or ZAB为何是最终一致性而不是强一致性

[参考](https://www.zhihu.com/question/455703356/answer/1847949827)

- 写是强一致性，单领导者模型，写需要majority保证（写节点超过一半），脑裂情况下也可以写强一致
- 读两种接口，1：读单个机器的，2：只读主的。如果是后者就是强一致性的。
- etcd做了读的优化，读时也需要majority，需要大伙同意认为它是主，但牺牲了效率。

这里的一致性是从读写方面，写一致性，都写成功，读一致性，从提供的读接口任意时刻咋读都一样。和事务一致性不太一样。