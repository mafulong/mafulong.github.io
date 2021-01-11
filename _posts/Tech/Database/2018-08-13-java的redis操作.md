---
layout: post
category: Database
title: java的redis操作
tags: Database
---

## 安装
### win10
[下载地址](https://github.com/MicrosoftArchive/redis/releases)

安装目录下运行 redis-server.exe redis.windows.conf 。

redis-cli.exe -h 127.0.0.1 -p 6379

设置键值对 set myKey abc

取出键值对 get myKey

![](https://i.imgur.com/WyKgA86.jpg)

server是服务器启动，cli是客户端

## Jedis

### Related jars
```xml
    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.12</version>
        </dependency>
        <dependency>
            <groupId>redis.clients</groupId>
            <artifactId>jedis</artifactId>
            <version>2.9.0</version>
        </dependency>
        <dependency>
            <groupId>org.apache.commons</groupId>
            <artifactId>commons-pool2</artifactId>
            <version>2.6.0</version>
        </dependency>
    </dependencies>
```

### connection and test
```java
package com.mfl;

import org.junit.Test;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

/**
 * jedis
 */
public class Demo1 {
    @Test
    /**
     * connection test1
     */
    public void t1(){
        //1. 设置ip和端口
        Jedis jedis=new Jedis("127.0.0.1",6379);
        //2. 保存数据
        jedis.set("name","mafulong");
        //3. get the data
        String value=jedis.get("name");
        System.out.println(value);
        jedis.close();
    }
    @Test
    /**
     * pool test
     */
    public void t2(){
        JedisPoolConfig config=new JedisPoolConfig();
        //设置最大连接数
        config.setMaxTotal(30);
        //最大空闲连接数
        config.setMaxIdle(10);
        //获得连接池
        JedisPool jedisPool=new JedisPool(config,"127.0.0.1",6379);
        //获得核心对象
        Jedis jedis=null;
        try{
            jedis=jedisPool.getResource();
            jedis.set("name","mafulong2");
            System.out.println(jedis.get("name"));
        }catch (Exception e){
            e.printStackTrace();
        }finally {
            if(jedis!=null){
                jedis.close();
            }
            if(jedisPool!=null){
                jedisPool.close();
            }
        }
    }

}

```

## Data structure

1. String
2. hash
3. list
4. set
5. sorted list

**Note for Key definition:**

1. not too long
2. not too short
3. unifed naming

### String
Assignment and get: 

	set key value
	get key
	getset key newvalue //get value and reassign
	del key

nil: it means value doesn't exist

incr num: if no value exists, create 0 and incr; Or add 1

decr num: initial value is 0

incrby num 5: add 5 every time

decrby num 3: reduce 3 every time

append num 5: append 5 if num exists, or create a key 0 and assigned to 5

-1: represents the last element in the list. Like this,-2 represents the second to last.

### hash

	//set
	hset hashname field-key value
	hmset myhash2 name mafulong age 18
	hget myhash name
	
	//get
	hmget myhash2 name age
	hgetall myhash
	//get all the values
	
	//delete
	hdel myhash2 name
	del myhash2
	
	//incr
	hincrby myhash age 5
	
	//if exist
	hexists myhash
	
	hgetall myhash
	
	hlen myhash
	
	hkeys myhash
	
	hvals myhash

### list
Redis列表是简单的字符串列表，按照插入顺序排序。你可以添加一个元素到列表的头部（左边）或者尾部（右边）

左边插入,就是从左边头插，因此a在最右边

	lpush mylist a b c
	//add a b c

右边插入
	
	rpush mylist a b c

查看链表

	lrange mylist 

弹出

	lpop mylist
	
	rop mylist

获取元素个数

	llen mylist

### set

	sadd set-key item
	sismember set-key item4
	smembers set-key
	//del 
	srem myset 1 2
	//diff
	sdiff myset1 myset2
	//inter
	sinter myset1 myset2
	//union
	sunion myset1 myset2
	//get the size
	scard myset


```

redis re 127.0.0.1:6379> sadd runoob redis
(integer) 1
redis 127.0.0.1:6379> sadd runoob mongodb
(integer) 1
redis 127.0.0.1:6379> sadd runoob rabitmq
(integer) 1
redis 127.0.0.1:6379> sadd runoob rabitmq
(integer) 0
redis 127.0.0.1:6379> smembers runoob
1) "redis"
2) "rabitmq"
3) "mongodb"
```

### sorted set
Redis zset 和 set 一样也是string类型元素的集合,且不允许重复的成员。

不同的是每个元素都会关联一个double类型的分数。redis正是通过分数来为集合中的成员进行从小到大的排序。

zset的成员是唯一的,但分数(score)却可以重复。

```
redis 127.0.0.1:6379> zadd runoob 0 redis
(integer) 1
redis 127.0.0.1:6379> zadd runoob 0 mongodb
(integer) 1
redis 127.0.0.1:6379> zadd runoob 0 rabitmq
(integer) 1
redis 127.0.0.1:6379> zadd runoob 0 rabitmq
(integer) 0
redis 127.0.0.1:6379> > ZRANGEBYSCORE runoob 0 1000
1) "mongodb"
2) "rabitmq"
3) "redis"
```
