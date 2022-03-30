---
title: Python多线程使用浅析
date: 2021-08-16 10:35:18
categories: 
- Python
tags:
- 编程基础
---
由于GIL(全局解释器锁)的存在，导致Python无法利用到多核CPU的优势，并行处理能力也是稍显不足，下面将从GIL开始说说什么是资源竞争，以及Python多线程的创建、锁、线程间通信等问题。
<!--more-->
在python中谈到多线程问题就绕不开一个点GIL，一个是资源竞争

- GIL全称python全局解释器锁，由于GIL的存在，在任意时刻只有一个线程在执行，这也导致python的多线程无法利用到多核CPU的优势，如果是多IO操作的线程影响较小。
- 在操作系统中进程是资源分配的最小单位，线程是系统调度和分派的最小单位，多个线程是共享同一套资源的，多个线程同时操作同一个资源时就会引发竞争。

乍一看由于GIL的存在能够避免多线程出现资源竞争的问题，其实不然，先看下面这个例子。

```python
import threading

a = 0

def add():
    global a
    for i in range(1000000):
        a += 1

def desc():
    global a
    for i in range(1000000):
        a -= 1

if __name__ == '__main__':
    t1 = threading.Thread(target=add)
    t2 = threading.Thread(target=desc)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(a)
```

多次运行结束后a的值是不固定的，很多初学者会认为python是一行一行来运行的，如果是这样的话上面的结果必然是0了，事实上python解释器会将我们的代码转换成字节码然后才执行的。通过dis函数可以打印出转换过后的字节码

```python
import dis

def add(a):
    a += 1

def desc(a):
    a -= 1

print(dis.dis(add))
print(dis.dis(desc))

"""
 25           0 LOAD_FAST                0 (a)
              2 LOAD_CONST               1 (1)
              4 INPLACE_ADD
              6 STORE_FAST               0 (a)
              8 LOAD_CONST               0 (None)
             10 RETURN_VALUE
None
 28           0 LOAD_FAST                0 (a)
              2 LOAD_CONST               1 (1)
              4 INPLACE_SUBTRACT
              6 STORE_FAST               0 (a)
              8 LOAD_CONST               0 (None)
             10 RETURN_VALUE
None
"""
```

可以看到a+=1, a-=1, 都被转换成四个字节码了，python在运行过程中执行一定数量的字节码或者运行了一段时间之后可能就会发生切换，从线程1切换到线程2，这个时候如果a+=1的操作没有执行完，a的结果就会是错误的。

所以GIL并不能保证线程安全。如何保证请往下看。

## 多线程的创建

#### 通过Thread类实例化

```python
import threading,time
def run(n):
    print(n)
    time.sleep(2)
t1 = threading.Thread(target=run,args=("t1",))
t2 = threading.Thread(target=run,args=("t2",))
t1.start()
t2.start()
```

#### 继承Thread

```python
from threading import Thread
import time

class MyThread(Thread):
    def __init__(self, name):
        super().__init__(name=name)

    def run(self):
        print(self.name)
        time.sleep(10)

t1 = MyThread('t1')
t2 = MyThread('t2')
t1.start()
t2.start()
```

#### join & setDaemon

在默认情况下，主线程会在子线程结束后才会退出，这在某些时候不是我们想要的，这时候将子线程设置为守护线程，守护线程的子线程不会阻止主线程的退出。

```python
from threading import Thread
import time

class MyThread(Thread):
    def __init__(self, name, sleep):
        self.sleep = sleep
        super().__init__(name=name)

    def run(self):
        print(self.name)
        time.sleep(self.sleep)
        print(self.name + 'end')

if __name__ == '__main__':
    t1 = MyThread('t1', 1)
    t2 = MyThread('t2', 2)
    t2.setDaemon(True)
    t1.start()
    t2.start()

# 将t2设置为守护线程的结果， 可以看出t1结束后主线程退出，没有打印出t2的结果
# t1
# t2
# t1end
```

join方法则会将线程阻塞，知道该线程执行完成后才继续往下运行

```python
if __name__ == '__main__':
    t1 = MyThread('t1', 1)
    t2 = MyThread('t2', 2)

    t1.start()
    t1.join()
    t2.start()

# t1阻塞后的结果，t1线程运行结束后才开始运行t2线程
# t1
# t1end
# t2
# t2end
```

## 线程间通信

#### 使用全局变量

在最上面的GIL部分已经使用到了全局变量来实现两个线程的通信，由于多线程资源竞争的关系，单纯的全局变量不是线程安全的，为了让全局变量变成线程安全需要使用线程锁来实现，这点会单独放到线程同步里面详细说明。

#### Queue

queue模块中总共包含三种队列模式，Queue（先进先出）LifoQueue（后进先出）PriorityQueue（自定义优先级），这三种队列都是线程安全的通过名称很容易知道每种模式的区别，这里不做详细说明。

Queue提供了 `get()` `put()`  方法实现获取以及添加，在实例化的时候通过maxsize参数指定队列的最大容量，默认为0不限制大小。

`get()` `put()`  方法默认都是阻塞的，可以通过block=False 以及 timeout参数实现非阻塞，超时后会抛出异常。同时也有`get_nowait()` `put_nowait()` 两个非阻塞的方法，没有get或者put成功会立即抛出异常

下面通过模拟一个简单的爬虫来了解如何通过queue实现两个线程间的通信

```python
from queue import Queue
import threading
import time

detail_list_queue = Queue(maxsize=4)

def get_detail_html(queue, name):
    while True:
        url = queue.get()
        print('{} start -- {}'.format(name, url))
        time.sleep(2)
        queue.task_done()
        print('{} end -- {}'.format(name, url))

def get_detail_url(queue):
    print('start get list')
    for i in range(4):
        queue.put('www.demo.com/detail/{}'.format(i))
        time.sleep(1)
    print('end get list')

if __name__ == '__main__':
    t1 = threading.Thread(target=get_detail_url, args=(detail_list_queue,))
    t2 = threading.Thread(target=get_detail_html, args=(detail_list_queue, 't2'))
    t3 = threading.Thread(target=get_detail_html, args=(detail_list_queue, 't3'))
    t1.start()
    t2.start()
    t3.start()
    detail_list_queue.join()
    print('---end---')
```

这段代码里面有一个线程模拟获取URL，另外两个线程模拟从队列里面获取URL并请求对应的HTML，从结果中能够看出，t2、t3线程依次从队列中获取URL并请求。

```
start get list
---end---
t2 start -- www.demo.com/detail/0
t3 start -- www.demo.com/detail/1
t2 end -- www.demo.com/detail/0
t2 start -- www.demo.com/detail/2
t3 end -- www.demo.com/detail/1
t3 start -- www.demo.com/detail/3
t2 end -- www.demo.com/detail/2
end get list
t3 end -- www.demo.com/detail/3
```

`join()` `task_done()` 和线程的 join 一样 queue 的 join 方法也会阻塞，queue 会记录未完成的个数，`put()` 成功后次数加一  ,  `task_done()`  次数减一。当未完成个数为0时会解除阻塞。需要注意使用了 join 后 必须调用 task_done 来解除阻塞

## 线程同步

线程同步主要解决的就是最上面介绍的资源竞争问题，防止在不同的线程中同时对同一个变量操作引发资源竞争，导致最终的结果不是预期情况。

#### Lock

Python多线程中一般通过 "锁" 来实现线程间的同步，Lock 可以让被加锁的代码段同一时刻只有一个能够运行，只有当这把锁释放了才会去运行其他代码，这就避免了当一个代码段没有执行完就切换到另外的线程中去。

这里我们对GIL部分的事例代码做一下优化，让最终的结果符合预期表现。

```python
import threading
from threading import Lock

a = 0
lock = Lock()

def add():
    global a
    for i in range(1000000):
        lock.acquire()
        a += 1
        lock.release()

def desc():
    global a
    for i in range(1000000):
        lock.acquire()
        a -= 1
        lock.release()

if __name__ == '__main__':
    t1 = threading.Thread(target=add)
    t2 = threading.Thread(target=desc)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(a)
```

上面的事例使用到了 Lock 的 `acquire()` `release()` 两个方法，分别对应 获取锁， 释放锁。当获取不到锁的时候会被阻塞，所以在使用锁的时候必须释放，否则我们的代码就会出现死锁。

常见的死锁导致的原因：

- 获取锁之后没有释放

- 互相等待

  我们模拟一个银行相互转账的例子来说明（不考虑真实场景）

  ```python
  import threading
  import time
  lock_a = threading.Lock()
  lock_b = threading.Lock()
  
  class Account(object):
      def __init__(self, name, money):
          self.name = name
          self.money = money
      def recv(self, amount):
          self.money += amount
          print(self.name, 'add', amount)
      def send(self, amount):
          self.money -= amount
          print(self.name, 'desc', amount)
  
  # 相互转账我们分为两个步骤，即A -> B , B -> A
  def a_to_b(account_a, account_b, amount):
      lock_a.acquire()  # 先获取锁将A账户金额锁住
      time.sleep(1)  # 模拟A账户扣减耗时
      account_a.send(amount)
      lock_b.acquire()
      account_b.recv(amount)  # 锁住B账户金额
      lock_a.release()
      lock_b.release()
  
  def b_to_a(account_b, account_a, amount):
      lock_b.acquire()  # 先获取锁将B账户金额锁住
      time.sleep(1)
      account_b.send(amount)
      lock_a.acquire()
      account_a.recv(amount)  # 锁住A账户金额
      lock_b.release()
      lock_a.release()
  
  if __name__ == '__main__':
      account_a = Account('a', 1000)
      account_b = Account('b', 2000)
      t1 = threading.Thread(target=a_to_b, args=(account_a, account_b, 100))
      t2 = threading.Thread(target=b_to_a, args=(account_b, account_a, 50))
      t1.start()
      t2.start()
      t1.join()
      t2.join()
      print('a', account_a.money)
      print('b', account_b.money)
      print('end')
  
  # -- result --   
  # a desc 100
  # b desc 50
  ```

  先获取账户A的锁等待获取B的锁，此时在另外的一个线程中已经获取了B账户的锁但是又在等待A账户的锁，这就导致两个线程中锁互相等待的情况出现，程序无法向下运行了

- 调用其他外部方法，外部方法中也调用了锁

  ```python
  lock = threading.Lock()
  
  def func1():
      lock.acquire()
      # do something
      lock.release()
  
  def func2():
      lock.acquire()
      func1()
      lock.release()
  ```

#### RLock

Rlock 和 Lock 功能上是类似的，Rlock在`同一个线程`内可以 acquire 多次，release 的次数一定要与 acquire 次数一致。

#### Condition

这个类可以让一个或多个线程等待，直到其他线程通知，通过这样我们可以让多个线程之间互相切换运行。

Condition 在实例化的时候可以传递一个Lock 或者 RLock 对象，否则会默认创建一个 RLock 作为底层锁。

Condition 提供了四种常用的方法，`wait(timeout=None)`  `notify(n=1)`  `wait_for(predicate, timeout=None)`  `notify_all()`  ，调用这些方法之前必须获取锁，否则会抛出 RuntimeError 异常

- wait 方法的时候 Condition 会先释放底层锁，然后阻塞，直到被另外线程的同一 Condition 通过 notify 或者 notify_all 唤醒。
- notify 方法可指定唤醒多少个等待这个 Condition 的线程，默认为一个。
- wait_for 方法作用同 wait 一样，只是多个 predicate 参数，此参数接收一个 callable 对象，他的返回值必须是可以判断真假的，调用次方法是将会一直等待只有当 predicate 返回为真时才将 predicate 返回值返回。
- notify_all  顾名思义唤醒所有等待这个 Condition 的线程。

例如下面的这个两个线程循环输出连续的数字

```python
import threading

cond = threading.Condition()

list_1 = [1, 3, 5, 7, 9]
list_2 = [2, 4, 6, 8, 10]

def func1():
    global list_1
    global cond
    with cond:
        for i in list_1:
            print(i)
            cond.notify()
            cond.wait()

def func2():
    global list_2
    global cond
    with cond:
        for i in list_2:
            cond.wait()
            print(i)
            cond.notify()

threading.Thread(target=func2).start()
threading.Thread(target=func1).start()
```

#### Semaphore & BoundedSemaphore

信号量，Python 多线程的一个内置计数器，通过 acquire 和 release 实现计数加减

- acquire(blocking=True, timeout=None)  当 blocking 设置为False 时将不会阻塞并立即返回 False，否则将阻塞直到计数大于 0 并返回 True ，timeout 将在超时后返回 False。
- release() 释放信号量，计数加一。

BoundedSemaphore 继承 Semaphore 类，重载了 release()  方法，使得不能无限制的 release ，当计数值大于等于初始值时会抛出异常。

下面是通过信号量实现同时只有三个线程运行的示例。

```python
import threading, time

sem = threading.Semaphore(value=3)

def func():
    sem.acquire()
    print('func start')
    time.sleep(1)
    sem.release()

for i in range(10):
    threading.Thread(target=func).start()
```

#### Event

多线程中的事件对象，管理一个标志位，通过 set () 、clear() 、 wait() 、is_set() 来获取或者管理标志位。

Event 初始化的时候标志位是False。

- set() 设置标志位为True。
- clear() 设置标志位为False。
- wait() 等待标志位设为True。
- is_set() 判断标志位是否为True。

过于简单不写对应的例子了。



回顾上面的 Condition 、Semaphore、Event 从源码上来看底层都是基于 Lock 和 Rlock 来实现的，只是封装了常用的一些用法方便开发者调用，万变不离其宗线程间的同步我们只需要抓住 “ 锁 ” 这个概念，理解和使用起来就没什么大问题。

## 线程池

在上面我们通过信号量实现了一个简单的线程池，只是功能比较简单。其实 Python 给我们提供了线程池功能，位于 concurrent.futures 模块下面 ThreadPoolExecutor，下面将简单的介绍 Python 线程池所提供的功能。

#### 创建线程池

实例化 ThreadPoolExecutor 时有四个可选参数，分别是

- max_workers 设置最大线程数量，默认为当前计算机CPU数量的5倍。
-  thread_name_prefix 设置线程名称前缀。
- initializer 设置每个线程初始化之前的都会调用的方法，参数值必须为可调用的。
- initargs 传给 initializer 的参数。

通过 submit 方法将需要执行的方法提交到线程池中，非阻塞，会立即返回一个 futures 对象

```python
from concurrent.futures import ThreadPoolExecutor
import time

def start(*args):
    print(args)

def run(times):
    print('run for {} seconds'.format(times))
    time.sleep(times)
    return times

executor = ThreadPoolExecutor(max_workers=2, initializer=start, initargs=('start',))
executor.submit(run, 2)
```

也可以使用 map 方法批量提交，返回一个 线程执行结果的生成器，此方法是阻塞的，只有等到所有的线程都执行完毕才会继续。

```python
for result in  executor.map(run, (1,2,3,4)):
    print(result)
```

关闭线程池  shutdown(wait=True) ，关闭后 submit 、map 将会抛出 RuntimeError ，wait 为 True 时将会阻塞直到所有线程执行结束，为 False 立即返回

#### 获取子线程返回结果

- 使用 map 提交线程 

- 使用 future.result()

  ```python 
  task = executor.submit(run, 10)
  print(task.result())
  ```

- 使用 as_completed  需要传递一个可迭代的 future 对象，将返回一个已完成的 future 生成器

  ```python
  tasks = [executor.submit(run, i) for i in [1, 2]]
  for future in as_completed(tasks):
      print(future.result())
  ```

#### 其他

- wait() 阻塞主线程直到 传递进去的 future 满足某些条件，可以通过 return_when 参数决定什么时候阻塞完成，返回值是一个有两个值 namedtuple 第一个是已完成或者已取消的 future 集合，第二个是没有完成的 future 集合

  - ALL_COMPLETED（默认）  等待所有 future 完成后返回

  - FIRST_COMPLETED  某一个 future 完成或者取消是返回
  - FIRST_EXCEPTION  抛出异常是返回，如果没有异常抛出则和 ALL_COMPLETED 等效

  ```python
  from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
  import time
  
  def run(times):
      print('run for {} seconds'.format(times))
      time.sleep(times)
      return times
  
  executor = ThreadPoolExecutor(max_workers=2)
  
  tasks = [executor.submit(run, i) for i in [1, 2]]
  future_tuple = wait(tasks, return_when=FIRST_COMPLETED)
  print(future_tuple.done)
  print(future_tuple.not_done)
  
  # -- result --
  # run for 1 seconds
  # run for 2 seconds
  # {<Future at 0x10a96eb38 state=finished returned int>}
  # {<Future at 0x10ab38240 state=running>}
  ```

- cancle() 由 future 提供的方法，可以将还没有运行的线程取消掉，取消成功返回True。

- done() 由future 提供的方法，判断是否运行结束。


