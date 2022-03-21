<h3>中间件执行流程</h3>

<p>django的中间件是一个轻量级的插件，可以改变django的输入和输出，中间件共有5种方法，分别为：</p>

<ul><li>process_request(self,request)</li>
	<li>process_view(self, request, callback, callback_args, callback_kwargs)</li>
	<li>process_template_response(self,request,response)</li>
	<li>process_exception(self, request, exception)</li>
	<li>process_response(self, request, response)</li>
</ul><p>前两个方法 都是自上而下的执行每个中间件，后面的三个都是反着来的<br /><img alt="" class="has" height="645" src="https://img-blog.csdnimg.cn/20181128012607646.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70" width="1164" /></p>

<p> </p>

<h3>CSRF验证</h3>

<p>django的CSRF是基于中间件来实现的，而且是放在中间件中的view方法中，原因是：django的中间件是作用于全局的，但是某些情况某个函数可能不需要用到CSRF验证，所以在执行路由匹配的时候找到视图函数，看看他是否需要用到CSRF认证，如果不需要则会跳过CSRF。</p>

<p>免除认证的方法：</p>

<pre class="has">
<code class="language-python"># FBV
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def test(request):
    pass

# 在CBV的方式中，单独给某个方法通过装饰器来免除是无效的，需要加到dispatch函数上面

# 方法1
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
class Test1(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        ret = super(Test1,self).dispatch(request, *args, **kwargs)
        return ret

# 方法2
@method_decorator(csrf_exempt,name='dispatch')
class Test2(APIView):
    pass

</code></pre>

<p>单独想用CSRF的方法：</p>

<pre class="has">
<code class="language-python"># 1.去掉setting中CSRF中间件
from django.views.decorators.csrf import csrf_protect
@csrf_protect
def test(request):
    pass</code></pre>

<p> </p>

<p> </p>

<p> </p>