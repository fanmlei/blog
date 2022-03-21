<p>首先需要在APP目录下创建一个templatetags目录</p>

<p>然后在这个目录下新建一个任意名的.py文件 如 test.py</p>

<p>创建一个template对象register</p>

<p> </p>

<pre class="has">
<code class="language-python">from django import template
from django.utils.safestring import mark_safe

register =template.Library()</code></pre>

<p>下面在这个文件中我们就可以写自定义函数了</p>

<p>有两种方式</p>

<p>一种是simple_tag,这种会限制参数的个数，但是不能作为IF的条件来使用</p>

<p> </p>

<pre class="has">
<code class="language-python">@register.simple_tag
def add(a,b):
    return a+b</code></pre>

<p>一种是filter，这个最多只能传递两个参数，可作为if条件使用</p>

<pre class="has">
<code class="language-python">@register.filter
def subtract(a,b):
    return a-b</code></pre>

<p> </p>

<p> </p>

<p> </p>

<p>这时候就可以在模板文件中使用这个函数了</p>

<p>首先在开头位置导入test.py文件</p>

<p>simple_tag直接使用%来调用函数，如果函数需要传参数，需要在函数后直接添加即可（用空格隔开）</p>

<p> </p>

<pre class="has">
<code class="language-python">{% load test %}

{% add 2 3 %}

{{ 1|subtract:2 }}</code></pre>

<p><img alt="" class="has" src="https://img-blog.csdn.net/20180329183633434?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" /></p>

<p> </p>

<p> </p>

<p> </p>

<p> </p>

<p> </p>

<p>要注意的是app目录下的templatetags名不能更改 register也不能更改</p>

<p>还需要在settings里面注册这个app</p>

<p> </p>

<p> </p>

<p> </p>

<p> </p>