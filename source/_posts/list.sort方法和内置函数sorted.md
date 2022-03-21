<h3>list.sort方法和内置函数sorted的异同</h3>

<p>list.sort方法和sorted函数都是对列表进行排序的，但是这两种方法也是有少许不同的，list.sort排序是在原有基础上进行的，不会生成返回一个新的list， 但是sorted函数则不同，他会产生一个新对象并返回。如下</p>

<pre class="has">
<code class="language-python">t = [1, 3, 4, 2, 5, 0]
t1 = [1, 3, 4, 2, 5, 0]
print(t.sort())
print(t)
print(sorted(t1))
print(t1)</code></pre>

<p><img alt="" class="has" height="113" src="https://img-blog.csdn.net/20181011115605325?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="284" /><br />
在同时对t和t1 排序并打印结果，t.sort()返回None  sorted(t1) 返回排序好的list，两者都正确，但是只有t的内容发生改变，t1的内容没有改变。</p>

<p>sorted()函数要比list.sort()强大很多，sorted()不仅仅只能将list作为参数传递进去，还可以接收任何形式的可迭代对象作为参数，甚至是不可变序列或者生成器，不管是接收的什么参数sorted()都是返回一个列表。</p>

<p>list.sort()和sorted()都有两个可选的参数：<br />
 1. reverse：决定是升序还是降序排列，True为降序，默认值为False<br />
 2. key: 一个只有一个参数的函数，这个函数会被用在序列的每一个元素上，通俗来讲就是排序规则，例如对字符串排序的时候可以使用key=str.lower来实现忽略大小的排序，或者是key=len来按照字符串长度排序等等。默认用元素自己的值来排序。<br /><img alt="" class="has" height="103" src="https://img-blog.csdn.net/20181011120952740?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="413" /></p>

<h3>想要在不打乱次序的情况下如何向有序列表中插入数据呢？</h3>

<p>可借助bisect模块来实现，bisect模块主要包含两个函数 ，bisect和insort ，这两个函数都是利用二分查找算法来实现在有序序列中查找或者插入元素的<br />
例如使用bisect来搜索可插入的位置：</p>

<pre class="has">
<code class="language-python">import bisect

t = [123, 3, 234, 1, 423, 5, 25, 235, 325]
t.sort()
print(bisect.bisect(t, 235))

###  7</code></pre>

<p>返回值为可插入的位置。前提是传入的参数是有序序列，bisect还有两个可选的参数 lo和 hi即搜索范围，lo默认为0，hi默认为序列长度。</p>

<p>如果有序序列中已存在要插入的元素的时候，又是如何处理的呢！这个就有两种情况，插入到原有元素之前或者之后，分别对应两个方法bisect_left和 bisect_right，而我们之前使用的bisect其实就是bisect_right方法。既然获取的插入位置，那么使用list.insert方法插入即可完成向有序序列插入元素。有没有更简单的方法呢，答案是肯定的，那就是我们之前提到的insort方法。</p>

<p>使用insort插入元素：</p>

<pre class="has">
<code class="language-python">import bisect

t = [123, 3, 234, 1, 423, 5, 25, 235, 325]
t.sort()
bisect.insort(t, 222)
print(t)

###   [1, 3, 5, 25, 123, 222, 234, 235, 325, 423]</code></pre>

<p>看了bisect源码之后发现其实insort方法和bisect方法是一样的，只是获取到了插入位置之后紧接着调用insert()方法<br /><img alt="" class="has" height="255" src="https://img-blog.csdn.net/20181011145138585?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="602" /><br />
insort方法和bisect方法是一样的也是有两个可选参数lo和hi来缩小范围，也分insort_left和insort_right，默认使用的是insort_right方法 </p>

<p><br />
 </p>