---
title: cookie和session
date: 2018-05-03 16:30:24
categories: 
- Django
tags:
- 网络
- Django
---
## cookie

cookie:客户端浏览器上的一个文件（键值对方式存储，类似于python中的字典），一般用于记录用户状态、和用户信息的，绝大多数的网站自动登录功能都是基于cookie实现的，下面使用Django实现一个用户登陆作为例子展示。<br>

首先是最简单的登录页面 login：
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<form action="/login/" method="post">
    <input type="text" name="username" placeholder="用户名">
    <input type="password" name="password" placeholder="密码">
    <input type="submit" value="提交">
</form>
</body>
</html>
```
login请求处理函数
```python
user_infp ={
    "fml":{"password":"123"}
}
 
def login(request):
    if request.method == "GET":
        return  render(request,"login.html")
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        dic = user_infp.get(u)
        if not dic:
            return render(request,"login.html")
        if dic["password"] == p:
            res = redirect('/index')
            res.set_cookie("username",u)
            return res
        else:
            return render(request,"login.html")
```
当请求为get方式的时候返回登录页面，为post方式的时候验证表单，这里只使用字典来简化从数据库验证的操作。当验证通过的时候跳转到index页面，并且设置一个cookie，内容为｛"username":username},否则任然返回当前页面。

index页面：仅仅用来显示登录的用户名
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>欢迎{{ user }}</h1>
</body>
</html>
```
index处理函数：
```python
def index(request):
    user = request.COOKIES.get("username")
    if not user:
        return redirect('/login')
    else:
        return render(request,'index.html',{"user":user})
```
如果上面我们如果登录成功浏览器会存储一个cookie，当我们再次请求index页面的时候，同时发送过去的还有本地的cookie，所以可以从request中的cookie中获取我们已经存储的用户名，如果不存在则跳转到login页面，如果有登录信息则显示登录页面

以上是最简单的cookie使用，其实cookie还有很多其他的用法

```python
rep = HttpResponse(...) 或 rep ＝ render(request, ...)
 
rep.set_cookie(key,value,...)
rep.set_signed_cookie(key,value,salt='加密盐',...)
参数：
    key,              键
    value='',         值
    max_age=None,     超时时间
    expires=None,     超时时间(IE requires expires, so set it if hasn't been already.)
    path='/',         Cookie生效的路径，/ 表示根路径，特殊的：跟路径的cookie可以被任何url的页面访问
    domain=None,      Cookie生效的域名
    secure=False,     https传输
    httponly=False    只能http协议传输，无法被JavaScript获取（不是绝对，底层抓包可以获取到也可以被覆盖）
```

下面再来详细说一说各个参数的作用。<br>
首先是获取cookie，salt：这个参数的具体作用目前我还是不太清除，猜测是cookie加密操作，等我弄懂了再回来修改。<br>

接下来是设置cookie，key和value不用再说了，<br>
`max_age`: 设置超时时间以秒为单位，很多网站上登录页面都有多长时间免登录的功能一般都是通过这个来设置的，当超过了一段时间这个cookie就会失效<br>
`expires`: 同样是设置超时时间的，但是和上面的不太一样，这里的单位不是秒，而是datetime,所以就有两种超时时间的设置方法<br>

```python
#max_age方法
res.set_cookie("username",u,max_age=10)
#expires方法
import datetime
current_time = datetime.datetime.utcnow()
end_time = current_time + datetime.timedelta(seconds=10)
res.set_cookie("username",u,expires=end_time)
```
`path` :是指定cookie生效的路径，参数默认为 ' / ' 可被当前网站任意URL页面访问，下面我们重新写一个页面index1，内容和index相同

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>这里是index1欢迎{{ user }}</h1>
</body>
</html>
```

index1的处理函数

```python
def index1(request):
    user = request.COOKIES.get("username")
    if not user:
        return HttpResponse("没有获取到cookie")
    else:
        return render(request,"index1.html",{"user":user})
```

这里我们将login函数里面的cookie设置为
```
res.set_cookie("username",u,path='/index')
```
然后重新运行登录，这里就能看出在index可以正常获取到cookie，而index1获取不到，path设置成功。

`domain`: 设置生效域名，这里只能设置当前域名的子域名，无法给其他域名设置<br>


## session
和cookie不同的是session是保存在服务器端的键值对，session基于cookie来使用的，一般情况下本地的cookie会存储session中的key名，然后通过cookie中的key去获取服务器上存储的信息。
下面依然以用户登录作为最简单的示例：<br>
模板还是上面的那两个，这里只重写对应的处理函数
```python
user_infp ={
    "fml":{"password":"123"}
}
 
def login(request):
    if request.method == "GET":
        return  render(request,"login.html")
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        dic = user_infp.get(u)
        if not dic:
            return render(request,"login.html")
        if dic["password"] == p:
            res = redirect('/index')
            request.session['username'] = u
            request.session["is_login"] = True
            return res
        else:
            return render(request,"login.html")
 
def index(request):
    print(request.session["is_login"])
    if request.session["is_login"]:
        return render(request, 'index.html', {"user": request.session["username"]})
    else:
        return redirect('/login')
```
乍一看和cookie的操作类似，其实这是因为django为我们在后台做了很多工作，例如
```
request.session['username'] = u
request.session["is_login"] = True
```
这两句就很简单的完成了session的创建，实际上django首先生成了一串随机字符串用来作为key并将这个随机字符串保存到本地的cookie中，然后在将后面的两个内容以字典的形式存到服务器端，django中默认session存储在数据库中。
```
request.session["is_login"]:
```
这一步首先从cookie中回去对应的key，然后再从数据库中获取对应的value进行判断<br>
同样的session和cookie一样也有一些高级功能，例如设置超时时间<br>
```python
request.session.set_expiry(value)
* 如果value是个整数，session会在些秒数后失效。
* 如果value是个datatime或timedelta，session就会在这个时间后失效。
* 如果value是0,用户关闭浏览器session就会失效。
* 如果value是None,session会依赖全局session失效策略。
```

除了超时时间设置还有一下功能：
```python
# 获取、设置、删除Session中数据
request.session['k1']
request.session.get('k1',None)
request.session['k1'] = 123
request.session.setdefault('k1',123) # 存在则不设置
del request.session['k1']

# 所有 键、值、键值对
request.session.keys()
request.session.values()
request.session.items()
request.session.iterkeys()
request.session.itervalues()
request.session.iteritems()


# 用户session的随机字符串
request.session.session_key

# 将所有Session失效日期小于当前日期的数据删除
request.session.clear_expired()

# 检查 用户session的随机字符串 在数据库中是否
request.session.exists("session_key")

# 删除当前用户的所有Session数据
request.session.delete("session_key")
```

在django中session共有5种方式来存储：数据库、缓存、文件、缓存加数据库、加密cookie，但是都需要我们在settings里面设置，下面就是每种的配置方式
```python
#数据库配置
 
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # 引擎（默认）
 
SESSION_COOKIE_NAME ＝ "sessionid"  # Session的cookie保存在浏览器上时的key，即：sessionid＝随机字符串（默认）
SESSION_COOKIE_PATH ＝ "/"  # Session的cookie保存的路径（默认）
SESSION_COOKIE_DOMAIN = None  # Session的cookie保存的域名（默认）
SESSION_COOKIE_SECURE = False  # 是否Https传输cookie（默认）
SESSION_COOKIE_HTTPONLY = True  # 是否Session的cookie只支持http传输（默认）
SESSION_COOKIE_AGE = 1209600  # Session的cookie失效日期（2周）（默认）
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # 是否关闭浏览器使得Session过期（默认）
SESSION_SAVE_EVERY_REQUEST = False  # 是否每次请求都保存Session，默认修改之后才保存（默认）
 
#缓存配置
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'  # 引擎
SESSION_CACHE_ALIAS = 'default'  # 使用的缓存别名（默认内存缓存，也可以是memcache），此处别名依赖缓存的设置
 
SESSION_COOKIE_NAME ＝ "sessionid"  # Session的cookie保存在浏览器上时的key，即：sessionid＝随机字符串
SESSION_COOKIE_PATH ＝ "/"  # Session的cookie保存的路径
SESSION_COOKIE_DOMAIN = None  # Session的cookie保存的域名
SESSION_COOKIE_SECURE = False  # 是否Https传输cookie
SESSION_COOKIE_HTTPONLY = True  # 是否Session的cookie只支持http传输
SESSION_COOKIE_AGE = 1209600  # Session的cookie失效日期（2周）
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # 是否关闭浏览器使得Session过期
SESSION_SAVE_EVERY_REQUEST = False  # 是否每次请求都保存Session，默认修改之后才保存
 
#文件配置
SESSION_ENGINE = 'django.contrib.sessions.backends.file'  # 引擎
SESSION_FILE_PATH = None  # 缓存文件路径，如果为None，则使用tempfile模块获取一个临时地址tempfile.gettempdir()                                                            # 如：/var/folders/d3/j9tj0gz93dg06bmwxmhh6_xm0000gn/T
 
SESSION_COOKIE_NAME ＝ "sessionid"  # Session的cookie保存在浏览器上时的key，即：sessionid＝随机字符串
SESSION_COOKIE_PATH ＝ "/"  # Session的cookie保存的路径
SESSION_COOKIE_DOMAIN = None  # Session的cookie保存的域名
SESSION_COOKIE_SECURE = False  # 是否Https传输cookie
SESSION_COOKIE_HTTPONLY = True  # 是否Session的cookie只支持http传输
SESSION_COOKIE_AGE = 1209600  # Session的cookie失效日期（2周）
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # 是否关闭浏览器使得Session过期
SESSION_SAVE_EVERY_REQUEST = False  # 是否每次请求都保存Session，默认修改之后才保存
 
#缓存加数据库（数据库实现持久化，缓存提高效率）
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'        # 引擎
 
#加密Cookie
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'   # 引擎
```
