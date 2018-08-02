---
layout: post
category: python
title: python连接mysql
---

## PyMySQL 安装

    pip install PyMySQL

或者

    $ git clone https://github.com/PyMySQL/PyMySQL
    $ cd PyMySQL/
    $ python3 setup.py install

## SQL
```sql
create table EMPLOYEE(
FIRST_NAME varchar(20),
LAST_NAME varchar(20),
AGE int,
SEX varchar(20),
INCOME int);
```
## 连接数据库
```python
import pymysql
user="root"
password="123456"
dbname="TESTDB"
# 打开数据库连接
db = pymysql.connect("localhost",user,password,dbname )
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()
# 关闭数据库连接
db.close()
```

## 创建表
```python
# 使用 execute() 方法执行 SQL，如果表存在则删除
cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
 
# 使用预处理语句创建表
sql = """CREATE TABLE EMPLOYEE (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,  
         SEX CHAR(1),
         INCOME FLOAT )"""
 
cursor.execute(sql)
```

## 插入
```python
# SQL 插入语句
sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
         LAST_NAME, AGE, SEX, INCOME)
         VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
try:
   # 执行sql语句
   cursor.execute(sql)
   # 提交到数据库执行
   db.commit()
except:
   # 如果发生错误则回滚
   db.rollback()
```

## 查询

fetchone(): 该方法获取下一个查询结果集。结果集是一个对象

fetchall(): 接收全部的返回结果行.

rowcount: 这是一个只读属性，并返回执行execute()方法后影响的行数。

```python
# SQL 查询语句
sql = "SELECT * FROM EMPLOYEE \
       WHERE INCOME > '%d'" % (1000)
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 获取所有记录列表
   results = cursor.fetchall()
   for row in results:
      fname = row[0]
      lname = row[1]
      age = row[2]
      sex = row[3]
      income = row[4]
       # 打印结果
      print ("fname=%s,lname=%s,age=%d,sex=%s,income=%d" % \
             (fname, lname, age, sex, income ))
except:
   print ("Error: unable to fetch data")
```

## 更新
```python
# SQL 更新语句
sql = "UPDATE EMPLOYEE SET AGE = AGE + 1 WHERE SEX = '%c'" % ('M')
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 提交到数据库执行
   db.commit()
except:
   # 发生错误时回滚
   db.rollback()
```

## 删除
```python
# SQL 删除语句
sql = "DELETE FROM EMPLOYEE WHERE AGE > '%d'" % (20)
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 提交修改
   db.commit()
except:
   # 发生错误时回滚
   db.rollback()
```

