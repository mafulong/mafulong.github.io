import datetime
# 修改标题
title="waaa"
file1=open("text.txt",encoding="UTF-8")
title=file1.readline();
title=title[:-1]
file1.close()

# 修改目录
category="PAT甲题"


m1='''---
layout: post
category: '''
m2='''
title: '''
m3='''
---
'''
# 获得代码内容 text
f1=r"D:\Code_Projects\c++\vs2017\Project1\Project1\code.cpp"
with open(f1, "rt") as in_file:
    text = in_file.read()
# print(text)
text0=""
f2=r"D:\mafulong.github.io\_posts\PAT_jia\text.txt"
with open(f2, "rt+",encoding='UTF-8') as in_file:
    # text0 = in_file.read()
    while True:
        lines=in_file.readline()
        if not lines:
            break
        text0=text0+lines+"\n"
    
# print(text0)

text1='''

```c++
'''+text+'''
```'''
# str 正文
str=m1+category+m2+"PAT甲题 "+title+m3+text0+text1;
print(str)
# 获取当前时间, 其中中包含了year, month, hour, 需要import datetime  
def datetime_toString(dt):
    return dt.strftime("%Y-%m-%d-%H")
today = datetime.date.today()  
t2=today.strftime("%Y-%m-%d")
# print(t2)


with open(t2+"-"+title+".md", "wt+",encoding='UTF-8') as out_file:
    out_file.write(str)

print("\n\n"+t2+"-"+title+".md"+" built")
