
<h4>使用python操作redis</h4>
<p>数据库的连接：</p>
<p></p>
<pre class="python">import redis
#连接数据库
db = redis.Redis('localhost',6379)
#连接池
# pool = redis.ConnectionPool(host='localhost',port=6379)
# db = redis.Redis(connection_pool=pool)</pre>
<p><span style="font-size:14px"><strong>String操作：</strong></span></p>
<p>使用key-value的模式来存储，相当于每个name对应一个value</p>
<p><strong><em>set(name, value, ex=None, px=None, nx=False, xx=False)<br>
</em></strong></p>
<p><strong><em>ex，过期时间（秒）<br>
px，过期时间（毫秒）<br>
nx，如果设置为True，则只有name不存在时，当前set操作才执行<br>
xx，如果设置为True，则只有name存在时，岗前set操作才执行</em></strong><br>
</p>
<p></p>
<pre class="python">db.set('name','fml')
print(db.get('name'))</pre>
结果：fml
<p><strong><em>setex(name,value,time)</em></strong></p>
<p><strong><em>time:过期时间（秒）</em></strong></p>
<p></p>
<pre class="python">db.setex('name','1',2)
time.sleep(2)
print(db.get('name'))</pre>
结果：None
<p>同样的还有</p>
<p><strong><em>setnx(name,value)</em></strong>，相当于set()中的nx参数为True</p>
<p><strong><em>psetex(name.time,value</em></strong>),time为毫秒数</p>
<p><em>mset(*args,**kwargs)&nbsp; </em>批量操作，可传入字典</p>
<p>方式一</p>
<p></p>
<pre class="python">db.mset(t1 = 1,t2 = 2)
print(db.get('t1'))
print(db.get('t2'))</pre>
结果 1，2<br>
方式二
<p></p>
<pre class="python">d = {'name':'fml','age':22}
db.mset(d)
print(db.get('name'))
print(db.get('age'))</pre>
结果：&nbsp;fml ， 22<br>
<br>
<p><span style="font-size:12px"><em>get(name):</em></span><span style="font-size:10px">返回name的&#20540;</span></p>
<p><span style="font-size:10px"><strong>mget(keys, *args):</strong>批量操作，返回多个&#20540;（列表的形式），可传入列表<br>
</span></p>
<p><span style="font-size:10px"></span></p>
<pre class="python">print(db.mget('name','age'))
print(db.mget(['t1','t2']))</pre>
<img src="https://img-blog.csdn.net/20180312172020750?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
<em><br>
</em>
<p><span style="font-size:10px"><em>getset(name,value):</em>设置新的&#20540;并返回之前的&#20540;</span></p>
<p><span style="font-size:10px"></span></p>
<pre class="python">print(db.getset('name','test'))
print(db.get('name'))</pre>
<img src="https://img-blog.csdn.net/20180312172409761?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
<p><span style="font-size:10px"><em>getrange(key,start,end):</em>获取子序列（根据字节获取，非字符）</span></p>
<p><span style="font-size:10px"><span style="color:rgb(51,51,51); font-family:verdana,Arial,Helvetica,sans-serif; font-size:10px">start：起始位，end结束位,&#20540;得注意的是这个是按照字节来计算而不是字符个数&nbsp;在utf-8的编码中一个中文汉字占三个字节，一个字符只占一位</span></span></p>
<p><span style="font-size:10px"><span style="color:rgb(51,51,51); font-family:verdana,Arial,Helvetica,sans-serif; font-size:10px"></span></span></p>
<pre class="python">db.set('name1','fml')
print(db.getrange('name1', 0, 1).decode())
db.set('name2','名字')
print(db.getrange('name2', 0, 2).decode())</pre>
<img src="https://img-blog.csdn.net/20180312182537723?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
<p><em>setrange(name, offset, value):&nbsp; &nbsp;</em>从指定字符串索引开始向后替换（新&#20540;太长时，则向后添加）<br>
</p>
<p>offset:字符串索引号</p>
<p></p>
<pre class="python">db.set('name','test set range')
db.setrange('name',1,'ls')  #从第二个字符开始替换
print(db.get('name').decode())</pre>
<img src="https://img-blog.csdn.net/20180312183816787?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt="">
<p><em>setbit(name, offset, value)：</em>和上面的一个功能类&#20284;，只不过是用bite方式来更改<br>
</p>
<p><strong><em>getbit(name, offset)</em></strong>：获取name的二进制表示中的某一位&#20540;<br>
</p>
<p><em>bitcount(key, start=None, end=None)：</em>统计name用二进制表示中的为1的个数</p>
<p>start，位起始位置end，位结束位置</p>
<p></p>
<pre class="python">db.set('name','f')
print(db.bitcount('name'))
#f对应的ASCII码的&#20540;为102,102转为二进制为 0110 0110 所以返回&#20540;为4</pre>
<em>strlen(name):</em>返回name对于&#20540;的<strong>字节长度</strong>，汉字三字节
<p></p>
<pre class="python">db.set('name1','发生')
db.set('name2','fml')
print(db.strlen('name1'))
print(db.strlen('name2'))</pre>
<img src="https://img-blog.csdn.net/20180312214428147?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
<p><strong><em>incr(self, name, amount=1)：</em></strong> name的对应&#20540;增加amount<br>
</p>
<p><strong>自增只适用于整数</strong>，当name不存在的时候会新建一个name&#20540;为amount<br>
</p>
<p></p>
<pre class="python">db.set('num1',2)
db.incr('num1', amount=2)
db.incr('num2', amount=2)
print(db.get('num1').decode())
print(db.get('num2').decode())</pre>
<img src="https://img-blog.csdn.net/20180312215147018?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
<p><strong>incrbyfloat(self, name, amount=1.0)：</strong>同上只不过是浮点型<br>
</p>
<p><em>decr(self, name, amount=1)：</em>同上功能为自减<br>
</p>
<p><strong><em>append(key, value) ：</em></strong>在name对应&#20540;后面追加value的内容，如果没有name就会新建一个name=value<br>
</p>
<p></p>
<pre class="python">db.set('name','fml')
db.append('name','test')
print(db.get('name').decode())</pre>
<img src="https://img-blog.csdn.net/20180312220700495?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
<p><br>
</p>
<p><span style="font-weight:bold; font-size:14px">Hash操作</span><br>
<span style="font-size:10px">使用字典的方式来存储，name为字典名</span></p>
<p><strong><em>hset(name, key, value):</em></strong><br>
</p>
<p><pre name="code" class="python">db.hset('info','name','fml')
db.hset('info','age',22)
print(db.hget('info','name').decode())
print(db.hget('info','age').decode())</pre><strong style="font-style:italic">hmset(name, mapping)：</strong>批量操作 ，mapping为字典</p>
<p><pre name="code" class="python">db.hmset('info1',{'name1':'fml','age1':23})
print(db.hget('info1','name1').decode())
print(db.hget('info1','age1').decode())</pre></p>
<p><img src="https://img-blog.csdn.net/20180313150927616?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
</p>
<p><strong style="font-style:italic">hget(name,key)：</strong>同get操作</p>
<p><strong style="font-style:italic">hmget(name, keys, *args)：</strong>同mget,可传入列表或者多个&#20540;<br>
</p>
<p><strong style="font-style:italic">hgetall(name)：</strong>获取name的所有key-和value&#20540;<br>
</p>
<p><strong><em>hlen(name)：</em></strong>获取name中key的个数<br>
</p>
<p><strong><em>hkeys(name)：</em></strong>获取name中所有的key<br>
</p>
<p><strong><em>hvals(name)：</em></strong>获取name中所有的value&#20540;<br>
</p>
<p><strong><em>hexists(name, key)：</em></strong>判断name中是否存在传入的key<br>
</p>
<p><strong><em>hdel(name,*keys)：</em></strong>删除name中的key，若不存在返回0，删除成功后返回1<br>
</p>
<p><strong><em>hincrby(name, key, amount=1)：</em></strong>自增，同string操作一样<br>
</p>
<p><strong><em>hincrbyfloat(name, key, amount=1.0)</em></strong>&nbsp;自增浮点型<br>
</p>
<p><br>
</p>
<p>hscan(name, cursor=0, match=None, count=None)&nbsp;过滤获取多个&#20540;<br>
</p>
<p>cursor:起始位置，match：过滤方法 ，count：获取的个数</p>
<p>过滤方法的例子：1：获取以n开头的key ：n*</p>
<p><span style="white-space:pre"></span>&nbsp; &nbsp; &nbsp;2：获取包含a的key：*a*</p>
<p><span style="white-space:pre"></span>&nbsp; &nbsp; &nbsp;3：获取以e结尾的key：*e</p>
<p><pre name="code" class="python">db.hset('info','name','fml')
db.hset('info','age',22)
print(db.hscan('info',cursor=0,match= 'n*'))
print(db.hscan('info',cursor=0,match= '*e'))
print(db.hscan('info',cursor=0,match= '*g*'))</pre><img src="https://img-blog.csdn.net/20180313154353952?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
</p>
<p><br>
</p>
<p><span style="font-size:14px; font-weight:700">List操作</span><br>
</p>
<p><span style="font-size:14px; font-weight:700"><br>
</span></p>
<p><strong style=""><em style=""><span style="font-size:10px">lpush(name,values):&nbsp;向name添加元素，从左边开始添加</span></em></strong></p>
<p><pre name="code" class="python" style=""><span style="font-size:10px;">db.lpush('list','1','2','3')
print(db.lrange('list',0,-1))</span></pre><span style="font-size:14px"><img src="https://img-blog.csdn.net/20180313165641539?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""></span><br>
<em><strong style=""><span style="font-size:10px">lpush(name,values):&nbsp;向name添加元素，从右边开始添加</span></strong></em><br>
</p>
<p><pre name="code" class="python">db.rpush('list3','1','2','3')
print(db.lrange('list3',0,-1))</pre><img src="https://img-blog.csdn.net/20180313165843605?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""></p>
<p><br>
<strong><em>lpushx(name,value)：</em></strong>只有当name存在的时候才在左边添加，相同的还有rpushx(name.value)<br>
</p>
<p><pre name="code" class="python">db.rpush('list3','1','2','3')
db.lpushx('list3',4)
print(db.lrange('list3',0,-1))</pre><img src="https://img-blog.csdn.net/20180313170111945?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""></p>
<p><strong><em>llen(name):&nbsp;</em></strong>返回name的存储的长度</p>
<p><strong><em>linsert(name, where, refvalue, value))&nbsp;</em></strong> 在name的refvalue前面或后面插入value,如果存在多个refvalue的时候只会在从左往右数第一个起作用</p>
<p>where：BEFORE/AFTER</p>
<p><pre name="code" class="python">db.rpush('list5','1','2','3')
db.linsert('list5','BEFORE','2','5')
db.linsert('list5','AFTER','2','6')
print(db.lrange('list5',0,-1))</pre><img src="https://img-blog.csdn.net/20180313170630387?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
<br>
<strong><em>lset(name, index, value)：</em></strong>修改index索引的&#20540;<br>
</p>
<p><pre name="code" class="python">db.rpush('list6','1','2','3')
db.lset('list6',1,4)
print(db.lrange('list6',0,-1))</pre><img src="https://img-blog.csdn.net/20180313171210000?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
<strong><em>lrem(name, value, num)：</em></strong>删除name中的value，num为需要删除的个数<br>
</p>
<p><pre name="code" class="python">db.rpush('list7',1,2,3,4,1,2,4,5,7)
db.lrem('list7',1,1)
db.lrem('list7',2,2)
print(db.lrange('list7',0,-1))</pre><img src="https://img-blog.csdn.net/20180313172150477?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""></p>
<p><strong><em>lpop(name)：</em></strong>删除左边第一个&#20540;并返回，同样的还有<strong><em>rpop(name)：</em></strong>从右边弹出<br>
</p>
<p><strong><em>lindex(name, index)：</em></strong>获取index索引的&#20540;<br>
</p>
<p><strong><em>lrange(name, start, end)：</em></strong>返回切片获得的&#20540;<br>
</p>
<p><strong><em>ltrim(name, start, end)：</em></strong>删除除start-end之外的所有&#20540;<br>
</p>
<p><strong><em>rpoplpush(src, dst) ：</em></strong>删除src的最右的一个&#20540;，并把它添加到dst的最左边<br>
</p>
<p><strong><em>blpop(keys, timeout)：</em></strong>将多个列表排列，按照从左到右去pop对应列表的元素&nbsp; 同<strong><em>brpop(keys, timeout)</em></strong><br>
</p>
<p><strong style="font-style:italic">brpoplpush(src, dst, timeout=0)：</strong>从一个列表的右侧移除一个元素并将其添加到另一个列表的左侧<br>
</p>
<p><br>
</p>
<p><span style="font-size:14px; font-weight:700">set集合操作</span><br>
</p>
<p><br>
</p>
