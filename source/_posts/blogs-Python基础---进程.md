
<p>python的多线程和多进程都是调用系统的原生线程和进程，多进程和多线程在使用上类&#20284;，同样有直接调用和继承调用两种，在进程中还可以创建其他的线程</p>
<p>可通过os模块中的getpid()获取自己的进程ID，getppid()获取父进程的ID</p>
<p><pre name="code" class="python">import multiprocessing,time,os
class MyProcessing(multiprocessing.Process):
    def __init__(self):
        super(MyProcessing,self).__init__()
    def run(self):
        print(os.getpid(),os.getppid())

p1 = MyProcessing()
p2 = MyProcessing()
p1.start()
p2.start()

print(os.getpid())</pre><img src="https://img-blog.csdn.net/20180311152838710?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""></p>
<h4>进程间通信</h4>
<div>1：Queue（）</div>
<p>不同进程中的内存空间是独立的，不同与线程无法直接访问，要想进程间互相通信需要用到进程Queue（multiprocessing.Queue()）不同与线程Queue（queue.Queue()），在使用进程Queue的时候父进程创建子进程的时候会复制一个队列到子进程内存空间里面，当子进程修改队列的时候，进程Queue会序列化到一个中间地方，然后再反序列化到父进程中，但是并不是直接访问的，这样就实现了父进程与子进程的数据访问</p>
<p><pre name="code" class="python">import multiprocessing,time,os
class MyProcessing(multiprocessing.Process):
    def __init__(self):
        super(MyProcessing,self).__init__()
    def run(self):
        q.put(1)
q = multiprocessing.Queue()
p1 = MyProcessing()
p1.start()

print(q.get())</pre><img src="https://img-blog.csdn.net/20180311155259697?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
</p>
<p>2：Pipe()</p>
<p>一个管道生成的时候会返回两个端口，一个可作为父进程访问端口，一个为子进程访问端口，若无数据可接收的时候会阻塞</p>
<p><pre name="code" class="python">import multiprocessing
class MyProcessing(multiprocessing.Process):
    def __init__(self):
        super(MyProcessing,self).__init__()
    def run(self):
        child_conn.send('f')
        
parent_conn, child_conn= multiprocessing.Pipe()

p1 = MyProcessing()
p2 = MyProcessing()
p1.start()
p2.start()

print(parent_conn.recv())
print(parent_conn.recv())</pre><img src="https://img-blog.csdn.net/20180311160321324?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
</p>
<p>3：Manage()</p>
<p>Manage()支持list, dict, Namespace, Lock, RLock, Semaphore, BoundedSemaphore, Condition, Event, Barrier, Queue, Value , Array.</p>
<p>在使用Manage的时候必须要使用join等待子进程完成后继续运行，但是不知道是什么原因，猜测可能是防止多个进程修改数据导致混乱</p>
<p><pre name="code" class="python">from multiprocessing import Manager,Process

def run (l,num):
    l.append(num)

l = Manager().list() #创建一个可以在进程中传递的空列表
p_list = []
for i in range(10):
    p = Process(target=run, args=(l, i))
    p.start()
    p_list.append(p)

for res in p_list:
    res.join()

print(l)</pre><img src="https://img-blog.csdn.net/20180311165052147?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
</p>
<p>进程锁和线程锁类&#20284;不在赘述</p>
<h4>进程池Pool()</h4>
<div>线程池中有两个方法：</div>
<div>1：apple()&nbsp; #串行方式</div>
<div>2：apple_async() #并行方式，使用并行方式的时候必须先close再join</div>
<p><pre name="code" class="python">import os,time
from multiprocessing import Pool

def run(num):
    time.sleep(2)
    print(num,os.getpid())
    
pool = Pool(5)
for i in range(5):
    #pool.apply(func=run,args=(i,))
    pool.apply_async(func=run,args=(i,))
print('end')
pool.close()
pool.join() #进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。</pre><img src="https://img-blog.csdn.net/20180311182622059?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
<br>
</p>
<p><br>
</p>
<p><br>
</p>
