---
layout: post
category: Java
title: Junit和Mockito
tags: Java
---

# Junit4

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

## 测试隔离

JUnit中每个测试方法都是在独立的类实例中执行的，因此只要没有使用全局变量和外部资源（如数据库和API），这些测试都将是彼此隔离的，即不管一个测试做什么，都不会影响其他测试。

[参考](https://www.letianbiji.com/java/java-test-junit-isolate.html)



### 测试运行器

JUnit 中所有的测试方法都是由测试运行器负责执行的。JUnit 为单元测试提供了默认的测试运行器，但 JUnit 并没有限制您必须使用默认的运行器。相反，您不仅可以定制自己的运行器（所有的运行器都继承自 org.junit.runner.Runner），而且还可以为每一个测试类指定使用某个具体的运行器。指定方法也很简单，使用注解 `org.junit.runner.RunWith` 在测试类上显式的声明要使用的运行器即可：

```java
@RunWith(CustomTestRunner.class) 
 public class TestWordDealUtil { 
……
 }
```

显而易见，如果测试类没有显式的声明使用哪一个测试运行器，JUnit 会启动默认的测试运行器执行测试类（比如上面提及的单元测试代码）。一般情况下，默认测试运行器可以应对绝大多数的单元测试要求；当使用 JUnit 提供的一些高级特性（例如即将介绍的两个特性）或者针对特殊需求定制 JUnit 测试方式时，显式的声明测试运行器就必不可少了。

## 异常测试、参数测试

[参考](https://www.w3cschool.cn/junit/1h4e1hva.html)

# Junit5

区别: 

注解不同：

- @Before变成了@BeforeEach。
- @After变成了@AfterEach。
- @BeforeClass变成了@BeforeAll。
- @AfterClass变成了@AfterAll。
- @Ignore变成了@Disabled。
- @Category变成了@Tag。
- @Rule和@ClassRule没有了，用@ExtendWith和@RegisterExtension代替。



扩展不同：

在JUnit 4中，使用Spring框架构建测试看起来是这样的：

```java
@RunWith(SpringJUnit4ClassRunner.class)
public class MyControllerTest {
    // ...
}
```

在JUnit 5中，你可以用Spring扩展来代替：

```java
@ExtendWith(SpringExtension.class)
class MyControllerTest {
    // ...
}
```

@ExtendWith 注解是可重复的，这意味着多个扩展可以很容易地组合在一起。

你也可以通过创建一个类来实现org.junit.jupiter.api.extendWith中的一个或多个接口，然后用@ExtendWith将其添加到你的测试中，从而轻松定义你自己的自定义扩展。

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



指定包名 Mockito



测试类加相关注解

Junit5:

```java
@ExtendWith(MockitoExtension.class)
public class UserServiceUnitTest {

```

Junit4:

```java
@RunWith(MockitoJUnitRunner.class)

@RunWith(PowerMockRunner.class)
```

##  创建 Mock 对象

```reasonml
@Test
public void createMockObject() {
    // 使用 mock 静态方法创建 Mock 对象.
    List mockedList = mock(List.class);
    Assert.assertTrue(mockedList instanceof List);

    // mock 方法不仅可以 Mock 接口类, 还可以 Mock 具体的类型.
    ArrayList mockedArrayList = mock(ArrayList.class);
    Assert.assertTrue(mockedArrayList instanceof List);
    Assert.assertTrue(mockedArrayList instanceof ArrayList);
}
```

如上代码所示, 我们调用了 **mock** 静态方法来创建一个 Mock 对象. mock 方法接收一个 class 类型, 即我们需要 mock 的类型.



when需要在mock对象上操作！！

包名冲突的可以用Mockito.when来操作

只有调用mock对象的方法才是走的mock逻辑，实际对象还不是mock的。

## 配置 Mock 对象

当我们有了一个 Mock 对象后, 我们可以定制它的具体的行为. 例如:

```java
@Test
public void configMockObject() {
    List mockedList = mock(List.class);

    // 我们定制了当调用 mockedList.add("one") 时, 返回 true
    when(mockedList.add("one")).thenReturn(true);
    // 当调用 mockedList.size() 时, 返回 1
    when(mockedList.size()).thenReturn(1);

    Assert.assertTrue(mockedList.add("one"));
    // 因为我们没有定制 add("two"), 因此返回默认值, 即 false.
    Assert.assertFalse(mockedList.add("two"));
    Assert.assertEquals(mockedList.size(), 1);

    Iterator i = mock(Iterator.class);
    when(i.next()).thenReturn("Hello,").thenReturn("Mockito!");
    String result = i.next() + " " + i.next();
    //assert
    Assert.assertEquals("Hello, Mockito!", result);
}
```

我们使用 **when(...).thenReturn(...)** 方法链来定义一个行为, 例如 "when(mockedList.add("one")).thenReturn(true)" 表示: **当调用了mockedList.add("one"), 那么返回 true.**. 并且要注意的是, **when(...).thenReturn(...)** 方法链不仅仅要匹配方法的调用, 而且要方法的参数一样才行.

而且有趣的是, **when(​...).thenReturn(​...)** 方法链可以指定多个返回值, 当这样做后, 如果多次调用指定的方法, 那么这个方法会依次返回这些值. 例如 "when(i.next()).thenReturn("Hello,").thenReturn("Mockito!");", 这句代码表示: 第一次调用 i.next() 时返回 "Hello,", 第二次调用 i.next() 时返回 "Mockito!".

上面的例子我们展示了方法调用返回值的定制, 那么我们可以指定一个抛出异常吗? 当然可以的, 例如:

```reasonml
@Test(expected = NoSuchElementException.class)
public void testForIOException() throws Exception {
    Iterator i = mock(Iterator.class);
    when(i.next()).thenReturn("Hello,").thenReturn("Mockito!"); // 1
    String result = i.next() + " " + i.next(); // 2
    Assert.assertEquals("Hello, Mockito!", result);

    doThrow(new NoSuchElementException()).when(i).next(); // 3
    i.next(); // 4
}
```

上面代码的第一第二步我们已经很熟悉了, 接下来第三部我们使用了一个新语法: `doThrow(ExceptionX).when(x).methodCall`, 它的含义是: 当调用了 x.methodCall 方法后, 抛出异常 ExceptionX.
因此 doThrow(new NoSuchElementException()).when(i).next() 的含义就是: 当第三次调用 i.next() 后, 抛出异常 NoSuchElementException.(因为 i 这个迭代器只有两个元素)



## 误解 注意事项

Mockito.mock() 并不是mock一整个类，而是根据传进去的一个类，mock出属于这个类的一个对象，并且返回这个mock对象；而传进去的这个类本身并没有改变，用这个类new出来的对象也没有受到任何改变！



mock出来的对象并不会自动替换掉正式代码里面的对象，你必须要有某种方式把mock对象应用到正式代码里面



mock后直接生效 默认是无限次数



## 对于手动new而不是依赖注入的Mock

[参考](https://stackoverflow.com/questions/5920153/test-class-with-a-new-call-in-it-with-mockito)

```java
public class TestedClass {
  public LoginContext login(String user, String password) {
    LoginContext lc = new LoginContext("login", callbackHandler);
  }
}
```

1. Mock 生成这个动作new, 改成用工厂生成，这样就可以Mock这个工厂了

   You can use a factory to create the login context. Then you can mock the factory and return whatever you want for your test.

```java
// 新方法
  public LoginContext login(String user, String password) {
    LoginContext lc = loginContextFactory.createLoginContext();
  }


public interface LoginContextFactory {
  public LoginContext createLoginContext();
}
```



1. mock部分方法，改写有new的方法逻辑， 用spy

   ```java
   TestedClass tc = spy(new TestedClass());
   LoginContext lcMock = mock(LoginContext.class);
   when(tc.login(anyString(), anyString())).thenReturn(lcMock);
   ```

## 校验 Mock 对象的方法调用

Mockito 会追踪 Mock 对象的所用方法调用和调用方法时所传递的参数. 我们可以通过 verify() 静态方法来来校验指定的方法调用是否满足断言. 语言描述有一点抽象, 下面我们仍然以代码来说明一下.

```routeros
@Test
public void testVerify() {
    List mockedList = mock(List.class);
    mockedList.add("one");
    mockedList.add("two");
    mockedList.add("three times");
    mockedList.add("three times");
    mockedList.add("three times");
    when(mockedList.size()).thenReturn(5);
    Assert.assertEquals(mockedList.size(), 5);

    verify(mockedList, atLeastOnce()).add("one");
    verify(mockedList, times(1)).add("two");
    verify(mockedList, times(3)).add("three times");
    verify(mockedList, never()).isEmpty();
}
```

上面的例子前半部份没有什么特别的, 我们关注后面的:

```scss
verify(mockedList, atLeastOnce()).add("one");
verify(mockedList, times(1)).add("two");
verify(mockedList, times(3)).add("three times");
verify(mockedList, never()).isEmpty();
```

读者根据代码也应该可以猜测出它的含义了, 很简单:

- 第一句校验 mockedList.add("one") 至少被调用了 1 次(atLeastOnce)
- 第二句校验 mockedList.add("two") 被调用了 1 次(times(1))
- 第三句校验 mockedList.add("three times") 被调用了 3 次(times(3))
- 第四句校验 mockedList.isEmpty() 从未被调用(never)



Mockito.verify(mockUserManager).performLogin("xiaochuang", "xiaochuang password");

这句话的作用是，验证 mockUserManager 的 performLogin() 得到了调用，同时参数是“xiaochuang”和"xiaochuang password"。其实更准确的说法是，这行代码验证的是， mockUserManager 的 performLogin() 方法得到了 一次 调用。因为这行代码其实是：

Mockito.verify(mockUserManager, Mockito.times(1)).performLogin("xiaochuang", "xiaochuang password");

的简写，或者说重载方法，注意其中的 Mockito.times(1) 。

## 使用 spy() 部分模拟对象

对于一个mock对象，我们可以指定返回值和执行特定的动作，当然，也可以不指定，如果不指定的话，一个mock对象的所有非void方法都将返回默认值：int、long类型方法将返回0，boolean方法将返回false，对象方法将返回null等等；而void方法将什么都不做。

如果你想实现这样的效果：指定时执行指定的动作，不指定时调用这个对象的默认实现，同时又能拥有验证方法调用的功能。那你可以使用Mockito.spy()来创建对象。



Mockito 提供的 spy 方法可以包装一个真实的 Java 对象, 并返回一个包装后的新对象. 若没有特别配置的话, 对这个新对象的所有方法调用, 都会委派给实际的 Java 对象. 例如:

```java
@Test
public void testSpy() {
    List list = new LinkedList();
    List spy = spy(list);

    // 对 spy.size() 进行定制.
    when(spy.size()).thenReturn(100);

    spy.add("one");
    spy.add("two");

    // 因为我们没有对 get(0), get(1) 方法进行定制,
    // 因此这些调用其实是调用的真实对象的方法.
    Assert.assertEquals(spy.get(0), "one");
    Assert.assertEquals(spy.get(1), "two");

    Assert.assertEquals(spy.size(), 100);
}
```

这个例子中我们实例化了一个 LinkedList 对象, 然后使用 spy() 方法对 list 对象进行部分模拟. 接着我们使用 **when(...).thenReturn(...)** 方法链来规定 spy.size() 方法返回值是 100. 随后我们给 spy 添加了两个元素, 然后再 调用 spy.get(0) 获取第一个元素.
这里有意思的地方是: 因为我们没有定制 add("one"), add("two"), get(0), get(1), 因此通过 spy 调用这些方法时, 实际上是委派给 list 对象来调用的.
然而我们 定义了 spy.size() 的返回值, 因此当调用 spy.size() 时, 返回 100.

## Spy和mock 对比，Stub

spy 和 mock不同，不同点是：

- spy 的参数是对象示例，mock 的参数是 class。
- 被 spy 的对象，调用其方法时默认会走真实方法。mock 对象不会。

mock默认是返回默认值的。



**假定**调用`dao`层的某方法时它的返回值是什么，这个过程就是**Stub**

## 执行特定动作 (替换成另一个方法)

```java
public class LoginPresenterTest {
   LoginPresenter loginPresenter;
   @Test
   public void testLogin() {
       UserManager mockUserManager = Mockito.mock(UserManager.class);
       PasswordValidator mPasswordValidator = Mockito.mock(PasswordValidator.class);
       Mockito.when(mPasswordValidator.verifyPassword(Mockito.anyString())).thenReturn(true);
​
       loginPresenter = new LoginPresenter(mockUserManager, mPasswordValidator);
​
       Mockito.doAnswer(new Answer() {
           @Override
           public Object answer(InvocationOnMock invocation) throws Throwable {
               //这里可以获得传给performLogin的参数
               Object[] arguments = invocation.getArguments();

               //callback是第三个参数
               UserManager.NetCallback callback = (UserManager.NetCallback) arguments[2];
               callback.onFailure("404 Not found");
               return 404;
          }
      }).when(mockUserManager).performLogin(Mockito.anyString(), Mockito.anyString(), Mockito.any(UserManager.NetCallback.class));

       loginPresenter.login("aya", "123456");
  }
}
```

通过doAnswer方法，生成替换，里面取Arguments手动转化来做某些事情。

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

## 实现原理-继承

Mockito使用继承的方式实现mock的，用CGLIB生成mock对象代替真实的对象进行执行，为了mock实例的方法，你可以在subclass中覆盖它。

因此无法mock静态方法。

**不能mock静态、final、私有方法**

## 参考

[手把手教你 Mockito 的使用](https://segmentfault.com/a/1190000006746409)



# Mockito 高版本特性

依赖上，一般是说要用 `mockito-inline` 替换 `mockito-core` 依赖。 实质上 `mockito-inline` 就是给 mockito-core 添加了两个插件配置



使用了什么技术？ bytebuddy, 运行时生成Java class



注意mockito mock静态只对当前线程有效， 这点不如powermock

## Mock静态无参方法支持

```java
@Test
void givenStaticMethodWithNoArgs_whenMocked_thenReturnsMockSuccessfully() {
    assertThat(StaticUtils.name()).isEqualTo("Baeldung");

    try (MockedStatic<StaticUtils> utilities = Mockito.mockStatic(StaticUtils.class)) {
        utilities.when(StaticUtils::name).thenReturn("Eugen");
        assertThat(StaticUtils.name()).isEqualTo("Eugen");
    }

    assertThat(StaticUtils.name()).isEqualTo("Baeldung");
}
```

从 Mockito 3.4.0 开始，我们可以使用*Mockito.mockStatic(Class<T> classToMock)*方法来模拟对静态方法调用的调用。**此方法为我们的类型返回一个\*MockedStatic\*对象，它是一个作用域模拟对象。**

因此，在我们上面的单元测试中，*实用程序*变量表示具有线程局部显式范围的模拟。**请务必注意，作用域模拟必须由激活模拟的实体关闭。**这就是为什么我们在 try-with-resources 构造中定义我们的模拟，以便在我们完成作用域块时自动关闭模拟。

## Mock带参数的静态方法

我们通常用的 Mockito.when(T methodCall) 的参数是一个方法调用的返回值，所以当 Mock 带参数的静态方法时与 Mockito.when(obj.foo(1, 2)).thenReturn(34)) 的用法是不一样的，MockedStatic.when() 的参数需要放一个 () -> 对象.of(anyInt(), anyInt(), anyInt()) 这样的 Lambda. 



比如原来是函数A(b int)

```java
theMock.when(() -> 类.A(any())).thenReturn(xxx);
```

theMock就是MockStatic返回的。

对静态方法调用的 verify 也要用 theMock 的 verify() 方法，而不是 Mockito.verify()。

## Mock final类和方法

和正常无区别

[参考](https://www.baeldung.com/mockito-final)

## Mock 自己new的对象

```
        //mock代码中自己new的实例及“该实例的方法”        
        MockedConstruction<NewObject> newObjectMocked = Mockito.mockConstruction(NewObject.class);        Mockito.when(obj.haha()).thenReturn("who am i ?");

```

[参考](https://cloud.tencent.com/developer/article/1877722)

# PowerMockito

## 和mockito比较

**Mockito、EasyMock、JMock等比较流行Mock框架有个共同的缺点，都不能mock静态、final、私有方法等，而PowerMock可以完美解决以上框架的不足**



## 使用

[参考](https://juejin.cn/post/6850418110105649166)

开头包是PowerMockito

### mock对Redis的静态调用

我们使用PowerMock来mock对静态方法的调用，注意需要将`RedisUtils`类，加入`@PrepareForTest`注解中，我们既mock了`getArray`方法，也mock了`setArray`方法，其实`setArray`不需要mock这里显式的mock了

mock静态类注意

1. 加到PrepareForTest
2. mockStatic下

```java
PowerMockito.mockStatic(RedisUtils.class);
// mock掉对Redis的静态调用
PowerMockito.when(RedisUtils.getArray(eq("tom"), eq(StudentBo.class))).thenReturn(Collections.emptyList());
// 显式的mock掉静态的void的方法（可以不mock）
PowerMockito.doNothing().when(RedisUtils.class, "setArray", anyString(), anyList(), anyInt());
复制代码
```

### mock单例类

mock单例类相对来说复杂一点，逻辑上先用Powermock mock出单例类，然后再给单例类的`getInstance`方法打桩，返回之前mock，再对mock类实际调用的方法打桩即可，代码如下

```scss
PowerMockito.mockStatic(SchoolManageProxy.class);
// Powermock mock出单例类
SchoolManageProxy mockSchoolManageProxy = PowerMockito.mock(SchoolManageProxy.class);
// 给单例类的getInstance方法打桩

PowerMockito.when(SchoolManageProxy.getInstance()).thenReturn(mockSchoolManageProxy);
// 对mock类queryPerson的方法打桩
when(mockSchoolManageProxy.queryPerson(anyList())).thenReturn(Collections.emptyList());
```

单例类就是构造方法为private无法实例化，



### mock私有方法

可以看到`queryStudentScoreByKeyword`方法调用了该类的私有方法`processKeyword`，如果该方法耗时过长，使用powermock也可以mock该私有方法。 这里用spy演示。

```csharp
// mock 实例
// spy的标准是：如果不打桩，默认执行真实的方法，如果打桩则返回桩实现。
studentServiceUnderTest = PowerMockito.spy(studentServiceUnderTest);
// mock私有方法processKeyword
// doReturn(...) when(...)不做真实调用，但是when(...) thenReturn(...)还是会真实调用原方法，只是返回了指定的结果
PowerMockito.doReturn("tom").when(studentServiceUnderTest, "processKeyword", anyString());
```

注意：

1. when不能调用private方法了，所以是用字符串表示。



## 注解 @PrepareForTest

当使用PowerMockito.whenNew方法时，必须加注解@PrepareForTest和@RunWith。注解@PrepareForTest里写的类是需要mock的new对象代码所在的类。


当需要mock final方法的时候，必须加注解@PrepareForTest和@RunWith。注解@PrepareForTest里写的类是final方法所在的类。 


当需要mock静态方法的时候，必须加注解@PrepareForTest和@RunWith。注解@PrepareForTest里写的类是静态方法所在的类。


当需要mock私有方法的时候, 只是需要加注解@PrepareForTest，注解里写的类是私有方法所在的类


当需要mock系统类的静态方法的时候，必须加注解@PrepareForTest和@RunWith。注解里写的类是需要调用系统方法所在的类






# 
