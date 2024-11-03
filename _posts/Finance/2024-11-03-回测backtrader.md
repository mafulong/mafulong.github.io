---
layout: post
category: Finance
title: 回测backtrader
tags: Finance
---

## 回测backtrader

参考资料

- https://github.com/WenmuZhou/crypto/blob/master/doc/backtrader/1%E3%80%81%E6%A6%82%E8%BF%B0.md

## 数据和策略

[参考](https://github.com/WenmuZhou/crypto/blob/master/doc/backtrader/3%E3%80%81%E7%AD%96%E7%95%A5%E7%AF%87.md)

  Strategy类的属性包含数据、cerebro实例、分析器、仓位等等。详细介绍如下：

- env:
  - 策略生存的cerebro实例对象
- datas:
  - 加载的数据队列
- dnames:
  - 用数据名称访问数据的属性
- broker:
  - 经纪人
- stats:
  - 观察者队列
- analyzers:
  - 分析器队列
- position:
  - data0的仓位，position中有两个重要的参数：size和price。size表示持仓量，price表示平均价格





  有关仓位的方法一共有6种，分别描述如下：

3.4.1 getsizer()
  返回自动股本计算的Sizer实例对象。

3.4.2 setsizer(sizer)
  替换默认的sizer

3.4.3 getsizing(data=None, isbuy=True)
  返回当前sizer实例计算出的股本

3.4.4 getposition(data=None, broker=None)
  返回指定经纪人指定数据上当前的仓位

3.4.5 getpositionbyname(name=None, broker=None)
  返回指定经纪人中指定名称的仓位

3.4.6 getpositionsbyname(broker=None)
  返回指定经纪人中仓位



```
通过notify_order(order)发出订单状态变化的通知
通过notify_trade(trade)发出交易开始/更新/关闭的通知
通过notify_cashvalue(cash, value)发出代理手中当前现金和资产的通知
通过notify_fund(cash, value, fundvalue, shares)发出代理手中当前现金和资产，以及正在交易的资金和股票的通知
通过notify_store(msg, *args, **kwargs)发出的事件通知（需要单独实现）
在next方法中，Strategy可以通过以下操作来尝试盈利：
使用buy方法，来做多或者减少/关闭空头交易
使用sell方法，来做空或者减少/关闭多头交易
使用close方法，来关闭一个现有的交易
使用cancel方法，来取消一个尚未执行的订单
当调用buy和sell方法后，都会生成订单，并且返回一个order（或者order子类）的实例，每个实例都包含有一个唯一的ref标识符，用于区分不同的order
```



Backtrader对数据进行了对齐处理，按照起始时间最大的开始截取。因为我们选股是根据不同股票同一天的数据进行对比的，因此多出的时间就没有意义。



```scala
取第一个数据集 可以下面3中方式。取不是第一个的数据集可以用后两种方式

self.data = self.data0 = self.data[0] 其实就是add_data的顺序。自动加了alias
```

line. 一个data可能有多个line，类似列的概念。

index 0是当前数据，index -1是昨天数据，这样依次递减。

```scala
今天收盘价
 self.close = self.datas[0].close
等同于
 print(self.datas[0].lines.close[0])


self.dataclose[0] # 当日的收盘价
self.dataclose[-1] # 昨天的收盘价
self.dataclose[-2] # 前天的收盘价

```

获取日期。

```scala


dt = dt or self.datas[0].datetime.date(0)
print('%s, %s' % (dt.isoformat(), txt))
```



params定义常量，可以这样的元素或者dict形式

```scala
    params = (("maperiod", 20),
              ("bprint", False),)
```

获取某个数据集的列表

```scala
        print(self.datas[0].getlinealiases())

example: ('close', 'low', 'high', 'open', 'volume', 'openinterest', 'datetime')
```

资金管理

```scala
broker.getcash() 获取余额 等同于getvalue()
```





https://www.cnblogs.com/sidianok/p/13554909.html

- __init__里任何操作line的数据都会生成一个新的line， 并在next调用前更新完成。
- next里函数会读取这个line， 默认就是读line[0]的数据



## Indicator 和 Plotting



When the logic gets really complicated and involves several operations it is usually much better to encapsulate that inside an `Indicator`.

*当逻辑变得非常复杂并涉及多个操作时，通常最好将其封装在一个指示符中。*



指标绘图

- Declared `Indicators` get automatically plotted (if cerebro.plot is called) init里声明的指标将自动绘制（如果cerebro.plot被调用）
- **lines** objects from operations DO NOT GET plotted (like `close_over_sma = self.data.close > self.sma`) 不打印来自操作的**lines**对象。 Strategy里init里的line. 
- There is an auxiliary `LinePlotterIndicator` which plots such operations if wished with the following approach  有一个辅助的LinePlotterIndicator，可根据需要使用以下方法绘制这些操作：　可手动画图。

```
close_over_sma = self.data.close > self.sma
LinePlotterIndicator(close_over_sma, name='Close_over_SMA')
```

 　name参数为该指示符保留的单行命名

```python
class MyIndicator(bt.Indicator):
    # 在lines里面声明指标的名称，使用时可以用self.lines.sma或者self.l.sma
    lines = ('sma', )
    # 相关参数
    params = (('period', 10), )

    # 如果指标可以一次性计算完，就可直接在__init__中完成计算；如果不能，就需要在next中计算，如果计算周期大于1，就需要加上addminperiod()方法，保证在next中计算时数据充足
    def __init__(self):
        self.addminperiod(self.params.period)

    # 每个bar运行一次
    def next(self):
        datasum = math.fsum(self.data.get(size=self.p.period))
        self.lines.sma[0] = datasum / self.p.period
```

上面是实现新指标计算的一般必须过程。在实现新指标过程中，也可以更改可视化的参数：

```python
class MyIndicator(bt.Indicator):
    # 画图的设置，详细的在可视化中介绍
    plotinfo = dict(
        plotymargin=0.15,
        plothlines=[1.0, -1.0],
        plotyticks=[1.0, -1.0])

    # Plot the line "overunder" (the only one) with dash style
    # ls stands for linestyle and is directly passed to matplotlib
    plotlines = dict(overunder=dict(ls='--'))

    # 获取指标的名称列表
    def _plotlabel(self):
        plabels = [self.p.period]

        plabels += [self.p.movav] * self.p.notdefault('movav')

        return plabels
```





[参考](https://github.com/WenmuZhou/crypto/blob/master/doc/backtrader/8%E3%80%81%E5%8F%AF%E8%A7%86%E5%8C%96%E7%AF%87.md)

 plot()函数原型如下：

```
plot(plotter=None, numfigs=1, iplot=True, start=None, end=None, width=16, height=9, dpi=300, tight=True, use=None, **kwargs)
```

- plotter：默认为None，画图的实例对象。如果为None，在plot()内用kwargs参数创建。
- numfigs：多少张图。用时间进行划分，比如numfigs=2，时间是两年，每张图都只画出一年的图
- iplot：如果为True，并且在notebook上运行，图形在行内显示
- start：画图的起始时间
- end：画图的结束时间
- width：保存图像的宽度(inches)
- height：保存图像的高度(inches)
- dpi：分辨率
- tight：仅仅保存实际内容
- use：没有用到