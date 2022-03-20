<p>以下是自己的学习记录，算是一个总结。</p>

<p style="text-indent:0;">接下来会依次对下面问题做一个解答：<br />
    1. Python的dict和set为什么是无序的？<br />
    2. 为什么不是所有的python对象都可以用作dict的键和set中的元素</p>

<p style="text-indent:50px;">要弄懂上面的问题，我们首先要了解Python内部是如何实现dict和set类型的。我们先来看看dict的内部结构，dict其实本质上是一个散列表（散列表即总有空白元素的数组，Python会保证至少有三分之一的数组元素是空的），dict的每个键都占用一个表元，而一个表元中又分为两个部分，分别是对键的引用和对值的引用。当我们存放一个对象的时候，首先会要计算这个元素的散列值，python中使用hash()方法来实现的，这也就回答了第二个问题，因为不是所有的python对象都可以使用hash来获取散列值，获取不到散列值也就不可能存放到dict中，所以只有可hash的对象才能够作为dict的键。值得注意的是内置的hash方法可以用于所有的内置类型对象的，所有用户自定义的对象默认都是可以作为键的，因为自定义对象的散列值是通过id()来获取的。例如：</p>

<pre class="has">
<code class="language-python">class T(object):
    pass


t = T()

print(id(t))
d = {t: 1}
print(d)

###  2133693018240
###  {&lt;__main__.T object at 0x000001F0CA03B080&gt;: 1}</code></pre>

<p style="text-indent:50px;">现在假设我们已经获取到了元素的散列值，接下来就该计算应当存放位置了，将散列值对数组长度进行取余，得到的结果就是存放位置的索引了。但是不同的key可能会得到相同的散列值，也就是哈希冲突的问题，python内部是使用开放寻址的方法来解决的，开放寻址法就不在此详细说了。关于为什么dict是无序的，这个是因为python内部会保证散列表至少有三分之一的位置为空，当我们增加元素的时候，python有可能会对散列表进行扩容，具体操作就是重新开辟一块更大的空间，将原有的元素添加到新表里面，这个过程中可能又会发生新的散列冲突，导致新的散列表中的键的次序发生变化。当然呢如果想要保存顺序也可以使用OrderedDict来处理</p>

<p style="text-indent:0;"> </p>

<p style="text-indent:0;">dict操作的时间复杂度：</p>

<table><thead><tr><th>操作</th>
			<th>操作说明</th>
			<th>时间复杂度</th>
		</tr></thead><tbody><tr><td>copy</td>
			<td>复制</td>
			<td>O(n)</td>
		</tr><tr><td>get(value)</td>
			<td>获取</td>
			<td>O(1)</td>
		</tr><tr><td>set(value)</td>
			<td>修改</td>
			<td>O(1)</td>
		</tr><tr><td>delete(value)</td>
			<td>删除</td>
			<td>O(1)</td>
		</tr><tr><td>search(in)</td>
			<td>字典搜索</td>
			<td>O(1)</td>
		</tr><tr><td>iterration</td>
			<td>字典迭代</td>
			<td>O(n)</td>
		</tr></tbody></table><p style="text-indent:50px;">set集合和dict一样也是基于散列表的，只是他的表元只包含值的引用而没有对键的引用，其他的和dict基本上是一致的，所以在此就不再多说了。</p>