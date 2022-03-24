---
title: PyQt5之SQLite数据库操作（1）
date: 2017-11-20 02:21:08
categories: 
- 未分类
tags:
- PyQt
---
<h3>连接数据库</h3>
<p>导入库文件</p>
<p><pre name="code" class="python">from PyQt5 import QtSql
from PyQt5.QtSql import QSqlQuery</pre><br>
QtSql类即QT中的QSqlDatabase类，用于处理与数据库的连接</p>
<p>QSqlQuery类提供了执行和操作SQL语句打方法</p>
<p><br>
</p>
<p>第一步连接sqlite数据库</p>
<p><pre name="code" class="python">database = QtSql.QSqlDatabase.addDatabase('QSQLITE')
database.setDatabaseName('test.db')
</pre>没有test.db这个文件的时候则会在当前目录新建一个test.db文件</p>
<p>打开数据库，打开成功返回True</p>
<p><pre name="code" class="python">database.open()</pre></p>
<p><br>
</p>
<h3>新建表</h3>
<div>建立一个名为student的表，包含id,name,age三个属性，其中ID为主键</div>
<div><br>
</div>
<p><pre name="code" class="python">query.prepare('create table student (id int primary key, name varchar(30),age int)')
if not query.exec_():
    query.lastError()
else:
    print('create a table')</pre></p>
<h3>插入数据</h3>
<div>addBindValue()将&#20540;添加到列表中，调用顺序决定添加的顺序</div>
<div><pre name="code" class="python">insert_sql = 'insert into student values (?,?,?)'
query.prepare(insert_sql)
query.addBindValue(4)
query.addBindValue('test3')
query.addBindValue(1)
if not query.exec_():
    print(query.lastError())
else:
    print('inserted')</pre><br>
<br>
</div>
<h3>查询</h3>
查询返回数据使用value(int)函数，例如select id,name,age from student&nbsp; &nbsp;value(0)等于返回id属性的&#20540;，value(2)等于age属性
<p>exec_()查询成功返回true查询 否则返回false</p>
<p><pre name="code" class="python">query.prepare('select id,name,age from student')
if not query.exec_():
    query.lastError()
else:
    while query.next():
        id = query.value(0)
        name = query.value(1)
        age = query.value(2)
        print(id,name,age)</pre></p>
<p>可以通过record().indexOf(str)来获取索引&#20540;，<br>
</p>
<p><pre name="code" class="python">if query.exec('select id ,name,age from student'):
    id_index = query.record().indexOf('id')
    name_index = query.record().indexOf('name')
    age_index = query.record().indexOf('age')
    while query.next():
        id = query.value(id_index)
        name = query.value(name_index)
        age = query.value(age_index)
        print(id, name, age)
</pre><br>
<br>
</p>
<p><br>
</p>
<p><br>
</p>
<p>一：使用exec()操作</p>
<p>指令执行成功则&nbsp;exec_()会返回True并把查询状态设为活跃状态，否则返回false</p>
<p>另外对于SQLite，查询字符串一次只能包含一条语句。如果给出多个语句，则函数返回false</p>
<p></p>
<p><pre name="code" class="python">if query.exec('select id ,name,age from student'):
    while query.next():
        id = query.value(0)
        name = query.value(1)
        age = query.value(2)
        print(id, name, age)
</pre></p>
<p><br>
</p>
二：execBatch()操作
<p>这个函数是批处理之前准备好的指令，如果数据库不支持批处理他会自己调用exec()来模拟</p>
<p><pre name="code" class="python">query.prepare('insert into student values (?,?,?)')
query.addBindValue([6,7,8])
query.addBindValue(['test5','test6','test7'])
query.addBindValue([1,1,1])
if query.execBatch():
    print(&quot;inserted &quot;)</pre><br>
</p>
<p>三：executedQuery()返回最后一个执行成功的指令</p>
<p><pre name="code" class="python">if query.exec('select id ,name,age from student'):
    while query.next():
        id = query.value(0)
        name = query.value(1)
        age = query.value(2)
        print(id, name, age)
        
print(query.executedQuery())</pre>执行结果为：select id ,name,age from student</p>
<p><br>
</p>
<p>四：&nbsp;其他</p>
<p>finish()终止当前的操作</p>
<p>isActive()返回当前是否处于活跃状态<br>
isNull(int&nbsp;field)返回当前是否不活跃</p>
<p>isSelect()返回是不是一个查询语句</p>
next()检索结果中的下一条记录（如果可用），并将查询放在检索到的记录上。请注意，结果必须处于活动状态，并且在调用此函数之前，isSelect（）必须返回true，否则它将不执行任何操作并返回false。
<p><br>
</p>
<div style="top:393px">指令执行成功则&nbsp;exec_()会返回True并把查询状态设为活跃状态，否则返回false</div>
