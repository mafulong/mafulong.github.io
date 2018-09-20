---
layout: post
category: SSM
title: Mybatix之mapper接口代理方法
---

## mapper代理方法
程序员只需要mapper接口（相当 于dao接口）

程序员还需要编写mapper.xml映射文件

程序员编写mapper接口需要遵循一些开发规范，mybatis可以自动生成mapper接口实现类代理对象。


## 开发规范
在mapper.xml中namespace等于mapper接口地址

```xml
<!--
 namespace 命名空间，作用就是对sql进行分类化管理,理解为sql隔离
 注意：使用mapper代理方法开发，namespace有特殊重要的作用,namespace等于mapper接口地址
 -->
<mapper namespace="com.iot.mybatis.mapper.UserMapper">
```

## 具体代码
项目下载可以参考我的github

UserMapper2.xml
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.mfl.map.UserMapper">
    <insert id="insert">
        insert into users(name,age) values (#{name},#{age})
    </insert>
    <update id="update" >
        update users set name=#{name}, age=#{age} where id=#{id}
    </update>
    <select id="selectOne" parameterType="int" resultType="com.mfl.model.User">
        select * from users where id=#{id1}
    </select>
    <select id="selectList" parameterType="int" resultType="com.mfl.model.User">
        select * from users where age=#{age}
    </select>
    <select id="selectAll" resultType="com.mfl.model.User">
        select * from users
    </select>
</mapper>
```

map接口类
```java
package com.mfl.map;

import com.mfl.model.User;

import javax.jws.soap.SOAPBinding;
import java.util.List;

public interface UserMapper {
    public void insert(User user);
    public void update(User user);
    public User selectOne(int id);
    public List<User> selectList(int age);
    public List<User> selectAll();

}

```

单元测试
```java
package com.mfl.mybatisdemo.test;

import com.mfl.map.UserMapper;
import com.mfl.model.User;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;
import org.junit.Test;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;

public class TestUserMapperInterface {
    @Test
    public void test1(){
        String resource = "mybatis-config.xml";
        InputStream inputStream = null;
        try {
            inputStream = Resources.getResourceAsStream(resource);
        } catch (IOException e) {
            e.printStackTrace();
        }
        SqlSessionFactory sqlSessionFactory =
                new SqlSessionFactoryBuilder().build(inputStream);
        SqlSession sqlSession=sqlSessionFactory.openSession();
        UserMapper userMapper=sqlSession.getMapper(UserMapper.class);
//        User user=new User();
//        user.setName("0802");
//        user.setAge(100);
//        for(int i=0;i<5;i++){
//            userMapper.insert(user);
//        }
        User user=userMapper.selectOne(1);
        System.out.println(user);
        userMapper.insert(new User("wahh",23));
        List<User> list=userMapper.selectAll();

        System.out.println(list);

        sqlSession.commit();
        sqlSession.close();
    }
}

```