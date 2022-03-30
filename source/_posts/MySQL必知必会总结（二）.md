---
title: MySQL必知必会总结（二）
date: 2019-12-23 02:21:08
categories: 
- 未分类
---

#### 计算字段

一般数据库中存储的数据可能不会是我们所需要的格式，例如存储一个地址，在数据库中可能会将城市、区和街道分别存入不同的列中，但是我们可能需要直接获取一个完整的地址，这时候就需要做一些转换操作了，可以直接取出每个字段的值，然后在我们自己的程序中组合，同样也可以使用SQL直接在数据库中完成，而且一般来说在数据库中完成这些操作要率相对于我们自己去实现要快，下面就是一些常用的计算方法。
<!--more-->
表：

| name         | category | number | price |
| ------------ | -------- | ------ | ----- |
| 硬盘         | 电子类   | 10     | 399   |
| 乐事薯片     | 食品类   | 24     | 7.5   |
| PS4          | 电子类   | 1      | 2799  |
| 流畅的Python | 书籍类   | 5      | 105   |

- 拼接字段

  在select语句中可以使用Concat()函数实现两列的拼接操作：

  ```sql
  select concat(name,'(',category,')') as goods from goods
  ```

  | goods                |
  | :------------------- |
  | 硬盘(电子类)         |
  | 乐事薯片(食品类)     |
  | PS4(电子类)          |
  | 流畅的Python(书籍类) |

  其他：RTrim()函数去除右边所有空格，LTrim()去除左边所有空格， as：使用别名

- 执行算术计算

  依然使用上面那个表，如果我们需要取出所有商品的总金额，我们可以取出每行的价格和数量自己计算，同样也可是使用MySQL计算完成之后直接返回总金额。

  ```sql
  select name, number*price as total_price from goods
  ```

  | name         | total_price |
  | ------------ | ----------- |
  | 硬盘         | 3990        |
  | 乐事薯片     | 180         |
  | PS4          | 2799        |
  | 流畅的Python | 525         |

  MySQL支持的运算符有 +、 -、 *、 /  ，可以使用()来区分计算顺序。

#### 函数

- 文本处理函数

  | 函 数                                                 | 说 明                                                        |
  | ----------------------------------------------------- | ------------------------------------------------------------ |
  | Left(str,length)                                      | 返回串左边的字符                                             |
  | Length(str)                                           | 返回串的长度(字节长度 )， UTF-8编码中文三个字节，英文一个字节 |
  | Locate([substr](http://xiaolan.gjjblog.com/),str,pos) | 返回子串 substr 在[字符串](http://xiaolan.gjjblog.com/) str 第 pos 位置后中第一次出现的位置。如果子串 substr 在 str 中不存在，返回值为 0   **（pos可选）** |
  | Lower(str)                                            | 将串转换为小写                                               |
  | LTrim(str)                                            | 去掉串左边的空格                                             |
  | Righ(str,length)                                      | 返回串右边的字符                                             |
  | RTrim(str)                                            | 去掉串右边的空格                                             |
  | Soundex()                                             | 返回串的SOUNDEX值（不常用）SOUNDEX是一个将任何文本串转换为描述其语音表示的字母数字模式的算法 |
  | SubString(str, pos, len)                              | 返回字符串第pos位置后的len长度的子串  **第一个字符pos为1，len可选，默认到最后一位** |
  | Upper()                                               | 将串转换为大写                                               |

- 日期和时间处理函数
  
  

  | AddDate()     | 作用                           |
  | ------------- | ------------------------------ |
  | AddDate()     | 增加一个日期（天、周等）       |
  | AddTime()     | 增加一个时间（时、分等）       |
  | CurDate()     | 返回当前日期                   |
  | CurTime()     | 返回当前时间                   |
  | Date()        | 返回日期时间的日期部分         |
  | DateDiff()    | 计算两个日期之差               |
  | Date_Add()    | 高度灵活的日期运算函数         |
  | Date_Format() | 返回一个格式化的日期或时间串   |
  | Day()         | 返回一个日期的天数部分         |
  | DayOfWeek()   | 对于一个日期，返回对应的星期几 |
  | Hour()        | 返回一个时间的小时部分         |
  | Minute()      | 返回一个时间的分钟部分         |
  | Month()       | 返回一个日期的月份部分         |
  | Now()         | 返回当前日期和时间             |
  | Second()      | 返回一个时间的秒部分           |
  | Time()        | 返回一个日期时间的时间部分     |
  | Year()        | 返回一个日期的年份部分         |

- 数值处理函数

  | 函数   | 说明               |
  | ------ | ------------------ |
  | Abs()  | 返回一个数的绝对值 |
  | Cos()  | 返回一个角度的余弦 |
  | Exp()  | 返回一个数的指数值 |
  | Mod()  | 返回除操作的余数   |
  | Pi()   | 返回圆周率         |
  | Rand() | 返回一个随机数     |
  | Sin()  | 返回一个角度的正弦 |
  | Sqrt() | 返回一个数的平方根 |
  | Tan()  | 返回一个角度的正切 |

- 聚集函数

  默认参数为ALL，可使用DISTINCT关键字

  | 函 数   | 说 明                                  |
  | ------- | -------------------------------------- |
  | AVG()   | 返回某列的平均值                       |
  | COUNT() | 返回某列的行数（指定列名会忽略NULL行） |
  | MAX()   | 返回某列的最大值                       |
  | MIN()   | 返回某列的最小值                       |
  | SUM()   | 返回某列值之和                         |

#### 数据的分组

| name         | category | number | price |
| ------------ | -------- | ------ | ----- |
| 硬盘         | 电子类   | 10     | 399   |
| 乐事薯片     | 食品类   | 24     | 7.5   |
| PS4          | 电子类   | 1      | 2799  |
| 流畅的Python | 书籍类   | 5      | 105   |

- GROUP BY

  按照category分组，并计算每组的数量

  ```sql
  select category , count(*)as num from goods group by category 
  ```

  | category | num  |
  | -------- | ---- |
  | 书籍类   | 1    |
  | 电子类   | 2    |
  | 食品类   | 1    |

  - GROUP BY子句可以包含任意数目的列
  - 如果在GROUP BY子句中嵌套了分组，数据将在最后规定的分组上进行汇总。换句话说，在建立分组时，指定的所有列都一起计算（所以不能从个别的列取回数据）。
  - GROUP BY子句中列出的每个列都必须是检索列或有效的表达式（但不能是聚集函数）。如果在SELECT中使用表达式，则必须在GROUP BY子句中指定相同的表达式。不能使用别名。
  - 除聚集计算语句外，SELECT语句中的每个列都必须在GROUP BY子句中给出。
  - 如果分组列中具有NULL值，则NULL将作为一个分组返回。如果列中有多行NULL值，它们将分为一组。
  - GROUP BY子句必须出现在WHERE子句之后，ORDER BY子句之前

- HAVING（过滤分组）

  HAVING类似于WHERE，所有的WHERE子句都可以使用HAVING来代替，两者唯一的差别是WHERE过滤行而HAVING过滤分组，换一句话说，WHERE在数据分组之前过滤，HAVING在分组之后过滤，WHERE排除的行不包含在分组之中。

  选取种类大于等于两个的分组

  ```sql
  select category, count(*) as num from goods group by category HAVING count(*) >= 2
  ```

  | category | num  |
  | -------- | ---- |
  | 电子类   | 2    |

- 分组排序

  使用GROUP BY分组得到的数据顺序可能不是统一的，如果想实现分组排序还需要用到ORDER BY对分组结果进行排序

  例如按照category分组，并按照数目从小到大排序

  ```sql
  select category ,count(*) num from goods group by category order by count(*)
  ```

  | category | num  |
  | -------- | ---- |
  | 食品类   | 1    |
  | 书籍类   | 1    |
  | 电子类   | 2    |



**总结一下**

**在SELECT语句中，所有子句的顺序如下**

**SELECT →  FROM  → WHERE → GROUP BY → HAVING → ORDER BY**


















