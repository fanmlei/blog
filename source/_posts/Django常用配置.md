<h3>配置MySQL连接</h3>

<p>setting.py中的数据库配置：</p>

<pre class="has">
<code class="language-python">DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'oa',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}</code></pre>

<p>然后需要在项目__init__.py中添加将，pymysql作为默认的驱动库</p>

<pre class="has">
<code class="language-python">import pymysql
pymysql.install_as_MySQLdb()</code></pre>

<h3>从已有的数据库中导入结构：</h3>

<p>命令行中输入python manage.py inspectdb &gt; appname/models.py</p>

<h3>允许跨域请求：</h3>

<pre class="has">
<code class="language-python">

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
</code></pre>

<h3>设置中国时区：</h3>

<pre class="has">
<code class="language-python">LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False</code></pre>

<p> </p>