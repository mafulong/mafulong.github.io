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

## 数据类型

### 变量和基础数据类型

字符串（String）、数字(Number)、布尔(Boolean)、数组(Array)、对象(Object)、空（Null）、未定义（Undefined）。



变量声明

let和var区别。

- var会变量提升，都是global, let不会
- 其次，当你使用 `var` 时，可以根据需要多次声明相同名称的变量，但是 `let` 不能。

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



变量初始化

一旦你定义了一个变量，你就能够初始化它。方法如下，在变量名之后跟上一个“=”，然后是数值：

```scala
myName = 'Chris';
myAge = 37;

// 你可以像这样在声明变量的时候给变量初始化：

let myName = 'Chris';
```



### 数组 

开头为0

```javascript
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

### 对象

见面向对象

### Undefined 和 Null

Undefined 这个值表示变量不含有值。

可以通过将变量的值设置为 null 来清空变量。

### 动态类型

JavaScript 是一种“动态类型语言”，这意味着不同于其他一些语言 (译者注：如 C、JAVA)，您不需要指定变量将包含什么数据类型（例如 number 或 string）

例如，如果你声明一个变量并给它一个带引号的值，浏览器就会知道它是一个字符串：

```
let myString = 'Hello';
```

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

### 逻辑运算符

- `&&` — 逻辑与; 使得并列两个或者更多的表达式成为可能，只有当这些表达式每一个都返回`true`时，整个表达式才会返回`true.`
- `||` — 逻辑或; 当两个或者更多表达式当中的任何一个返回 `true` 则整个表达式将会返回 `true`.
- ! — 逻辑非; 对一个布尔值取反，非 true 返回 false，非 false 返回 true.

## 类型转换

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

- 字符串转换为数字用Number(str)或则和parseInt(str)/parseFloat(str)方法
- 数字转换为字符串用var.toString()方法
- 获取字符串或者数组的长度，用arr.length属性
- 数组添加头部元素: arr.unshift("a","b"....); 结尾用push()方法
- NaN： not a number
- 将数组元素连接成字符串： arr.join("连接符")
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