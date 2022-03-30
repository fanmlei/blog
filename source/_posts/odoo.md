---
title: Odoo
date: 2021-04-07 02:21:08
categories: 
- Odoo
tags:
- 后端
- odoo
---

### Odoo的配置项
---
odoo生成配置文件：./odoo-bin -s -c <保存路径>

odoo使用指定的配置文件进行加载 ./odoo-bin -c <配置文件的路径>

odoo脚手架工具-创建简单的模块 ： ./odoo-bin scaffold module-name save-path

odoo的addons路径在命令行中是相对路径，配置文件中为绝对路径
<!--more-->
### odoo模块的基本文件结构：
---
- controllers：网页控制器
- demo：测试数据
- models：模型结构
- security：权限安全相关的文件
  - ir.model.access.csv：控制访问权限
    - id：外部标识符
    - name：描述性标题
    - model_id：model的名称（对应model的\_name值，具体的值为model\_+（\_name的值，将.更换成_）
    - group_id：指明授权的安全组
    - perm_read：是否可读
    - perm_write：是否可写
    - perm_create：是否可新建
    - perm_read：是否可删除
- views ：视图文件
- \_\_init\_\_.py：模块初始化
- \_\_manufest\_\_.py: 模块的配置和介绍：
  - name：模块名称
  - summary：模块副标题
  - description：模块描述
  - author：模块作者
  - category：功能性分类字符串
  - version：版本号
  - depends：模块依赖
  - data：安装或更新时需要加载的模块列表
  - application：是否在应用列表种以APP形式展现
  - demo：测试数据的文件路径


### 一个简单的APP
---



### Odoo模块继承
---

### Odoo-模型
---
**模型的属性：**
- _name：我们创建模型的内部标识，必填属性。（一般来说命名规则是以点连接小写单词，模型名必须全局唯一）
- _description：模型的别称，让用户可以更好的记录，选填属性。
- _inherit
- _inherits
- _order：设置浏览模型记录或者列表视图时的默认排序，对应SQL语句中的order by的值
- _rec_name：指定关联字段引用描述，默认使用name字段。
- _table：模型对应数据库中的表名。
- _log_access=False：用于设置不自动创建审计追踪的字段：create_uid, create_date, write_uid, write_date.
- _auto=False： 设置不自动创建模型对应的数据表，这样设置之后可通过init()方法创建数据库对象。

**模型的常用字段：**
- Char(string,size,translate,trim)：单行文本，size设置最大长度，translate使字段内容可翻译，trim默认为True去除空格
- Text(string)：多行文本
- Selection(selection, string)：下拉选项，选项参数为元组列表第一个元素是数据库存储的值，第二个值为界面的显示内容。
- Html(string)：针对HTML内容的特殊处理。
- Integer(string)：整数类型
- Float(string,digits)：浮点型，digits指定字段的精度，是一个元组(x,y)，x为总长度，y为小数位。
- Monetary(string,currency_field)：货币类型，与浮点型类似，currency_field用于存储使用的货币种类，默认使用currency_id字段。
- Date(string)：日期字段（没有时分秒）
- Datetime(string)：日期字段（包含时分秒信息）
- Boolean(string)：bool类型，只能为True和False
- Binary(string)：存储二进制数据。

**字段的常见属性：**
- string：字段的标签名，会在页面中显示，如果不设置默认使用字段名
- default：设置字段的默认值，可以是具体值，也可以是调用、引用、函数、匿名函数等
- help：界面中鼠标悬停时的提示文本
- readonly=True：在界面中不可编辑
- required=True：使字段为必填的不可为空值
- index=True：建立索引
- copy=False：使用ORM的copy方法时忽略该字段
- groups：限制字段仅对一些组可见，值为逗号分隔的安全组XML ID列表
- states:
- deprecated=True：字段在被使用的时候会记录一条warning日志
- oldname

**特殊的字段：**

Odoo的ORM保留字段，除id字段外，下面的字段只要在模型中没有设置_log_access=False都会自动创建。
- create_uid：创建记录的用户
- create_date：创建记录的时间
- write_uid：最后写入记录的用户
- write_date：最后写入记录的日期
- name(Char类型)：默认作为记录的显示名称
- active(Boolean类型)：允许是否关闭记录
- state(Selection类型)：记录生命周期的基本状态，允许使用states字段属性来根据记录状态以具备不同的UI行为
- parent_id(Integer类型)：父子层级关系
- parent_path(Char类型)：父子层级关系

**模型间的关系**

以图书、出版社、作者为例。
- **many-to-one:**<br>
   many-to-one关联是对其他模型记录的引用，基本的使用：
    ```python
    publisher_id = fields.Many2one('res.partner', string='Publisher')
    ```
    第一个位置参数是关联模型（`comodel`关键字参数），第二个位置参数为字段标签（`string`关键字参数）
    - `ondelete`关键字参数：定义关联记录被删除时的操作：
       - set nulll(默认值)：关联字段被删除时置为空
       - restricted：抛出错误阻止删除
       - cascade：关联记录被删除的时候同时删除当前记录
    - `context`：
    - `domain`：
    - `auto_join=True`：允许ORM在使用关联进行搜索的时候使用SQL连接，使用时会跳过访问安全规则，用户可以访问安全规则不允许访问的关联记录，可以加快SQL的查询效率。
    - `delegate=True`：创建一个关联记录的代理继承，使用时必须设置`required=True`和`ondelete=cascade`
- **one-to-many:**<br>
  one-to-many关联是many-to-one的反向关联
  ```python
  published_book_ids = fields.One2many(
        'library.book', 
        'publisher_id',
        string='Published Books')
  ```
  三个参数分别是关联模型、被引用的字段名、字段标签，其他的参数和many-to-one相同，（context、domain、ondelete只用于关联中的many一方）
- **many-to-many：**<br>
  在两端都存在to-many关联的时候就可以使用many-to-many关联：
  ```python
  # Book model
  author_ids = fields.Many2many('res.partner',string="Authors")
  # Partner model
  book_ids = fields.Many2many('library.book', string='Authored Books')
  ```
  Many2many最少要包含一个关联模型位置参数（comodel\_name关键字参数），在数据库层面上many-to-many关联不会在已有的表中添加任何列，而是自动创建一个关联表来存储记录间的关联，和django的多对多一样的关联表中仅有两个ID字段，为两张关联表的外键，默认的关联表名由两个表名中间加下划线并在最后加上`\_rel`组成<br>
  在默认情况下有可能会出现表名长度过长，超出Postgresql数据库63个字符的上限，这时候我们可以选择手动模式，指定关联表<br>
  **使用手动方式设置关联表**
  ```python
  # 使用位置参数的方式：
  author_ids = fields.Many2many(
    'res.partner', # 关联模型（必填）
    'library_book_res_partner_rel', # 要使用的关联表名
    'a_id', # 本记录关联表字段
    'p_id', # 关联记录关联表字段
    'Authors') # string标签文本
  # 使用关键字参数的方式：
  author_ids = fields.Many2many(
    comodel_name='res.partner', # 关联模型(必填)
    relation='library_book_res_partner_rel', # 关联表名
    column1='a_id', # 本记录关联表字段
    column2='p_id', # 关联记录关联表字段
    string='Authors') # string标签文本
  ```
**使用引用字段的弹性关联：**<br>
  普通关联字段指定固定的引用模型，但是Reference字段可不受限，支持弹性关联，例如：
  ```python
  highlighted_id = fields.Reference(
      [('library.book',Book),('res.partner','Author')] , # [(model, id),()]
      'Category Highlight'
  )
  ```
  用户可以在操作界面中选择模型，然后选择模型中的记录

**计算字段：**<br>
  字段值除了普通的读取数据库存储外，还可以实现函数计算，计算字段和普通的字段相似，只是增加了一个额外的compute参数来定义用于计算的函数
  ```python
  publisher_country_id = fields.Many2many(
      'res.country', string="publisher Country",
      compute='_compute_publisher_country'
  )
  @api.depends('publisher_id.country_id')
  def _compute_publisher_country(self):
      for book in self:
          book.publisher_country_id = book.publisher_id.country_id
  ```
  compute的值为定义的计算函数名，如果计算函数需要使用其他字段就需要使用`@api.depends`装饰器，参数为一个或多个字段名。
  - 搜索和写入计算字段<br>
    上面简单的例子只能读取，还不能搜索和写入，默认情况下计算字段是实时计算，不会存储到数据库中，如果需要写入数据库可以通过现实特殊的方法来开启搜索和写入的操作，计算字段可预compute方法一起设置实现搜索逻辑的search方法，以及实现写入逻辑的inverse方法，例如：
    ```python
    publisher_country_id = fields.Many2many(
        'res.country', string='Publisher Country',
        compute = '_compute_publish_country',
        inverser = '_inverser_publish_country',
        search = '_serach_publish_country'
    )
    
    def _inverse_publisher_country(self):
        for book in self:
            book.publisher_id.country_id = book.publisher_country_id
            
    def _search_publisher_country(self, opearator, value):
        return [('publisher_id.country_id', operator, value)]
    ```
    计算字段的写入是计算的反向逻辑
    
**存储计算字段：**<br>
   通过在定义时设置`store=True`还可以将计算字段值保存到数据库中。在任意依赖变更时值就会重新计算。因为值已被存储，所以可以像普通字段一样被搜索，也就不需要使用search方法了。
   
**关联字段：**<br>
   创建关联字段的时候，我们像普通计算字段一样声明一个所需字段类型，使用related属性设置用点号标记链来使用所需的字段，可以使用引用字段来获取与上例publisher_country_id计算字段相同的效果：
   ```python
   publisher_country_id = fields.Many2one(
       'res.country', string='Publisher Country',
        related='publisher_id.country_id',
    )
   ```
   本质上关联字段仅仅是快捷实现`search`和`inverse`方法的计算字段。也就是说可以直接对其进行搜索和写入，而无需书写额外的代码。默认关联字段是只读的，因inverse写操作不可用，可通过readonly=False字段属性来开启写操作。

**模型约束：**
- SQL模型约束：<br>
  SQL约束加在数据表定义中，并由Postgresql直接执行，使用_sql_constraints类属性来定义，值一般是一个由元组组成的列表，每个元组格式为(name,code,error):
  - name:约束标识名
  - code:SQL语句
  - error:是在约束验证为通过时向用户显示的错误信息
```python
_sql_constraints = [
        ('library_book_name_date_uq', # 约束唯一标识符
        'UNIQUE (name, date_published)', # 约束 SQL 语法
        'Book title and publication date must be unique'), # 消息
        ('library_book_check_date',
        'CHECK (date_published <= current_date)',
        'Publication date must not be in the future.'),
    ]
```
- Python模型约束：<br>
  Python约束可以自定义代码来检查条件。检查方法应添加@api.constrains装饰器，并且包含要检查的字段列表，其中任意字段被修改就会触发验证，并且在未满足条件时抛出异常。
```python
@api.constrains('isbn')
def _constrain_isbn_valid(self):
    for book in self:
        if book.isbn and not book._check_isbn():
            raise ValidationError('%s is an invalid ISBN' % book.isbn)
```
**base模型**

Odoo自带有base插件，提供了Odoo应用所需的基本功能，base模块中包含两类模型：
- ir模型：信息仓库，存储Odoo所需的数据
  - ir.actions.act_window：用于窗口操作
  - ir.ui.menu：用于菜单选项
  - ir.ui.view：用于视图
  - ir.model：用于模型
  - ir.model.fields：用于模型字段
  - ir.model.data：用于XML ID
- res模型：资源，包含基本数据
  - res.partner：用于业务伙伴，如客户、供应商和地址等等
  - res.company：用于公司数据
  - res.currency：用于货币
  - res.country：用于国家
  - res.users：用于应用用户
  - res.groups：用于应用安全组


### 使用模型数据
---
shell命令行工具：./odoo-bin shell -d dbname

- 环境属性：
  - env.cr：正在使用的数据库游标
  - env.user： 当前用户的记录
  - env.uid：会话用户ID，与env.user.id相同
  - env.context：会话上下文的不可变字典
  
环境提供了对所有已安装模型注册表的访问，如self.env['res.partent']返回一条对partner模型的引用，然后可以使用`search()`或`browse()`方法来获取记录集。

- 环境上下文：<br>
  环境上下文是一个带有会话数据的字典，用于客户端用户界面以及ORM和业务逻辑中，在客户端中可以把信息从一个视图带到另一个视图，在服务器端中一些记录集的值会依赖与上下文提供多的本地化设置，也可为服务端代码提供信号。
- 修改记录集执行环境：<br>
  记录集执行环境是不可变的，如果想要修改可以创建一个变更环境并使用它来执行操作。




### 业务逻辑的处理
---



















### 其他问题
- 增加字段出现问题<br>
  修改类似与res.partner这种基础表的结构需要先使用命令更新数据库方可运行
    ```shell
    ./odoo-bin -d database_name  -u module_name
    ```
- 第一次运行使用命令
  ```shell
   ./odoo-bin --addons-path=addons,./odoo/addons --ddatabase=scm_erp -i base
  ```
  
- 创建模块
  ```shell
   ./odoo-bin scaffold purchase_separate my_addons
  ```


odoo的api修饰符
- @api.returns
- @api.one：自动遍历记录集，self会变成当前的记录集（类似于一个for循环的遍历）
- @api.multi：不遍历，self保持为当前的记录集
- @api.model：将旧的API函数转换为带有新API函数，使得代码可以平滑迁移
- @api.constrains：被修饰函数会在create、write、unlink时被调用
- @api.depends：添加依赖字段
- @api.onchange
- @api.noguess