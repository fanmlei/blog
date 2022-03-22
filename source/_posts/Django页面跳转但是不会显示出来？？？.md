---
title: Django页面跳转但是不会显示出来？？？
date: 2018-12-14 19:42:49
categories: 
- Django
tags:
- bug
---
一脸懵逼，点击登录，如果错了会有提示，但是登录成功了后台会显示跳转到dashboard上，也能正常获取到cookie，但是就是页面不会变化，单独访问dashboard也是正常的。
问题代码如下：
```python
# login   

class Login(View):
    '''
    用户登录
    '''
    def get(self, request):
        return render(request, 'website/signin.html')

    def post(self, request):
        res = {'status': 'succ'}
        user_name = request.POST.get("name", None)
        password = request.POST.get("password", None)
        u = models.WebsiteUserinfo.objects.filter(username=user_name).first()
        if not u:
            res['status'] = '用户名错误'
        else:
            if password == u.password:
                # re = render(request,'website/dashboard.html')
                re = redirect('/oa/dashboard')
                re.set_cookie('is_log', True)  # 设置cookie
                re.set_cookie('username', user_name)
                return re
            else:
                res['status'] = '密码错误'
        return HttpResponse(json.dumps(res), content_type="application/json")


#  dashboard

class Dashboard(View):
    '''
    主页
    '''
    def get(self, request):
        print(request.COOKIES['username'])
        return render(request, '../templates/website/dashboard.html', {'auth': '1234'})



#  路由配置

from django.conf.urls import url,include
from django.contrib import admin
from website import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.init),
    url(r'^oa/', include('website.urls')),
]


from django.conf.urls import url
from website import views
urlpatterns = [
    url(r'^dashboard', views.Dashboard.as_view()),
    url(r'^realtime_table', views.RealTimeTable.as_view()),
    url(r'^everyday_table', views.EveryDayTable.as_view()),
    url(r'^login', views.Login.as_view()),
]
```
后台输出：
![](1.png)

解决问题
注意力一直放在后台上了，之前是通过session保存用户状态的，现在需要改为cookie验证，如果要设置cookie返回类型必须为render，redirect，因此就将原来登录成功返回json改为了redirect，但是没有想到的是前端是通过Ajax发送消息的，无法识别返回类型，就导致了登录成功了却没有反应。总结来说是一个很、非常、超级低端的问题，只怪自己想当然的修改。

还是返回json格式，让js去设置cookie

```javascript
function login() {
    $.ajax({
        type: "POST",//方法类型
        dataType: "json",//预期服务器返回的数据类型
        url: "/oa/login",//url
        data: $('#login_form').serialize(),
        success: function (data) {
            if (data['status'] != "succ"){
                alert(data['status']);
            }
            if (data['status'] == "succ"){
                var name = document.getElementById('u1').value;
                document.cookie="is_log=True;";
                document.cookie="username="+name;
                window.location.href='/oa/dashboard';
            }
        }
    });
}
```
