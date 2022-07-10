---
layout: post
category: Mybatis
title: Mybatis复杂查询Example文件
tags: Mybatis
---

## 如何进行混合查询

简单介绍：

Criteria，包含一个 Cretiron 的集合,每一个 Criteria 对象内包含的 Cretiron 之间是由 AND 连接的,是逻辑与的关系。

oredCriteria，Example 内有一个成员叫 oredCriteria,是 Criteria 的集合,就想其名字所预示的一样，这个集合中的 Criteria 是由 OR 连接的，是逻辑或关系。oredCriteria 就是 ORed Criteria。

查询条件 1：a=? and (b=? or c=?) 不支持

查询条件 2：(a=? And b=?) or (a=? And c=?) 支持

**写法 1**

```java
DemoExample example=new DemoExample();

DemoExample.Criteria criteria1=example.createCriteria();
criteria1.andAEqualTo(?).andBEqualTo(?);

DemoExample.Criteria criteria2=example.createCriteria();
criteria2.andAEqualTo(?).andCEqualTo(?);

example.or(criteria2);

SqlSession sqlSession = MyBatisUtil.openSession();
DemoMapper m = sqlSession.getMapper(DemoMapper.class);
m.countByExample(example);
//生成的sql语句
select count(*) from demo WHERE ( a = ? and b = ? ) or ( a = ? and c = ? )
```

**写法 2**

推荐

```java
DemoExample example=new DemoExample();

example.or().andAEqualTo(?).andBEqualTo(?);
example.or().andAEqualTo(?).andCEqualTo(?);

SqlSession sqlSession = MyBatisUtil.openSession();
DemoMapper m = sqlSession.getMapper(DemoMapper.class);
m.countByExample(example);
//生成的sql语句
select count(*) from demo WHERE ( a = ? and b = ? ) or ( a = ? and c = ? )
```

## 单独查询用法

### 1.模糊搜索用户名：

```java
String name = "明";
UserExample ex = new UserExample();
ex.createCriteria().andNameLike('%'+name+'%');
List<User> userList = userDao.selectByExample(ex);
```

### 2.通过某个字段排序：

```java
String orderByClause = "id DESC";
UserExample ex = new UserExample();
ex.setOrderByClause(orderByClause);
List<User> userList = userDao.selectByExample(ex);
```

### 3.条件搜索，不确定条件的个数：

```java
UserExample ex = new UserExample();
Criteria criteria = ex.createCriteria();
if(StringUtils.isNotBlank(user.getAddress())){
	criteria.andAddressEqualTo(user.getAddress());
}
if(StringUtils.isNotBlank(user.getName())){
	criteria.andNameEqualTo(user.getName());
}
List<User> userList = userDao.selectByExample(ex);
```

### 4.分页搜索列表：

```java
pager.setPageNum(1);
pager.setPageSize(5);
UserExample ex = new UserExample();
ex.setPage(pager);
List<User> userList = userDao.selectByExample(ex);
```
