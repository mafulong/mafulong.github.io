---
layout: wiki
title: Wiki
description: 人越学越觉得自己无知
comments: false
copyright: false
permalink: /wiki/
---

> 个人学习笔记

{% case site.components.wiki.view %}

{% when 'list' %}


{% assign item_grouped = site.wiki | where_exp: 'item', 'item.title != "Wiki Template"' | group_by: 'category' | sort: 'name' %}
{% for group in item_grouped %}

## {{ group.name }} 
{% assign cate_items = group.items | sort: 'title' %}
{% assign item2_grouped = cate_items | group_by: 'cate2' | sort: 'name' %}
{% for sub_group in item2_grouped %}
{% assign name_len = sub_group.name | size %}
{% if name_len > 0 -%}
### {{ sub_group.name }} ({{ sub_group.items | size }})
<!-- <i>{{ sub_group.name }}: <sup>{{ sub_group.items | size }}</sup></i> -->
{%- endif -%}
{%- assign item_count = sub_group.items | size -%}
{%- assign item_index = 0 -%}

<ol class="posts-list">
{% for wiki in sub_group.items %}

<li class="posts-list-item">
<!-- <span class="posts-list-meta">{{ wiki.date | date:"%Y-%m-%d" }}</span> -->
<a class="posts-list-name" href="{{ site.url }}{{ post.url }}">{{ wiki.title }}</a>
</li>
{% endfor %}
</ol>

{% endfor %}
{% endfor %}



{% when 'cate' %}

{% assign item_grouped = site.wiki | where_exp: 'item', 'item.title != "Wiki Template"' | group_by: 'category' | sort: 'name' %}
{% for group in item_grouped %}
### {{ group.name }}
{% assign cate_items = group.items | sort: 'title' %}
{% assign item2_grouped = cate_items | group_by: 'cate2' | sort: 'name' %}
{% for sub_group in item2_grouped %}
{% assign name_len = sub_group.name | size %}
{% if name_len > 0 -%}
<i>{{ sub_group.name }}: <sup>{{ sub_group.items | size }}</sup></i>
{%- endif -%}
{%- assign item_count = sub_group.items | size -%}
{%- assign item_index = 0 -%}
{%- for item in sub_group.items -%}
{%- assign item_index = item_index | plus: 1 -%}
<a href="{%- if item.type == 'link' -%}{{ item.link }}{%- else -%}{{ site.url }}{{ item.url }}{%- endif -%}" style="display:inline-block;padding:0.5em" {% if item.type == 'link' %} target="_blank" {% endif %} >{{ item.title }}<span style="font-size:12px;color:red;font-style:italic;"></span></a>{%- if item_index < item_count -%}<span> <b>·</b></span>{%- endif -%}
{%- endfor -%}
{% endfor %}
{% endfor %}

{% endcase %}
