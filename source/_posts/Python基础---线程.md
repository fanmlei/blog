---
title: Python基础---线程
date: 2018-03-07 02:21:08
categories: 
- Python
tags:
- 编程基础
---
<h4>调用方式</h4>
<p>python的线程调用有两种方式。一种是直接调用，一种是继承式调用</p>
<p>直接调用</p>
<pre class="python">import threading,time

#方法一
def run(n):

    print(n)
    time.sleep(2)
t1 = threading.Thread(target=run,args=(&quot;t1&quot;,))
t2 = threading.Thread(target=run,args=(&quot;t2&quot;,))
t1.start()
t2.start()</pre>
使用类的方法调用
<pre class="python">#方法二（使用类的方法）
import threading,time
class MyThread(threading.Thread):
    def __init__(self,n):
        super(MyThread,self).__init__()
        self.n = n

    def run(self):     #函数名必须为run
        print(self.n)
        time.sleep(2)

t1 = MyThread(1)
t2 = MyThread(2)

t1.start()
t2.start()</pre>
<p><br>
</p>
<h4>join和Daemon</h4>
<p><span style="font-family:verdana,Arial,Helvetica,sans-serif; font-size:10px; color:#333333">join()等待线程结束后再往后继续运行</span></p>
<p><span style="font-family:verdana,Arial,Helvetica,sans-serif; font-size:10px; color:#333333">Daemon()守护线程</span></p>
<p><span style="font-family:verdana,Arial,Helvetica,sans-serif; font-size:10px; color:#333333">使用setDaemon(True)那么主线程不会等待子线程结束才结束，主线程结束后子线程也会直接结束，必须要在start之前设置否则会报错</span></p>
<p><span style="font-family:verdana,Arial,Helvetica,sans-serif; font-size:10px; color:#333333">python中默认为setDaemon(False),主线程结束了子线程依然会执行直到完毕。</span></p>
<p><span style="color:rgb(51,51,51); font-family:verdana,Arial,Helvetica,sans-serif; font-size:10px">join例子：</span></p>
<pre class="python">import threading,time
class MyThread(threading.Thread):
    def __init__(self,n):
        super(MyThread,self).__init__()
        self.n = n

    def run(self):     #函数名必须为run
        print(self.n)
        time.sleep(2)
        print('end')

t1 = MyThread('t1')
t2 = MyThread('t2')
t1.start()
t1.join()
t2.start()
t2.join()</pre>
结果
<p><span style="font-family:verdana,Arial,Helvetica,sans-serif; font-size:10px; color:#333333"><img src="https://img-blog.csdn.net/20180310153251692?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center" alt=""><br>
</span></p>
<p>setDaemon()例子</p>
<pre class="python">import threading,time
class MyThread(threading.Thread):
    def __init__(self,n):
        super(MyThread,self).__init__()
        self.n = n

    def run(self):     #函数名必须为run
        print(self.n)
        time.sleep(2)
        print('end')

t1 = MyThread('t1')
t2 = MyThread('t2')
t1.setDaemon(True)
t2.setDaemon(True)
t1.start()
t2.start()</pre>
<p>结果</p>
<img src="https://img-blog.csdn.net/20180310153422919?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
<br>
<p></p>
<h4><span style="font-family:verdana,Arial,Helvetica,sans-serif; color:#333333"><span style="font-size:14px">线程锁</span></span></h4>
<div>子线程可以共享父线程的内存空间，当存在多个子线程需要同时修改一个数据的时候就可能出现问题</div>
<div>假设两个子线程执行的操作都是num&#43;1，由于线程是同时执行的，第一个子线程先取num = 1 ，第二个线程有取出num依然为1，线程一结束后num更改为2，随之线程二结束num依然被改为2，就与我们的目标出现冲突，这个时候就需要用到线程锁了，当线程一访问num的时候线程二是无法访问num的，线程一结束后释放num线程二才能访问num，这就使得num的结果不会产生冲突了。</div>
<div>
<pre class="python">#线程锁示例
import threading

num = 0
t_objs = []
lock = threading.Lock()

def run():
    lock.acquire()  #加锁
    global num      #声明全局变量
    num &#43;= 1        #执行加一操作
    lock.release()  #释放锁

for i in range(500):
    t = threading.Thread(target=run)
    t.start()
    t_objs.append(t)

for t in t_objs:    #等待所有线程结束
    t.join()

print(num)</pre>
递归锁则是在一个锁里面又嵌套另外一个线程锁</div>
<div>
<pre class="python">#递归锁
import threading

def run1():
    lock.acquire()
    global num
    num &#43;= 1
    lock.release()
    return num

def run2():
    lock.acquire()
    global num2
    num2 &#43;= 1
    lock.release()
    return num2

def run3():
    lock.acquire()
    res = run1()
    res2 = run2()
    lock.release()
    print(res, res2)

if __name__ == '__main__':

    num, num2 = 0, 0
    lock = threading.RLock()
    for i in range(10):
        t = threading.Thread(target=run3)
        t.start()</pre>
结果<br>
<img src="https://img-blog.csdn.net/20180310173722570?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
</div>
<div><br>
</div>
<h4>信号量（Semaphore）</h4>
<div><span style="margin:0px; padding:0px; color:rgb(51,51,51); font-family:verdana,Arial,Helvetica,sans-serif"><span style="font-size:10px">线程锁每次只允许一个线程操作数据，Semaphore则可同时允许多个线程操作，当达到允许的最大&#20540;的时候后面的则需要等待，前面的线程执行完毕后才可执行，因此操作同一个数据的时候依然有可能出错</span></span></div>
<div><span style="margin:0px; padding:0px; color:rgb(51,51,51); font-family:verdana,Arial,Helvetica,sans-serif"><span style="font-size:10px"></span></span>
<pre class="python">#信号量

import threading,time

def run(num):
    semaphore.acquire()
    time.sleep(1)
    print(num)
    semaphore.release()

semaphore = threading.BoundedSemaphore(3) #最多运行三个线程
for i in range(10):
    t = threading.Thread(target=run,args=(i,))
    t.start()</pre>
<h4><span style="margin:0px; padding:0px; color:rgb(51,51,51); font-family:verdana,Arial,Helvetica,sans-serif"><span style="font-size:10px">事件（Event）</span></span></h4>
</div>
<div><span style="margin:0px; padding:0px; color:rgb(51,51,51); font-family:verdana,Arial,Helvetica,sans-serif"><span style="font-size:10px">Event默认内置了一个标志，初始&#20540;为False<br>
</span></span></div>
<div><span style="margin:0px; padding:0px; color:rgb(51,51,51); font-family:verdana,Arial,Helvetica,sans-serif"><span style="font-size:10px">event总共就四中方法：set()、clear()、wait()、is_set()</span></span></div>
<div><span style="font-family:verdana,Arial,Helvetica,sans-serif; font-size:10px; color:#333333">set()设置标志位为True</span></div>
<div><span style="font-family:verdana,Arial,Helvetica,sans-serif; font-size:10px; color:#333333">clear()设置标志位为False</span></div>
<div><span style="font-family:verdana,Arial,Helvetica,sans-serif; font-size:10px; color:#333333">wait()等待标志位设为True</span></div>
<div><span style="font-family:verdana,Arial,Helvetica,sans-serif; font-size:10px; color:#333333">is_set()判断标志位是否被设为True</span></div>
<div><span style="font-family:verdana,Arial,Helvetica,sans-serif; font-size:10px; color:#333333"><br>
</span></div>
<div><span style="font-family:verdana,Arial,Helvetica,sans-serif; font-size:10px; color:#333333">已红绿灯为例说明，首先写出交通灯，event.clear()相当于红灯，event.set()相当于绿灯,红灯为5秒绿灯也为5秒，用count来计数，当count超过10的时候重置count，这样红绿灯就能以5秒为间隔循环运行</span></div>
<div><span style="margin:0px; padding:0px; color:rgb(51,51,51); font-family:verdana,Arial,Helvetica,sans-serif"><span style="font-size:10px"></span></span>
<pre class="python">import time,threading

event = threading.Event()

def light():
    count = 0
    while True:
        if count &gt;= 5 and count &lt; 10:
            event.clear()     #相当于红灯了
            print(&quot;red light please wait...&quot;)
        elif count &gt; 10 :
            event.set()       #相当于绿灯
            count = 0        
        else:
            print(&quot;go go go ...&quot;)
        time.sleep(1)
        count &#43;= 1</pre>
再来写car</div>
<div><span style="margin:0px; padding:0px; color:rgb(51,51,51); font-family:verdana,Arial,Helvetica,sans-serif"><span style="font-size:10px"></span></span>
<pre class="python">def car():
    while True:
        if event.is_set():  #判断event是否被set，相当于检测是否为绿灯
            print('run...')
            time.sleep(1)
        else:
            print('waiting for green light..')
            event.wait()
            print('green light is on go...')</pre>
运行</div>
<div><span style="margin:0px; padding:0px; color:rgb(51,51,51); font-family:verdana,Arial,Helvetica,sans-serif"><span style="font-size:10px"></span></span>
<pre class="python">l = threading.Thread(target=light)
c = threading.Thread(target=car)
l.start()
c.start()</pre>
最终的结果</div>
<div><span style="margin:0px; padding:0px; color:rgb(51,51,51); font-family:verdana,Arial,Helvetica,sans-serif"><span style="font-size:10px"><img src="https://img-blog.csdn.net/20180310202538695?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
<br>
<br>
</span></span></div>
<div></div>
<p></p>
