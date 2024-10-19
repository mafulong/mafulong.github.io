---
layout: post
category: Python
title: python数据处理pandas
tags: Python
---

## python数据处理pandas

# Numpy

NumPy 最重要的一个特点是其 N 维数组对象 ndarray，它是一系列同类型数据的集合，以 0 下标为开始进行集合中元素的索引。

ndarray 对象是用于存放同类型元素的多维数组。

ndarray 中的每个元素在内存中都有相同存储大小的区域。

ndarray 内部由以下内容组成：

- 一个指向数据（内存或内存映射文件中的一块数据）的指针。
- 数据类型或 dtype，描述在数组中的固定大小值的格子。
- 一个表示数组形状（shape）的元组，表示各维度大小的元组。
- 一个跨度元组（stride），其中的整数指的是为了前进到当前维度下一个元素需要"跨过"的字节数。



```scala
import numpy as np 
a = np.array([1,2,3])  
print (a)

a = np.array([[1,  2],  [3,  4]])  
print (a)

设置维度2

a = np.array([1, 2, 3, 4, 5], ndmin =  2)  
print (a)


多数据类型
# 类型字段名可以用于存取实际的 age 列
import numpy as np
dt = np.dtype([('age',np.int8)]) 
a = np.array([(10,),(20,),(30,)], dtype = dt) 
print(a['age'])

x =  [1,2,3] 
a = np.asarray(x)  


```



# Pandas

Pandas 主要引入了两种新的数据结构：**DataFrame** 和 **Series**。

- **Series**： 类似于一维数组或列表，是由一组数据以及与之相关的数据标签（索引）构成。Series 可以看作是 DataFrame 中的一列，也可以是单独存在的一维数据结构。
  - `Series` 中的数据是有序的。
  - 可以将 `Series` 视为带有索引的一维数组。
  - 索引可以是唯一的，但不是必须的。
  - 数据可以是标量、列表、NumPy 数组等。

- **DataFrame**： 类似于一个二维表格，它是 Pandas 中最重要的数据结构。DataFrame 可以看作是由多个 Series 按列排列构成的表格，它既有行索引也有列索引，因此可以方便地进行行列选择、过滤、合并等操作。

```python
        import pandas as pd

        a = [1, 2, 3]
        myvar = pd.Series(a)
        print(myvar)
        print(myvar[1])
        # 指定索引
        a = ["Google", "Runoob", "Wiki"]
        myvar = pd.Series(a, index=["x", "y", "z"])
        print(myvar)
        # 字典创建对象
        sites = {1: "Google", 2: "Runoob", 3: "Wiki"}
        myvar = pd.Series(sites)
        print(myvar)

        # 运算
        # 算术运算
        series = pd.Series([2,3,3,2])
        result = series * 2  # 所有元素乘以2
        print(result)
        # 过滤
        filtered_series = series[series > 2]  # 选择大于2的元素
        # 数学函数
        import numpy as np
        result = np.sqrt(series)  # 对每个元素取平方根

        # 统计
        s = series

        # 获取索引
        index = s.index

        # 获取值数组
        values = s.values

        # 获取描述统计信息
        stats = s.describe()

        # 获取最大值和最小值的索引
        max_index = s.idxmax()
        min_index = s.idxmin()

        # 其他属性和方法
        print(s.dtype)  # 数据类型
        print(s.shape)  # 形状
        print(s.size)  # 元素个数
        print(s.head())  # 前几个元素，默认是前 5 个
        print(s.tail())  # 后几个元素，默认是后 5 个
        print(s.sum())  # 求和
        print(s.mean())  # 平均值
        print(s.std())  # 标准差
        print(s.min())  # 最小值
        print(s.max())  # 最大值

```





Dataframe, 类似spark里的dataframe

```scala
       import pandas as pd
        data = [['Google', 10], ['Runoob', 12], ['Wiki', 13]]
        # 创建DataFrame
        df = pd.DataFrame(data, columns=['Site', 'Age'])
        df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                          columns=['Column1', 'Column2', 'Column3'])
        # 使用astype方法设置每列的数据类型
        df['Site'] = df['Site'].astype(str)
        df['Age'] = df['Age'].astype(float)
        print(df)

        #字典形式来创建
        data = {'Site': ['Google', 'Runoob', 'Wiki'], 'Age': [10, 12, 13]}
        df = pd.DataFrame(data)


        import numpy as np
        # 创建一个包含网站和年龄的二维ndarray
        ndarray_data = np.array([
            ['Google', 10],
            ['Runoob', 12],
            ['Wiki', 13]
        ])
        # 使用DataFrame构造函数创建数据帧
        df = pd.DataFrame(ndarray_data, columns=['Site', 'Age'])
        # 返回第一行
        print(df.loc[0])
        # 返回第二行
        print(df.loc[1])
        # 返回第一行和第二行
        print(df.loc[[0, 1]])

        # DataFrame 的属性和方法
        print(df.shape)  # 形状
        print(df.columns)  # 列名
        print(df.index)  # 索引
        print(df.head())  # 前几行数据，默认是前 5 行
        print(df.tail())  # 后几行数据，默认是后 5 行
        print(df.info())  # 数据信息
        print(df.describe())  # 描述统计信息
        print(df.mean())  # 求平均值
        print(df.sum())  # 求和

        # 通过列名访问
        print(df['Column1'])

        # 通过属性访问
        print(df.Name)

        # 通过 .loc[] 访问
        print(df.loc[:, 'Column1'])

        # 通过 .iloc[] 访问
        print(df.iloc[:, 0])  # 假设 'Column1' 是第一列

        # 访问单个元素
        print(df['Name'][0])


        # 修改
        df['Column1'] = [10, 11, 12]

        # 添加新行
        new_row = {'Column1': 13, 'Column2': 14, 'NewColumn': 16}
        df = df.append(new_row, ignore_index=True)

        # 删除列
        df_dropped = df.drop('Column1', axis=1)
        # 删除行
        df_dropped = df.drop(0)  # 删除索引为 0 的行
```

## Matplotlib

常用的 pyplot 函数：

- `plot()`：用于绘制线图和散点图
- `scatter()`：用于绘制散点图
- `bar()`：用于绘制垂直条形图和水平条形图
- `hist()`：用于绘制直方图
- `pie()`：用于绘制饼图
- `imshow()`：用于绘制图像
- `subplots()`：用于创建子图



```scala
import matplotlib.pyplot as plt
import numpy as np

xpoints = np.array([0, 6])
ypoints = np.array([0, 100])

plt.plot(xpoints, ypoints)
plt.show()

# 画单条线
plot([x], y, [fmt], *, data=None, **kwargs)
# 画多条线
plot([x], y, [fmt], [x2], y2, [fmt2], ..., **kwargs)
参数说明：

x, y：点或线的节点，x 为 x 轴数据，y 为 y 轴数据，数据可以列表或数组。
fmt：可选，定义基本格式（如颜色、标记和线条样式）。
**kwargs：可选，用在二维平面图上，设置指定属性，如标签，线的宽度等。



    print(df.head())
    df['MA2'] = df['price'].rolling(window=2).mean()
    import matplotlib.pyplot as plt
    plt.figure(figsize=(50, 30))
    plt.plot(df['ts'], df['price'], label="价格", color='blue')
    plt.plot(df['ts'], df['MA2'], label="MA2", color='red')

    # 设置图表标题和标签
    plt.title('分时图与移动平均线')
    plt.xlabel('时间')
    plt.ylabel('价格')
    plt.legend()
    plt.grid(True)

    # 展示图表
    plt.show()


```

| Item\Metrics | Avg    | p90     | P99     |
| ----------------------------- | ------ | ------- | ------- |
| C (No display on Desktop)     | 984.97 | 1849.12 | 3126.60 |
| T1 (Display TB Widget on ATF) | 996.65 | 1856.86 | 3178.04 |
| Increased Latency | 11.68 | 7.74 | 51.44 |
| Increased Latency Percentage | 1.19% | 0.42% | 1.64% |

