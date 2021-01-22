---
layout: post
category: Python
title: python依赖requirements
tags: Python
---

## python依赖requirements

在虚拟环境中使用pip生成：

```
pip freeze >requirements.txt
```



示例：

```
alembic==0.8.6
bleach==1.4.3
click==6.6
dominate==2.2.1
Flask==0.11.1
Flask-Bootstrap==3.3.6.0
Flask-Login==0.3.2
Flask-Migrate==1.8.1
Flask-Moment==0.5.1
Flask-PageDown==0.2.1
Flask-Script==2.0.5
Flask-SQLAlchemy==2.1
Flask-WTF==0.12
html5lib==0.9999999
itsdangerous==0.24
Jinja2==2.8
Mako==1.0.4
Markdown==2.6.6
MarkupSafe==0.23
PyMySQL==0.7.5
python-editor==1.0.1
six==1.10.0
SQLAlchemy==1.0.14
visitor==0.1.3
Werkzeug==0.11.10
WTForms==2.1
```



当需要创建这个虚拟环境的完全副本，可以创建一个新的虚拟环境，并在其上运行以下命令：

```
pip install -r requirements.txt
```

