---
title: MySQL必知必会总结（一）
date: 2019-12-20 02:21:08
categories: 
- 未分类
---
#### 去重

MySQL中不能部分使用DISTINCT，DISTINCT关键字会应用于所有列而不仅是前置它的列。如果给出SELECT DISTINCT score,age，除非指定的两个列都不同，否则所有行都将被检索出来。

例如如下的表

| name  | score | age  |
| ----- | ----- | ---- |
| test1 | 11    | 11   |
| test2 | 11    | 11   |
| test3 | 123   | 123  |
| test4 | 123   | 11   |

```sql
SELECT DISTINCT score ,age FROM `student` 
```

结果：

| score | age  |
| :---- | :--- |
| 11    | 11   |
| 123   | 123  |
| 123   | 11   |

#### 排序

- 按单个列排序

  ```sql
  SELECT score FROM 'student' ORDER BY score
  ```

  | score |
  | ----- |
  | 11    |
  | 11    |
  | 123   |
  | 123   |

- 按多个列排序

  会先按照第一列排序，如果第一列存在相同的会根据后面的列继续排列，换句话说就是当第一列所有数据全部不同，那么是不会根据后面的列再次排序的

  ```sql
  SELECT score, age FROM 'student' ORDER BY score, age
  ```

  | score | age  |
  | ----- | ---- |
  | 11    | 11   |
  | 11    | 11   |
  | 123   | 11   |
  | 123   | 123  |

- 指定排序方向

  MySQL中默认为升序排序，如果想用降序排序需要指定DESC关键字，和DISTINCT不同的是DESC只会作用于它前面的列，想要每列都已降序排序就必须对每列都指定DESC关键字。

  ```sql
  SELECT score, age FROM 'student' ORDER BY score DESC，age
  ```

  | score | age  |
  | ----- | ---- |
  | 123   | 11   |
  | 123   | 123  |
  | 11    | 11   |
  | 11    | 11   |

- 排序规则

  在对文本性的数据排序时，MySQL默认是不区分大小写的，即A和a相同，如果想要区分的话可能需要对数据库的设置做更改

#### 过滤数据

- WHERE语句的操作符

  | 操作符        | 作用             |
  | ------------- | ---------------- |
  | =             | 等于             |
  | <>            | 不等于           |
  | !=            | 不等于           |
  | <             |                  |
  | <=            |                  |
  | >             |                  |
  | >=            |                  |
  | BETWEEN… AND… | 在两个指定值之间 |

- 匹配操作

  MySQL在执行WHERE语句匹配时默认不区分大小写，Abc和abc是一样的

  ```sql
  select name from tbnaem where name='Abc';
  select name from tbnaem where name='abc';
  ```

- 空值检查

  NULL和0、空字符串是不同的，如果要匹配NULL需要用IS NULL子句实现

  ```sql
  select * from tbname where name IS NULL
  ```

- 组合过滤

  - AND操作符

    会对每个判断条件取与，满足所有条件才会返回

  - OR操作符

    满足任意一个条件即符合要求

  - 同时使用AND和OR操作符

    MySQL会优先处理AND操作符，例如 ：

    ```sql
    select name, price from tbname where id = 2 or id = 3 and price<10
    ```

    上面这个SQL语句会过滤出ID等于2或者ID等于3并且价格小于10的行，这显然和我们的意图不一样（ID等于2或者3，并且价格小于10）。为了解决这个问题，需使用圆括号将操作符分组区分开来，改为下面这种：

    ```sql
    select name, price from tbname where (id = 2 or id = 3) and price<10
    ```

    **因此在使用具有AND和OR操作符的where子句时，应当使用圆括号将操作符分组处理，不要依赖于默认的计算顺序以免出现错误。**

- IN操作符

  IN操作符可以指定条件范围，范围中的每个条件都可以进行匹配，类似于之前的OR操作符

  ```sql
  select name, price from tbname where id in (2,3)
  ```

  相交于OR操作符，在更多的过滤条件下显得更为简洁直观，会有比OR操作符更好的性能，另外IN操作符可以包含其他的SELECT语句：

- NOT操作符

  NOT操作符只有一个功能，否定它之后所跟的任何条件，例如IN、BETWEEN、EXISTS

  ```sql
  select name from tbname where id not in (2,3)
  ```

  选取ID不是2,3的行。

- 通配符过滤（LIKE操作符）

  - 百分号（%）通配符

    %可以表示任何字符串出现任何次数，例如找到name是以`fml`开头的行

    ```sql
    select name from tbname where name LIKE 'fml%'
    ```

    或者包含abc的行

    ```sql
    select name from tbname where name LIKE '%abc%'
    ```

    或者以a开头c结尾的行

    ```sql
    select name from tbname where name LIKE 'a%c'
    ```

    **%看似可以匹配任何东西，但是NULL是例外的， LIKE  ‘’%‘’无法匹配值为NULL的行，另外值得注意的是尾空格可能也会干扰通配符的匹配**

  - 下划线（_）通配符

    _只能匹配单个字符其他的和%一样

  - 技巧

    1. 不要过度使用通配符，如果其他操作符能够实现同样的目的那么就使用其他操作符。
    2. 除非是必要的，否则不要将通配符放在开始处，那样是最慢的

- 使用正则表达式

  使用正则表达式匹配的时候需要使用REGEXP关键字来代替LIKE，REGEXP后所跟的字符串就是正则表达式了。正则表达式怎么写就不在这说了
























