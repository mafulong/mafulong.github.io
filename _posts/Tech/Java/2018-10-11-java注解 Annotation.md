---
layout: post
category: Java
title: java注解 Annotation
tags: Java
---

## 注解

Annotation是Java5开始引入的新特征，中文名称叫注解。它提供了一种安全的类似注释的机制，用来将任何的信息或元数据（metadata）与程序元素（类、方法、成员变量等）进行关联。为程序的元素（类、方法、成员变量）加上更直观更明了的说明，这些说明信息是与程序的业务逻辑无关，并且供指定的工具或框架使用。Annontation像一种修饰符一样，应用于包、类型、构造方法、方法、成员变量、参数及本地变量的声明语句中。

Java注解是附加在代码中的一些元信息，用于一些工具在编译、运行时进行解析和使用，起到说明、配置的功能。注解不会也不能影响代码的实际逻辑，仅仅起到辅助性的作用。包含在 java.lang.annotation 包中。

### 注解的用处

1. 生成文档。这是最常见的，也是java 最早提供的注解。常用的有@param @return 等
2. 跟踪代码依赖性，实现替代配置文件功能。比如Dagger 2依赖注入，未来java开发，将大量注解配置，具有很大用处;
3. 在编译时进行格式检查。如@override 放在方法前，如果你这个方法并不是覆盖了超类方法，则编译时就能检查出。

### jdk5提供的注解

    @Override：告知编译器此方法是覆盖父类的
    @Deprecated：标注过时
    @SuppressWarnings：压制警告

## 自定义注解

### 元注解

java.lang.annotation提供了四种元注解，专门注解其他的注解（在自定义注解的时候，需要使用到元注解）：

    @Documented –注解是否将包含在JavaDoc中
    @Retention –什么时候使用该注解
    @Target –注解用于什么地方
    @Inherited – 是否允许子类继承该注解

1.）@Retention– 定义该注解的生命周期

    RetentionPolicy.SOURCE : 在编译阶段丢弃。这些注解在编译结束之后就不再有任何意义，所以它们不会写入字节码。@Override, @SuppressWarnings都属于这类注解。
    RetentionPolicy.CLASS : 在类加载的时候丢弃。在字节码文件的处理中有用。注解默认使用这种方式
    RetentionPolicy.RUNTIME : 始终不会丢弃，运行期也保留该注解，因此可以使用反射机制读取该注解的信息。我们自定义的注解通常使用这种方式。

2.）Target – 表示该注解用于什么地方。默认值为任何元素，表示该注解用于什么地方。可用的ElementType参数包括

    ElementType.CONSTRUCTOR:用于描述构造器
    ElementType.FIELD:成员变量、对象、属性（包括enum实例）
    ElementType.LOCAL_VARIABLE:用于描述局部变量
    ElementType.METHOD:用于描述方法
    ElementType.PACKAGE:用于描述包
    ElementType.PARAMETER:用于描述参数
    ElementType.TYPE:用于描述类、接口(包括注解类型) 或enum声明

3.) @Documented–一个简单的Annotations标记注解，表示是否将注解信息添加在java文档中。

4.) @Inherited – 定义该注解的地方是否子类可继承。

 @Inherited 元注解是一个标记注解，@Inherited阐述了某个被标注的类型是被继承的。如果一个使用了@Inherited修饰的annotation类型被用于一个class，则这个annotation将被用于该class的子类。



### 自定义注解
自定义注解类编写的一些规则:

1. Annotation型定义为@interface, 所有的Annotation会自动继承java.lang.Annotation这一接口,并且不能再去继承别的类或是接口.
2. 参数成员只能用public或默认(default)这两个访问权修饰
3. 参数成员只能用基本类型byte,short,char,int,long,float,double,boolean八种基本数据类型和String、Enum、Class、annotations等数据类型,以及这一些类型的数组.
4. 要获取类方法和字段的注解信息，必须通过Java的反射技术来获取 Annotation对象,因为你除此之外没有别的获取注解对象的方法
5. 注解也可以没有定义成员, 不过这样注解就没啥用了

PS:自定义注解需要使用到元注解

[自定义注解例子](https://www.cnblogs.com/acm-bingzi/p/javaAnnotation.html)

部分代码

```java
/**
 * 水果名称注解
 */
@Target(FIELD)
@Retention(RUNTIME)
@Documented
public @interface FruitName {
    String value() default "";
}
```

## 注解列表

### java注解

1. @Override: 表示该方法是重写父类的方法。
2. @Deprecated: 表示该方法已经过时，不推荐使用，但仍然可以使用。
3. @SuppressWarnings: 抑制警告信息。
4. @FunctionalInterface: 表示该接口是一个函数式接口。
5. @SafeVarargs: 表示方法使用了可变长度参数，并且对参数的类型安全性进行了验证。
6. @Retention: 表示注解的保留策略。
7. @Target: 表示注解的作用对象。
8. @Documented: 表示注解应该包含在生成的文档中。
9. @Inherited: 表示注解可以被继承。
10. @SuppressWarnings: 表示抑制编译器警告。
11. @FunctionalInterface: 表示函数式接口。
12. @SafeVarargs: 表示可变参数类型安全。
13. @Retention: 表示注解的保留策略。
14. @Target: 表示注解的作用对象。
15. @Documented: 表示注解应该包含在生成的文档中。
16. @Inherited: 表示注解可以被继承。
17. @Repeatable: 表示注解可以重复使用。
18. @Native: 表示方法的实现是由本地代码实现的。
19. @SuppressWarnings: 表示抑制编译器警告。
20. @FunctionalInterface: 表示函数式接口。
21. @SafeVarargs: 表示可变参数类型安全。
22. @Retention: 表示注解的保留策略。
23. @Target: 表示注解的作用对象。
24. @Documented: 表示注解应该包含在生成的文档中。
25. @Inherited: 表示注解可以被继承。
26. @Repeatable: 表示注解可以重复使用。
27. @Native: 表示方法的实现是由本地代码实现的。

### spring注解

1. @Component: 用于标识一个普通的Java对象为一个Spring Bean。
2. @Service: 用于标识一个业务逻辑层的Bean。
3. @Repository: 用于标识一个数据访问层的Bean。
4. @Controller: 用于标识一个控制器层的Bean。
5. @Configuration: 用于标识一个类为Spring配置类。
6. @Bean: 用于标识一个方法返回值为一个Bean实例。
7. @Autowired: 用于自动装配一个Bean。
8. @Qualifier: 用于指定自动装配的Bean的名称。
9. @Resource: 用于注入一个Bean。
10. @Value: 用于注入一个值。
11. @RequestMapping: 用于映射请求路径和处理方法。
12. @PathVariable: 用于获取请求路径中的参数。
13. @RequestParam: 用于获取请求参数。
14. @ResponseBody: 用于返回JSON或XML格式的数据。
15. @ExceptionHandler: 用于处理异常。
16. @Transactional: 用于标识一个方法或类为事务方法或类。
17. @Async: 用于标识一个方法为异步方法。
18. @Scheduled: 用于定时任务。
19. @PostConstruct: 用于在Bean初始化后执行的方法。
20. @PreDestroy: 用于在Bean销毁前执行的方法。

### Guice注解

1. @Inject: 用于标记需要注入依赖的构造方法、字段或方法。
2. @Named: 用于标记需要注入的依赖，通过名称来指定具体的实现类。
3. @Singleton: 用于标记一个类为单例，每次注入时都返回同一个实例。
4. @Provides: 用于标记一个方法为提供依赖的方法。
5. @ScopeAnnotation: 用于标记一个注解为作用域注解，该注解可以用于自定义作用域。
6. @Assisted: 用于标记需要通过工厂方法注入的依赖。
7. @AssistedInject: 用于标记需要通过工厂方法注入的类，自动生成工厂方法。
8. @ImplementedBy: 用于标记一个接口的默认实现类。
9. @Interceptor: 用于标记一个类为拦截器。
10. @InterceptorBinding: 用于标记一个注解为拦截器绑定注解。

### Spring MVC注解

1. @Controller: 用于标识一个类为控制器类。
2. @RestController: 用于标识一个类为RESTful风格的控制器类。
3. @RequestMapping: 用于映射请求路径和处理方法。
4. @GetMapping: 用于映射GET请求。
5. @PostMapping: 用于映射POST请求。
6. @PutMapping: 用于映射PUT请求。
7. @DeleteMapping: 用于映射DELETE请求。
8. @PatchMapping: 用于映射PATCH请求。
9. @PathVariable: 用于获取请求路径中的参数。
10. @RequestParam: 用于获取请求参数。
11. @RequestBody: 用于获取请求体中的数据。
12. @ResponseBody: 用于返回JSON或XML格式的数据。
13. @ResponseStatus: 用于指定返回的HTTP状态码。
14. @ExceptionHandler: 用于处理异常。
15. @ModelAttribute: 用于绑定请求参数到模型中。
16. @SessionAttribute: 用于将模型属性保存到会话中。
17. @ModelAttribute: 用于绑定模型属性到请求中。

### Lombok 注解

1. @Getter/@Setter: 用于自动生成getter/setter方法。
2. @ToString: 用于自动生成toString方法。
3. @EqualsAndHashCode: 用于自动生成equals和hashCode方法。
4. @NoArgsConstructor/@AllArgsConstructor: 用于自动生成无参/有参构造函数。可以同时用，同时加多个构造函数。AllArgsConstructor它能够自动生成一个包含所有字段作为参数的构造函数， 会对非final字段也生效。
5. @RequiredArgsConstructor: 用于自动生成必要的参数构造函数。只对final的类字段生产构造函数。
6. @Data: 用于自动生成getter/setter、toString、equals和hashCode方法。
7. @Value: 用于生成不可变的JavaBean。将自动生成 getter 方法、equals 方法、hashCode 方法等，以及一个不可变的构造函数。`@Value` 注解会默认将所有字段都标记为 `final` 和 `private`。
8. @Builder: 用于自动生成Builder模式。
9. @SneakyThrows: 用于在方法中抛出受检异常，但不需要显式捕获。
10. @Slf4j: 用于自动生成Slf4j的Logger对象。
11. @Delegate: 用于为某个字段自动生成委托方法。
12. @Cleanup: 用于自动释放资源。

```scala
import lombok.Getter;
import lombok.Setter;
import lombok.EqualsAndHashCode;
import lombok.ToString;

@Getter
@Setter
@EqualsAndHashCode(exclude = "age")
@ToString(exclude = "age") // exclude排除字段
public class Person {
    private String firstName;
    private String lastName;
    @Getter(AccessLevel.NONE) // 这将排除 age 字段的 getter 方法
    private int age;
}


其他

@AllArgsConstructor(access = AccessLevel.PRIVATE) // 将生成具有 private 访问权限的构造函数

可以和guice结合，比如对所有final变量自动guide注入，可以使用
@AllArgsConstructor(onConstructor = @__(@Inject))
```

### JetBrains 注解

JetBrains是一家开发IDE（集成开发环境）的软件公司，他们开发的IDE工具（如IntelliJ IDEA、PyCharm、RubyMine等）在支持Java开发的同时，也提供了许多有用的Java注解库，其中常用的注解包括：

1. @NotNull：标注属性、方法参数、方法返回值不能为null。
2. @Nullable：标注属性、方法参数、方法返回值可以为null。
3. @Contract：用于描述方法的行为契约。
4. @TestOnly：标注仅用于测试的方法。
5. @Deprecated：标注已经过时的方法或类。
6. @SuppressWarnings：标注告知编译器忽略特定的警告信息。
7. @ReadOnly：标注集合类型的参数或返回值只读，不能修改。
8. @Mutable：标注集合类型的参数或返回值可变，可以修改。

### Junit注解

1. @Test: 用于标识测试方法。
2. @Before: 用于标识在测试方法执行之前需要执行的方法。
3. @After: 用于标识在测试方法执行之后需要执行的方法。
4. @BeforeClass: 用于标识在所有测试方法执行之前需要执行的方法。
5. @AfterClass: 用于标识在所有测试方法执行之后需要执行的方法。
6. @Ignore: 用于标识忽略某个测试方法。
7. @RunWith: 用于指定测试运行器。
8. @Rule: 用于添加测试规则。
9. @FixMethodOrder: 用于控制测试方法执行的顺序。
10. @Parameterized: 用于指定参数化测试。

### Mockito注解

1. @Mock：用于创建一个mock对象。
2. @InjectMocks：用于将mock对象注入到被测试的类中。
3. @Spy：用于创建一个真实的对象，并对其中某些方法进行mock操作。
4. @Captor：用于捕获mock对象中的参数。
5. @RunWith(MockitoJUnitRunner.class)：用于指定Mockito运行器。