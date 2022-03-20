之前做过一个jieba+whoosh的商品搜索功能，后来发现Postgresql数据库自带有全文检索的功能，那么就尝试使用Postgresql的全文检索功能来实现一次
### postgresql配置
- 环境：Ubuntu16.04
- 版本：v9.5
---
- 外部远程访问：
数据库配置文件路径为 `/etc/postgresql/9.5/main`需要修改的配置文件为postgresql.conf和pg_hba.conf
  - `postgresql.conf`（这个文件是数据库的配置文件）
  `#listen_addresses='localhost'` 修改为 `listen_addresses='*'`
  - `pg_hba.conf`（这个文件是数据库的连接配置文件）
  在最后添加一行：`host    all    all    0.0.0.0/0    md5`（意思就是允许任何用户从任何IP访问任何数据库，加密方式为MD5）
  - 重启服务：`sudo service postgresql restart`
- 插件路径：`/usr/share/postgresql/9.5/extension`

### zhparser插件的安装
---
postgresql的本身分词并不支持中文，所以需要使用其他的插件实现中文分词的功能，在这里采用的是zhparser+scws，具体的介绍可以看github主页。
- 下载zhparser源码：<br>
  ```git
  git clone https://github.com/amutu/zhparser.git
  ```
- 安装SCWS：<br>
  ```shell
  wget http://www.xunsearch.com/scws/down/scws-1.2.3.tar.bz2
  tar xvjf scws-1.2.3.tar.bz2
  cd scws-1.2.3
  ./configure
  make install
  ```
- 安装zhparser：<br>
  ```shell
  cd zhparser
  make && make install
  # 如果安装报错请先安装相关的库和头文件
  # sudo apt-get install postgresql-server-dev-9.5
  # sudo apt-get install postgresql-common
  ```
- 配置zhparser扩展：<br>
  ```sql
  # 连接至目标数据库后
  CREATE EXTENSION zhparser;
  # 这里如果报错：ERROR:  could not open file "/usr/share/postgresql/9.5/tsearch_data/qc_dict_demo_1.txt" for writing: Permission denied
  # 在那个目录下没有找到这个文件,最后手动创建了那个文件
  # 将zhparser解析器作为全文检索配置项
  CREATE TEXT SEARCH CONFIGURATION chinese (PARSER = zhparser);
  ALTER TEXT SEARCH CONFIGURATION chinese ADD MAPPING FOR n,v,a,i,e,l,j WITH simple;
  ```
  安装完成后使用`\dFp`查看是否安装成功。
  
### 简单的使用
---
```sql
SELECT * FROM table WHERE to_tsvector('chinese', name) @@ to_tsquery('chinese', '小米Pro');
```
插件装好后好像并不需要我们编写代码了，一个简单的SQL语句就实现了之前的功能。那么如果你使用的是Postgresql数据库推荐使用自带的全文检索功能去实现。
