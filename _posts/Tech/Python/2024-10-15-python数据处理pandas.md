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
- 索引和索引标签不一样，一般索引是索引标签，但Series也可以s[idx]使用，其中idx从0开始递增，这个就是真正的索引。 
  

```python
a = [1, 2, 3]
# 一个kv map
# 索引是0开头的
s = pd.Series(a)
print(s)
# 1,4,3是索引标签，和索引不一样！
s = pd.Series(a, index=[1, 4, 3])
print(s)
print(s[1])
# a,b,c,d为index
s = pd.Series({'a': 1, 'b': 2, 'c': 3, 'd': 4})
print(s)
# 这是索引取值, 返回的还是个Series，不是索引标签取值
print(s[1:4])
# 索引标签取值
print(s['a'])
print(s['a':'d'])
s['a'] = "哈哈哈"
# 删除
del s['a']
s['a'] = "哈哈哈"
s = s.drop(['a'])
s['a'] = 3
print(s)
# 运算, value是数字才行
s = s * 2
print(s)
# 过滤, 过滤value
s = s[s > 2]
print(s)
print(s.sum())
print(type(s.index))
# numpy.ndarry
print(type(s.values))
s = s.astype('float64')
print(s.dtype)
```

```python


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

**DataFrame**： 类似于一个二维表格，它是 Pandas 中最重要的数据结构。DataFrame 可以看作是由多个 Series 按列排列构成的表格，它既有行索引也有列索引，因此可以方便地进行行列选择、过滤、合并等操作。

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
# 也可以加个index=[a,b,c]作为索引标签，默认是[0,1,2]
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
		
这里的第一个参数是索引标签，不能数字索引来访问。
        # 通过 .loc[] 访问
        print(df.loc[:, 'Column1'])

        # 通过 .iloc[] 访问
        print(df.iloc[:, 0])  # 假设 'Column1' 是第一列

        print(df.iloc[1, 0]) 两个参数都是数字索引行索引和列索引
        print(df.loc['a', "Column1"])



loc:

使用标签（label）进行选择。
可以用来选择行和列的名字，例如 df.loc[行标签, 列标签]。
包括结束位置的值，即区间是闭合的。例如，df.loc[0:2] 会选择从行标签 0 到 2 的所有行。
iloc:

使用整数位置（integer position）进行选择。
用于按位置选择数据，例如 df.iloc[行索引, 列索引]。
不包括结束位置的值，即区间是开放的。例如，df.iloc[0:2] 只会选择行索引为 0 和 1 的行，不包括 2。



        # 访问单个元素 后面的是索引标签。如果是数字索引请用iloc
        print(df['Name']['a'])


        # 修改
        df['Column1'] = [10, 11, 12]

        # 添加新行
        new_row = {'Column1': 13, 'Column2': 14, 'NewColumn': 16}
        df = df.append(new_row, ignore_index=True)

        # 删除列
        df_dropped = df.drop('Column1', axis=1)
        # 删除行
        df_dropped = df.drop(0)  # 删除索引为 0 的行


，concat 函数用于将多个 DataFrame 或 Series 沿着特定轴（行或列）进行拼接。

df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})
沿着行方向拼接 DataFrame：变成4行
result = pd.concat([df1, df2])
变成4列
result = pd.concat([df1, df2], axis=1)


索引可以修改
df_set = df.set_index('Column1')
过滤

df[df['column_name'] > value]	选择列中满足条件的行。




# 索引和切片
print(df[['Name', 'Age']])  # 提取多列
print(df[1:3])               # 切片行
print(df.loc[:, 'Name'])     # 提取单列
print(df.loc[1:2, ['Name', 'Age']])  # 标签索引提取指定行列
print(df.iloc[:, 1:])        # 位置索引提取指定列



        df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                          columns=['Column1', 'Column2', 'Column3'], index=['a', 'b', 'c'])
        print(df)
        print(df.loc[:])
        print(df.loc['b':])
        print(df['Column1'][0])
        print(df['Column1']['a'])
        # print(df['a'])
        print(df.iloc[1, 0])
        print(df.loc['a', "Column1"])
        print(df)

        # Row是个Dict, index是索引标签
        for index, row in df.iterrows():
            print(f'Index: {index}, A: {row["Column1"]}, B: {row["Column2"]}')
        # index=True为包含索引
        #  列名作为对象属性来访问, 推荐这个, 性能较快，但不知道列名就需要用上面那个
        for row in df.itertuples(index=True):
            print(f'Index: {row.Index}, A: {row.Column1}, B: {row.Column2}')
        # 拿到列名 可for循环查看
        print(df.columns)

        # column_data是Series 这个列的所有数据，column_name就是列名
        for column_name, column_data in df.items():
            print(f'Column: {column_name}')
            print(column_data)
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

