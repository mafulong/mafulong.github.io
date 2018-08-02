---
layout: post
category: web
title: javascript速查
---

## js用法
外部脚本, 可以插入任何位置
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

## JavaScript 输出
JavaScript 没有任何打印或者输出的函数。

document.write是直接写入到页面的内容流，如果在写之前没有调用document.open, 浏览器会自动调用open。每次写完关闭之后重新调用该函数，会导致页面被重写。

    JavaScript 显示数据
    JavaScript 可以通过不同的方式来输出数据：

    使用 window.alert() 弹出警告框。
    使用 document.write() 方法将内容写到 HTML 文档中。
    使用 innerHTML 写入到 HTML 元素。
    使用 console.log() 写入到浏览器的控制台。

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
字符串（String）、数字(Number)、布尔(Boolean)、数组(Array)、对象(Object)、空（Null）、未定义（Undefined）。
```javascript
//声明变量
var a;
var name="Gates", age=56, job="CEO";
//JavaScript 拥有动态类型。这意味着相同的变量可用作不同的类型：

//声明变量时可以确定其类型，如
var carname=new String;
var x=      new Number;
var y=      new Boolean;
var cars=   new Array;
var person= new Object;
```

## 数组 
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
```

## 对象
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

## Undefined 和 Null
Undefined 这个值表示变量不含有值。

可以通过将变量的值设置为 null 来清空变量。

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

## 语法
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

## 类型转化

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

## 其他
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