
<p>队列Queue包含三个类&nbsp;</p>
<p>1：Queue(maxsize=0)&nbsp; 普通模式先进先出</p>
<p>2：LifoQueue(maxsize=0)&nbsp; 后进先出</p>
<p>3：PriorityQueue(maxsize=0)&nbsp; 优先级模式</p>
<p><br>
</p>
<p>Queue.qsize()&nbsp;返回当前队列里存在的个数</p>
<p>Queue.empty()&nbsp;返回队列是否为空</p>
<p>Queue.full()&nbsp;返回队列是否存满</p>
<p>Queue.put(item, block=True, timeout=None)<br>
将item放入队列中。<br>
如果可选的参数block为True且timeout为空对象（默认的情况，阻塞调用，无超时）。<br>
如果timeout是个正整数，阻塞调用进程最多timeout秒，如果一直无空空间可用，抛出Full异常（带超时的阻塞调用）。<br>
如果block为False，如果有空闲空间可用将数据放入队列，否则立即抛出Full异常</p>
<p>Queue.put_nowait()无阻塞版本,等同于block=False，timeout=None</p>
<p>Queue.get(block=True, timeout=None)&nbsp;取出数据，其他与put类&#20284;</p>
<p><br>
</p>
<p>Queue()示例</p>
<pre class="python">import queue

q = queue.Queue()  #普通的（先进先出

q.put(1)
q.put(2)
q.put(3)

print(q.qsize()) #获取当前存在的个数

print(q.get()) #取出 当超过的时候会报错
print(q.get())
print(q.get())</pre>
结果：
<p>1 2 3&nbsp;</p>
<p>LifoQueue()示例<br>
</p>
<pre class="python">import queue

q = queue.LifoQueue()  #普通的（先进先出

q.put(1)
q.put(2)
q.put(3)

print(q.qsize()) #获取当前存在的个数

print(q.get()) #取出 当超过的时候会报错
print(q.get())
print(q.get())</pre>
<p>结果：</p>
<p>3&nbsp; 2 1&nbsp;</p>
<p>PriorityQueue()示例&nbsp;&nbsp;<br>
</p>
<p>按照一定的规律确定优先级，例如数字越小优先级越高，或者按字符排序，&#20540;得注意的是只能采用一种模式来确定，全为数字或是全为字符，两者不能混在一起，不然会报错。</p>
<pre class="python">import queue

q = queue.PriorityQueue()  #普通的（先进先出

q.put((2,'b'))
q.put((1,'a'))
q.put((3,'c'))

print(q.qsize()) #获取当前存在的个数

print(q.get()) #取出 当超过的时候会报错
print(q.get())
print(q.get())</pre>
结果：
<p>(1, 'a')<br>
(2, 'b')<br>
(3, 'c')<br>
</p>
<p><br>
</p>
<p>简单的生产者和消费者模型</p>
<pre class="python">import queue,threading,time
q = queue.Queue()

def Producer():
    count = 0
    while True:
        q.put('Switch %s' %count)
        print('Switch %s' %count)
        count &#43;= 1
        time.sleep(1)

def Consumer():
    while True:
        if q.qsize() &gt; 0 :
            print('buy %s'%q.get())
            time.sleep(2)

p = threading.Thread(target=Producer)
c = threading.Thread(target=Consumer)

p.start()
c.start()</pre>
结果：
<p>生成了Switch 0<br>
购买了 Switch 0<br>
生成了Switch 1<br>
购买了 Switch 1<br>
生成了Switch 2<br>
生成了Switch 3<br>
购买了 Switch 2<br>
生成了Switch 4<br>
生成了Switch 5<br>
生成了Switch 6<br>
购买了 Switch 3<br>
生成了Switch 7<br>
购买了 Switch 4<br>
生成了Switch 8<br>
<br>
</p>
<p><br>
</p>
