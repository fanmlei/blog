---
title: Django使用邮箱进行验证操作的实现方法
date: 2018-05-24 19:42:49
categories: 
- Django
tags:
- 登录
- 邮箱
---
上一篇博客简单的说了说Django发送邮件的方法，这一篇仅仅谈一下如何通过邮件的方式进行验证，以重置密码功能为例。

其实验证方法比较简单，只需要发送指定的链接给目标邮箱，用户点击链接即可通过验证，但是合成和验证这个指定的链接需要我们来处理，我用到的方法是，当用户申请邮箱验证的时候根据其邮箱地址和一个32位随机验证码去合成一个连接，当正常访问的使用后台可通过URL获取邮箱名以及验证码，再根据这两个值去数据库中匹配，看能否成功，若是成功则完成验证失败则提示用户链接无效，接下来是具体的实现方法

首先我们需要建立一张数据库表，其中内容包括：邮箱地址、32位随机验证码、创建时间。
```python
class email_reset(models.Model):
    email_address = models.EmailField(null=False,unique=True) #邮箱地址唯一的
    vc_code = models.CharField(max_length=64,null=False) #随机验证码
    send_time = models.DateTimeField(auto_now=True)  #邮箱发送时间</code></pre>
```
当用户需要用到邮箱验证的时候，则往数据库中新建一条数据之后在将邮箱地址和随机验证码合成为连接发送给目标
```python
def send_email(email_address):
    vc_code = vc_code_generator()
    msg = '<h2>重置密码</h1>'\
          '<h6>如果不是你本人操作请忽略本消息,本条消息30分钟内有效,如果被禁止跳转请复制链接在浏览器中重新打开</h6>'\
          '<a href="http://localhost:8000/iot/resetpwd/?email=%s&code=%s">点击重置密码</a>' % (email_address,vc_code)
    u = models.email_reset.objects.filter(email_address=email_address).first()
    if u :
        models.email_reset.objects.filter(email_address=email_address).update(vc_code= vc_code)
    else:
        models.email_reset.objects.create(email_address=email_address,vc_code=vc_code)
    send_mail('重置密码', '请前往这个网址：localhost:8000/forgetpwd重置密码', "*****管理员<****************@163.com>",
              [email_address], fail_silently=False, html_message=msg)
 
#生成随机验证码
def vc_code_generator(size=32, chars=string.ascii_uppercase + string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
```

接下来则是处理URL了，根据之前发送的链接格式我们可以通过GET方式获取到其邮箱地址和验证码，再从数据库中查询是否有从 稍作简单的判断即可知道当前
```python
if request.method == "GET":
    email = request.GET.get("email")
    code = request.GET.get("code")
    if email and code:
        if models.email_reset.objects.filter(email_address=email).filter(vc_code=code):
            return render(request,'../templates/website/reset.html',{'email':email})
        else:
            return HttpResponse("<h1>抱歉你访问的网址有误</h1>")
    else:
        return HttpResponse("<h1>抱歉你访问的网址有误</h1>")
```
