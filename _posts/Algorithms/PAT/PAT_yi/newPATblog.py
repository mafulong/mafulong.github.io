import datetime
# 修改标题
title="1034. 有理数四则运算(20)"
# 修改目录
category="PAT乙题"


m1='''---
layout: post
category: '''
m2='''
title: '''
m3='''
---'''
# 获得代码内容 text
f1=r"D:\Code_Projects\c++\vs2017\Project1\Project1\code.cpp"
with open(f1, "rt") as in_file:
    text = in_file.read()
# print(text)
text1='''
```c++
'''+text+'''
```'''
# str 正文
str=m1+category+m2+"PAT乙题 "+title+m3+text1;
print(str)
# 获取当前时间, 其中中包含了year, month, hour, 需要import datetime  
def datetime_toString(dt):
    return dt.strftime("%Y-%m-%d-%H")
today = datetime.date.today()  
t2=today.strftime("%Y-%m-%d")
# print(t2)


with open(t2+"-"+title+".md", "wt") as out_file:
    out_file.write(str)
