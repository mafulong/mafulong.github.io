---
layout: post
category: JAVA
title: java final static
---
## final
### final 变量：

final 变量能被显式地初始化并且只能初始化一次。被声明为 final 的对象的引用不能指向不同的对象。但是 final 对象里的数据可以被改变。也就是说 final 对象的引用不能改变，但是里面的值可以改变。

final 修饰符通常和 static 修饰符一起使用来创建类常量。


    public class Test{
    final int value = 10;
    // 下面是声明常量的实例
    public static final int BOXWIDTH = 6;
    static final String TITLE = "Manager";
    
    public void changeValue(){
        value = 12; //将输出一个错误
    }
    }

### final 方法
类中的 final 方法可以被子类继承，但是不能被子类修改。

声明 final 方法的主要目的是防止该方法的内容被修改。

如下所示，使用 final 修饰符声明方法。

    public class Test{
        public final void changeName(){
        // 方法体
        }
    }

### final 类
final 类不能被继承，没有类能够继承 final 类的任何特性。

    实例
    public final class Test {
    // 类体
    }

## static
父类中的静态成员变量和方法是可以被子类继承的,但是不能被自己重写,无法形成多态
### static 变量
static 关键字用来声明独立于对象的静态变量，无论一个类实例化多少对象，它的静态变量只有一份拷贝。 静态变量也被称为类变量。局部变量不能被声明为 static 变量。

子类把父类的变量继承过来,内存中会存在两个同名的变量,父类的变量会出现在子类变量之前
### static 方法
static 关键字用来声明独立于对象的静态方法。静态方法不能使用类的非静态变量。静态方法从参数列表得到数据，然后计算这些数据。

1、父类方法如果是静态方法，子类不能覆盖为非静态方法；

2、父类方法如果是非静态方法，子类不能覆盖为静态方法；

3、父类静态方法可以被覆盖，允许在子类中定义同名的静态方法，但是没有多态。

### static 内部类
可以当做普通类使用，而不用先实例化一个外部类。（用他修饰后，就成了静态内部类了）。 使用对象：类、变量、方法、初始化函数（注意：修饰类时只能修饰 内部类 ）
