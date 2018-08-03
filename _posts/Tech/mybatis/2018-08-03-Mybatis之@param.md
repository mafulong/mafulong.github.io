---
layout: post
category: mybatis
title: Mybatis之@param
---

实现多参数传入

```java
public interface UserMapper {
    public void insert(User user);
    public void update(User user);
    public User selectOne(int id);
    public List<User> selectList(int age);
    public List<User> selectAll();
    public List<User> selectUserByBetweenAandB(@Param("a")int a1,@Param("b")int b1);
}

```


```xml
    <select id="selectUserByBetweenAandB" resultType="com.mfl.model.User">
        select * from users where age between #{a} and #{b1}
    </select>
```