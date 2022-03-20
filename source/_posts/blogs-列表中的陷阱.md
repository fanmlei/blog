
<p>列表是python中常用的一种数据结构，能够存放任意的其他数据类型，int、str、list 、tuple等，但是最近发现了一个问题，代码如下</p>
<pre class="python">data = []
buff = dict()
for i in range(5):
    buff['d'] = i
    data.append(buff)
print(data)</pre>
<p>原本以为打印的结果会是</p>
<p>[{'d':0},{'d':1},{'d':2},{'d':3},{'d':4}]</p>
<p>但是最终的结果为<img src="" alt=""><img src="" alt=""></p>
<p>[{'d':4},{'d':4},{'d':4},{'d':4},{'d':4}]<br>
</p>
<p><img src="" alt=""><img src="" alt=""><img src="" alt=""><img src="" alt=""><img src="" alt=""><img src="" alt=""><img src="" alt=""><img src="" alt=""></p>
<p>最后发现其实当我们使用列表存储数据的时候，只是把数据的内存地址给存入列表中了而不是数据本身，所以上面的代码就不难理解我们只是在data列表中存了5个buff的内存地址，而且这5个内存地址是指向同一个数据的，当运行到最后一个循环的时候buff里面的数据就变为{'d':4},所以data最后的结果就是5个相同的内容。</p>
<p>弄清楚了上面的问题，我们可以做以下更改来实现我们的目的</p>
<pre class="html">data = []
buff = dict()
for i in range(5):
    buff['d'] = i
    data.append(buff)
    buff = dict()
print(data)</pre>
<p>最终的结果如下<img src="" alt=""><img src="" alt=""></p>
<p>[{'d':0},{'d':1},{'d':2},{'d':3},{'d':4}],</p>
<p><img src="" alt=""></p>
<p>因为我们在append之后相当于新建了一个空字典，buff不再指向之前的内存地址了，在下次循环的时候会将数据存档在新的内存空间里面，而列表中其实是存了5个不同的内存地址。</p>
<p>总结：</p>
<p>列表并不是直接存放数据对象本身，而是存放数据对象的内存地址，如果内存地址对应的内容被修改了那么列表也会被更改掉。</p>
