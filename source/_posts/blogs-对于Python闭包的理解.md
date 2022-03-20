<p>首先看一个面试中非常常见的题目</p>

<pre class="has">
<code class="language-python">def num():
    return [lambda x: x * i for i in range(4)]


print([ n(2) for n in num()])
</code></pre>

<p>先看一下num函数的作用，定义了一个匿名函数，返回传入参数乘以列表生成式的每一个元素，所以乍一看结果应该为[0,2,4,6]，如果这样想的话就落入陷阱了。这个题目考察的就是在python中闭包是延迟绑定的，当num()赋值给n的时候就已经完成for循环了，i已经等于3，所以到最后输出值都为 2 *3 也就是[6,6,6,6]</p>

<p> </p>

<p style="text-indent:50px;">闭包就是在一个外部函数中定义一个内函数，内函数里运用了外部函数的临时变量，并且外函数的返回值是内函数的引用。如下是最简单的一个闭包：</p>

<p><img alt="" class="has" src="https://img-blog.csdn.net/20180920143854274?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" /><br />
在python中一切皆对象，小到一个变量，大到一个函数一个类都是对象，变量名，函数名类名都是指向内存地址。因此当返回值为一个函数的引用的时候可以跟括号来调用此函数。<br />
一般来说，当一个函数结束的时候，会将临时变量释放掉，但是在闭包中，临时变量会在内部函数中用到，因此在返回内函数的时候会将临时变量和内函数绑定在一起，外函数结束后，在调用内函数的时候依然可以使用外函数的临时变量。每次在调用外函数的时候都会在内存中创建一个内函数，并且返回的是当前的内函数地址，需要知道的的是虽然内函数被重新创建了，但是外函数的临时变量只存在一份，每次创建的内函数都是使用的同一份临时变量。如下两次调用的返回值是不同的</p>

<p><img alt="" class="has" src="https://img-blog.csdn.net/2018092014391017?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" /><br />
Python中内函数想要修改外函数的临时变量可以使用nonlocal关键字来定义变量，如下：</p>

<p><img alt="" class="has" src="https://img-blog.csdn.net/20180920143921274?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" /></p>