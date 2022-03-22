---
title: Django中间件执行流程和CSRF验证
date: 2020-09-24 16:42:49
categories: 
- Django
tags:
- CSRF
- web中间件
---

### 中间件执行流程
django的中间件是一个轻量级的插件，可以改变django的输入和输出，中间件共有5种方法，分别为
1. process_request(self,request)
2. process_view(self, request, callback, callback_args, callback_kwargs)
3. process_template_response(self,request,response)
4. process_exception(self, request, exception)
5. process_response(self, request, response)

前两个方法 都是自上而下的执行每个中间件，后面的三个都是反着来的
![](1.png)


### CSRF验证
django的CSRF是基于中间件来实现的，而且是放在中间件中的view方法中，原因是：django的中间件是作用于全局的，但是某些情况某个函数可能不需要用到CSRF验证，所以在执行路由匹配的时候找到视图函数，看看他是否需要用到CSRF认证，如果不需要则会跳过CSRF。

免除认证的方法：
```python
# FBV
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

```

单独想用CSRF的方法：
```python
# 1.去掉setting中CSRF中间件
from django.views.decorators.csrf import csrf_protect
@csrf_protect
def test(request):
    pass
```
