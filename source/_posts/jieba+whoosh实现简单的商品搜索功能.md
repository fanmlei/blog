---
title: jieba+whoosh实现简单的商品搜索功能
date: 2021-04-17 19:42:49
categories: 
- 未分类
tags:
- 分词
---
#### 功能描述
实现一个类似淘宝的搜索功能，例如下面这个例子
![](1.png)
简单点来说我们需要先根据商品名称创建索引，然后再用索引文件匹配去查询字符串来实现商品的搜索，这种搜索是有别于正则匹配的，他会对字符串进行分词处理，准确度也会更高。

---
#### 准备工作
这个项目种主要用到了jieba、whoosh两个库，其中jieba实现对中文的分词处理，whoosh则是创建索引文件。
安装依赖：
- 系统：Ubuntu 16.04
- Python版本： 3.5
	```shell
	pip install jieba
	pip install whoosh
	```
测试数据：
从github上找到的空气净化器的csv数据，需要的可点击下载[测试数据](https://github.com/Ckend/taobao_scrapy/blob/master/result/%E7%A9%BA%E6%B0%94%E6%B8%85%E6%96%B0%E5%99%A8_result.csv)

---
#### 正式开始
- **创建索引文件**
首先需要利用whoosh提供的接口对csv中的数据进行处理，生成索引文件。
whoosh对中文分词处理不是很好，所以选择jieba实现对中文的分词处理，jieba这个库也有对whoosh的支持，所以处理起来很方便，直接将索引模式中的analyzer更换为jieba的ChineseAnalyzer即可。<br>
`schema`定义了索引的模式，规定了索引的字段信息，其中索引字段包含`ID`、`STROED`、`KEYWORD`、`TEXT`、`NUMERIC`、`BOOLEAN`、`DATETIME`等几种，具体的含义和使用对象还是去看whoosh的官方文档来的直接，另外schema只需要我们创建一次，然后就会和索引一起被保存。（只需在第一次创建的时候声明schema）
	```python
	from whoosh.index import create_in
	from whoosh.fields import *
	from jieba.analyse.analyzer import ChineseAnalyzer
	import os.path
	import csv
	
	def create_index():
    	"""
    	创建索引文件
    	:return: None
    	"""
    	analyzer = ChineseAnalyzer()
    	schema = Schema(id=ID(stored=True, unique=True), content=TEXT(stored=True, analyzer=analyzer))  # 声明索引模式
    	if not os.path.exists("index"):  # 创建目录
        	os.mkdir("index")
    	ix = create_in("index", schema)
    	writer = ix.writer()
	
    	# csv数据
    	csv_file = open('goods.csv', 'r')  # 读取csv文件
    	data = csv.reader(csv_file)
    	for i in data:
        	writer.add_document(
            	id=i[3],
            	content=i[0]
        	)
  		writer.commit()
	```
	使用`create_in`来创建索引文件，以后对索引文件的更删改查都是使用`open_dir`代开文件。<br>
	在读取csv数据的时候，使用`add_document`来新增索引，其中并不是所有在schema中申明的字段都需要存储的可以为空。最后使用`commit`实现索引文件的正式写入，这一点和数据库很像。
- **简单的查询**
  ```python
 	from whoosh.index import open_dir
	from whoosh.qparser import QueryParser
	from create_index import create_index
	import os.path
	
	def search(keyword, limit=10):
    """
    按照关键字搜索商品
    :param keyword: 商品名称  type: str
    :param limit: 检索数量  type: int
    :return: [{'id':'','content':''},{}]  type：list
    """
    if not os.path.exists("index"):  # 查询时没有缩索引文件，需先创建索引文件
        create_index()
    ix = open_dir("index")  # 读取索引文件
    with ix.searcher() as searcher:
        parser = QueryParser("content", schema=ix.schema)
        keyword = parser.parse(keyword)  # 构造查询语句
        results = searcher.search(keyword, limit=limit)
        res = []
        for i in results:
            res.append({'id': i['id'], 'content': i['content']})
            print(i['id'], i['content'])
        print(res)
  ```
  在查询的时候需要先调用whoosh的`QueryParser`来构建查询字符串，通过调试我发现在构造查询字符串的时候whoosh默认会分词处理，并且使用`AND`连接符
![](2.png)通过`search(keyword,limit)`去索引文件中匹配相关信息，其中`limit`为匹配到的最大数目，默认为10个。
- **索引的增删改查**
  在一个系统中商品的信息必然不会是一成不变的，所以我们的索引文件就不可避免的需要按照商品信息去做调整，whoosh同样给我们提供了这样的接口。
  - 增：
    ```python
    from whoosh.index import open_dir
	def add_index(name, id):
    """
    新增索引
    :param name: 商品名称  type: str
    :param id: 商品id  type: str
    :return: None
    """
    ix = open_dir("index")
    writer = ix.writer()
    writer.add_document(
        id=id,
        content=name
    )
    writer.commit(optimize=True)
    ```
     索引的增加和创建索引只有稍许不同，在`commit`中增加了`optimize`参数，翻看whoosh的文档在Merging Segments中提到了两个参数分别是`merge`和`optimize`，在默认情况下`merge`为True，意味着whoosh会将多个segments文件合并到一个文件中，如果`merge`为False的时候我们提交commit的时候会重新生成一个单独的索引文件，多个索引文件不会对搜索的结果产生很大的差异，如果过多的存在索引会降低整体的查询速度。通常情况下使用whoosh的合并算法将多个文件合并到一个文件中会更好，这只会让在更新索引的速度变慢，用户查询的速度影响较小，这样的用户体验会更好。
   - 删:
	    ```python
	    from whoosh.index import open_dir
	    
		def add_index(name, id):
		    """
		    新增索引
		    :param name: 商品名称  type: str
		    :param id: 商品id  type: str
		    :return: None
		    """
	    	ix = open_dir("index")
	    	writer = ix.writer()
	    	writer.add_document(
	        	id=id,
	        	content=name
	    	)
	    	writer.commit(optimize=True)
	    ```
		whoosh总共有两种删除方式
		- `delete_by_query(query)`：删除与给定查询匹配的所有文档。
		- `delete_by_term(fieldname, termtext)`根据字段删除指定的文档，这里的字段需要在创建schema时指定为unique
	- 改
	  ```python
	  from whoosh.index import open_dir

	  def update_index(name, id):
    	"""
    	更新索引文件
    	:param name: 商品名称  type: str
    	:param id: 商品id  type: str
    	:return: None
    	"""
    	ix = open_dir("index")
    	writer = ix.writer()
    	writer.update_document(
        	id=id,
        	content=name
    	)
    	writer.commit()
		```
		和删除操作一样索引字段中需要有一个unique

#### 总结
---
整个功能算是比较简单的了，各种库都给了对应的接口，很够很方便的实现功能。在实现的过程中也遇到了一个问题，最开始在实现增删改查功能的时候使用的事`create_in`来打开索引文件，这样导致操作完成之后之前的数据被覆盖了，还是自己当初粗心没有仔细看文档导致的。以后要注意这个问题。
