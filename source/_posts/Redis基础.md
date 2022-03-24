---
title: Redis基础
date: 2019-03-07 02:21:08
categories: 
- 未分类
tags:
- Reids
- 编程基础
---

# Redis基础

# Redis
[toc]

## Redis的数据结构

Redis 总共有五种不同的数据结构，分别是`STRING`、`LIST`、`SET`、`HASH`、`ZSET`，各种具体含义见下图


结构类型| 存储的值
---|---|---
 STRING | 字符串、整数、浮点数 
 List | 一个链表，链表里面每个节点都是一个字符串
 SET | 集合，集合里面的每个字符串都是唯一的
 HASH | 包含键值对的无序散列表
 ZSET | 有序集合，元素顺序由分值的大小决定

## Redis 基础命令

### STRING（字符串）

#### 基础命令


命令 | 行为
---|---
GET | 获取给定键中的值
SET | 设置给定键中的值（返回OK，python客户端会转换为True）
DEL | 删除给定键中的值（返回成功删除数量 *可一次删除多个*）


```shell
# redis-cli
127.0.0.1:6379> set hello world
OK
127.0.0.1:6379> get hello
"world"
127.0.0.1:6379> del hello
(integer) 1
```
#### 自增自减命令


命令 | 用例和行为
---|---
INCR | `INCR key-name` 将对应值加一
DECR | `DECR key-name` 将对应值减一
INCRBY | `INCRBY key-name num` 将对应值加上整数`num` (num非整数会报错)
DECRBY | `DECRBY key-name num` 将对应值减去整数`num`
INCRBYFLOAT | `INCRBYFLOAT key-name num` 将对应值加上浮点数`num`


```shell
# redis-cli
127.0.0.1:6379> set amount 1
OK
127.0.0.1:6379> incr amount
(integer) 2
127.0.0.1:6379> decr amount
(integer) 1
127.0.0.1:6379> incrby amount 10
(integer) 11
127.0.0.1:6379> decrby amount 5
(integer) 6
127.0.0.1:6379> incrbyfloat amount 2.333
"8.333"
```

上面的都是正常的数值加减，那么如果值为字符串类型redis会如何处理呢？

在redis中，如果存储的字符串可以十进制转换为整数或者浮点数那么也是可以使用自增自减操作的，否则会出异常。另外如果对一个不存在的键操作的时候，默认会当作0来处理。
```shell
# redis-cli
# 可以转换的字符串自增
127.0.0.1:6379> set string-test "12"
OK
127.0.0.1:6379> incr string-test
(integer) 13
# 不可以转换的字符串自增
127.0.0.1:6379> set string-test "ab"
OK
127.0.0.1:6379> incr string-test
(error) ERR value is not an integer or out of range
# 空值自增
127.0.0.1:6379> get nil-test
(nil)
127.0.0.1:6379> incr nil-test
(integer) 1
```

#### 字符串命令


命令 | 用例和行为
---|---
APPEND | `APPEND key-name value` 将value追加到对应值的末尾，返回总长度。
GETRANGE | `GETRANGE key-name start end` 获取对应值从start到end范围类的所有内容(包含start和end)
SETRANGE | `SETRANGE key-name offset value` 将offset之后所有的内容替换为value，返回总长度。（如果offset超过最大长度，redis会使用空值补位）


```shell
# redis-cli
127.0.0.1:6379> set string 'abc'
OK
# 追加
127.0.0.1:6379> append string 'def'
(integer) 6
# 获取全部
127.0.0.1:6379> getrange string 0 -1
"abcdef"
# 设置offset之后的值
127.0.0.1:6379> setrange string 3 'abc'
(integer) 6
127.0.0.1:6379> get string
"abcabc"
# offset超过最大长度时
127.0.0.1:6379> setrange string 8 'def'
(integer) 11
127.0.0.1:6379> get string
"abcabc\x00\x00def"
```


#### 二进制命令

会将字节串看作是二进制位串来操作

命令 | 用例和行为
---|---
GETBIT | `GETBIT key-name offset` 获取偏移量为offset的二进制值值，超过最大长度返回0
SETBIT | `SETBIT key-name offset value` 将偏移量为offset的二进制值设为value，返回之前的二进制
BITCOUNT | `BITCOUNT key-name [start end]` 统计值为1的数量，可指定范围
BITOP | `BITOP operation dest-key key-name [key-name ...]`对一个或多个二进制位串执行`AND`、`OR`、`XOR`、`NOT`的按位运算操作，并将结果报错至dest-key键里面。


### LIST（列表）

#### 基础命令


命令 | 用例和行为
---|---
RPUSH | `RPUSH key-name value [value ...]` 将一个或多个推入列表右端，返回列表长度
LPUSH | `LPUSH key-name value [value ...]` 将一个或多个推入列表左端，返回列表长度
RPOP | `RPOP key-name` 移除并返回列表最右端元素
LPOP | `LPOP key-name` 移除并返回列表最左端元素
LINDEX | `LINDEX key-name offset` 返回列表中偏移量为offset的元素值
LRANGE | `LRANGE key-name start end` 返回偏移量在start和end之间的所有元素值(包括start和end)
LTRIM | `LTRIM key-name start end` 只保留偏移量在start和end之间的元素(包括start和end)


```shell
# redis-cli
# 右端推入一个或多个元素
127.0.0.1:6379> rpush list-test 1
(integer) 1
127.0.0.1:6379> rpush list-test 2 3
(integer) 3
# 左端推入一个或多个元素
127.0.0.1:6379> lpush list-test 4
(integer) 4
127.0.0.1:6379> lrange list-test 0 -1
1) "4"
2) "1"
3) "2"
4) "3"
# 弹出右端元素
127.0.0.1:6379> rpop list-test
"3"
# 弹出左端元素
127.0.0.1:6379> lpop list-test
"4"
# 获取偏移量对应元素的值
127.0.0.1:6379> lindex list-test 1
"2"
# 当偏移量不符合时
127.0.0.1:6379> lindex list-test 10
(nil)
127.0.0.1:6379> rpush list-test 5 6 7
(integer) 5
127.0.0.1:6379> lrange list-test 0 -1
1) "1"
2) "2"
3) "5"
4) "6"
5) "7"
# 保留0-1间的元素
127.0.0.1:6379> ltrim list-test 0 1
OK
127.0.0.1:6379> lrange list-test 0 -1
1) "1"
2) "2"
```

#### 阻塞弹出、列表间移动


命令 | 用例和行为
---|---
BRPOP | `BRPOP key-name [key-name ...] timeout` 从第一个非空列表中弹出最右端元素，返回被弹出的key-name和弹出的元素值，如果全部为空则阻塞timeout秒，超过timeout秒任然没有则返回None
BLPOP | `BLPOP key-name [key-name ...] timeout` 变为最左端元素，其他同上
RPOPLPUSH | `RPOPLPUSH source-key dest-key` 从source-key中弹出最右端元素并将该元素推入到dest-key的最左端，然后返回该值
BRPOPLPUSH | `RPOPLPUSH source-key dest-key timeout` 同上，如果source-key为空则阻塞timeout秒等待可弹出元素，超时返回None


```shell
# redis-cli
# list1为空，按顺序弹出list2的值
127.0.0.1:6379> rpush list2 1 2
(integer) 2
127.0.0.1:6379> rpush list3 1
(integer) 1
127.0.0.1:6379> brpop list1 list2 list3 1
1) "list2"
2) "2"

# list1阻塞1秒后
127.0.0.1:6379> brpop list1 1
(nil)
(1.08s)

# 在另一个终端向空的list1推入值
# shell-1
127.0.0.1:6379> rpush list-test 1
(integer) 1

# shell-2
127.0.0.1:6379> brpop list1 1 10
1) "list1"
2) "1"
(10.00s)

# list2和list3间的移动
127.0.0.1:6379> lrange list2 0 -1
1) "1"
127.0.0.1:6379> lrange list3 0 -1
1) "1"
127.0.0.1:6379> rpoplpush list2 list3
"1"
127.0.0.1:6379> lrange list3 0 -1
1) "1"
2) "1"
```

### SET（集合）

#### 基础命令


命令 | 用例和行为
---|---
SADD | `SADD key-name item [item ...]` 将一个或多个元素添加到集合里面，返回添加进去的数量
SREM | `SREM key-name item [item ...]` 从集合里面移除一个或者多个元素，返回成功删除的数量
SISMEMBER | `SISMEMBER key-name item` 检查item是否存在与集合里面，存在返回1否则返回0
SCARD | `SCARD key-name` 返回集合包含元素的总数
SMEMBERS | `SMEMBERS key-name` 返回集合包含的所有元素
SRANDMEMBER | `SRANDMEMBER key-name [count]` 从集合里面随机返回一个或多个元素，count为正返回结果不会重复，count为负可能会重复
SPOP | `SPOP key-name [count]` 随机移除一个或多个元素，并返回被移除的元素
SMOVE | `SMOVE source-key dest-key item` 如果source-key包含item则将item添加到dest-key集合，如果item存在则返回1否则返回0


```shell
# 添加时返回被添加的数量
127.0.0.1:6379> sadd set-test 1 2 3 1
(integer) 3
127.0.0.1:6379> smembers set-test
1) "1"
2) "2"
3) "3"
# 移除时返回被移除的数量
127.0.0.1:6379> srem set-test 4 1
(integer) 1
# 获取当前元素数量
127.0.0.1:6379> scard set-test
(integer) 2
# 不存在时返回0
127.0.0.1:6379> sismember set-test 1
(integer) 0
# 存在时返回1
127.0.0.1:6379> sismember set-test 2
(integer) 1
127.0.0.1:6379> sadd set-test 5 6 7
(integer) 3
# 默认返回一个
127.0.0.1:6379> srandmember set-test
"7"
# count为负数时返回结果重复
127.0.0.1:6379> srandmember set-test -6
1) "6"
2) "2"
3) "5"
4) "7"
5) "6"
6) "2"
# count为正数结果不会重复
127.0.0.1:6379> srandmember set-test 6
1) "2"
2) "3"
3) "5"
4) "6"
5) "7"
# 移除一个
127.0.0.1:6379> spop set-test
"2"
# 移除多个，count不能小于0
127.0.0.1:6379> spop set-test 2
1) "7"
2) "3"
# 移动失败
127.0.0.1:6379> smove set-test set2 8
(integer) 0
# 移动成功
127.0.0.1:6379> smove set-test set2 5
(integer) 1
127.0.0.1:6379> smembers set2
1) "5"
```


#### 集合的运算


命令 | 用例和行为
---|---
SDIFF | `SDIFF key-name [key-name ...]` 返回存在于第一个集合但是不存在与其他集合的元素（差集）
SDIFFSTORE | `SDIFFSTORE dest-key key-name [key-name ...]` 将存在于第一个不存在于其他集合的元素存到dest-key里面
SINTER | `SINTER key-name [key-name ...]` 返回同时存在与所有集合的元素（交集）
SINTERSTORE | `SINTERSTORE dest-key key-name [key-name ...]` 将同时存在于所有集合的元素存放到dest-key里面
SUNION | `SUNION key-name [key-name ...]` 返回至少存在于一个集合的元素（并集）
SUNIONSTORE | `SUNIONSTORE dest-key key-name [key-name ...]` 将至少存在于一个集合的元素存放到dest-key里面


```shell
# redis-cli
# 创建set1、set2、set3
127.0.0.1:6379> sadd set1 1 2 3 4
(integer) 4
127.0.0.1:6379> sadd set2 2 3 4 5
(integer) 3
127.0.0.1:6379> sadd set3 0
(integer) 1
# set1和set2的差集
127.0.0.1:6379> sdiff set1 set2
1) "1"
# set1和set2的差集存储到set4里面 
127.0.0.1:6379> sdiffstore set4 set2 set3
(integer) 4
127.0.0.1:6379> smembers set4
1) "2"
2) "3"
3) "4"
4) "5"
# set1和set2和set3的交集
127.0.0.1:6379> sinter set1 set2 set3
(empty array)
# set1和set2的交集
127.0.0.1:6379> sinter set1 set2
1) "2"
2) "3"
3) "4"
# set1和set2和set3的并集
127.0.0.1:6379> sunion set1 set2 set3
1) "0"
2) "1"
3) "2"
4) "3"
5) "4"
6) "5"
```


### HASH（散列）

#### 基础命令

在以前的版本中，有hset，hmset命令，分别是设置一个键值，设置多个键值，不过在4.0.0版本以后中hset也可以设置获取多个键值对，推荐使用hset


命令 | 用例和行为
---|---
HSET | `HSET key-name key value [key value ...]` 设置一个或多个键值对，返回设置成功的数量
HGET | `HGET key-name key ` 获取指定键值对，如果不存在则返回空值
HMGET | `HMGET key-name key [key ...]` 获取一个或多个键值对，如果不存在则用空值代替
HGETALL | `HGETALL key-name` 获取所有键值对
HDEL | `HDEL key-name key [key ...]` 删除一个或多个键值对，返回删除成功数量
HLEN | `HLEN key-name` 获取所有键值对的数量


```shell
# redis-cli
# 设置一个键值对
127.0.0.1:6379> hset hash-test 'a' 1
(integer) 1
# 设置多个键值对
127.0.0.1:6379> hset hash-test 'b' 2 'c' 3
(integer) 2
# 获取指定键值对
127.0.0.1:6379> hget hash-test a
"1"
# 获取多个键值对
127.0.0.1:6379> hmget hash-test b c
1) "2"
2) "3"
# 存在空值的情况
127.0.0.1:6379> hmget hash-test b c d
1) "2"
2) "3"
3) (nil)
# 获取所有键值对
127.0.0.1:6379> hgetall hash-test
1) "a"
2) "1"
3) "b"
4) "2"
5) "c"
6) "3"
# 删除键值对
127.0.0.1:6379> hdel hash-test a
(integer) 1
# 删除不存在的键值对
127.0.0.1:6379> hdel hash-test d
(integer) 0
# 删除多个键值对
27.0.0.1:6379> hdel hash-test b c
(integer) 2
# 获取所有键值对数量
127.0.0.1:6379> hlen hash-test
(integer) 0
127.0.0.1:6379> hset hash-test d 4
(integer) 1
127.0.0.1:6379> hlen hash-test
(integer) 1
```

#### 高级命令


命令 | 用例和行为
---|---
HEXISTS | `HEXISTS key-name key` 检查给定的键是否存在
HKEYS | `HKEYS key-name` 获取所有的键
HVALS | `HVALS key-name` 获取所有的值
HINCRBY | `HINCRBY key-name key num` 将key对应的值加上整数num，如果key对应的值不能增加则会报错
HINCRBYFLOAT | `HINCRBYFLOAT key-name key increment`将key对应的值加上浮点数数num，如果key对应的值不能增加则会报错


```shell
# redis-cli
127.0.0.1:6379> hset hash2 a 1 b 2 c 3 d d
(integer) 4
127.0.0.1:6379> hexists hash2 a
(integer) 1
127.0.0.1:6379> hexists hash2 g
(integer) 0
127.0.0.1:6379> hkeys hash2
1) "a"
2) "b"
3) "c"
4) "d"
127.0.0.1:6379> hvals hash2
1) "1"
2) "2"
3) "3"
4) "d"
127.0.0.1:6379> hincrby hash2 a 1
(integer) 2
# 不可增加的情况
127.0.0.1:6379> hincrby hash2 d 1
(error) ERR hash value is not an integer
127.0.0.1:6379> hincrbyfloat hash2 a 1
"3"
127.0.0.1:6379> hincrbyfloat hash2 a 1.33
"4.33"
# 不可增加的情况
127.0.0.1:6379> hincrbyfloat hash2 d 1.33
(error) ERR hash value is not a float
127.0.0.1:6379>
```


### ZSET（有序集合）
#### 基础命令


命令 | 用例和行为 
---|---
ZADD | `ZADD key-name score item [score item ...]` 将带有给定分值的元素添加到集合里面
ZREM | `ZREM key-name item [item ...]` 删除给定的元素，返回删除成功的个数
ZCARD | `ZCARD key-name` 返回集合里面元素总数
ZINCRBY | `ZINCRBY key-name num item` 将指定元素的分值加上num
ZCOUNT | `ZCOUNT key-name min max` 返回分值在min和max之间的元素数量
ZRANK | `ZRANK key-name item` 返回指定元素在集合里面的排名
ZSCORE | `ZSCORE key-name item` 返回指定元素的分值
ZRANGE | `ZRANGE key-name start stop [WITHSCORES]` 返回排名在start和stop之间的成员，WITHSCORES可同时返回对应的分值






### 发布与订阅

### 其他命令

