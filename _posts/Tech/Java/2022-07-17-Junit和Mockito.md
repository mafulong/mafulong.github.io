---
layout: post
category: Java
title: Junit和Mockito
tags: Java
---

# Junit

## 例子+常用注解

需要使用junit.jar这个包。

 @Test 注解，表示这个方法是一个测试方法。

常用注解

- @Test:将一个普通方法修饰成一个测试方法 @Test(excepted=xx.class): xx.class 表示异常类，表示测试的方法抛出此异常时，认为是正常的测试通过的 @Test(timeout = 毫秒数) :测试方法执行时间是否符合预期
- @BeforeClass： 会在所有的方法执行前被执行，static 方法 （全局只会执行一次，而且是第一个运行）
- @AfterClass：会在所有的方法执行之后进行执行，static 方法 （全局只会执行一次，而且是最后一个运行）
- @Before：会在每一个测试方法被运行前执行一次
- @After：会在每一个测试方法运行后被执行一次
- @Ignore：所修饰的测试方法会被测试运行器忽略
- @RunWith：可以更改测试运行器 org.junit.runner.Runner
- Parameters：参数化注解

例子

```java
import static org.junit.Assert.*;

import org.junit.*;

/**
 * 了解一个测试类单元测试的执行顺序为：
 * @BeforeClass –> @Before –> @Test –> @After –> @AfterClass
 * @author hao
 *
 */
public class TestJunit1 {
  @BeforeClass
  public static void setUpBeforeClass() throws Exception {
    System.out.println("in BeforeClass================");
  }
 
  @AfterClass
  public static void tearDownAfterClass() throws Exception {
    System.out.println("in AfterClass=================");
  }
 
  @Before
  public void before() {
    System.out.println("in Before");
  }
 
  @After
  public void after() {
    System.out.println("in After");
  }
 
  @Test(timeout = 10000)
  public void testadd() {
    TestJunit2 a = new TestJunit2();
    assertEquals(6, a.add(3, 3));
    System.out.println("in Test ----Add");
  }
 
  @Test
  public void testdivision() {
    TestJunit2 a = new TestJunit2();
    assertEquals(3, a.division(6, 2));
    System.out.println("in Test ----Division");
  }
 
  @Ignore
  @Test
  public void test_ignore() {
    TestJunit2 a = new TestJunit2();
    assertEquals(6, a.add(1, 5));
    System.out.println("in test_ignore");
  }
 
  @Test
  public void teest_fail() {
    fail();
  }
}
class TestJunit2 extends Thread {
   
  int result;
 
  public int add(int a, int b) {
    try {
      sleep(1000);
      result = a + b;
    } catch (InterruptedException e) {
    }
    return result;
  }
 
  public int division(int a, int b) {
    return result = a / b;
  }
}
```

一个**测试类单元测试的执行顺序**为：

**@BeforeClass –> @Before –> @Test –> @After –> @AfterClass**

每一个**测试方法的调用顺序**为：

@Before –> @Test –> @After



## JUnit的一些注意事项

- 测试方法必须使用 @Test 修饰
- 测试方法必须使用 public void 进行修饰，不能带参数
- 一般使用单元测试会新建一个 test 目录存放测试代码，在生产部署的时候只需要将 test 目录下代码删除即可
- 测试代码的包应该和被测试代码包结构保持一致
- 测试单元中的每个方法必须可以独立测试，方法间不能有任何依赖
- 测试类一般使用 Test 作为类名的后缀
- 测试方法使一般用 test 作为方法名的前缀

## **Assert的用法**

Assert就是断言，断言是编写测试用例的核心实现方式，即期望值是多少，测试的结果是多少，以此来判断测试是否通过。

Assert的核心方法：

![img](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202207171631342.jpeg)

## TestSuite测试套件

测试套件，一下执行多个测试类。

需要遵循以下规则：

1. 创建一个空类作为测试套件的入口。
2. 使用注解 org.junit.runner.RunWith 和 org.junit.runners.Suite.SuiteClasses 修饰这个空类。
3. 将 org.junit.runners.Suite 作为参数传入注解 RunWith，以提示 JUnit 为此类使用套件运行器执行。
4. 将需要放入此测试套件的测试类组成数组作为注解 SuiteClasses 的参数。
5. 保证这个空类使用 public 修饰，而且存在公开的不带有任何参数的构造函数

## 异常测试、参数测试

[参考](https://www.w3cschool.cn/junit/1h4e1hva.html)

# Mockito

[Tutorial](https://www.baeldung.com/mockito-series)

## 添加mockito



```xml
      <dependency>
          <groupId>org.mockito</groupId>
          <artifactId>mockito-all</artifactId>
          <version>1.9.5</version>
          <scope>test</scope>
      </dependency>
      <dependency>
        <groupId>junit</groupId>
        <artifactId>junit</artifactId>
        <version>4.11</version>
        <scope>test</scope>
      </dependency>

```



```java
import static org.mockito.Mockito.*;
import static org.junit.Assert.*;
```

## Spy和mock

spy 和 mock不同，不同点是：

- spy 的参数是对象示例，mock 的参数是 class。
- 被 spy 的对象，调用其方法时默认会走真实方法。mock 对象不会。

mock默认是返回默认值的。



## 注解

@Mock用于代替Mockito.mock创建mock对象。



spy 对应注解 @Spy，和 @Mock 是一样用的。



对于@Spy，如果发现修饰的变量是 null，会自动调用类的无参构造函数来初始化。

所以下面两种写法是等价的：

```java
// 写法1
@Spy
private ExampleService spyExampleService;

// 写法2
@Spy
private ExampleService spyExampleService = new ExampleService();
```

## 测试隔离

根据 JUnit 单测隔离 ，当 Mockito 和 JUnit 配合使用时，也会将非static变量或者非单例隔离开。

比如使用 @Mock 修饰的 mock 对象在不同的单测中会被隔离开。

## 实现原理

Mockito使用继承的方式实现mock的，用CGLIB生成mock对象代替真实的对象进行执行，为了mock实例的方法，你可以在subclass中覆盖它。

因此无法mock静态方法。
