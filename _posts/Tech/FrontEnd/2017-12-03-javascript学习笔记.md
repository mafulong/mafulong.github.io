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
// 方式1：字面量 对象的字面量就是一个{}。里面的属性和方法均是键值对. key可以也可以没有引号
var person={
    firstname : "Bill",
    lastname  : "Gates",
    id        :  5566
};

// 方式2：工厂模式 new Object()。弊端： 使用工厂方法创建的对象，使用的构造函数都是 Object。所以创建的对象都是 Object 这个类型，就导致我们无法区分出多种不同类型的对象。

person=new Object();
person.firstname="Bill";
person.lastname="Gates";
person.age=56;
person.eyecolor="blue";
//或者
person={firstname:"John",lastname:"Doe",age:50,eyecolor:"blue"};
//或者对象构造器 构造函数  推荐
function person(firstname,lastname,age,eyecolor)
{
    this.firstname=firstname;
    this.lastname=lastname;
    this.age=age;
    this.eyecolor=eyecolor;
}
var myFather=new person("Bill","Gates",56,"blue");
```

**构造函数**：是一种特殊的函数，主要用来创建和初始化对象，也就是为对象的成员变量赋初始值。它与 `new` 一起使用才有意义。

- 构造函数的创建方式和普通函数没有区别，不同的是构造函数习惯上首字母大写。
- 构造函数和普通函数的区别就是**调用方式**的不同：普通函数是直接调用，而构造函数需要使用 new 关键字来调用。

**this 的指向也有所不同**：

- 1.以函数的形式调用时，this 永远都是 window。比如`fun();`相当于`window.fun();`
- 2.以方法的形式调用时，this 是调用方法的那个对象
- 3.以构造函数的形式调用时，this 是新创建的实例对象





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

### instanceof

使用 instanceof 可以检查**一个对象是否为一个类的实例**。

**语法如下**：

```javascript
对象 instanceof 构造函数;
```

### 浅拷贝

ES6 给我们提供了新的语法糖，通过 `Object.assgin()` 可以实现**浅拷贝**。

`Object.assgin()` 在日常开发中，使用得相当频繁，非掌握不可。

**语法**：

```js
// 语法1
obj2 = Object.assgin(obj2, obj1);

// 语法2
Object.assign(目标对象, 源对象1, 源对象2...);
```

**解释**：将`obj1` 拷贝给 `obj2`。执行完毕后，obj2 的值会被更新。

**作用**：将 obj1 的值追加到 obj2 中。如果对象里的属性名相同，会被覆盖。

从语法2中可以看出，Object.assign() 可以将多个“源对象”拷贝到“目标对象”中。



深拷贝其实就是将浅拷贝进行递归。

### 原型

原型就是父类 继承的父类。

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



### 闭包（closure）

**闭包**：如果**外部作用域**有权访问另外一个**函数内部**的**局部变量**时，那就产生了闭包。这个内部函数称之为闭包函数。注意，这里强调的是访问**局部变量**。

闭包代码举例：

```js
function fun1() {
  const a = 10;
  return function fun2() {
    console.log(a);
  };
}
fun1();
// 调用外部函数，就能得到内部函数，并用 变量 result 接收
const result = fun1();
// 在 fun1函数的外部，执行了内部函数 fun2，并访问到了 fun2的内部变量a
result(); // 10
```

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





## 原型和原型链

## 其他 小结

- 字符串转换为数字用Number(str)或者parseInt(str)/parseFloat(str)方法
- 数字转换为字符串用var.toString()方法
- NaN： not a number
- 可以直接使用Math.方法名，如max(...), 
- 
- ByName()只用于表单元素，一般是单选和复选框
- 两个特殊方法，document.title, document.body
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



## 事件

### 事件 绑定

- [事件](https://web.qianguyihao.com/04-JavaScript%E5%9F%BA%E7%A1%80/35-%E4%BA%8B%E4%BB%B6%E7%AE%80%E4%BB%8B.html#%E4%BA%8B%E4%BB%B6%E7%AE%80%E4%BB%8B)

![img](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202212150003045.png)



```scala
    //这种事件绑定的方式，如果绑定多个，则后面的会覆盖掉前面的
    btn.onclick = function () {
        console.log("事件1");
    }
		// 方式2
    element.addEventListener('click', function () {

    }, false);
    参数解释：

    参数1：事件名的字符串(注意，没有on)

    参数2：回调函数：当事件触发时，该函数会被执行

    参数3：true表示捕获阶段触发，false表示冒泡阶段触发（默认）。如果不写，则默认为false。【重要】
```

也可以传入event参数。

```html
small.onmousemove = function (event) {}
```

### 事件的传播和事件冒泡

- [事件的传播和事件冒泡](https://web.qianguyihao.com/04-JavaScript%E5%9F%BA%E7%A1%80/42-%E4%BA%8B%E4%BB%B6%E7%9A%84%E4%BC%A0%E6%92%AD%E5%92%8C%E4%BA%8B%E4%BB%B6%E5%86%92%E6%B3%A1.html#dom%E4%BA%8B%E4%BB%B6%E6%B5%81)

事件传播的三个阶段是：事件捕获、事件冒泡和目标。

- 事件捕获阶段：事件从祖先元素往子元素查找（DOM树结构），直到捕获到事件目标 target。在这个过程中，默认情况下，事件相应的监听函数是不会被触发的。
- 事件目标：当到达目标元素之后，执行目标元素该事件相应的处理函数。如果没有绑定监听函数，那就不执行。
- 事件冒泡阶段：事件从事件目标 target 开始，从子元素往冒泡祖先元素冒泡，直到页面的最上一级标签。



捕获阶段，事件依次传递的顺序是：window --> document --> html--> body --> 父元素、子元素、目标元素。



**事件冒泡**: 当一个元素上的事件被触发的时候（比如说鼠标点击了一个按钮），同样的事件将会在那个元素的所有**祖先元素**中被触发。这一过程被称为事件冒泡；这个事件从原始元素开始一直冒泡到DOM树的最上层。

通俗来讲，冒泡指的是：**子元素的事件被触发时，父元素的同样的事件也会被触发**。取消冒泡就是取消这种机制。



以下事件不冒泡：blur、focus、load、unload、onmouseenter、onmouseleave。意思是，事件不会往父元素那里传递。

大部分情况下，冒泡都是有益的。当然，如果你想阻止冒泡，也是可以的。可以按下面的方法阻止冒泡。

```javascript
  event.stopPropagation();
```



可以用这个冒泡做一些[事件委托](https://web.qianguyihao.com/04-JavaScript%E5%9F%BA%E7%A1%80/43-%E4%BA%8B%E4%BB%B6%E5%A7%94%E6%89%98.html)  为父节点注册 click 事件，当子节点被点击的时候，click事件会从子节点开始**向父节点冒泡**。**父节点捕获到事件**之后，开始执行方法体里的内容：通过判断 event.target 拿到了被点击的子节点`<a>`。从而可以获取到相应的信息，并作处理。

## Dom

> [DOM](https://web.qianguyihao.com/04-JavaScript%E5%9F%BA%E7%A1%80/36-DOM%E7%AE%80%E4%BB%8B%E5%92%8CDOM%E6%93%8D%E4%BD%9C.html#%E5%B8%B8%E8%A7%81%E6%A6%82%E5%BF%B5)

**节点**（Node）：构成 HTML 网页的最基本单元。网页中的每一个部分都可以称为是一个节点，比如：html标签、属性、文本、注释、整个文档等都是一个节点。

虽然都是节点，但是实际上他们的具体类型是不同的。常见节点分为四类：

- 文档节点（文档）：整个 HTML 文档。整个 HTML 文档就是一个文档节点。
- 元素节点（标签）：HTML标签。
- 属性节点（属性）：元素的属性。
- 文本节点（文本）：HTML标签中的文本内容（包括标签之间的空格、换行）。

节点的类型不同，属性和方法也都不尽相同。所有的节点都是Object。

**解析过程**： HTML加载完毕，渲染引擎会在内存中把HTML文档，生成一个DOM树，getElementById是获取内中DOM上的元素节点。然后操作的时候修改的是该元素的**属性**。

![img](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202212151021206.png)



### 有三种方式可以获取DOM节点

```javascript
var div1 = document.getElementById("box1"); //方式一：通过 id 获取 一个 元素节点（为什么是一个呢？因为 id 是唯一的）

var arr1 = document.getElementsByTagName("div"); //方式二：通过 标签名 获取 元素节点数组，所以有s

var arr2 = document.getElementsByClassName("hehe"); //方式三：通过 类名 获取 元素节点数组，所以有s
```

document.querySelector()方法，querySelectorAll()方法选择器写法和css选择器写法一样，但效率低



DOM的节点并不是孤立的，因此可以通过DOM节点之间的相对关系对它们进行访问。

![img](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv6/v6/202212151022606.png)



获取父节点

```javascript
	节点.parentNode
```

获取所有的子节点

（1）childNodes：标准属性。返回的是指定元素的子节点的集合（包括元素节点、所有属性、文本节点）
（2）children：非标准属性。返回的是指定元素的子元素节点的集合。【重要】它只返回HTML节点，甚至不返回文本节点。



创建节点的流程：createElement(), createTextNode()，把文本节点插入元素节点 appendChild()



### 获取节点的属性值

**方式1**：

```javascript
	元素节点.属性名;
	元素节点[属性名];
```

**方式2**：

```javascript
	元素节点.getAttribute("属性名称");
```

### 设置节点的属性值

方式1举例：（设置节点的属性值）

```javascript
    myNode.src = "images/2.jpg"   //修改src的属性值
    myNode.className = "image2-box";  //修改class的name
```

方式2：

```javascript
	元素节点.setAttribute("属性名", "新的属性值");
```

方式2举例：（设置节点的属性值）

```javascript
    myNode.setAttribute("src","images/3.jpg");
```



**如果是节点的“原始属性”**（比如 普通标签的`class/className`属性、普通标签的`style`属性、普通标签的 title属性、img 标签的`src`属性、超链接的`href`属性等），**方式1和方式2是等价的**，可以混用。怎么理解混用呢？比如说：用 `div.title = '我是标题'`设置属性，用 `div.getAttribute('title')`获取属性，就是混用。

但如果是节点的“非原始属性”，**这两种方式不能交换使用**，get值和set值必须使用同一种方法。



### nodeType属性

这里讲一下nodeType属性。

- **nodeType == 1 表示的是元素节点**（标签） 。记住：在这里，元素就是标签。
- nodeType == 2 表示是属性节点。
- nodeType == 3 是文本节点。



## style属性的获取和修改

在DOM当中，如果想设置样式，有两种形式：

- className（针对内嵌样式）
- style（针对行内样式）

需要注意的是：style是一个对象，只能获取**行内样式**，不能获取内嵌的样式和外链的样式。

### 通过 js 读取/设置元素的样式 只能行内

```javascript
 元素.style["属性"];  //格式

 box.style["width"];  //举例

box1.style.width = "300px";
box1.style.backgroundColor = "red"; // 驼峰命名法
```

备注：我们通过style属性设置的样式都是**行内样式**，而行内样式有较高的优先级。但是如果在样式中的其他地方写了`!important`，则此时`!important`会有更高的优先级。



### 通过 js 获取元素当前显示的样式 不只行内

（1）w3c的做法：

```javascript
    window.getComputedStyle("要获取样式的元素", "伪元素");
```

两个参数都是必须要有的。参数二中，如果没有伪元素就用 null 代替（一般都传null）。

（2）IE和opera的做法：

```javascript
    obj.currentStyle;
```

注意：

- 如果当前元素没有设置该样式，则获取它的默认值。
- 该方法会返回一个**对象**，对象中封装了当前元素对应的样式，可以通过`对象.样式名`来读取具体的某一个样式。
- 通过currentStyle和getComputedStyle()读取到的样式都是只读的，不能修改，如果要修改必须通过style属性。



```js
    var div1 = document.getElementsByTagName("div")[0];

    console.log(getStyle(div1, "width"));
    console.log(getStyle(div1, "padding"));
    console.log(getStyle(div1, "background-color"));

    /*
     * 兼容方法，获取元素当前正在显示的样式。
     * 参数：
     *      obj     要获取样式的元素
     *.     name    要获取的样式名
    */
    function getStyle(ele, attr) {
        if (window.getComputedStyle) {
            return window.getComputedStyle(ele, null)[attr];
        }
        return ele.currentStyle[attr];
    }
```



## BOM

- [BOM](https://web.qianguyihao.com/04-JavaScript%E5%9F%BA%E7%A1%80/45-BOM%E7%AE%80%E4%BB%8B%E5%92%8Cnavigator.userAgent&History&Location.html#%E5%B8%B8%E8%A7%81%E6%A6%82%E5%BF%B5)

- **BOM**：浏览器对象模型（Browser Object Model），操作**浏览器部分功能**的API。比如让浏览器自动滚动。

```text
location.href = 'https://xxx';
```

解释：获取当前页面的 url 路径（或者设置 url 路径）；或者跳转到指定路径。

需要特别注意的是：window.location.href的赋值，并不会中断Javascript的执行立即进行页面跳转。因为 LocationChange 行为在浏览器内核中是起定时器异步执行的。异步执行的好处是为了防止代码调用过深，导致栈溢出，另外也是为了防止递归进入加载逻辑，导致状态紊乱，保证导航请求是顺序执行的。

解决办法：在 location.href 的下一行，加上 return 即可。意思是，执行了 location.href 之后，就不要再继续往下执行了。



```javascript
 location.reload();
```

解释：用于重新加载当前页面，作用和刷新按钮一样。

## 定时器

- setInterval()：循环调用。将一段代码，**每隔一段时间**执行一次。（循环执行）
- setTimeout()：延时调用。将一段代码，等待一段时间之后**再执行**。（只执行一次）

每间隔一秒，将 数字 加1：

```javascript
   let num = 1;
   setInterval(function () {
       num ++;
       console.log(num);
   }, 1000);
```



定时器的返回值是作为这个定时器的**唯一标识**，可以用来清除定时器。具体方法是：假设定时器setInterval()的返回值是`参数1`，那么`clearInterval(参数1)`就可以清除定时器。

setTimeout()的道理是一样的。



# MDN

> [参考](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Guide/Using_promises)

## 模块module

> [Kingdom](https://en.wikipedia.org/wiki/%2B44_(band))

可命名.mjs文件，和.js文件实际一样，但便于理解

需要导出。类似

```js
export const name = 'square';

export function draw(ctx, length, x, y, color) {}
```

需要导入。类似

```scala
import { name, draw, reportArea, reportPerimeter } from '/js-examples/modules/basic-modules/modules/square.mjs';
```

现在我们只需要将 main.mjs 模块应用到我们的 HTML 页面。这与我们将常规脚本应用于页面的方式非常相似，但有一些显着的差异。首先，你需要把 `type="module"` 放到 [``](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/script) 标签中，来声明这个脚本是一个模块：

```
<script type="module" src="main.mjs"></script>
```



支持重命名

```js
// inside module.mjs
export {
  function1 as newFunctionName,
  function2 as anotherNewFunctionName
};

// inside main.mjs
import { newFunctionName, anotherNewFunctionName } from '/modules/module.mjs';
```



```js
// inside module.mjs
export { function1, function2 };

// inside main.mjs
import { function1 as newFunctionName,
         function2 as anotherNewFunctionName } from '/modules/module.mjs';
```





支持模块对象创建

一个更好的解决方是，导入每一个模块功能到一个模块功能对象上。可以使用以下语法形式：

```js
import * as Module from '/modules/module.mjs';
```

这将获取 `module.mjs` 中所有可用的导出，并使它们可以作为对象模块的成员使用，从而有效地为其提供自己的命名空间。例如：

```js
Module.function1()
Module.function2()
etc.
```

## 原型

> [原型（prototype）](https://developer.mozilla.org/zh-CN/docs/Learn/JavaScript/Objects/Object_prototypes#%E4%BD%BF%E7%94%A8_javascript_%E4%B8%AD%E7%9A%84%E5%8E%9F%E5%9E%8B)

在传统的 OOP 中，首先定义“类”，此后创建对象实例时，类中定义的所有属性和方法都被复制到实例中。在 JavaScript 中并不如此复制——而是在对象实例和它的构造器之间建立一个链接（它是__proto__属性，是从构造函数的`prototype`属性派生的），之后通过上溯原型链，在构造器中找到这些属性和方法。

理解对象的原型（可以通过 [`Object.getPrototypeOf(obj)`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Object/GetPrototypeOf)或者已被弃用的[`__proto__`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Object/proto)属性获得）与构造函数的 `prototype` 属性之间的区别是很重要的。前者是每个实例上都有的属性，后者是构造函数的属性。也就是说，`Object.getPrototypeOf(new Foobar())` 和 `Foobar.prototype` 指向着同一个对象。



在 javascript 中，函数可以有属性。每个函数都有一个特殊的属性叫作**原型（prototype）**。

prototype是个对象。`prototype` 属性的值是一个对象，我们希望被原型链下游的对象继承的属性和方法，都被储存在其中。

原型对象是一个内部对象，应当使用 `__proto__` 访问）。`prototype` 属性包含（指向）一个对象，你在这个对象中定义需要被继承的成员。

原型链中的方法和属性**没有**被复制到其他对象——它们被访问需要通过前面所说的“原型链”的方式。这是和构造器里直接声明定义方法的区别，构造器里的是每个实例都有一份。原型链里全部只有一份。



每个实例对象都从原型中继承了一个 constructor 属性，该属性指向了用于构造此实例对象的构造函数。



事实上，一种极其常见的对象定义模式是，在构造器（函数体）中定义属性、在 `prototype` 属性上定义方法。如此，构造器只包含属性定义，而方法则分装在不同的代码块，代码更具可读性。例如：

```js
// 构造器及其属性定义

function Test(a,b,c,d) {
  // 属性定义
};

// 定义第一个方法

Test.prototype.x = function () { ... }

// 定义第二个方法

Test.prototype.y = function () { ... }

// 等等……
```



Object.prototype的**proto**属性是一个访问器属性（一个getter函数和一个setter函数），它公开访问它的对象的内部[[Prototype]]（对象或null）。



> [轻松理解JS 原型原型链](https://juejin.cn/post/6844903989088092174)

1. js分为**函数对**象和**普通对象**，每个对象都有__proto__属性，但是只有函数对象才有prototype属性
2. Object、Function都是js内置的**函数**, 类似的还有我们常用到的Array、RegExp、Date、Boolean、Number、String
3. 属性__proto__是一个对象，它有两个属性，constructor和__proto__；
4. 原型对象prototype有一个默认的constructor属性，用于记录实例是由哪个构造函数创建；



```scala
 function Person(name, age){ 
    this.name = name;
    this.age = age;
 }
 
 Person.prototype.motherland = 'China'
 let person01 = new Person('小明', 18);
```




js之父在设计js原型、原型链的时候遵从以下两个准则
1. Person.prototype.constructor == Person // **准则1：原型对象（即Person.prototype）的constructor指向构造函数本身**
2. person01.__proto__ == Person.prototype // **准则2：实例（即person01）的__proto__和原型对象指向同一个地方**





构造函数和原型可支持面向对象的特性。但不容易实现。下面是es6里的class笔记。



# ES6

> [参考](https://web.qianguyihao.com/05-JavaScript%E5%9F%BA%E7%A1%80%EF%BC%9AES6%E8%AF%AD%E6%B3%95/01-ES5%E5%92%8CES6%E7%9A%84%E4%BB%8B%E7%BB%8D.html#%E5%89%8D%E8%A8%80)

简单来说，ECMAScript 是 JS 的语言标准。当然，ECMAScript 还包括其他脚本语言的语言标准。

ES6 是新的 JS 语法标准。**ES6 实际上是一个泛指，泛指 ES 2015 及后续的版本**。

ES6 的改进如下：

- ES6 之前的变量提升，会导致程序在运行时有一些不可预测性。而 ES6 中通过 let、const 变量优化了这一点。
- ES6 增加了很多功能，比如：**常量、作用域、对象代理、异步处理、类、继承**等。这些在 ES5 中想实现，比较复杂，但是 ES6 对它们进行了封装。
- ES6 之前的语法过于松散，实现相同的功能，不同的人可能会写出不同的代码。

ES6 的目标是：让 JS 语言可以编写复杂的大型应用程序，成为企业级开发语言。







在 ES6 语法及之后的版本里，可以使用 `const`、`let`关键字来定义一个变量

```js
const name; // 定义一个常量

let age; // 定义一个变量
```

如果你想定义一个常量，就用 const；如果你想定义一个变量，就用 let。



