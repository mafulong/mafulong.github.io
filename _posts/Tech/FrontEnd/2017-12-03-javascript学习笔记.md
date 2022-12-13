---
layout: post
category: FrontEnd
title: javascript笔记
tags: FrontEnd
---

# 语法

## 页面如何添加js

外部脚本, 可以插入任何位置。 需要js后缀

```javascript
<script src="myScript.js"></script>
```

内部脚本

```javascript
<script>
alert("我的第一个 JavaScript");
</script>
```

脚本可被放置在 HTML 页面的 body和head部分中。

内联，在html里。

```scala
<button onclick="createParagraph()">点我呀</button>
```



## Js调用策略

调用顺序：HTML 元素是按其在页面中出现的次序调用的，如果用 JavaScript 来管理页面上的元素（更精确的说法是使用 [文档对象模型](https://developer.mozilla.org/zh-CN/docs/Web/API/Document_Object_Model) DOM），若 JavaScript 加载于欲操作的 HTML 元素之前，则代码将出错。

JavaScript 调用于文档头处，解析 HTML 文档体之前。这样做是有隐患的，需要使用一些结构来避免错误发生。



“内部”示例使用了以下结构：

```js
document.addEventListener("DOMContentLoaded", function() {
  . . .
});
```

这是一个事件监听器，它监听浏览器的 "`DOMContentLoaded`" 事件，即 HTML 文档体加载、解释完毕事件。事件触发时将调用 " `. . .`" 处的代码，从而避免了错误发生（[事件](https://developer.mozilla.org/zh-CN/docs/Learn/JavaScript/Building_blocks/Events) 的概念稍后学习）。

“外部”示例中使用了 JavaScript 的一项现代技术（`async` “异步”属性）来解决这一问题，它告知浏览器在遇到 `<script>` 元素时不要中断后续 HTML 内容的加载。

```js
<script src="script.js" async></script>
```

上述情况下，脚本和 HTML 将一并加载，代码将顺利运行。

**备注：** “外部”示例中 `async` 属性可以解决调用顺序问题，因此无需使用 `DOMContentLoaded` 事件。而 `async` 只能用于外部脚本，因此不适用于“内部”示例。



另外用了async后 多个js顺序就保证不了了，需要用defer

解决这一问题可使用 `defer` 属性，脚本将按照在页面中出现的顺序加载和运行：

```js
<script defer src="js/vendor/jquery.js"></script>

<script defer src="js/script2.js"></script>

<script defer src="js/script3.js"></script>
```



脚本调用策略小结：

- 如果脚本无需等待页面解析，且无依赖独立运行，那么应使用 `async`。
- 如果脚本需要等待页面解析，且依赖于其它脚本，调用这些脚本时应使用 `defer`，将关联的脚本按所需顺序置于 HTML 中。



## 注释

```
// 我是一条注释
```

```
/*
  我也是
  一条注释
*/
```

## JavaScript 输入输出

JavaScript 没有任何打印或者输出的函数。

document.write是直接写入到页面的内容流，如果在写之前没有调用document.open, 浏览器会自动调用open。每次写完关闭之后重新调用该函数，会导致页面被重写。

    JavaScript 显示数据
    JavaScript 可以通过不同的方式来输出数据：
    
    使用 window.alert() 弹出警告框。
    使用 document.write() 方法将内容写到 HTML 文档中。
    使用 innerHTML 写入到 HTML 元素。
    使用 console.log() 写入到浏览器的控制台。

输入可以prompt

```js
function updateName() {
  let name = prompt('输入一个新的名字：');
  para.textContent = '玩家 1：' + name;
}
```

```scala
console.log('name:' + name + ',age:' + age); //传统写法
console.log(`我是${name},age:${age}`); //ES6 写法。注意语法格式
```



## 操作 HTML 元素

如需从 JavaScript 访问某个 HTML 元素，您可以使用 document.getElementById(id) 方法。

```javascript
//通过标签找html元素
var x=document.getElementById("main");//id： main
var y=x.getElementsByTagName("p");

var element=document.getElementById("header");
element.innerHTML="New Header";

document.getElementById(id).attribute=new value;

document.getElementById("image").src="landscape.jpg";

document.getElementById("p2").style.color="blue";

```

## 变量

在 ES6 语法之前，统一使用`var`关键字来声明一个变量。比如：

```javascript
var name; // 定义一个名为 name 的变量。name是变量名。
```

在 ES6 语法及之后的版本里，可以使用 `const`、`let`关键字来定义一个变量

```js
const name; // 定义一个常量

let age; // 定义一个变量
```



**变量初始化**

一旦你定义了一个变量，你就能够初始化它。方法如下，在变量名之后跟上一个“=”，然后是数值：

```scala
myName = 'Chris';
myAge = 37;

// 你可以像这样在声明变量的时候给变量初始化：

let myName = 'Chris';
```

变量不声明，直接赋值：（正常） ；只声明，不赋值：（注意，打印 undefined）；不声明，不赋值，直接使用：（会报错）



## 数据类型

### 数据类型

#### JS 中一共有八种数据类型

- **基本数据类型（值类型）**：String 字符串、Number 数值、BigInt 大型数值、Boolean 布尔值、Null 空值、Undefined 未定义、Symbol。
- **引用数据类型（引用类型）**：Object 对象。

注意：内置对象 Function、Array、Date、RegExp、Error 等都是属于 Object 类型。也就是说，除了那七种基本数据类型之外，其他的，都称之为 Object 类型。



**数据类型之间最大的区别**：

- 基本数据类型：参数赋值的时候，传数值。
- 引用数据类型：参数赋值的时候，传地址。

```javascript
// 声明一个变量的语法是在 var 或 let 关键字之后加上这个变量的名字：

let myName;
let myAge;

//JavaScript 拥有动态类型。这意味着相同的变量可用作不同的类型：

//声明变量时可以确定其类型，如
var carname=new String;
var x=      new Number;
var y=      new Boolean;
var cars=   new Array;
var person= new Object;
```



### String

字符串是由若干个字符组成的，这些字符的数量就是字符串的长度。我们可以通过字符串的 length 属性可以获取整个字符串的长度。

字符串型可以是引号中的任意文本，其语法为：双引号 `""` 或者单引号 `''`。

js中常用单引号，html中用双引号



有了 ES6 语法，字符串拼接可以这样写：

```javascript
var name = 'qianguyihao';
var age = '26';

console.log('我是' + name + ',age:' + age); //传统写法
console.log(`我是${name},age:${age}`); //ES6 写法。注意语法格式


// 模板字符串支持换行
const html = `<div>
	<span>${result.name}</span>
	<span>${result.age}</span>
	<span>${result.sex}</span>
</div>`;

// 模板字符串中可以调用函数。字符串中调用函数的位置，将会显示函数执行后的返回值。
function getName() {
    return 'qianguyihao';
}

console.log(`www.${getName()}.com`); // 打印结果：www.qianguyihao.com


var str = 'smyhvae';
console.log(str.length); // 获取字符串的长度
console.log(str[2]); // 获取字符串中的第3个字符（下标为2的字符）

```

### Number

在 JS 中，只要是数，就是 Number 数值型的。无论整浮、浮点数（即小数）、无论大小、无论正负，都是 Number 类型的。

#### 数值范围

由于内存的限制，ECMAScript 并不能保存世界上所有的数值。

- 最大值：`Number.MAX_VALUE`，这个值为： 1.7976931348623157e+308
- 最小值：`Number.MIN_VALUE`，这个值为： 5e-324

如果使用 Number 表示的变量超过了最大值，则会返回 Infinity。

- 无穷大（正无穷）：Infinity
- 无穷小（负无穷）：-Infinity

注意：`typeof Infinity`的返回结果是 number。

#### NaN

**NaN**：是一个特殊的数字，表示 Not a Number，非数值。在进行数值运算时，如果得不到正常结果，就会返回 NaN。

比如：

```javascript
console.log('abc' / 18); //结果是NaN
```

**Undefined 和任何数值计算的结果为 NaN。NaN 与任何值都不相等，包括 NaN 本身。**







### 数组 

开头为0

- 获取字符串或者数组的长度，用arr.length属性
- 数组添加头部元素: arr.unshift("a","b"....); 结尾用push()方法
- 将数组元素连接成字符串： arr.join("连接符")
- 当数组的存储空间不够时，数组会自动扩容。其它编程语言中数组的大小是固定的，不会自动扩容。
- 如果访问数组中不存在的索引时，不会报错，会返回undefined。
- 数组可以存储不同类型数据，其它编程语言中数组只能存储相同类型数据。
- 数组分配的存储空间不一定是连续的。其它语言数组分配的存储空间是连续的。

```javascript
let arr1 = []; // 创建一个空的数组

let arr2 = [1, 2, 3]; // 创建带初始值的数组

var cars=new Array();
cars[0]="Audi";
cars[1]="BMW";
cars[2]="Volvo";
// 或者
var cars=new Array("Audi","BMW","Volvo");
// 或者
var cars=["Audi","BMW","Volvo"];

let sequence = [1, 1, 2, 3, 5, 8, 13];
for (let i = 0; i < sequence.length; i++) {
  console.log(sequence[i]);
}
sequence.length;
myArray.push('Cardiff');
let removedItem = myArray.pop();
```



数组解构赋值，代码举例：

```js
let [a, b, c] = [1, 2, [3, 4]];
```

判断是否为数组

```javascript
布尔值 = Array.isArray(被检测的数组);
```



```scala
const name = 'qianguyihao';
console.log(Array.from(name)); // 打印结果是数组：["q","i","a","n","g","u","y","i","h","a","o"]
```



```scala
// ES5语法
arr.forEach(function (currentItem, currentIndex, currentArray) {
	console.log(currentValue);
});

// ES6语法
arr.forEach((currentItem, currentIndex, currentArray) => {
	console.log(currentValue);
});

参数1：当前正在遍历的元素

参数2：当前正在遍历的元素的索引

参数3：正在遍历的数组

注意，forEach() 没有返回值。也可以理解成：forEach() 的返回值是 undefined。
forEach() 通过参数 2、参数 3 修改原数组：（标准做法。 如果你想在遍历数组的同时，去改变数组里的元素内容，那么，最好是用 map() 方法来做，不要用 forEach()方法，避免出现一些低级错误。

// ES6语法
const newArr = arr.map((currentItem, currentIndex, currentArray) => {
    return newItem;
});
```



### 对象

见面向对象

### Undefined 和 Null

Undefined 这个值表示变量不含有值。

- case1：变量已声明，未赋值时

- case2：变量未声明（未定义）时, 如果用 `typeof` 检查这个变量时，会返回 `undefined`

- case3：函数无返回值时, 如果一个函数没有返回值，那么，这个函数的返回值就是 undefined。

  或者，也可以这样理解：在定义一个函数时，如果末尾没有 return 语句，那么，其实就是 `return undefined`。

- case4：调用函数时，未传参。调用函数时，如果没有传参，那么，这个参数的值就是 undefined。



可以通过将变量的值设置为 null 来清空变量。**null 虽然是一个单独的数据类型，但null 相当于是一个 object，只不过地址为空（空指针）而已**。



undefined 实际上是由 null 衍生出来的，所以`null == undefined`的结果为 true。

- 任何值和 null 运算，null 可看做 0 运算。
- 任何数据类型和 undefined 运算都是 NaN。



### 动态类型

JavaScript 是一种“动态类型语言”，这意味着不同于其他一些语言 (译者注：如 C、JAVA)，您不需要指定变量将包含什么数据类型（例如 number 或 string）

例如，如果你声明一个变量并给它一个带引号的值，浏览器就会知道它是一个字符串：

```
let myString = 'Hello';
```

### 基本包装类型

我们都知道，js 中的数据类型包括以下几种。

- 基本数据类型：String、Number、Boolean、Null、Undefined
- 引用数据类型：Object

JS 为我们提供了三个**基本包装类**：

- String()：将基本数据类型字符串，转换为 String 对象。
- Number()：将基本数据类型的数字，转换为 Number 对象。
- Boolean()：将基本数据类型的布尔值，转换为 Boolean 对象。

通过上面这这三个包装类，我们可以**将基本数据类型的数据转换为对象**。



```javascript
let str1 = 'qianguyihao';
let str2 = new String('qianguyihao');

let num = new Number(3);

let bool = new Boolean(true);

console.log(typeof str1); // 打印结果：string
console.log(typeof str2); // 注意，打印结果：object
```

**需要注意的是**：我们在实际应用中一般不会使用基本数据类型的**对象**。如果使用基本数据类型的对象，在做一些比较时可能会带来一些**不可预期**的结果。



当我们对一些基本数据类型的值去调用属性和方法时，JS引擎会**临时使用包装类将基本数据类型转换为引用数据类型**（即“隐式类型转换”），这样的话，基本数据类型就有了属性和方法，然后再调用对象的属性和方法；调用完以后，再将其转换为基本数据类型。

比如str.length

## 运算符

### typeof 操作符

你可以使用 typeof 操作符来查看 JavaScript 变量的数据类型。
请注意：

    NaN 的数据类型是 number
    数组(Array)的数据类型是 object
    日期(Date)的数据类型为 object
    null 的数据类型是 object
    未定义变量的数据类型为 undefined

实例

```javascript
typeof "John"                 // 返回 string 
typeof 3.14                   // 返回 number
typeof NaN                    // 返回 number
typeof false                  // 返回 boolean
typeof [1,2,3,4]              // 返回 object
typeof {name:'John', age:34}  // 返回 object
typeof new Date()             // 返回 object
typeof function () {}         // 返回 function
typeof myCar                  // 返回 undefined (如果 myCar 没有声明)
typeof null                   // 返回 object
```

### constructor 属性

constructor 属性返回所有 JavaScript 变量的构造函数。

实例

```javascript
"John".constructor                 // 返回函数 String()  { [native code] }
(3.14).constructor                 // 返回函数 Number()  { [native code] }
false.constructor                  // 返回函数 Boolean() { [native code] }
[1,2,3,4].constructor              // 返回函数 Array()   { [native code] }
{name:'John', age:34}.constructor  // 返回函数 Object()  { [native code] }
new Date().constructor             // 返回函数 Date()    { [native code] }
function () {}.constructor         // 返回函数 Function(){ [native code] }

function isArray(myArray) {
    return myArray.constructor.toString().indexOf("Array") > -1;
}

function isDate(myDate) {
    return myDate.constructor.toString().indexOf("Date") > -1;
}
```

### 比较

| 运算符 | 名称       | 作用                     | 示例          |
| :----- | :--------- | :----------------------- | :------------ |
| `===`  | 严格等于   | 测试左右值是否相同       | `5 === 2 + 4` |
| `!==`  | 严格不等于 | 测试左右值是否**不**相同 | `5 !== 2 + 3` |

```text
== 	等于
=== 全等于
```



`==`这个符号并不严谨，会做隐式转换，将不同的数据类型，**转为相同类型**进行比较。例如：

```javascript
console.log('6' == 6); // 打印结果：true。这里的字符串"6"会先转换为数字6，然后再进行比较
console.log(true == '1'); // 打印结果：true
console.log(0 == -0); // 打印结果：true

console.log(null == 0); // 打印结果：false
```

```javascript
console.log(undefined == null); //打印结果：true。
```



**全等在比较时，不会做类型转换**。如果要保证**完全等于**（即：不仅要判断取值相等，还要判断数据类型相同），我们就要用三个等号`===`。例如：

```javascript
console.log('6' === 6); //false
console.log(6 === 6); //true
```

### 逻辑运算符

- `&&` — 逻辑与; 使得并列两个或者更多的表达式成为可能，只有当这些表达式每一个都返回`true`时，整个表达式才会返回`true.`
- `||` — 逻辑或; 当两个或者更多表达式当中的任何一个返回 `true` 则整个表达式将会返回 `true`.
- ! — 逻辑非; 对一个布尔值取反，非 true 返回 false，非 false 返回 true.

## 类型转换

### 显式类型转换

- toString()
- String()
- Number()
- parseInt(string)
- parseFloat(string)
- Boolean()

### 隐式类型转换

- isNaN ()
- 自增/自减运算符：`++`、`—-`
- 正号/负号：`+a`、`-a`
- 加号：`+`
- 运算符：`-`、`*`、`/`



### 将数字转换为字符串

```javascript
全局方法 String() 可以将数字转换为字符串。

String(x)         // 将变量 x 转换为字符串并返回
String(123)       // 将数字 123 转换为字符串并返回
String(100 + 23)  // 将数字表达式转换为字符串并返回

Number 方法 toString() 也是有同样的效果。

实例
x.toString()
(123).toString()
(100 + 23).toString()

```

### 将布尔值转换为字符串

```javascript
全局方法 String() 可以将布尔值转换为字符串。

String(false)        // 返回 "false"
String(true)         // 返回 "true"
Boolean 方法 toString() 也有相同的效果。

false.toString()     // 返回 "false"
true.toString()      // 返回 "true"
```

### 将日期转换为字符串

```javascript
Date() 返回字符串。

Date()      // 返回 Thu Jul 17 2014 15:38:19 GMT+0200 (W. Europe Daylight Time)
全局方法 String() 可以将日期对象转换为字符串。

String(new Date())      // 返回 Thu Jul 17 2014 15:38:19 GMT+0200 (W. Europe Daylight Time)
Date 方法 toString() 也有相同的效果。

实例
obj = new Date()
obj.toString()   // 返回 Thu Jul 17 2014 15:38:19 GMT+0200 (W. Europe Daylight Time)
```

### 将字符串转换为数字

```javascript
全局方法 Number() 可以将字符串转换为数字。

字符串包含数字(如 "3.14") 转换为数字 (如 3.14).

空字符串转换为 0。

其他的字符串会转换为 NaN (不是个数字)。

Number("3.14")    // 返回 3.14
Number(" ")       // 返回 0 
Number("")        // 返回 0
Number("99 88")   // 返回 NaN

一元运算符 +
Operator + 可用于将变量转换为数字：
```

### 将布尔值转换为数字

```javascript
全局方法 Number() 可将布尔值转换为数字。

Number(false)     // 返回 0
Number(true)      // 返回 1
```

### 将日期转换为数字

```javascript
全局方法 Number() 可将日期转换为数字。

d = new Date();
Number(d)          // 返回 1404568027739
日期方法 getTime() 也有相同的效果。

d = new Date();
d.getTime()        // 返回 1404568027739
```



### 布尔值情况列举【重要】

其他的数据类型都可以转换为 Boolean 类型。无论是隐式转换，还是显示转换，转换结果都是一样的。有下面几种情况：

（1）情况一：数字 --> 布尔。 0 和 NaN的转换结果 false，其余的都是 true。比如 `Boolean(NaN)`的结果是 false。

（2）情况二：字符串 ---> 布尔。空串的转换结果是false，其余的都是 true。全是空格的字符串，转换结果也是 true。字符串`'0'`的转换结果也是 true。

（3）情况三：null 和 undefined 都会转换为 false。

（4）情况四：引用数据类型会转换为 true。注意，空数组`[]`和空对象`{}`，**转换结果也是 true**，这一点，很多人都不知道。







## 面向对象

### 对象

对象由花括号分隔。在括号内部，对象的属性以名称和值对的形式 (name : value) 来定义。属性由逗号分隔

### 对象创建

```javascript
var person={
    firstname : "Bill",
    lastname  : "Gates",
    id        :  5566
};

//创建对象
person=new Object();
person.firstname="Bill";
person.lastname="Gates";
person.age=56;
person.eyecolor="blue";
//或者
person={firstname:"John",lastname:"Doe",age:50,eyecolor:"blue"};
//或者对象构造器
function person(firstname,lastname,age,eyecolor)
{
    this.firstname=firstname;
    this.lastname=lastname;
    this.age=age;
    this.eyecolor=eyecolor;
}
var myFather=new person("Bill","Gates",56,"blue");
```

### 访问对象属性

对象属性有两种寻址方式：

```javascript
    name=person.lastname;
    name=person["lastname"];
```

### 对象方法

```javascript
var person = {
    firstName: "John",
    lastName : "Doe",
    id : 5566,
    fullName : function() 
	{
       return this.firstName + " " + this.lastName;
    }
};
document.getElementById("demo").innerHTML = person.fullName();
```

### 使用对象方法

对象方法通过添加 () 调用 (作为一个函数)。

```javascript
name = person.fullName();
```



## 函数

### 定义

```javascript
// 传统定义函数方式
function myFunction(a,b)
{
    if (a>b)
    {
        return;
    }
    x=a+b
}

function Test () {
  //
}

const Test = function () {
  //
}

// 使用箭头函数定义函数时可以省略 function 关键字
const Test = (...params) => {
  //
}

// 该函数只有一个参数时可以简写成：
const Test = param => {
  return param;
}

console.log(Test('hello'));   // hello

// 很少用，
const 变量名/函数名  = new Function('形参1', '形参2', '函数体');
const fun3 = new Function('a', 'b', 'console.log("我是函数内部的内容");  console.log(a + b);');
```

### 实际参数和形式参数的个数，可以不同

实际参数和形式参数的个数，可以不同。调用函数时，解析器不会检查实参的数量。

- 如果实参个数 > 形参个数，则末尾的实参是多余的，不会被赋值，因为没有形参能接收它。
- 如果实参个数 < 形参个数，则末尾的形参是多余的，值是 undefined，因为它没有接收到实参。（undefined参与运算时，表达式的运算结果为NaN）

函数的实参可以是任意的数据类型。调用函数时，解析器不会检查实参类型，所以要注意，是否有可能会接收到非法的参数，如果有可能则需要对参数进行类型检查。

函数体内可以没有返回值，也可以根据需要加返回值。语法格式：`return 函数的返回值`。



### 类数组对象 arguments

在调用函数时，浏览器每次都会传递进两个隐含的参数：

- 1.函数的上下文对象 this
- 2.**封装实参的对象** arguments

```javascript
function foo() {
    console.log(arguments);
    console.log(typeof arguments);
}

foo('a', 'b');
```

函数内的 arguments 是一个**类数组对象**，里面存储的是它接收到的**实参列表**。所有函数都内置了一个 arguments 对象，有个讲究的地方是：只有函数才有arguments。

具体来说，在调用函数时，我们所传递的实参都会在 arguments 中保存。**arguments 代表的是所有实参**。

arguments 的展示形式是一个**伪数组**。意思是，它和数组有点像，但它并不是数组。它具有以下特点：

- 可以进行遍历；具有数组的 length 属性，可以获取长度。
- 可以通过索引（从0开始计数）存储数据、获取和操作数据。比如，我们可以通过索引访问某个实参。
- 不能调用数组的方法。比如push()、pop() 等方法都没有。
- 即使我们不定义形参，也可以通过 arguments 来获取实参：arguments[0] 表示第一个实参、arguments[1] 表示第二个实参，以此类推。
- 当我们不确定有多少个参数传递的时候，可以用 **arguments** 来获取。

###  立即执行函数

```scala
(function() {
  // 函数体
})(a, b);
```

即执行函数往往只会执行一次。为什么呢？因为没有变量保存它，执行完了之后，就找不到它了。



### This指向

> - [this指向](https://web.qianguyihao.com/04-JavaScript%E5%9F%BA%E7%A1%80/25-this%E6%8C%87%E5%90%91.html#%E6%89%A7%E8%A1%8C%E6%9C%9F%E4%B8%8A%E4%B8%8B%E6%96%87)

解析器在调用函数每次都会向函数内部传递进一个隐含的参数，这个隐含的参数就是 this，this 指向的是一个对象，这个对象我们称为函数执行的 上下文对象。



在ES5语法中，根据函数的调用方式的不同，this 会指向不同的对象：

1、以函数的形式（包括普通函数、定时器函数、立即执行函数）调用时，this 的指向永远都是 window。比如`fun();`相当于`window.fun();`

2、以方法的形式调用时，this 指向调用方法的那个对象

3、以构造函数的形式调用时，this 指向实例对象

4、以事件绑定函数的形式调用时，this 指向**绑定事件的对象**

5、使用 call 和 apply 调用时，this 指向指定的那个对象



```scala
//以函数形式调用，this是window
fun(); //可以理解成 window.fun()

function fun() {
    console.log(this);
    console.log(this.name);
}

打印结果：
    Window
    全局的name属性



//以方法的形式调用，this是调用方法的对象
obj2.sayName();
```



ES6 中的箭头函数并不使用上面的准则，而是会继承外层函数调用的 this 绑定（无论 this 绑定到什么）。



#### call() 方法的作用

可以通过函数.call方法调用函数。

call() 方法的作用：可以**调用**一个函数，与此同时，它还可以改变这个函数内部的 this 指向。

call() 方法的另一个应用：**可以实现继承**。之所以能实现继承，其实是利用了上面的作用。

语法：

```js
fn1.call(想要将this指向哪里, 函数实参1, 函数实参2);
```

备注：第一个参数中，如果不需要改变 this 指向，则传 null。



```js
fn1.call(this); // this的指向并没有被改变，此时相当于 fn1();
```



通过 call() 实现继承：

```js
// 给 Father 增加 name 和 age 属性
function Father(myName, myAge) {
    this.name = myName;
    this.age = myAge;
}

function Son(myName, myAge) {
    // 【下面这一行，重要代码】
    // 通过这一步，将 father 里面的 this 修改为 Son 里面的 this；另外，给 Son 加上相应的参数，让 Son 自动拥有 Father 里的属性。最终实现继承
    Father.call(this, myName, myAge);
}
```





#### apply() 方法的作用

apply() 方法的作用：可以**调用**一个函数，与此同时，它还可以改变这个函数内部的 this 指向。这一点，和 call()类似。

apply() 方法的应用： 由于 apply()需要传递数组



语法：

```js
fn1.apply(想要将this指向哪里, [函数实参1, 函数实参2]);
```



备注：第一个参数中，如果不需要改变 this 指向，则传 null。

到这里可以看出， call() 和 apply() 方法的作用是相同的。唯一的区别在于，apply() 里面传入的**实参，必须是数组（或者伪数组）**。

主要是个Math.max这样用的。使用场景较少，知道即可。



#### bind() 方法的作用【常用】

bind() 方法**不会调用函数**，但是可以改变函数内部的 this 指向。

把call()、apply()、bind()这三个方法做一下对比，你会发现：实际开发中， bind() 方法使用得最为频繁。如果有些函数，我们不需要立即调用，但是又想改变这个函数内部的this指向，此时用 bind() 是最为合适的。

语法：

```js
新函数 = fn1.bind(想要将this指向哪里, 函数实参1, 函数实参2);
```



参数：

- 第一个参数：在 fn1 函数运行时，指定 fn1 函数的this 指向。如果不需要改变 this 指向，则传 null。
- 其他参数：fn1 函数的实参。

解释：它不会调用 fn1 函数，但会返回 由指定this 和指定实参的**原函数拷贝**。可以看出， bind() 方法是有返回值的。





## if和循环

### if else

```javascript
if (time<10)
{
    x="Good morning";
}
else if (time<20)
{
    x="Good day";
}
else
{
    x="Good evening";
}
```

### swith语法

```javascript
var day=new Date().getDay();
switch (day)
{
    case 6:
        x="Today it's Saturday";
        break;
    case 0:
        x="Today it's Sunday";
        break;
    default:
        x="Looking forward to the Weekend";
}
```

### for循环

```javascript
for (var i=0;i<cars.length;i++)
{
    document.write(cars[i] + "<br>");
}

for (var i=0,len=cars.length; i<len; i++)
{
    document.write(cars[i] + "<br>");
}
//循环遍历对象的属性
var person={fname:"John",lname:"Doe",age:25};
for (x in person)
{
    txt=txt + person[x];
}
forin不推荐用在数组上。数组应该用forof
for(let value of arr) {
	console.log(value);
}
```

### while循环

```javascript
while (i<5)
{
    x=x + "The number is " + i + "<br>";
    i++;
}

do
{
    x=x + "The number is " + i + "<br>";
    i++;
}
while (i<5);
//break; continue;
```

## 作用域

> [参考](https://web.qianguyihao.com/04-JavaScript%E5%9F%BA%E7%A1%80/23-%E4%BD%9C%E7%94%A8%E5%9F%9F%E3%80%81%E5%8F%98%E9%87%8F%E6%8F%90%E5%8D%87%E3%80%81%E5%87%BD%E6%95%B0%E6%8F%90%E5%8D%87.html#%E4%BD%9C%E7%94%A8%E5%9F%9F%EF%BC%88scope%EF%BC%89%E7%9A%84%E6%A6%82%E5%BF%B5%E5%92%8C%E5%88%86%E7%B1%BB)

直接编写在 script 标签中的 JS 代码，都在全局作用域。全局作用域在页面打开时创建，在页面关闭时销毁。

在全局作用域中有一个全局对象 window，它代表的是浏览器的窗口，由浏览器创建，我们可以直接使用。相关知识点如下：

- 创建的**变量**都会作为 window 对象的属性保存。比如在全局作用域内写 `const a = 100`，这里的 `a` 等价于 `window.a`。
- 创建的**函数**都会作为 window 对象的方法保存。
- 无论是在函数外还是函数内，变量如果未经声明就赋值（意思是，如果不加var/let/const），这个变量是**全局变量**。

JS在解析代码之前，有一个“**预处理**（预解析）”阶段，将当前 JS 代码中所有变量的定义和函数的定义，放到所有代码的最前面。

- 使用 var 关键字声明的变量（ 比如 `var a = 1`），**会在所有的代码执行之前被声明**（但是不会赋值）。但是如果声明变量时不是用 var 关键字（比如直接写`a = 1`），则变量不会被声明提前。
- 使用`函数声明`的形式创建的函数`function foo(){}`，**会被声明提前**。
- 在JS的规则中，函数提升优先于变量提升。



在函数作用域中，也有声明提前的现象：

- 函数中，使用 var 关键字声明的变量，会在函数中所有代码执行之前被提前声明。
- 函数中，没有 var 声明的变量都是**全局变量**，且并不会被提前声明。



在 ES5 中没有块级作用域

## try catch

```javascript
try
{
    throw exception;
    adddlert("Welcome guest!");
}
catch(err)
{
    txt="There was an error on this page.\n\n";
    txt+="Error description: " + err.message + "\n\n";
    txt+="Click OK to continue.\n\n";
    alert(txt);
}
```

## 事件

```javascript
//DOM事件
//<h1 onclick="this.innerHTML='谢谢!'">请点击该文本</h1> this就是自己的id
//<h1 onclick="changetext(this)">请点击该文本</h1>
document.getElementById("myBtn").onclick=function(){displayDate()};
// <input type="text" id="fname" onchange="upperCase()">
//分配事件
document.getElementById("myBtn").onclick=function(){displayDate()};

//创建元素
var para=document.createElement("p");
var node=document.createTextNode("这是新段落。");
para.appendChild(node);
var element=document.getElementById("div1");
element.appendChild(para);
//删除元素
var parent=document.getElementById("div1");
var child=document.getElementById("p1");
parent.removeChild(child);
//正则表达式 RegExp
```



## 其他 小结

- 字符串转换为数字用Number(str)或者parseInt(str)/parseFloat(str)方法
- 数字转换为字符串用var.toString()方法
- NaN： not a number
- 可以直接使用Math.方法名，如max(...), 
- document.querySelector()方法，querySelectorAll()方法选择器写法和css选择器写法一样，但效率低
- ByName()只用于表单元素，一般是单选和复选框
- 两个特殊方法，document.title, document.body
- 节点有三种：元素节点，属性节点，文本节点
- 创建节点的流程：createElement(), createTextNode()，把文本节点插入元素节点 appendChild()，把组装好的节点插入到已有元素中:appendChild（）
- obj.style.属性名只可以获得行内样式，是没办法获得内部样式和外部样式的。一般用getComputedStyle.属性名或者obj.style.cssText()="width:3px"等来写，后者可以写多个，css写法，前者驼峰样式，没有-了
- html中onclick="f()", js中obj.click=f，前者是调用属性，后者是给属性赋值
- 只执行最后一次window.onload=function(){ }
- 事件绑定： obj.addEventListener("click",funcion,false);



# jquery教程

## 语法
```javacript
 $(document).ready(function(){

   // 开始写 jQuery 代码...

 }); 

 简洁写法（与以上写法效果相同）:
 $(function(){

   // 开始写 jQuery 代码...

 }); 

#id 选择器 
$("#test")
.class 选择器
$(".test")
$("p").css("background-color","red");
$(this)	选取当前 HTML 元素
```

## 事件
```javascript
$("p").click(function(){        
  // action goes here!!        
});
$("p").click();
$("p").dblclick(function(){ 
  $(this).hide(); 
});

jQuery hide() 和 show()
通过 jQuery，您可以使用 toggle() 方法来切换 hide() 和 show() 方法。

$(selector).toggle(speed,callback);
可选的 speed 参数规定隐藏/显示的速度，可以取以下值："slow"、"fast" 或毫秒。
可选的 callback 参数是 toggle() 方法完成后所执行的函数名称。
可选的 callback 参数，具有以下三点说明：
$(selector)选中的元素的个数为n个，则callback函数会执行n次
callback函数名后加括号，会立刻执行函数体，而不是等到显示/隐藏完成后才执行
callback既可以是函数名，也可以是匿名函数

Callback 函数在当前动画 100% 完成之后执行。

通过 jQuery，可以把动作/方法链接在一起。
Chaining 允许我们在一条语句中运行多个 jQuery 方法（在相同的元素上）。
$("#p1").css("color","red").slideUp(2000).slideDown(2000);
$("#p1").css("color","red")
  .slideUp(2000)
  .slideDown(2000);

三个简单实用的用于 DOM 操作的 jQuery 方法：
text() - 设置或返回所选元素的文本内容
html() - 设置或返回所选元素的内容（包括 HTML 标记）
val() - 设置或返回表单字段的值

$("#btn1").click(function(){
  alert("Text: " + $("#test").text());
});
$("#btn2").click(function(){
  alert("HTML: " + $("#test").html());
});
$("#btn1").click(function(){
  alert("Value: " + $("#test").val());
});

下面的例子演示如何通过 jQuery val() 方法获得输入字段的值：
<script>
$(document).ready(function(){
  $("button").click(function(){
    alert("值为: " + $("#test").val());
  });
});
</script>
</head>

<body>
<p>名称: <input type="text" id="test" value="W3Cschool教程"></p>
<button>显示值</button>
</body>
</html>

$("button").click(function(){
  alert($("#w3s").attr("href"));
});

下面的例子演示如何通过 text()、html() 以及 val() 方法来设置内容：
$("#btn1").click(function(){ 
  $("#test1").text("Hello world!"); 
}); 
$("#btn2").click(function(){ 
  $("#test2").html("<b>Hello world!</b>"); 
}); 
$("#btn3").click(function(){ 
  $("#test3").val("Dolly Duck"); 
});
text()、html() 以及 val() 的回调函数

上面的三个 jQuery 方法：text()、html() 以及 val()，同样拥有回调函数。
回调函数由两个参数：被选元素列表中当前元素的下标，以及原始（旧的）值。
然后以函数新值返回您希望使用的字符串。
$("#btn1").click(function(){ 
  $("#test1").text(function(i,origText){ 
    return "Old text: " + origText + " New text: Hello world! 
    (index: " + i + ")"; 
  }); 
}); 

$("button").click(function(){ 
  $("#w3s").attr("href","//www.w3cschool.cn/jquery"); 
});

append() - 在被选元素内部的结尾插入指定内容
prepend() - 在被选元素内部的开头插入指定内容
after() - 在被选元素之后插入内容
before() - 在被选元素之前插入内容

$("p").append("Some appended text.");

$("#div1").remove();

$("#div1").empty();

addClass() - 向被选元素添加一个或多个类
removeClass() - 从被选元素删除一个或多个类
toggleClass() - 对被选元素进行添加/删除类的切换操作
css() - 设置或返回样式属性

$("button").click(function(){
  $("h1,h2,p").addClass("blue");
  $("div").addClass("important");
});

您也可以在 addClass() 方法中规定多个类：
$("button").click(function(){
  $("#div1").addClass("important blue");
});

下面的例子将返回首个匹配元素的 background-color 值：
$("p").css("background-color");

$("p").css("background-color","yellow");

$("p").css({"background-color":"yellow","font-size":"200%"});



旧版本
$("").hide()
//必须
$(document).ready(function(){

--- jQuery functions go here ----

});

jQuery 语法实例
$(this).hide()
演示 jQuery hide() 函数，隐藏当前的 HTML 元素。
$("#test").hide()
演示 jQuery hide() 函数，隐藏 id="test" 的元素。
$("p").hide()
演示 jQuery hide() 函数，隐藏所有 <p> 元素。
$(".test").hide()
演示 jQuery hide() 函数，隐藏所有 class="test" 的元素。

jQuery 元素选择器
jQuery 使用 CSS 选择器来选取 HTML 元素。
$("p") 选取 <p> 元素。
$("p.intro") 选取所有 class="intro" 的 <p> 元素。
$("p#demo") 选取所有 id="demo" 的 <p> 元素。
jQuery 属性选择器
jQuery 使用 XPath 表达式来选择带有给定属性的元素。
$("[href]") 选取所有带有 href 属性的元素。
$("[href='#']") 选取所有带有 href 值等于 "#" 的元素。
$("[href!='#']") 选取所有带有 href 值不等于 "#" 的元素。
$("[href$='.jpg']") 选取所有 href 值以 ".jpg" 结尾的元素。
jQuery CSS 选择器
jQuery CSS 选择器可用于改变 HTML 元素的 CSS 属性。
下面的例子把所有 p 元素的背景颜色更改为红色：
$("p").css("background-color","red");

$(document).ready(function)	将函数绑定到文档的就绪事件（当文档完成加载时）
$(selector).click(function)	触发或将函数绑定到被选元素的点击事件
$(selector).dblclick(function)	触发或将函数绑定到被选元素的双击事件
$(selector).focus(function)	触发或将函数绑定到被选元素的获得焦点事件
$(selector).mouseover(function)	触发或将函数绑定到被选元素的鼠标悬停事件

$("#btn1").click(function(){
  $("#test1").text("Hello world!");
});
$("#btn2").click(function(){
  $("#test2").html("<b>Hello world!</b>");
});
$("#btn3").click(function(){
  $("#test3").val("Dolly Duck");
});
//回调函数
$("#btn1").click(function(){
  $("#test1").text(function(i,origText){
    return "Old text: " + origText + " New text: Hello world!
    (index: " + i + ")";
  });
});

$("button").click(function(){
  $("#w3s").attr("href","http://www.w3school.com.cn/jquery");
});
//同时设置多个属性
$("button").click(function(){
  $("#w3s").attr({
    "href" : "http://www.w3school.com.cn/jquery",
    "title" : "W3School jQuery Tutorial"
  });
});

$("p").append("Some appended text.");
$("p").prepend("Some prepended text.");

function appendText()
{
var txt1="<p>Text.</p>";               // 以 HTML 创建新元素
var txt2=$("<p></p>").text("Text.");   // 以 jQuery 创建新元素
var txt3=document.createElement("p");  // 以 DOM 创建新元素
txt3.innerHTML="Text.";
$("p").append(txt1,txt2,txt3);         // 追加新元素
}

$("img").after("Some text after");
$("img").before("Some text before");

$("#div1").remove();
$("#div1").empty();
$("p").remove(".italic");

$("button").click(function(){
  $("h1,h2,p").addClass("blue");
  $("div").addClass("important");
});

$("button").click(function(){
  $("h1,h2,p").removeClass("blue");
});

$("p").css("background-color","yellow");
$("p").css({"background-color":"yellow","font-size":"200%"});
```

# Jquery ajax淘汰

[参考](https://www.xiejiahe.com/blog/detail/59b35ad615c192bd11b90469)





# ajax教程

## ajax请求数据
### get
```javascript
    var xmlhttp=new XMLHttpRequest();
	xmlhttp.open("GET","/test/GetSearchTips?sear="+thisnode.value,true);
    xmlhttp.send();
```

### post
```javascript
    xmlhttp.open("POST","/myservlet",true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.send("name=mafulong&age=14");
```

## 后台处理数据
```java
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
//        super.doGet(req, resp);
//        resp.setContentType("text/html");
        String name=req.getParameter("name");
        System.out.println(name);
        resp.setContentType("application/json; charset=UTF-8");
        PrintWriter out=resp.getWriter();
//        out.print("fjdkfjdk");
//        out.println("<h1>abc</h1>");
        JSONObject jsonObject=new JSONObject();
        JSONArray jsonArray=new JSONArray();
        jsonArray.put(jsonObject);
        jsonArray.put(jsonObject);
        try{
            jsonObject.put("name","mafulong");
            jsonObject.put("age",18);
        }catch (Exception e){
            e.printStackTrace();
        }
//        out.print(jsonObject.toString());
        out.print(jsonArray.toString());

    }
```

## 前端处理后端接收得数据
```javascript
    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            // document.getElementById("myDiv").innerHTML=xmlhttp.responseText;
            alert("success ");
            var data=xmlhttp.responseText;
            var djson=JSON.parse(data);
            var str="";
            for(var i=0;i<djson.length;i++){
                str+=djson[i].name+"<br>";
                str+=djson[i].age+"<br>";
            }
            document.getElementById("myDiv").innerHTML=str;
        }
    }
```

# 千古 笔记

> [参考](https://web.qianguyihao.com/04-JavaScript%E5%9F%BA%E7%A1%80/03-%E5%B8%B8%E9%87%8F%E5%92%8C%E5%8F%98%E9%87%8F.html#%E5%8F%98%E9%87%8F%E7%9A%84%E5%88%9D%E5%A7%8B%E5%8C%96%E3%80%90%E9%87%8D%E8%A6%81%E3%80%91)

变量不声明，直接赋值：（正常） ；只声明，不赋值：（注意，打印 undefined）；不声明，不赋值，直接使用：（会报错）





# ES6

在 ES6 语法及之后的版本里，可以使用 `const`、`let`关键字来定义一个变量

```js
const name; // 定义一个常量

let age; // 定义一个变量
```

如果你想定义一个常量，就用 const；如果你想定义一个变量，就用 let。

