---
title: Django发送邮件
date: 2018-05-21 10:20:45
categories: 
- Django
tags:
- 邮箱
---
Django提供了发送邮件的接口，仅需做简单的设置即可实现发送邮件的功能。
首先需要在setting做简单的配置，以163邮箱为例：
```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com' 
EMAIL_PORT = 25
EMAIL_HOST_USER = '****' # 帐号
EMAIL_HOST_PASSWORD = '****'  # 密码
DEFAULT_FROM_EMAIL = "*******" #默认发送名
```
下面是官网的一个示例：
```python
from django.core.mail import send_mail

send_mail('Subject here', 'Here is the message.', 'from@example.com',
    ['to@example.com'], fail_silently=False)
```
自定义一个测试的URL地址，传入相应的参数即可成功发送邮件
![](1.png)

如果是放在云服务器上运行的时候需要注意25号端口有没有被禁用，有些服务商会将25号端口默认禁用，需要解禁后才能使用