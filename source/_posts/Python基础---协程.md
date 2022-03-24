---
title: Python基础---协程
date: 2018-03-07 02:21:08
categories: 
- Python
tags:
- 编程基础
---
协程是一种用户态的轻量级线程，本质上是单线程<br>
<p>协程拥有自己的寄存器上下文和栈。协程调度切换时，将寄存器上下文和栈保存到其他地方，在切回来的时候，恢复先前保存的寄存器上下文和栈。</p>
<p>因此：协程能保留上一次调用时的状态（即所有局部状态的一个特定组合），每次过程重入时，就相当于进入上一次调用的状态，换种说法：进入上一次离开时所处逻辑流的位置。&nbsp;&nbsp;</p>
<p>使用greenlet实现协程操作，greenlet需要手动进行切换</p>
<p>首先需要使用greenlet创建类&#20284;与堆栈空间，然后使用switch进行切换</p>
<p><pre name="code" class="python">from greenlet import greenlet

def test1():
    print(12)
    gr2.switch()
    print(34)
    gr2.switch()

def test2():
    print(56)
    gr1.switch()
    print(78)

gr1 = greenlet(test1)
gr2 = greenlet(test2)

gr1.switch()</pre><img src="https://img-blog.csdn.net/20180311225407524?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""></p>
<p><br>
</p>
<p>使用Gevent实现协程，无需手动切换，遇到IO操作就会进行切换</p>
<p><pre name="code" class="python">import gevent


def func1(num):
&nbsp; &nbsp; print('in func1',num)
&nbsp; &nbsp; gevent.sleep(1) #模仿IO操作
&nbsp; &nbsp; print('back func1')


def func2():
&nbsp; &nbsp; print('in func2')
&nbsp; &nbsp; gevent.sleep(2) #模仿IO操作
&nbsp; &nbsp; print('back func2')


def func3():
&nbsp; &nbsp; print('in func3')
&nbsp; &nbsp; gevent.sleep(3)
&nbsp; &nbsp; print('back func3')


gevent.joinall([
&nbsp; &nbsp; gevent.spawn(func1,1),&nbsp; #传参的方式
&nbsp; &nbsp; gevent.spawn(func3),
&nbsp; &nbsp; gevent.spawn(func2),
])
</pre><img src="https://img-blog.csdn.net/20180311232911179?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
</p>
<p>先执行func1，打印第一句后遇到IO操作切换到func3又遇到IO，再次切换到func2，遇到IO操作后由于没有可执行的函数，开始等待，func1最先可执行自动跳转到func1打印第二句，然后func2IO操作结束输出func2的第二句，最后func3才结束IO操作，所有func3的第二句最后打印</p>
<p>事件驱动模式：每次有一个事件发生的时候会首先存入到一个消息队列中，然后会有专门的函数循环不断的从队列中取出事件进行处理，执行完一个事件后一般会执行一个回调函数来告知当前事件处理完毕。</p>
<p>异步操作也算是一种事件驱动的模式，遇到IO操作的时候交个操作系统来执行，IO操作结束后会执行一个回调函数告知程序IO结束可继续执行<br>
</p>
<p><br>
</p>
<p><br>
</p>
