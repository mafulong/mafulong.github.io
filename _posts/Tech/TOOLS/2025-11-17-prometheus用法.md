---
layout: post
category: Tools
title: prometheus用法
tags: Tools
---

## prometheus用法

# 数据上报

Prometheus 和一般的 APM 工具不一样，它采用的是由 server 端主动 pull 的交互模型，就是你准备好本地数据，然后在 Prometheus server 上配置好数据所在的地址，接下来就是等 Prometheus 来主动、定期拉取数据。


Prometheus 有好几种数据类型，但是通常我们只需要关注 counter、gauge、histogram、summary 这 4 种

Prometheus 的核心是一个时序数据库，它按照**时间序列**来存储数据

## counter
我们的每条数据包含了：

-   指标名称 metric name：http_request_total
-   标签 labels：uri, method, application, instance_ip  **以及它们的值**
-   样本值：比如上面这个是 counter 类型的指标，它的值是不断累加上去的，那这个样本值就代表当前实例从启动开始累积到现在的某接口的请求次数
-   隐式包含了时间戳 timestamp，因为数据是一直在变化的，当前数据仅代表当前时间的值


单单看这个一直增长的图通常没什么意义，能用的场景太少了，所以我们要先来了解下面的几个函数

-   rate: 计算每秒平均增长率
-   increase: 计算总增长量
-   irate: 计算瞬时增长率

### rate 函数

rate 函数的含义是每秒的平均增长率，其实就类似 QPS 的意思。**速率=数量/时间**，所以我们在做图的时候，还需要考虑分母的时间取多长比较合适，比如下面我先使用 1 分钟作为一个统计区间，也就是说 **图上每个时间点的数值 = 这个时间点往前1分钟的数据增长量 / 60秒**。

我们通常需要对结果进行聚合，这里需要用到 **sum** 函数，它非常简单，就是把搜索到的满足条件的时间序列求和。

比如我们可以按照 application 的维度，或者按照 application+ip+接口 的维度，如下：

`sum( rate(http_request_total[1m]) ) by(application)`，这样我们可以看到每个应用的总体 QPS 了，而不是某个接口的 QPS

`sum( rate(http_request_total[1m]) ) by(application, uri)`，这样我们可以看到每个接口的 QPS

sum by 有两种写法，把 by 写在前面也是可以的，比如 `sum by(application, uri) (rate(http_request_total[1m]))`

sum 函数还有一个特点，就是它的结果是分组数据，在一些场景中很适合用来做对比，也就是饼状图

总结一下 rate 函数，它很适合用来制作代表速率的图，比如订单的创建速率、网络的速率、接口的 QPS 等等，同时它适合搭配 sum 函数一起使用。



### irate 函数制图

有了 rate 函数的概念以后，理解 irate 就会容易很多。

比如某个指标，每 10 秒被采集一次数据，有如下数据：

```
2024-09-09 00:00:00 100
2024-09-09 00:00:10 150
2024-09-09 00:00:20 160
2024-09-09 00:00:30 400
2024-09-09 00:00:40 450
2024-09-09 00:00:50 600
2024-09-09 00:01:00 1000
```

先观察一下上面这组数据，每 10 秒增加的数量非常不均匀，有些时候只增加了 10 个，但是最后 10 秒一下子增加了 400 个。

如果我们使用 rate 函数，每分钟作为一个统计区间，计算在 00:01:00 这个时间点的速率，得到的结果是 (1000-100)/60=15。

但是如果我们使用 **irate** 函数，它只会考虑**最后两个数据点的增长率**，也就是说，在 00:01:00 这个时间点的**瞬时**增长率，为 (1000-600)/10=40。

从这个例子，我们可以看到，虽然 rate 和 irate 都是描述增长率，但是 irate 对数据的增长速率非常敏感，而 rate 表现得比较平滑。

既然 irate 只取最后的两个数据，所以我们其实也可以猜到，下面的两个表达式，虽然时间范围看上去差异很大，一个 1m 一个 10m，但是基本上可以肯定，做出来的图是一样的，之所以要指定时间，是因为怕采样频率的问题，以及数据可能有丢失等。

```
irate(http_request_total{application="order-service", ip="10.100.0.3", uri="/api/v1/order/query-detail"}[1m])

irate(http_request_total{application="order-service", ip="10.100.0.3", uri="/api/v1/order/query-detail"}[10m])
```

### increase 函数制图

increase 非常容易理解，它代表在一段时间内，第一个数据到最后一个数据，它们之间的差值。

比如我设置一个这种图：

```
increase(http_request_total{application="order-service", ip="10.100.0.3", uri="/api/v1/order/query-detail"}[5m])
```

图上出现的每个点，它代表这个时间点往前5分钟，这个时间序列总共增长了多少数值。

其实大家应该很容易发现，increase 和 rate 函数用了一样的数据，都是一个时间区间的**第一条**和**最后一条**数据。

所以从数学上，很容易推出：`increase(v[t]) = rate(v[t]) * t`。因此，理论上我们是可以只使用它们之中的一个函数的。

很多时候，我们想知道一段时间的总体变化，而不是变化速率，这个时候我们一般会使用 increase 函数。比如我想知道过去 24 小时内的新用户注册数、24 小时订单数等，这种图可以不局限于做折线图或者是柱状图，也可以做饼图。

counter 类型大概就说这么多，最后需要指出的是，前面我们说过了 counter 的数据是一直增长的，但是如果我们的应用重启了，也就是说，本地的数据发生了重置，Prometheus 会记录新的从 0 开始的样本值，但是对 rate, irate, increase 这些函数，会特殊处理，看下面这两个图就清楚了。


## Gauge 类型

Gauge 类型非常简单，它就是代表某个指标在某个时间点的数值，基本上每个点的数值都是独立的，前后之前没什么关联。

它的使用场景也非常多，比如当前的 CPU 使用率、内存使用率、kafka 的 consumer lag、当前线程数等等。

首先是，它非常适合用来做一些仪表盘的图

当然，把它们做成折线图也很有用，可以看到数据的变化趋势，比如下面这个 cpu 使用率的趋势图

另一个很好用的图，是 stat panel，也就是把上面两个结合在一起，既可以看到趋势，也可以看到当前最新值。

这里要强调一下，如果你觉得有需要，你依然可以使用前面介绍的 rate、irate、increase 等这些函数在 gauge 类型上，虽然很奇怪。对这些函数而言，gauge 和 counter 都是一样的时序数据，只不过 counter 类型的数据有可能要处理数据重置的情况，而 gauge 不存在。


在。

## Summary 类型

接下来我们要进入到 Summary 类型的介绍，它比 counter 和 gauge 稍微复杂一些，我们要介绍一些内部细节，才能帮助大家理解它，进而更容易理解后面要介绍的 Histogram 类型。

首先，我们需要在 application.properties 文件中配置下面这 3 个属性（当然你也可以通过 @Configuration 来配置），这里指明我们要统计 **http.request** 的 P90 和 P99，另外指定了使用 3 个时间窗口，每个窗口是 1 分钟，后面会解释它们的作用。

```
management.metrics.distribution.percentiles.[http.request]=0.9, 0.99
management.metrics.distribution.buffer-length.[http.request]=3 聚合几个窗口
management.metrics.distribution.expiry.[http.request]=1m 每个窗口长度
```
每过一分钟：

-   当前窗口满了 → 切到下一个；
    
-   被切换出去的旧窗口清空后等待重用；
    
-   总是保持 3 个窗口的滑动统计（约 3 分钟范围）。
    

这样计算的 P90 就是最近 3 分钟所有样本的 90th percentile。


Micrometer 的 summary 在计算 P90 时，会：

> 把当前配置的多个时间窗口（如 3×1 分钟）的所有样本合并，排序后取第 90% 位置的值作为 P90。

窗口只是存储样本的分片，真正计算时是**跨窗口合并后一起算分位数**。


它的 API 也非常简单，下面我模拟这些接口，每秒钟被请求一次，每次耗时几十到几百毫秒

一个 summary 类型包含好几个时间序列，另外还有一个 gauge 类型的时间序列。

我们分别来看：

http_request_seconds{quantile="0.9"}，这个记录的是当前的 P90 数据

http_request_seconds{quantile="0.99"}，这个记录的是当前的 P99 数据

http_request_seconds_count：请求次数的总和，它和我们前面介绍 counter 类型的时候的 http_request_total 其实就是一个东西，记录累计访问次数。

http_request_seconds_sum：响应时间的总和，单位是秒，对接口的每次访问都会增加这个值，也是一个 counter 类型。

http_request_seconds_max：这个更好理解了，就是记录最大响应时间，它是 gauge 类型。

-   **核心机制**  
    Summary 类型的核心在于计算分位数（如 P90、P99）。每个 Summary 时间序列会维护若干个时间窗口（如 3 个，每个 1 分钟），用来暂存请求耗时等样本数据。
    
    -   第 1 分钟写入窗口 0；
        
    -   第 2 分钟写入窗口 1，同时聚合窗口 0+1 计算分位数；
        
    -   第 3 分钟写入窗口 2，同时聚合 0+1+2；
        
    -   第 4 分钟循环回窗口 0，清空再用。  
        Prometheus 每次抓取时，Micrometer 会将当前 3 个窗口的样本合并计算分位数后返回。
    
-   **计算方式**  
    P90、P99 等分位数代表“90%/99% 请求耗时不超过的值”，是从当前窗口中统计出的结果。  
    例如：
    
    `http_request_seconds{quantile="0.9"} = 0.788s` 
    
    表示该时间段 90% 的请求耗时 ≤ 0.788 秒。
    
-   **数据来源与限制**
    
    -   Summary 是**客户端计算型指标**，即由应用实例自身计算分位数后暴露给 Prometheus。
        
    -   因此 **无法跨实例聚合**，也不能跨时间窗口聚合（例如 1h 的 P90 无法从多个 1m 的 P90 得出）。
        
    -   这意味着如果多个实例的 P90 分别是 50ms 和 150ms，无法合并成一个整体 P90。
    
-   **与 Histogram 的区别**
    
    -   **Summary**：客户端计算分位数，占用资源少，但无法全局聚合。
        
    -   **Histogram**：将样本按区间（bucket）划分，由 Prometheus 统一计算分位数，支持跨实例、跨时间聚合，但开销更高。
    
-   **适用场景**
    
    -   单实例性能监控、快速查看延迟分布；
        
    -   不适合全局统计或多实例聚合分析。




Histogram 的原理可以总结得很清楚，核心思想就是 **通过固定桶（bucket）统计样本数量，由服务端聚合计算分位数和其他指标**。





# Grafana用法



根据数据类型选择图表：

- 折线图（Time series）
- 统计卡片（Stat）
- 饼图（Pie）
- 表格（Table）
- 仪表盘（Gauge）



## 常见 PromQL 使用技巧

### 1. 忽略标签（去掉维度差异）

```
sum without(instance) (rate(http_request_total[1m]))
```

### 2. 指定标签

```
http_request_total{application="order-service", uri="/api/query"}
```

### 3. 分组聚合

```
sum(rate(http_request_total[1m])) by (uri)
```

### 4. 排序

```
topk(5, sum(rate(http_request_total[1m])) by (uri))
```

------

## Prometheus + Grafana 常用面板画法（简要笔记）

### 1. **QPS（Counter → rate）**

#### 整体 QPS

```
sum(rate(http_request_total[1m]))
```

#### 按接口

```
sum(rate(http_request_total[1m])) by (uri)
```

#### 按应用

```
sum(rate(http_request_total[1m])) by (application)
```

#### 面板类型

- 折线（Time series）
- Legend：按 uri 或 application 展示
- 适合监控「流量趋势」

------

### 2. **瞬时 QPS（irate）**

```
sum(irate(http_request_total[1m])) by (uri)
```

更敏感，用来抓突发。

面板类型：折线图
 注意：抖动比 rate 大。

------

#### 3. **周期总请求量（increase）**

### 过去 24 小时的请求数

```
sum(increase(http_request_total[24h])) by (uri)
```

适用于：

- 饼图：接口占比
- 柱状：不同接口的访问量对比
- Stat：展示总访问量

------

#### 4. **响应时间（Summary）**

### P90

```
http_server_requests_seconds{quantile="0.9"}
```

### P99

```
http_server_requests_seconds{quantile="0.99"}
```

面板类型：折线
 注意：Summary 的 quantile 不可跨实例聚合。

------

#### 5. **响应时间（Histogram）**

### P99（可聚合）

```
histogram_quantile(0.99,
  sum(rate(http_request_duration_seconds_bucket[1m])) by (le)
)
```

可用于：

- 跨实例服务延迟监控
- 高并发系统延迟趋势图

------

#### 6. **平均响应时间**

```
sum(rate(http_request_duration_seconds_sum[1m]))
/
sum(rate(http_request_duration_seconds_count[1m]))
```

用于平均耗时趋势图（比 P99 平稳）。

------

#### 7. **CPU / Memory（Gauge）**

CPU：

```
instance_cpu_usage_percent
```

内存：

```
instance_memory_usage_bytes
```

面板类型：

- 折线
- Stat（显示当前最新值）
- Gauge（仪表盘实时值）

------

#### 8. **Kafka Consumer Lag**

```
kafka_consumergroup_lag
```

面板类型：

- 折线（看趋势）
- Stat（看当前 lag）
- 阈值线（如 >1000 报警）

------

#### 9. **链同步高度（Gauge）**

```
blockchain_block_height
```

常用图法：

- 折线 → 各节点高度
- Stat → 当前高度
- Bar → 节点之间差异