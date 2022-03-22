---
title: Django常用配置
date: 2018-05-01 10:20:45
categories: 
- Django
tags:
- 邮箱
---

配置MySQL连接
```python
# setting.py中的数据库配置：
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'oa',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

然后需要在项目__init__.py中添加将，pymysql作为默认的驱动库
```python
import pymysql
pymysql.install_as_MySQLdb()
```

从已有的数据库中导入结构
命令行中输入python manage.py inspectdb > appname/models.py

允许跨域请求
```python

INSTALLED_APPS = [
    
    'corsheaders',
    
]

MIDDLEWARE = [
    
    'corsheaders.middleware.CorsMiddleware',
]
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
   "*"
)
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)
```

设置中国时区
```
LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False
```