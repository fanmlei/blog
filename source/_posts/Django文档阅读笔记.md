---
title: Django文档阅读笔记
date: 2020-12-07 02:21:08
categories: 
- Django
tags:
- 后端
---
## 模型（Model）

#### 字段

- null和blank的区别

  null和blank默认都是为false的，不能为空，而null是数据库层面的不为空，blank则会影响form验证（blank=True表单验证的时候可以为空，blank=False表单验证不能为空）
<!--more-->
- choice

  choice参数值为列表或元组，可以通过`get_FOO_display()`方法获取其显示的值

  ```python
  from django.db import models
  
  class Person(models.Model):
      SHIRT_SIZES = (
          ('S', 'Small'),
          ('M', 'Medium'),
          ('L', 'Large'),
      )
      name = models.CharField(max_length=60)
      shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)
    
  
  >>> p = Person(name="Fred Flintstone", shirt_size="L")
  >>> p.save()
  >>> p.shirt_size
  'L'
  >>> p.get_shirt_size_display()
  'Large'
  ```

- primary_key

  在Django的一个模型中必须有一个主键字段，如果没有设置过primary_key = True，Django会自动创建一个自增的字段作为主键

  ```python
  id = models.AutoField(primary_key=True)
  ```
- related_name

    ForeignKey 的 related_name 可以为反向关系定义一个有意义的名称
 
    ```python
    class Company:
        name = models.CharField(max_length=30)

    class Employee:
        first_name = models.CharField(max_length=30)
        last_name = models.CharField(max_length=30)
        company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')
    ```
    上面代码意味着， Company 有一个employees特殊属性, 该属性将返回一个 QuerySet，其中包含与此公司相关的所有员工实例
    ```python
    google = Company.objects.get(name='Google')
    google.employees.all()
    ```
    你也可以通过反向关系， 来更新Company的employees字段.
    ```python
    vitor = Employee.objects.get(first_name='Vitor')
    google = Company.objects.get(name='Google')
    google.employees.add(vitor)
    ```
- related_query_name

  这种关系也是用于查询过滤器， 比如我们要查询雇佣名为「Vitor」的所有公司:

  ```python
    companies = Company.objects.filter(employee__first_name='Vitor')
  ```
  如果你想自定义此关系的查询名称可以这样
  ```python
    class Employee:
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='employees',
        related_query_name='person'
    )
  ```
  然后这样查询
  ```python
  companies = Company.objects.filter(person__first_name='Vitor')
  ```

#### Meta选项

- app_label：string

  定义APP名称（模型不是在APP中定义的，需要声明）

- db_table：string

  自定义数据库表名

- ordering：[string, ]

  对象的默认排序，参数值为包含字段名的列表， 其中如果字段名前缀加了`-` 为降序，否则为升序

- managed：Boolean

  默认为True，Django会在迁移过程中创建或删除数据库表，如果为False时则不会执行数据库表创建或删除操作，（如果模型中包含多对多的关联字段则不会创建多对多联接中间表，但是托管模型和非托管模型之间的中间表，想要修改这个行为需要将中间表设为自定义模型）

- order_with_respect_to: string

  可用于使相关对象相对于父对象可排序，**需要注意的是不能和ordering一起使用**  例如问题和回答的排序。

  ```python
  from django.db import models
  
  class Question(models.Model):
      text = models.TextField()
      # ...
  
  class Answer(models.Model):
      question = models.ForeignKey(Question, on_delete=models.CASCADE)
      # ...
  
      class Meta:
          order_with_respect_to = 'question'
  
  # 提供两个默认的方法来设置相关对象的顺序
  # 1.get_RELATED_order() 返回包含相关对象的主键列表
  >>> question = Question.objects.get(id=1)
  >>> question.get_answer_order()
  [1, 2, 3]
  # 2.set_RELATED_order() 通过传入主键列表来设置排序结果
  >>> question.set_answer_order([3, 1, 2])
  # get_next_in_order() get_previous_in_order() 获取下一个、前一个对象
  >>> answer = Answer.objects.get(id=2)
  >>> answer.get_next_in_order()
  <Answer: 3>
  >>> answer.get_previous_in_order()
  <Answer: 1>
  ```

- permission：[(permission_code, human_readable_permission_name),]

  Django会自动为每个模型创建添加，修改，删除和查看的权限，permission可以添加新的自定义权限

- default_permission: []

  默认权限

- required_db_features

  仅在某些功能（数据库的）打开的情况下同步

- required_db_vendor

  指定数据库类型，满足条件才会同步

- indexes

  指定模型上的索引列表

- unique_together: tuple(tuple)

  联合唯一

#### 管理器

