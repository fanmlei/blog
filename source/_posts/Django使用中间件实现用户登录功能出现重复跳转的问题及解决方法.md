<p>先看一下出错的代码</p>

<pre class="has">
<code class="language-python"># 中间件
class AuthMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        print(request.path)
        print(request.session.get('is_log'))
        if request.path != '/oa/login':
            if request.session.get('is_log'):
                return redirect('/oa/dashboard')
            else:
                return redirect('/oa/login')
        else:
            return</code></pre>

<p> </p>

<pre class="has">
<code class="language-python"># view
class Login(View):
    def get(self, request):
        return render(request, 'website/signin.html')

    def post(self, request):
        res = {'status': 'succ'}
        user_name = request.POST.get("name", None)
        password = request.POST.get("password", None)
        re_log = request.POST.get("remember", None)
        if user_name == 'root' and password == '123':
            # 设置session
            request.session['user'] = user_name
            request.session['is_log'] = True
            # 如果选择记住状态则保持一周的session信息
            if re_log == 1:
                request.session.set_expiry(1209600)
            res['status'] = 'succ'
        else:
            res['status'] = '密码错误'
        return HttpResponse(json.dumps(res), content_type="application/json")


class Dashboard(View):
    def get(self, request):
        db = DataBase()
        data = db.dashboard()
        return render(request, 'website/dashboard.html', {'data': data})
       </code></pre>

<p>访问效果：<br /><img alt="" class="has" height="300" src="https://img-blog.csdn.net/20180720102424649?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="530" /><br />
登录成功之后一直出现重复的跳转问题。</p>

<p>我们在来重新审视一下代码：<br />
首先我们登录成功之后访问/oa/dashboard这个页面，然后在中间间的处理过程中由于第一个if判断和第二个if判断都满足导致再次跳转到oa/dashboard页面一直重复。而且在访问其他页面的时候依然是一直跳转dashboard这个页面的，逻辑有误。</p>

<p>解决方法：在验证用户登录之后的session之后直接return掉而不是进行跳转。</p>

<pre class="has">
<code class="language-python">class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.path != '/oa/login':
            if request.session.get('is_log'):
                return
            else:
                return redirect('/oa/login')
        else:
            return</code></pre>

<h2>之前逻辑没看清，现在突然发现这个问题好傻逼<br />
 </h2>