---
layout: post
category: Finance
title: 回测backtrader
tags: Finance
---

## 回测backtrader

参考资料

- https://github.com/WenmuZhou/crypto/blob/master/doc/backtrader/1%E3%80%81%E6%A6%82%E8%BF%B0.md
- https://github.com/jrothschild33/learn_backtrader
- https://www.wuzao.com/document/backtrader/order.html
- strategy的所有可用方法: https://www.backtrader.com/docu/strategy/?h=getdata

在 Backtrader 中，交易流程大致如下：



- step1：设置交易条件：初始资金、交易税费、滑点、成交量限制等；
- step2：在 Strategy 策略逻辑中下达交易指令 buy、sell、close，或取消交易 cancel；
- step3：Order 模块会解读交易订单，解读的信息将交由经纪商 Broker 模块处理；
- step4：经纪商 Broker 会根据订单信息检查订单并确定是否接收订单；
- step5：经纪商 Broker 接收订单后，会按订单要求撮合成交 trade，并进行成交结算；
- step6：Order 模块返回经纪商 Broker 中的订单执行结果。

## 策略

[参考](https://github.com/WenmuZhou/crypto/blob/master/doc/backtrader/3%E3%80%81%E7%AD%96%E7%95%A5%E7%AF%87.md)

  Strategy类的属性包含数据、cerebro实例、分析器、仓位等等。详细介绍如下

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



self.broker有一些仓位的方法

  有关仓位的方法一共有6种，分别描述如下：

```scala
getsizer()
返回自动股本计算的 Sizer 实例对象。

setsizer(sizer)
替换默认的 Sizer，允许使用自定义的股本计算逻辑。

getsizing(data=None, isbuy=True)
返回当前 Sizer 实例计算出的股本。

getposition(data=None, broker=None)
返回指定经纪人和数据集上的当前仓位信息。

getpositionbyname(name=None, broker=None)
返回指定经纪人中指定名称的仓位信息。

getpositionsbyname(broker=None)
返回指定经纪人下的所有仓位信息。
```





一些可override的方法以及一些交易方法

- 通过 `notify_order(order)` 发出订单状态变化的通知。
- 通过 `notify_trade(trade)` 发出交易开始/更新/关闭的通知。 这个会在一个卖单成功后被调用， 落后于notify_order. 
- 通过 `notify_cashvalue(cash, value)` 发出代理手中当前现金和资产的通知。
- 通过 `notify_fund(cash, value, fundvalue, shares)` 发出代理手中当前现金和资产，以及正在交易的资金和股票的通知。
- 通过 `notify_store(msg, *args, **kwargs)` 发出的事件通知（需要单独实现）。
- 在 `next` 方法中，`Strategy` 可以通过以下操作来尝试盈利：
  - 使用 `buy` 方法，来做多或者减少/关闭空头交易。
  - 使用 `sell` 方法，来做空或者减少/关闭多头交易。
  - 使用 `close` 方法，来关闭一个现有的交易。
  - 使用 `cancel` 方法，来取消一个尚未执行的订单。
  - 当调用 `buy` 和 `sell` 方法后，都会生成订单，并且返回一个 `order`（或者 `order` 子类）的实例，每个实例都包含有一个唯一的 `ref` 标识符，用于区分不同的 `order`。

资金管理

```scala
broker.getcash() 获取余额，不包含市值，只是现金 
broker.getvalue() 余额现金+市值

# 在 Strategy 中添加资金或获取当前资金
self.broker.add_cash(10000) # 正数表示增加资金
self.broker.add_cash(-10000) # 负数表示减少资金
self.broker.getcash() # 获取当前可用资金



class TestStrategy(bt.Strategy):
    def next(self):
        print('当前可用资金', self.broker.getcash())
        print('当前总资产', self.broker.getvalue())
        print('当前持仓量', self.broker.getposition(self.data).size)
        print('当前持仓成本', self.broker.getposition(self.data).price)
        # 也可以直接获取持仓
        print('当前持仓量', self.getposition(self.data).size)
        print('当前持仓成本', self.getposition(self.data).price)
        # 注：getposition() 需要指定具体的标的数据集
```



**滑点管理**



在实际交易中，由于市场波动、网络延迟等原因，交易指令中指定的交易价格与实际成交价格会存在较大差别，出现滑点。为了让回测结果更真实，在交易前可以通过 brokers 设置滑点，滑点的类型有 2 种：**百分比滑点和固定滑点**。不论哪种设置方式，都是起到相同的作用：买入时，在指定价格的基础上提高实际买入价格；卖出时，在指定价格的基础上，降低实际卖出价格；买的 “更贵”，卖的 “更便宜” 。



注：在 Backtrader 中，如果同时设置了百分比滑点和固定滑点，前者的优先级高于后者，最终按百分比滑点的设置处理。



**交易时机管理**

对于交易订单生成和执行时间，Backtrader 默认是 “当日收盘后下单，次日以开盘价成交”，这种模式在回测过程中能有效避免使用未来数据。但对于一些特殊的交易场景，比如“all_in”情况下，当日所下订单中的数量是用当日收盘价计算的（总资金 / 当日收盘价），次日以开盘价执行订单时，如果开盘价比昨天的收盘价提高了，就会出现可用资金不足的情况。为了应对一些特殊交易场景，Backtrader 还提供了一些 cheating 式的交易时机模式：Cheat-On-Open 和 Cheat-On-Close。

Cheat-On-Open 是“当日下单，当日以开盘价成交”模式，在该模式下，Strategy 中的交易逻辑不再写在 next() 方法里，而是写在特定的 next_open()、nextstart_open() 、prenext_open() 函数中，具体设置可参考如下案例：

- 方式1：bt.Cerebro(cheat_on_open=True)；
- 方式2：cerebro.broker.set_coo(True)；
- 方式3：BackBroker(coo=True)。



**下单高级函数**

buy_bracket() 和 sell_bracket() 会一次性生成 3 个自定义类型的订单：主订单 main order、针对主订单的止损单 stop order、针对主订单的止盈单 limit order 。

**buy_bracket()**

buy_bracket() 用于long side 的交易场景，买入证券后，在价格下跌时，希望通过止损单卖出证券，限制损失；在价格上升时，希望通过限价单卖出证券，及时获利，通过 buy_bracket() 可以同时提交上述 3 个订单，而无需繁琐的调用 3 次常规交易函数。

```
# 函数可用参数
buy_bracket(# 主订单的参数
            data=None, size=None, price=None,
            plimit=None,exectype=bt.Order.Limit,
            valid=None, tradeid=0,
            trailamount=None, trailpercent=None,
            oargs={},
            # 止损单的参数
            stopprice=None, stopexec=bt.Order.Stop, stopargs={},
            # 止盈单的参数
            limitprice=None, limitexec=bt.Order.Limit, limitargs={},
            **kwargs):......
```





Broker 在执行交易时，会根据执行流程给订单赋予不同的状态，不同阶段的订单状态可以通过Strategy 中定义 notify_order() 方法来捕获，从而进行自定义的处理，从下达交易指令到订单执行结束，订单可能会依次呈现如下状态：



- Order.Created：订单已被创建；
- Order.Submitted：订单已被传递给经纪商 Broker；
- Order.Accepted：订单已被经纪商接收；
- Order.Partial：订单已被部分成交；
- Order.Complete：订单已成交；
- Order.Rejected：订单已被经纪商拒绝；
- Order.Margin：执行该订单需要追加保证金，并且先前接受的订单已从系统中删除；
- Order.Cancelled (or Order.Canceled)：确认订单已经被撤销；
- Order.Expired：订单已到期，其已经从系统中删除 。  

上述状态的排列顺序依次为：

['Created'、'Submitted'、'Accepted'、'Partial'、'Completed'、'Canceled'、'Expired'、'Margin'、'Rejected']，而 order.status 的取值对应上述专题的位置索引，如order.status==4，对应 'Completed' 状态 。

## 数据



Backtrader对数据进行了对齐处理，按照起始时间最大的开始截取。因为我们选股是根据不同股票同一天的数据进行对比的，因此多出的时间就没有意义。

```scala
取第一个数据集 可以下面3中方式。取不是第一个的数据集可以用后两种方式

self.data = self.data0 = self.data[0] 其实就是add_data的顺序。自动加了alias
```

**line**. 一个data有多个line，类似列的概念。

以 `self.datas` 为例，调用语句可以写成如下形式：

```scala
# 访问第一个数据集的 close 线
self.data.lines.close # 可省略 lines 简写成：self.data.close
self.data.lines_close # 可省略 lines 简写成：self.data_close
# 访问第二个数据集的 open 线
self.data1.lines.close # 可省略 lines 简写成：self.data1.close
self.data1.lines_close # 可省略 lines 简写成：self.data1_close
# 注：只有从 self.datas 调用 line 时可以省略 lines，调用 indicators 中的 line 时不能省略
```

推荐就用self.data[x].lines[y] 或者self.data[x].lines.close这样。 这样不会出错。 



line上取某个值，索引注意 index 0是当前数据，index -1是昨天数据，这样依次递减。

```scala
今天收盘价
 self.datas[0].close
等同于
 print(self.datas[0].lines.close[0])

self.dataclose[0] # 当日的收盘价
self.dataclose[-1] # 昨天的收盘价
self.dataclose[-2] # 前天的收盘价

```

获取 line 长度：

1、self.data0.buflen() 返回整条线的总长度，固定不变；

2、在 next() 中调用 len(self.data0)，返回的是当前已处理（已回测）的数据长度，会随着回测的推进动态增长。

datetime 线：

1、datetime 线中的时间点存的是数字形式的时间，可以通过 bt.num2date() 方法将其转为“xxxx-xx-xx xx:xx:xx”这种形式；

2、对 datetime 线进行索引时，xxx.date(X) 可以直接以“xxxx-xx-xx xx:xx:xx”的形式返回，X 就是索引位置，可以看做是传统 [X] 索引方式的改进版 。

```scala
dt = dt or self.datas[0].datetime.date(0)
print('%s, %s' % (dt.isoformat(), txt))
```



params定义常量，可以这样的元组或者dict形式。 是Strategy的属性。访问时用self.params.xxx或者self.p.xxx来使用。

```scala
    params = (("maperiod", 20),
              ("bprint", False),)
```



获取某个数据集的列表，看都有哪些lines

```scala
        print(self.datas[0].getlinealiases())
example: ('close', 'low', 'high', 'open', 'volume', 'openinterest', 'datetime')
```



Backtrader 将数据表格的列拆成了一个个 line 线对象，一列→一个指标→该指标的时间序列→一条线 line。Backtrader 默认情况下要求导入的数据表格要包含 7 个字段：'datetime'、 'open'、 'high'、 'low'、 'close'、 'volume'、 'openinterest' ，这 7 个字段序列就对应了 7 条 line 。其实给列赋予“线”的概念也很好理解，回测过程中用到的时间序列行情数据可视化后就是一条条曲线：close 曲线、 open 曲线、high 曲线 ......

```scala
class TestStrategy(bt.Strategy):
 
    def __init__(self):
        print("--------- 打印 self 策略本身的 lines ----------")
        print(self.lines.getlinealiases())
        print("--------- 打印 self.datas 第一个数据表格的 lines ----------")
        print(self.datas[0].lines.getlinealiases())
        # 计算第一个数据集的s收盘价的20日均线，返回一个 Data feed
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0].close, period=20)
        print("--------- 打印 indicators 对象的 lines ----------")
        print(self.sma.lines.getlinealiases())
        print("---------- 直接打印 indicators 对象的所有 lines -------------")
        print(self.sma.lines)
        print("---------- 直接打印 indicators 对象的第一条 lines -------------")
        print(self.sma.lines[0])
        
    def next(self):
        print('验证索引位置为 6 的线是不是 datetime')
        print(bt.num2date(self.datas[0].lines[6][0]))
        # num2date() 作用是将数字形式的时间转为 date 形式
        
cerebro = bt.Cerebro()
st_date = datetime.datetime(2019,1,2)
ed_date = datetime.datetime(2021,1,28)
datafeed1 = bt.feeds.PandasData(dataname=data1,
                                fromdate=st_date,
                                todate=ed_date)
cerebro.adddata(datafeed1, name='600466.SH')
datafeed2 = bt.feeds.PandasData(dataname=data2,
                                fromdate=st_date,
                                todate=ed_date)
cerebro.adddata(datafeed2, name='603228.SH')
cerebro.addstrategy(TestStrategy)
rasult = cerebro.run()

--------- 打印 self 策略本身的 lines ----------
('datetime',)
--------- 打印 self.datas 第一个数据表格的 lines ----------
('close', 'low', 'high', 'open', 'volume', 'openinterest', 'datetime')
--------- 打印 indicators 对象的 lines ----------
('sma',)
---------- 直接打印 indicators 对象的所有 lines -------------
<backtrader.lineseries.Lines_LineSeries_LineIterator_DataAccessor_IndicatorBase_Indicator_MovingAverageBase_MovingAverageSimple_SimpleMovingAverage object at 0x7fa883e4a470>
---------- 直接打印 indicators 对象的第一条 lines -------------
<backtrader.linebuffer.LineBuffer object at 0x7fa883e4a2b0>
验证索引位置为 6 的线是不是 datetime
2019-01-29 00:00:00
验证索引位置为 6 的线是不是 datetime
2019-01-30 00:00:00
验证索引位置为 6 的线是不是 datetime
2019-01-31 00:00:00
验证索引位置为 6 的线是不是 datetime
2019-02-01 00:00:00
验证索引位置为 6 的线是不是 datetime
2019-02-11 00:00:00
......




class TestStrategy(bt.Strategy):
    def __init__(self):
        self.count = 0 # 用于计算 next 的循环次数
        # 打印数据集和数据集对应的名称
        print("------------- init 中的索引位置-------------")
        print("0 索引：",'datetime',self.data1.lines.datetime.date(0), 'close',self.data1.lines.close[0])
        print("-1 索引：",'datetime',self.data1.lines.datetime.date(-1),'close', self.data1.lines.close[-1])
        print("-2 索引",'datetime', self.data1.lines.datetime.date(-2),'close', self.data1.lines.close[-2])
        print("1 索引：",'datetime',self.data1.lines.datetime.date(1),'close', self.data1.lines.close[1])
        print("2 索引",'datetime', self.data1.lines.datetime.date(2),'close', self.data1.lines.close[2])
        print("从 0 开始往前取3天的收盘价：", self.data1.lines.close.get(ago=0, size=3))
        print("从-1开始往前取3天的收盘价：", self.data1.lines.close.get(ago=-1, size=3))
        print("从-2开始往前取3天的收盘价：", self.data1.lines.close.get(ago=-2, size=3))
        print("line的总长度：", self.data1.buflen())
        
    def next(self):
        print(f"------------- next 的第{self.count+1}次循环 --------------")
        print("当前时点（今日）：",'datetime',self.data1.lines.datetime.date(0),'close', self.data1.lines.close[0])
        print("往前推1天（昨日）：",'datetime',self.data1.lines.datetime.date(-1),'close', self.data1.lines.close[-1])
        print("往前推2天（前日）", 'datetime',self.data1.lines.datetime.date(-2),'close', self.data1.lines.close[-2])
        print("前日、昨日、今日的收盘价：", self.data1.lines.close.get(ago=0, size=3))
        print("往后推1天（明日）：",'datetime',self.data1.lines.datetime.date(1),'close', self.data1.lines.close[1])
        print("往后推2天（明后日）", 'datetime',self.data1.lines.datetime.date(2),'close', self.data1.lines.close[2])
        print("已处理的数据点：", len(self.data1))
        print("line的总长度：", self.data0.buflen())
        self.count += 1
```





https://www.cnblogs.com/sidianok/p/13554909.html

- __init__里任何操作line的数据都会生成一个新的line， 并在next调用前更新完成。

- next里函数会读取这个line， 默认就是读line[0]的数据

  

**init() 中：** 

访问的是整条 line，索引编号也是对整条 line 上所有数据点进行编号的，所以 0 号位置对应导入的行情数据中最晚的那个时间点 2021-01-28，然后依次 backwards；

通过 get() 切片时，如果是从 ago=0 开始取，不会返回数据，从其他索引位置开始取，能返回数据 。



**next()中**

在 next() 中，只要记住 0 是当前回测的时间点（今日），然后站在当前时刻回首过往：-1 是昨日、-2 是前日，依次类推 ；或者站在当前时刻期盼未来：1 是明日、2 是明后日，以此类推 。



**数据扩展**

在回测时，除了常规的高开低收成交量这些行情数据外，还会用到别的指标，比如选股回测时会用到很多选股因子（PE、PB 、PCF、......），那这些数据又该如何添加进 Backtrader 的数据表格呢？往 Backtrader 的数据表格里添加指标，就是给数据表格新增列，也就是给数据表格新增 line：以导入 DataFrame 为例，在继承原始的数据读取类 bt.feeds.PandasData 的基础上，设置 lines 属性和 params 属性，新的 line 会按其在 lines 属性中的顺序依次添加进数据表格中，具体对照下面例子的输出部分：

```scala
class PandasData_more(bt.feeds.PandasData):
    lines = ('pe', 'pb', ) # 要添加的线
    # 设置 line 在数据源上的列位置
    params=(
        ('pe', -1),
        ('pb', -1),
           )
    # -1表示自动按列明匹配数据，也可以设置为线在数据源中列的位置索引 (('pe',6),('pb',7),)
class TestStrategy(bt.Strategy):
    def __init__(self):
        print("--------- 打印 self.datas 第一个数据表格的 lines ----------")
        print(self.data0.lines.getlinealiases())
        print("pe line:", self.data0.lines.pe)
        print("pb line:", self.data0.lines.pb)

data1['pe'] = 2 # 给原先的data1新增pe指标（简单的取值为2）
data1['pb'] = 3 # 给原先的data1新增pb指标（简单的取值为3）
# 导入的数据 data1 中
cerebro = bt.Cerebro()
st_date = datetime.datetime(2019,1,2)
ed_date = datetime.datetime(2021,1,28)
datafeed1 = PandasData_more(dataname=data1,
                            fromdate=st_date,
                            todate=ed_date)
cerebro.adddata(datafeed1, name='600466.SH')
cerebro.addstrategy(TestStrategy)
rasult = cerebro.run()

--------- 打印 self.datas 第一个数据表格的 lines ----------
('close', 'low', 'high', 'open', 'volume', 'openinterest', 'datetime', 'pe', 'pb')
pe line: <backtrader.linebuffer.LineBuffer object at 0x7fc71f858250>
pb line: <backtrader.linebuffer.LineBuffer object at 0x7fc71f8582b0>
```



## 指标 Indicator



在编写策略时，除了常规的高开低收成交量等行情数据外，还会用到各式各样的指标（变量），比如宏观经济指标、基本面分析指标、技术分析指标、另类数据等等。Backtrader 大致有 2 种获取指标的方式：

```
1. 直接通过 DataFeeds 模块导入已经计算好的指标，比如《数据篇》中的导入新增指标 PE、PB；
2. 在编写策略时调用 Indicators 指标模块临时计算指标，比如 5 日均线、布林带等 。
```

**建议在 __init__() 中提前计算指标**

Strategy 中的 __init__() 函数在回测过程中只会在最开始的时候调用一次，而 next() 会每个交易日依次循环调用多次，所以为了提高回测效率，建议先在 __init__() 中一次性计算好指标（甚至是交易信号），然后在 next() 中调用已经算好的指标，这样能有效避免指标的重复计算，提高回测运行速度。建议遵循“__init__() 负责指标计算，next() 负责指标调用”的原则。

*当逻辑变得非常复杂并涉及多个操作时，通常最好将其封装在一个指示符中。*



**计算指标时的各种简写形式**

调用 Indicators 模块的函数计算指标时，默认是对 self.datas 数据对象中的第一张表格中的第一条line （默认第一条line是 close line）计算相关指标。以计算 5 日均线为例，各种不同级别的简写方式都是默认基于收盘价 close 计算 5 日均线，所以返回的结果都是一致的：

```scala

class TestStrategy(bt.Strategy):
    def __init__(self):
        # 最简方式：直接省略指向的数据集
        self.sma1 = btind.SimpleMovingAverage(period=5)
        # 只指定第一个数据表格
        self.sma2 = btind.SMA(self.data, period=5)
        # 指定第一个数据表格的close 线
        self.sma3 = btind.SMA(self.data.close, period=5)
        # 完整写法
        self.sma4 = btind.SMA(self.datas[0].lines[0], period=5)
        # 指标函数也支持简写 SimpleMovingAverage → SMA
        
    def next(self):
        # 提取当前时间点
        print('datetime', self.datas[0].datetime.date(0))
        # 打印当日、昨日、前日的均线
        print('sma1',self.sma1.get(ago=0, size=3))
        print('sma2',self.sma2.get(ago=0, size=3))
        print('sma3',self.sma3.get(ago=0, size=3))
        print('sma4',self.sma4.get(ago=0, size=3))
```



**好用的运算函数**



在计算指标或编写策略逻辑时，离不开算术运算、关系运算、逻辑运算、条件运算......，为了更好的适用于Backtrader 框架的语法规则，Backtrader 的开发者还对一些常用的运算符做了优化和改进，使用起来更简便高效：

```python
class TestStrategy(bt.Strategy):
    
    def __init__(self):
        self.sma5 = btind.SimpleMovingAverage(period=5) # 5日均线
        self.sma10 = btind.SimpleMovingAverage(period=10) # 10日均线
        # bt.And 中所有条件都满足时返回 1；有一个条件不满足就返回 0
        self.And = bt.And(self.data>self.sma5, self.data>self.sma10, self.sma5>self.sma10)
        # bt.Or 中有一个条件满足时就返回 1；所有条件都不满足时返回 0
        self.Or = bt.Or(self.data>self.sma5, self.data>self.sma10, self.sma5>self.sma10)
        # bt.If(a, b, c) 如果满足条件 a，就返回 b，否则返回 c
        self.If = bt.If(self.data>self.sma5,1000, 5000)
        # bt.All,同 bt.And
        self.All = bt.All(self.data>self.sma5, self.data>self.sma10, self.sma5>self.sma10)
        # bt.Any，同 bt.Or
        self.Any = bt.Any(self.data>self.sma5, self.data>self.sma10, self.sma5>self.sma10)
        # bt.Max，返回同一时刻所有指标中的最大值
        self.Max = bt.Max(self.data, self.sma10, self.sma5)
        # bt.Min，返回同一时刻所有指标中的最小值
        self.Min = bt.Min(self.data, self.sma10, self.sma5)
        # bt.Sum，对同一时刻所有指标进行求和
        self.Sum = bt.Sum(self.data, self.sma10, self.sma5)
        # bt.Cmp(a,b), 如果 a>b ，返回 1；否则返回 -1
        self.Cmp = bt.Cmp(self.data, self.sma5)
        
    def next(self):
        print('---------- datetime',self.data.datetime.date(0), '------------------')
        print('close:', self.data[0], 'ma5:', self.sma5[0], 'ma10:', self.sma10[0])
        print('close>ma5',self.data>self.sma5, 'close>ma10',self.data>self.sma10, 'ma5>ma10', self.sma5>self.sma10)
        print('self.And', self.And[0], self.data>self.sma5 and self.data>self.sma10 and self.sma5>self.sma10)
        print('self.Or', self.Or[0], self.data>self.sma5 or self.data>self.sma10 or self.sma5>self.sma10)
        print('self.If', self.If[0], 1000 if self.data>self.sma5 else 5000)
        print('self.All',self.All[0], self.data>self.sma5 and self.data>self.sma10 and self.sma5>self.sma10)
        print('self.Any', self.Any[0], self.data>self.sma5 or self.data>self.sma10 or self.sma5>self.sma10)
        print('self.Max',self.Max[0], max([self.data[0], self.sma10[0], self.sma5[0]]))
        print('self.Min', self.Min[0], min([self.data[0], self.sma10[0], self.sma5[0]]))
        print('self.Sum', self.Sum[0], sum([self.data[0], self.sma10[0], self.sma5[0]]))
        print('self.Cmp', self.Cmp[0], 1 if self.data>self.sma5 else -1)
```



**如何对齐不同周期的指标**



通常情况下，操作的都是相同周期的数据，比如日度行情数据计算返回各类日度指标、周度行情数据计算返回各类周度指标、......，行情数据和指标的周期是一致的，时间也是对齐的。但有时候也会遇到操作不同周期数据的情况，比如拿日度行情与月度指标作比较，日度行情每天都有数据，而月度指标每个月只有一个，2 条数据在时间上是没有对齐的



可以使用“ ( ) ”语法操作来对齐不同周期的数据，对齐的方向是“大周期向小周期对齐”，可以选择指标对象中的某条 line 进行对齐，也可以对整个指标对象进行对齐。在使用该语法时，要将 cerebro.run() 中的 runonce 设置为 False，才能实现对齐操作：



```python
# self.data0 是日度行情、self.data1 是月度行情
self.month = btind.xxx(self.data1) # 计算返回的 self.month 指标也是月度的
# 选择指标对象中的第一条 line 进行对齐
self.sellsignal = self.data0.close < self.month.lines[0]()
# 对齐整个指标对象
self.month_ = self.month()
self.signal = self.data0.close < self.month_.lines[0]

cerebro.run(runonce=False)
```



“ ( ) ”语法类似于线的切片操作 get (ago=-1, size=1)，然后在更细的时间点上始终取当前最新的指标值。比如对于月度指标，向日度对齐时，月中的那些时间点的数据取得是当前最新的数据（即：月初的指标值），直到下个月月初新的指标值计算出来为止



**在 Backtrader 中调用 TA-Lib 库**



为了满足大家的使用习惯，Backtrader 还接入了 TA-Lib 技术指标库，具体信息可以查阅官方 document ：*https://www.backtrader.com/docu/talibindautoref/* ，文档中同样对各个函数的输入、输出，以及在 Backtrader 中特有的绘图参数、返回的 lines 属性等信息都做了介绍和说明。TA-Lib 指标函数的调用形式为 bt.talib.xxx ：



```python
class TALibStrategy(bt.Strategy):
    def __init__(self):
        # 计算 5 日均线
        bt.talib.SMA(self.data.close, timeperiod=5)
        bt.indicators.SMA(self.data, period=5)
        # 计算布林带
        bt.talib.BBANDS(self.data, timeperiod=25)
        bt.indicators.BollingerBands(self.data, period=25)
```



**自定义新指标**



在 Backtrader 中，如果涉及到自定义操作，一般都是通过继承原始的父类，然后在新的子类里自定义属性，比如之前介绍的自定义数据读取函数 class My_CSVData (bt.feeds.GenericCSVData)，就是继承了原始GenericCSVData 类，自定义新指标也类似，需要继承原始的 bt.Indicator 类，然后在新的子类里构建指标。新的子类里通常可以设置如下属性：



- lines = ('xxx', 'xxx', 'xxx',)：定义指标函数返回的 lines 名称，方便后面通过名称调用具体的指标，如 self.lines.xxx、self.l.xxx、self.xxx；
- params = (('xxx', n),)：定义参数，方便在子类里全局调用，也方便在使用指标函数时修改参数取值；
- __init__() 方法：同策略 Strategy 里的 __init__() 类似，对整条 line 进行运算，运算结果也以整条 line 的形式返回；
- next() 方法：同策略 Strategy 里的 next() 类似，每个 bar 都会运行一次，在 next() 中是对数据点进行运算；
- once() 方法：这个方法只运行一次，但是需要从头到尾循环计算指标；
- 指标绘图相关属性的设置：例如：plotinfo = dict() 通过字典形式修改绘图参数；plotlines = dict() 设置曲线样式 等等，指标绘制相关内容会在后期的《可视化篇》进行重点讲解。
- 自定义指标时，建议首选 __init__()，因为 __init__() 最智能，能自动实现 next() 和 once() 的功能，计算指标一气呵成 。



```python
class MyInd(bt.Indicator):
    lines = (xxx,xxx, ) # 最后一个 “,” 别省略
    params = ((xxx, n),) # 最后一个 “,” 别省略
    
    def __init__(self):
        '''可选'''
        pass
    
    def next(self):
        '''可选'''
        pass
    
    def once(self):
        '''可选'''
        pass 
    
    plotinfo = dict(...)
    plotlines = dict(...)
    ...
```



下面是通过自定义指标复现 MACD 算法的例子，可以再具体的感受一下自定义指标的大致操作：



```python
class My_MACD(bt.Indicator):
    lines = ('macd', 'signal', 'histo')
    params = (('period_me1',12),
              ('period_me2', 26),
              ('period_signal', 9),)
    def __init__(self):
        me1 = EMA(self.data, period=self.p.period_me1)
        me2 = EMA(self.data, period=self.p.period_me2)
        self.l.macd = me1 - me2
        self.l.signal = EMA(self.l.macd, period=self.p.period_signal)
        self.l.histo = self.l.macd - self.l.signal
```

## 策略2

[参考](https://mp.weixin.qq.com/s?__biz=MzAxNTc0Mjg0Mg==&mid=2653317634&idx=1&sn=e92fec0b0b5fd5f62805e7c2be5830f8&chksm=802da817b75a2101c5812a6fc9daf0b2c08ce21d882bdd3059d2e9f391432b3ac9e950d5e151&cur_album_id=2380299870701420545&scene=189#wechat_redirect)



**基于交易信号直接生成策略**

除了在 Strategy 类中编写策略外，追求 “极简” 的 Backtrader 还给大家提供了一种更为简单的策略生成方式，这种方式不需要定义 Strategy 类，更不需要调用交易函数，只需计算信号 signal 指标，然后将其 add_signal 给大脑 Cerebro 即可，Cerebro 会自动将信号 signal 指标转换为交易指令，通常可以将这类策略称为信号策略 SignalStrategy 。下面以官方文档中的例子介绍信号策略生成方式：

- step1：自定义交易信号，交易信号和一般的指标相比的区别只在于：交易信号指标在通过 add_signal 传递给大脑后，大脑会将其转换为策略，所以在自定义交易信号时直接按照 Indicator 指标定义方式来定义即可（具体可以参考之前的《指标篇》）。定义时需要声明信号 'signal' 线，信号指标也是赋值给 'signal' 线；

- step2：按常规方式，实例化大脑 cerebro、加载数据、通过 add_signal 添加交易信号线 ；

- 备注1：信号策略每次下单的成交量取的是 Sizer 模块中的 FixedSize，默认成交 1 单位的标的，比如 1 股、1 张合约等；

- 备注2：生成的是市价单 Market，订单在被取消前一直都有效。



```
import backtrader as bt

# 自定义信号指标
class MySignal(bt.Indicator):
    lines = ('signal',) # 声明 signal 线，交易信号放在 signal line 上
    params = (('period', 30),)

    def __init__(self):
        self.lines.signal = self.data - bt.indicators.SMA(period=self.p.period)

# 实例化大脑
cerebro = bt.Cerebro()
# 加载数据
data = bt.feeds.OneOfTheFeeds(dataname='mydataname')
cerebro.adddata(data)
# 添加交易信号
cerebro.add_signal(bt.SIGNAL_LONGSHORT, MySignal, period=xxx)
cerebro.run()
```



支持添加多条交易信号：

```
import backtrader as bt

# 定义交易信号1
class SMACloseSignal(bt.Indicator):
    lines = ('signal',)
    params = (('period', 30),)

    def __init__(self):
        self.lines.signal = self.data - bt.indicators.SMA(period=self.p.period)

# 定义交易信号2
class SMAExitSignal(bt.Indicator):
    lines = ('signal',)
    params = (('p1', 5), ('p2', 30),)

    def __init__(self):
        sma1 = bt.indicators.SMA(period=self.p.p1)
        sma2 = bt.indicators.SMA(period=self.p.p2)
        self.lines.signal = sma1 - sma2
        
# 实例化大脑
cerebro = bt.Cerebro()
# 加载数据
data = bt.feeds.OneOfTheFeeds(dataname='mydataname')
cerebro.adddata(data)
# 添加交易信号1
cerebro.add_signal(bt.SIGNAL_LONG, MySignal, period=xxx)
# 添加交易信号2
cerebro.add_signal(bt.SIGNAL_LONGEXIT, SMAExitSignal, p1=xxx, p2=xxx)
cerebro.run()
```



**信号指标取值与多空信号对应关系：**

- signal 指标取值大于0 → 对应多头 long 信号；
- signal 指标取值小于0 → 对应空头 short 信号；
- signal 指标取值等于0 → 不发指令；



## Plotting 不推荐

cerebro.plot() 写在 cerebro.run() 后面，用于回测的可视化。总的来说，cerebro.plot() 支持回测如下 3 大内容：

- Data Feeds：即在回测开始前，通过 adddata、replaydata、resampledata 等方法导入大脑的原始数据；
- Indicators ：即回测时构建的各类指标，比如在 strategy 中构建的指标、通过 addindicator 添加的；
- Observers ：即上文介绍的观测器对象； [参考](https://mp.weixin.qq.com/s?__biz=MzAxNTc0Mjg0Mg==&mid=2653317947&idx=1&sn=8422b62036c4a0693114f6b779fb9cde&chksm=802da92eb75a20380ed04560bf2ed947d7879d5f0f806b094dccc30cc8de83e269c73c375931&cur_album_id=2380299870701420545&scene=189#wechat_redirect)
- 在绘制图形时，默认是将 Data Feeds 绘制在主图上；Indicators 有的与 Data Feeds 一起绘制在主图上，比如均线，有的以子图形式绘制；Observers 通常绘制在子图上。



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

## 分析器

在 Backtrader 中，有专门负责回测收益评价指标计算的模块 analyzers，大家可以将其称为“策略分析器”。关于 analyzers 支持内置的指标分析器的具体信息可以参考官方文档 Backtrader ~ Analyzers Reference 。分析器的使用主要分为 2 步：



- 第一步：通过 addanalyzer(ancls, _name, *args, **kwargs) 方法将分析器添加给大脑，ancls 对应内置的分析器类，后面是分析器各自支持的参数，添加的分析器类 ancls 在 cerebro running 区间会被实例化，并分配给 cerebro 中的每个策略，然后分析每个策略的表现，而不是所有策略整体的表现 ；

- 第二步：分别基于results = cerebro.run() 返回的各个对象 results[x] ，提取该对象 analyzers 属性下的各个分析器的计算结果，并通过 get_analysis() 来获取具体值。



- 说明：addanalyzer() 时，通常会通过 _name 参数对分析器进行命名，在第二步获取分析器结果就是通过_name 来提取的。



```python
......
# 添加分析指标
# 返回年初至年末的年度收益率
cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='_AnnualReturn')
# 计算最大回撤相关指标
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='_DrawDown')
# 计算年化收益：日度收益
cerebro.addanalyzer(bt.analyzers.Returns, _name='_Returns', tann=252)
# 计算年化夏普比率：日度收益
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='_SharpeRatio', timeframe=bt.TimeFrame.Days, annualize=True, riskfreerate=0) # 计算夏普比率
cerebro.addanalyzer(bt.analyzers.SharpeRatio_A, _name='_SharpeRatio_A')
# 返回收益率时序
cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='_TimeReturn')
# 启动回测
result = cerebro.run()

# 提取结果
print("--------------- AnnualReturn -----------------")
print(result[0].analyzers._AnnualReturn.get_analysis())
print("--------------- DrawDown -----------------")
print(result[0].analyzers._DrawDown.get_analysis())
print("--------------- Returns -----------------")
print(result[0].analyzers._Returns.get_analysis())
print("--------------- SharpeRatio -----------------")
print(result[0].analyzers._SharpeRatio.get_analysis())
print("--------------- SharpeRatio_A -----------------")
print(result[0].analyzers._SharpeRatio_A.get_analysis())
......
```



各个分析器的结果通常以 OrderedDict 字典的形式返回，如下所示，大家可以通过 keys 取需要的 values：



```python
AutoOrderedDict([('len', 56),
                 ('drawdown', 8.085458202746946e-05),
                 ('moneydown', 8.08547225035727),
                 ('max',
                  AutoOrderedDict([('len', 208),
                                   ('drawdown', 0.00015969111320873712),
                                   ('moneydown', 15.969112889841199)]))])

# 常用指标提取
analyzer = {}
# 提取年化收益
analyzer['年化收益率'] = result[0].analyzers._Returns.get_analysis()['rnorm']
analyzer['年化收益率（%）'] = result[0].analyzers._Returns.get_analysis()['rnorm100']
# 提取最大回撤
analyzer['最大回撤（%）'] = result[0].analyzers._DrawDown.get_analysis()['max']['drawdown'] * (-1)
# 提取夏普比率
analyzer['年化夏普比率'] = result[0].analyzers._SharpeRatio_A.get_analysis()['sharperatio']

# 日度收益率序列
ret = pd.Series(result[0].analyzers._TimeReturn.get_analysis())
```



除了上面提到的这些内置分析器外，Backtrader 当然还支持自定义分析器（不然就不符合 Backtrader style 了）。凡是涉及到自定义的操作，遵循的都是“在继承了 xxx 原始父类的基础上，在新的子类里自定义相关属性和方法”，分析器毕竟是用来分析整个回测的，既涉及过程，又涉及结果，所以继承的 bt.Analyzer 父类中的方法和相应的运行逻辑和策略中的基本一致：



```python
import backtrader as bt # 导入 Backtrader
    
# 官方提供的 SharpeRatio 例子
class SharpeRatio(Analyzer):
    params = (('timeframe', TimeFrame.Years), ('riskfreerate', 0.01),)

    def __init__(self):
        super(SharpeRatio, self).__init__()
        self.anret = AnnualReturn()

    def start(self):
        # Not needed ... but could be used
        pass

    def next(self):
        # Not needed ... but could be used
        pass

    def stop(self):
        retfree = [self.p.riskfreerate] * len(self.anret.rets)
        retavg = average(list(map(operator.sub, self.anret.rets, retfree)))
        retdev = standarddev(self.anret.rets)
        self.ratio = retavg / retdev
        
    def get_analysis(self):
        return dict(sharperatio=self.ratio)
      
      
例子2

class trade_list(bt.Analyzer):
    def __init__(self):

        self.trades = []
        self.cumprofit = 0.0

    def notify_trade(self, trade):

        if trade.isclosed:
            brokervalue = self.strategy.broker.getvalue()

            dir = 'short'
            if trade.history[0].event.size > 0: dir = 'long'

            pricein = trade.history[len(trade.history)-1].status.price
            priceout = trade.history[len(trade.history)-1].event.price
            datein = bt.num2date(trade.history[0].status.dt)
            dateout = bt.num2date(trade.history[len(trade.history)-1].status.dt)
            if trade.data._timeframe >= bt.TimeFrame.Days:
                datein = datein.date()
                dateout = dateout.date()

            pcntchange = 100 * priceout / pricein - 100
            pnl = trade.history[len(trade.history)-1].status.pnlcomm
            pnlpcnt = 100 * pnl / brokervalue
            barlen = trade.history[len(trade.history)-1].status.barlen
            pbar = pnl / barlen
            self.cumprofit += pnl

            size = value = 0.0
            for record in trade.history:
                if abs(size) < abs(record.status.size):
                    size = record.status.size
                    value = record.status.value

            highest_in_trade = max(trade.data.high.get(ago=0, size=barlen+1))
            lowest_in_trade = min(trade.data.low.get(ago=0, size=barlen+1))
            hp = 100 * (highest_in_trade - pricein) / pricein
            lp = 100 * (lowest_in_trade - pricein) / pricein
            if dir == 'long':
                mfe = hp
                mae = lp
            if dir == 'short':
                mfe = -lp
                mae = -hp

            self.trades.append({'ref': trade.ref,
             'ticker': trade.data._name,
             'dir': dir，
             'datein': datein,
             'pricein': pricein,
             'dateout': dateout,
             'priceout': priceout,
             'chng%': round(pcntchange, 2),
             'pnl': pnl, 'pnl%': round(pnlpcnt, 2),
             'size': size,
             'value': value,
             'cumpnl': self.cumprofit,
             'nbars': barlen, 'pnl/bar': round(pbar, 2),
             'mfe%': round(mfe, 2), 'mae%': round(mae, 2)})
            
    def get_analysis(self):
        return self.trades
```



**PyFolio**

BackTrader bt.analyzers.PyFolio，不涉及 PyFolio 库。本节梳理返回的四组数据，都包含哪些内容。

|       值       |    变量名    |                      说明                      | 对应 Analyzer  |
| :------------: | :----------: | :--------------------------------------------: | :------------: |
|   TimeReturn   |   returns    |                    回报序列                    |   TimeReturn   |
| PositionsValue |  positions   |                    仓位序列                    | PositionsValue |
|  Transactions  | transactions | 每笔交易，按照 `(size, price, value)` 格式记录 |  Transactions  |
| GrossLeverage  |  gross_lev   |        追踪总杠杆率（策略的投资额度）。        | GrossLeverage  |

从中可以看出，bt.analyzers.PyFolio 的四组数据，在内部分别由对应的子 Analyzer 负责实现。每组数据的功能，可参见对应的子 Analyzer 介绍文章。

## 策略进阶

[参考](https://mp.weixin.qq.com/s?__biz=MzAxNTc0Mjg0Mg==&mid=2653317634&idx=1&sn=e92fec0b0b5fd5f62805e7c2be5830f8&chksm=802da817b75a2101c5812a6fc9daf0b2c08ce21d882bdd3059d2e9f391432b3ac9e950d5e151&cur_album_id=2380299870701420545&scene=189#wechat_redirect)



如果策略的收益表现可能受相关参数的影响，需要验证比较参数不同取值对策略表现的影响，就可以使用 Backtrader 的参数优化功能，使用该功能只需通过 cerebro.optstrategy() 方法往大脑添加策略即可：



```python
class TestStrategy(bt.Strategy):
  
    params=(('period1',5),
            ('period2',10),) #全局设定均线周期
    ......

    
# 实例化大脑
cerebro1= bt.Cerebro(optdatas=True, optreturn=True)
# 设置初始资金
cerebro1.broker.set_cash(10000000)
# 加载数据
datafeed1 = bt.feeds.PandasData(dataname=data1, fromdate=datetime.datetime(2019,1,2), todate=datetime.datetime(2021,1,28))
cerebro1.adddata(datafeed1, name='600466.SH')

# 添加优化器
cerebro1.optstrategy(TestStrategy, period1=range(5, 25, 5), period2=range(10, 41, 10))

# 添加分析指标
# 返回年初至年末的年度收益率
cerebro1.addanalyzer(bt.analyzers.AnnualReturn, _name='_AnnualReturn')
# 计算最大回撤相关指标
cerebro1.addanalyzer(bt.analyzers.DrawDown, _name='_DrawDown')
# 计算年化收益
cerebro1.addanalyzer(bt.analyzers.Returns, _name='_Returns', tann=252)
# 计算年化夏普比率
cerebro1.addanalyzer(bt.analyzers.SharpeRatio_A, _name='_SharpeRatio_A')
# 返回收益率时序
cerebro1.addanalyzer(bt.analyzers.TimeReturn, _name='_TimeReturn')

# 启动回测
result = cerebro1.run()

# 打印结果
def get_my_analyzer(result):
    analyzer = {}
    # 返回参数
    analyzer['period1'] = result.params.period1
    analyzer['period2'] = result.params.period2
    # 提取年化收益
    analyzer['年化收益率'] = result.analyzers._Returns.get_analysis()['rnorm']
    analyzer['年化收益率（%）'] = result.analyzers._Returns.get_analysis()['rnorm100']
    # 提取最大回撤(习惯用负的做大回撤，所以加了负号)
    analyzer['最大回撤（%）'] = result.analyzers._DrawDown.get_analysis()['max']['drawdown'] * (-1)
    # 提取夏普比率
    analyzer['年化夏普比率'] = result.analyzers._SharpeRatio_A.get_analysis()['sharperatio']
    
    return analyzer
  
ret = []
for i in result:
    ret.append(get_my_analyzer(i[0]))
    
pd.DataFrame(ret)

# 优化结果
period1 period2 年化收益率 年化收益率（%） 最大回撤（%） 年化夏普比率
0  5  10  4.024514e-05  4.024514e-03  -0.010175  -140.948647
1  5  20  -3.240455e-06  -3.240455e-04  -0.008839  -229.402157
2  5  30  -1.211110e-05  -1.211110e-03  -0.008674  -236.577612
3  5  40  -1.284502e-05  -1.284502e-03  -0.011886  -370.807650
4  10  10  0.000000e+00  0.000000e+00  -0.000000   NaN
5  10  20  8.568641e-06  8.568641e-04  -0.009392  -282.835125
6  10  30  1.835459e-06  1.835459e-04  -0.008545  -265.568666
7  10  40  -7.817367e-06  -7.817367e-04  -0.013492  -261.387903
8  15  10  -6.560915e-09  -6.560915e-07  -0.017579  -161.893285
9  15  20  -1.857955e-05  -1.857955e-03  -0.009652  -611.196458
10  15  30  -2.226534e-05  -2.226534e-03  -0.008160  -641.959703
11  15  40  1.708522e-05  1.708522e-03  -0.013492  -213.637841
12  20  10  -3.799574e-05  -3.799574e-03  -0.025414  -109.665911
13  20  20  0.000000e+00  0.000000e+00  -0.000000   NaN
14  20  30  -1.398007e-05  -1.398007e-03  -0.010388  -527.518303
15  20  40  6.699340e-06  6.699340e-04  -0.013492  -301.729232
```





[策略案例](https://mp.weixin.qq.com/s?__biz=MzAxNTc0Mjg0Mg==&mid=2653330626&idx=1&sn=83bed9723d81cd6b636f3efff43db926&chksm=802d5ed7b75ad7c19927c4fce4d5da4aa39d87bf9e519f1c5e64ee4aae82cdbb55c7e5ef5c65&cur_album_id=2380299870701420545&scene=189#wechat_redirect)