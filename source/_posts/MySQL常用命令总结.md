<p style="margin-left:0pt;"><strong><strong>显示所有数据库：</strong></strong>show databases;<br /><img alt="" class="has" height="176" src="https://img-blog.csdn.net/20180818091228226?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="260" /></p>

<p style="margin-left:0pt;"><strong><strong>新建数据库：</strong></strong>create database dbname;</p>

<p style="margin-left:0pt;"><strong><strong>删除数据库：</strong></strong>drop database dbname;</p>

<p style="margin-left:0pt;"><strong><strong>切换数据库：</strong></strong>use dbname;</p>

<p style="margin-left:0pt;"><strong><strong>新建表：</strong></strong>create table tbname(clo1 type ,col2 type,……);<br /><img alt="" class="has" height="158" src="https://img-blog.csdn.net/20180818091257226?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="350" /></p>

<p style="margin-left:0pt;"><strong><strong>显示所有表：</strong></strong>show tables;</p>

<p style="margin-left:0pt;"><strong><strong>根据已有表结构创建新表：</strong></strong></p>

<p style="margin-left:0pt;">create table new_table_name like old_table_name;</p>

<p style="margin-left:0pt;">create table new_table as select col1,col2,…. from old_table only;</p>

<p style="margin-left:0pt;"><strong><strong>显示表结构：</strong></strong>describe table_name;<br /><img alt="" class="has" height="119" src="https://img-blog.csdn.net/20180818091433792?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="412" /></p>

<p style="margin-left:0pt;"><strong><strong>删除表：</strong></strong>drop table table_name;</p>

<p style="margin-left:0pt;"><strong><strong>增加一列：</strong></strong>alter table tbname add column col type;</p>

<p style="margin-left:0pt;"><strong><strong>删除一列：</strong></strong>alter table tbname drop column name;</p>

<p style="margin-left:0pt;"><strong><strong>修改列属性:</strong></strong>alter table tbname modify col typr;</p>

<p style="margin-left:0pt;"><strong><strong>增加主键：</strong></strong>alter table tbname add primary key (col);</p>

<p style="margin-left:0pt;"><strong><strong>删除主键：</strong></strong>alter table tbname drop primary key(col);</p>

<p style="margin-left:0pt;"><strong><strong>修改表名：</strong></strong>alter table tbname rename new;</p>

<p style="margin-left:0pt;"><strong><strong>创建索引：</strong></strong>create index idxname on tbname (col,….);</p>

<p style="margin-left:0pt;"><strong><strong>删除索引：</strong></strong>drop index idxname on tbname;</p>

<p style="margin-left:0pt;"><strong><strong>查看索引：</strong></strong>show index from tbname;</p>

<p style="margin-left:0pt;"><strong><strong>创建视图：</strong></strong>create view name as select (col,….) from tbname;</p>

<p style="margin-left:0pt;"><strong><strong>删除视图：</strong></strong>drop view name;</p>

<p style="margin-left:0pt;"> </p>

<p style="margin-left:0pt;"><strong><strong>增删改查：</strong></strong></p>

<p style="margin-left:0pt;"><strong><strong>增：</strong></strong>insert into tbname (col,col,…) values(value1,value2,…);</p>

<p style="margin-left:0pt;"><strong><strong>删：</strong></strong>delete from tbname where 条件;</p>

<p style="margin-left:0pt;"><strong><strong>改：</strong></strong>update tbname set field=value where条件;</p>

<p style="margin-left:0pt;"><strong><strong>查：</strong></strong>select filed from tbname where 条件;</p>

<p style="margin-left:0pt;"> </p>

<p style="margin-left:0pt;"><strong><strong>求和：</strong></strong>select sum(col) as name from tbname;</p>

<p style="margin-left:0pt;"><strong><strong>平均：</strong></strong>select avg(col) as name from tbname;</p>

<p style="margin-left:0pt;"><strong><strong>最大：</strong></strong>select max(col) as name from tbname;</p>

<p style="margin-left:0pt;"><strong><strong>最小：</strong></strong>select min(col) as name from tbname;</p>

<p style="margin-left:0pt;"> </p>

<p style="margin-left:0pt;"><strong><strong>外键定义：</strong></strong>外键是指引用另一个表中的一列或者多列，被引用的列应该具有主键约束或者唯一约束，外键用于建立和加强两个表数据之间的连接，被引用的表是主表，引用外键的表是从表。</p>

<p style="margin-left:0pt;"><strong><strong>多表操作：</strong></strong></p>

<p style="margin-left:0pt;"><strong><strong>建立外键：</strong></strong>alter table tbname add constraint 外键名 froeign key(外键字段名) references 外表表名(主键字段名);</p>

<p style="margin-left:0pt;">示例：alter table student add constraint fk_id foreign key(gid) references grade(id);</p>

<p style="margin-left:0pt;"><strong><strong>删除外键：</strong></strong>alter table tbname drop foreign key 外键名;</p>

<p style="margin-left:0pt;">示例：alter table student drop foreign key fk_id;</p>

<p style="margin-left:0pt;"><strong><strong>添加数据：</strong></strong>当有外键的表添加数据的时候其字段值只能是被关联表中已有的数据，例如grade中id字段只有1和2，那么student中的gid值只能设为1和2.</p>

<p style="margin-left:0pt;"><strong><strong>删除数据：</strong></strong>因为grade表和student表具有关联关系，参照列中的被参照值是不能被删除的，所以想删除grade表中的数据必须先将student中关联数据都删除掉后再删除grade中的数据。</p>

<p style="margin-left:0pt;"><strong><strong>连接查询：</strong></strong></p>

<p style="margin-left:0pt;">首先建立两个表：</p>

<p style="margin-left:0pt;">表1：create table department (did int not null primary key, dname varchar(32));</p>

<p style="margin-left:0pt;">表2：create table employee(id int not null primary key, name varchar(32), age int, did int not null);</p>

<p style="margin-left:0pt;">插入数据</p>

<p style="margin-left:0pt;">insert into department(did,dname)VALUES (1,'网络部'),(2,'媒体部'),(3,'研发部'),(5,'人事部');</p>

<p style="margin-left:0pt;"><span style="color:#000000;">I</span><span style="color:#000000;">nsert into</span><span style="color:#000000;"> employee(id,name,age,did)</span> <span style="color:#000000;">VALUES (1,'王红',20,1),(2,'李强',22,1),(3,'赵四',20,2),(4,'郝娟',20,4);</span></p>

<p style="margin-left:0pt;"><strong><strong>交叉连接：</strong></strong>交叉连接返回的结果是两个连接表中所有数据的笛卡尔集，即返回第一个表中符合条件的数据乘以第二个表中符合条件的数据。</p>

<p style="margin-left:0pt;">语句：select 字段 from tbname1 cross join tbname2;</p>

<p style="margin-left:0pt;">例如：select * from department cross join employee;</p>

<p style="margin-left:0pt;">返回结果为：有16行（4*4）</p>

<p style="margin-left:0pt;"><strong><strong>内连接：</strong></strong>使用比较运算符对两个表中的数据进行比较，并列出与连接条件匹配的数据</p>

<p style="margin-left:0pt;">语句：select 字段 from tbname1 [inner] join tbname2 on tbname1.关系字段=tbname2.关系字段;</p>

<p style="margin-left:0pt;">例如 select name from employee join department on employee.did=department.did;</p>

<p style="margin-left:0pt;">返回结果为：3行（did为1，2，3的数据）<br /><img alt="" class="has" height="109" src="https://img-blog.csdn.net/20180818091518909?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="123" /></p>

<p style="margin-left:0pt;"><strong><strong>自连接：</strong></strong>如果在一个连接查询中涉及的两个表其实是同一个表，这种查询称为自连接查询</p>

<p style="margin-left:0pt;">语句：select p1.* from tbname as p1 join tbname as p2 on p1.字段 = p2.字段;</p>

<p style="margin-left:0pt;">示例：查询 name为王红的人所属部门员工</p>

<p style="margin-left:0pt;">select p1.* from employee as p1 join employee as p2 on p1.did = p2.did where p2.name = ‘王红’;</p>

<p style="margin-left:0pt;">返回结果为：2行（网络部的两个：王红和李强）<br /><img alt="" class="has" height="114" src="https://img-blog.csdn.net/20180818091540331?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="229" /></p>

<p style="margin-left:0pt;"> </p>

<p style="margin-left:0pt;"><strong><strong>外连接：</strong></strong>外连接分为左连接和右连接，当返回的查询结果不仅需要包括符合条件的数据，还需要包含其中的一个表或者两个表的所有数据的时候，需要用到外连接查询</p>

<p style="margin-left:0pt;">语句：select 字段 from tbname1 left|right [outer] join tbname2;</p>

<p style="margin-left:0pt;">左连接：left join：返回包括左表中的所有记录和右表中符合条件的记录。</p>

<p style="margin-left:0pt;">例如：select department.dname,employee.name from department left join employee on department.did = employee.did;</p>

<p style="margin-left:0pt;"><img alt="" class="has" height="146" src="https://img-blog.csdn.net/20180818091604776?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="157" /></p>

<p style="margin-left:0pt;">右连接：right join：返回包括右表的所有记录和左表符合条件的记录。</p>

<p style="margin-left:0pt;">例如：select department.dname,employee.name from department right join employee on department.did = employee.did;</p>

<p style="margin-left:0pt;"><img alt="" class="has" height="123" src="https://img-blog.csdn.net/20180818091619299?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="155" /></p>

<p style="margin-left:0pt;"><strong><strong>子查询：</strong></strong>指一个查询语句嵌套在另一个查询语句内部的查询，在执行的时候会先执行子查询中的语句，然后将返回的结果作为外层查询的过滤条件。<strong><strong>需要注意的是第一个条件的判断字段要包含在第二个查询语句的字段中，否则报错。</strong></strong></p>

<p style="margin-left:0pt;"><strong><em><strong><em>IN/NOT IN语句</em></strong></em></strong>：select 字段from tbname where 条件 in /not in (select 字段 where 条件)  </p>

<p style="margin-left:0pt;"><strong><em><strong><em>EXISTS语句</em></strong></em></strong>：EXISTS关键字后面的参数可以是任何一个子查询，但是不会产生任何数据，只返回TRUE或者FALSE，当返回TRUE的时候外层查询才会执行。</p>

<p style="margin-left:0pt;">语句：select 字段 from tbname where exists (select 字段 from tbname where 条件)</p>

<p style="margin-left:0pt;"><strong><em><strong><em>ANY语句：</em></strong></em></strong>ANY关键字表示只要满足内层子查询中的任意一个条件，就会返回一个结果作为外层查询条件。</p>

<p style="margin-left:0pt;">语句：select 字段from tbname where 字段 比较符 any(select字段 from tbnamewhere条件)</p>

<p style="margin-left:0pt;"><strong><em><strong><em>ALL语句</em></strong></em></strong>：类似于ANY只是他需要满足所有条件</p>

<p style="margin-left:0pt;">语句：select字段 from tbname where 字段 比较符 all(select 字段 from tbname where条件)</p>

<p style="margin-left:0pt;"> </p>