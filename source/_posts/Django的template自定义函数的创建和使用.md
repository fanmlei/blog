---
title: Django的template自定义函数的创建和使用
date: 2018-08-23 10:20:45
categories: 
- Django
tags:
- Django模版
---
首先需要在APP目录下创建一个templatetags目录
然后在这个目录下新建一个任意名的.py文件 如 test.py
创建一个template对象register
```python
from django import template
from django.utils.safestring import mark_safe

register =template.Library()
```

下面在这个文件中我们就可以写自定义函数了
有两种方式
一种是simple_tag,这种会限制参数的个数，但是不能作为if的条件来使用
```python
@register.simple_tag
def add(a,b):
    return a+b
```
一种是filter，这个最多只能传递两个参数，可作为if条件使用
```python
@register.filter
def subtract(a,b):
    return a-b
```
这时候就可以在模板文件中使用这个函数了
首先在开头位置导入test.py文件
simple_tag直接使用%来调用函数，如果函数需要传参数，需要在函数后直接添加即可（用空格隔开）
```python
{% load test %}

{% add 2 3 %}

{{ 1|subtract:2 }}
```
![](1.png)

要注意的是app目录下的templatetags名不能更改 register也不能更改，还需要在settings里面注册这个app
