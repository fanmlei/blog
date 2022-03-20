
<p><span style="color:#ff0000">自学笔记：逻辑可能比较混乱，想到哪说到哪，可能存在不少的问题欢迎指出。</span></p>
<h3>创建一个类：</h3>
<h4>最简单的一个类</h4>
<div>在python中类的命名必须以字母或者下画线开头，并且只能包含字母、下画线和数字。另外推荐使用驼峰命名方式（大写字母开头，随后的任意一个单词都以大写字母开头）</div>
<div>python最简单的一个类的创建</div>
<div><pre name="code" class="python">class MyFirstClass:
	pass</pre>
<h4>类的属性和方法</h4>
在类中我们还可以为其添加属性和方法</div>
<div><pre name="code" class="python">class MyFirstClass:
    def __init__(self):
        self.x = 1
        self.y = 1

    def show(self):
        print(self.x,self.y)

c = MyFirstClass()
c.show()</pre></div>
<div>其中self.x和self.y为该类的属性，show()为该类的方法</div>
<div>类中的方法的定义方式和普通函数相同，都是以关键字def开头，但是有一点不同的是类中的方法有一个必需的参数，通常这个参数被命名为self,但是我们实例化类后调用show方法的时候并没有传入参数，这是因为python自动帮我们做了，当我们调用c对象的show方法的时候，python会自动将c对象传给show方法了。因此下面这个调用方式运行结果是一样的。</div>
<div><pre name="code" class="python">c = MyFirstClass()
MyFirstClass.show(c)</pre>其实类中的方法本质上就是一个函数，我们可以在外部调用也可以在类中调用，例如：</div>
<div><pre name="code" class="python">class Point:
    def __init__(self, x ,y ):
        self.x = x
        self.y = y

    def reset(self):
        self.x = 0
        self.y = 0
        self.show()

    def show(self):
        print(self.x, self.y)

p = Point(1,1)
p.reset()</pre></div>
<div>运行结果为：0&nbsp; 0</div>
<div>
<h4>类的初始化</h4>
<div>一般的编程语言中都有一个叫构造函数的特殊方法，当它被创建的时候会创建和初始化对象，这一点Python会有些许不同，python有一个构造函数和一个初始化函数，一般情况下构造函数很少被用到，除非是想实现一些特别的操作，所以在此主要说一下类的初始化。我们在之前的示例中有一个方法名为__init__(),其实这个方法就是给类进行初始化操作的。当我们实例化的时候会首先执行__init__()方法，因此当__init__()方法需要传递参数的时候我们在实例化的时候同样需要传递参数，不然会报错。</div>
<div>由于方法本质上就是函数，当我们不想传递参数的时候也可以同函数的操作一样使用默认参数。</div>
<div><pre name="code" class="python">def __init__(self, x=0, y=0):
    self.x = x
    self.y = y</pre></div>
</div>
<h3>面向对象三个基本特征</h3>
<div>面向对象编程的三个基本特征分别为：封装、继承、多态，下面一一说明。</div>
<h4>继承</h4>
<div>继承就是让一个类获得另一个类的属性和方法，在Python中所有的类都是object类的子类，只是在实际的使用中我们并不需要表明，python在后台自己帮我们做了</div>
<div><br>
</div>
<div><br>
</div>
<div><br>
</div>
<p><br>
</p>
