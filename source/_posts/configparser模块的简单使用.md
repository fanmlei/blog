---
title: configparser模块的简单使用
date: 2018-05-01 23:56:10
categories: 
- Python
---

configparser是python中自带的一个配置文件读写的库，python2中为ConfigParser在python3中更名为configparser，首先我们建立一个test.ini的配置文件，内容如下：
```python
[device]
port=COM9
baud_rate=9600</pre><h5>读操作：</h5><p>实例：</p><pre class="python">import configparser
cf=configparser.ConfigParser()
cf.read("test.ini")
print(cf.sections())
print(cf.options("device"))
print(cf.items("device"))
print(cf.get("device","port"))
```
首先导入configparser模块，再使用read方法读取配置文件内容。

sections()方法返回文件中所有section

options(section_name)方法返回该section_name下所有的option

items(section_name)方法以元祖的格式返回该section_name下的所有option的key和value

get(section_name, option_name)方法只返回key

运行结果
![](1.png)

##### 写操作：
```python
cf.add_section("section1")
cf.set('section1','key1','value1')
cf.write(open("test.ini",'w'))

print(cf.sections())
print(cf.items("section1"))
```
add_section(new_section_name)：新建一个section，如果已存在会报错。

set(section_name, option_name, value): 如果option_name存在则更新value，如果不存在则新建一个option和value，但是如果section不存在会报错。

write(）方法将内容重新写入到文件中，需要注意的是如果在写之前没有读去过这个文件那么这次写入将会导致之前的文件内容被覆盖掉。

运行结果
![](2.png)

##### 删除操作：
```cpp
print(cf.sections())
print(cf.items("section1"))

cf.remove_section("section1")
print(cf.sections())
```
remove_option(section_name,option_name)：删除指定的option，section不存在会报错。

remove_section(section_name)：删除指定的section。

需要注意这里的删除仅仅只是在内存中进行的，还要进行write()操作写入到文件中，否则配置文件实际上是没有被更改的。

运行结果：
![](3.png)
