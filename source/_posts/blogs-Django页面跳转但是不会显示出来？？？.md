<p>一脸懵逼，点击登录，如果错了会有提示，但是登录成功了后台会显示跳转到dashboard上，也能正常获取到cookie，但是就是页面不会变化，单独访问dashboard也是正常的。<br />
问题代码如下：</p>

<pre class="has">
<code class="language-python"># login   


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
]</code></pre>

<p>后台输出：<br /><img alt="" class="has" height="99" src="https://img-blog.csdn.net/20180830100235311?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="685" /></p>

<p> </p>

<h1><span style="color:#f33b45;"><strong>解决问题：</strong></span></h1>

<p><span style="color:#f33b45;">注意力一直放在后台上了，之前是通过session保存用户状态的，现在需要改为cookie验证，如果要设置cookie返回类型必须为render，</span><span style="color:#f33b45;">redirect，因此</span><span style="color:#f33b45;">就将原来登录成功返回json改为了</span><span style="color:#f33b45;">redirect，但是没有想到的是前端是通过Ajax发送消息的，无法识别返回类型，就导致了登录成功了却没有反应。总结来说是一个很、非常、超级低端的问题，只怪自己想当然的修改。</span></p>

<p><span style="color:#f33b45;">还是返回json格式，让js去设置cookie</span></p>

<pre class="has">
<code class="language-javascript">function login() {
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
    }</code></pre>

<p> </p>