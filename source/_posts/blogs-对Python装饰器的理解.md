
想要弄明白装饰器是什么东西，首先我们需要了解一下什么是闭包，因为装饰器是闭包的一种应用。
#### 闭包
闭包的定义：

​	通俗的来说闭包就是在一个函数内部定义另外一个函数，这个函数又引用了外部函数的变量，并且外函数的返回值是内函数的引用，下面是一个最简单的闭包示例：

```python
def outer():
    a = 10
    def inner():
        print(a)
    return inner

demo = outer()
demo()
```

那么再回到装饰器上面，我们都知道在python中任何东西都是对象，一个函数也好一个字符串也好都是对象，在传递过程中都是传递其内容的引用，当传递的是函数的时候只需在变量名后边加上()即可调用这个函数。

好了基础知识了解了，那么下面来看一个简单的装饰器应用：

#### 装饰器

```python
def auth(func):
    print('before run')
    def wrapper():
        func()
    return wrapper

@auth
def response():
    print('this is a test function')
    
response()  

###### result ######
# before run
# this is a test function
```

乍一看是不是和闭包一样，只不过把变量替换成函数名了

##### 参数的传递

上面的示例中被装饰函数是没有传递参数的，倘若被装饰函数需要传递参数的时候那么就需要稍微做一下调整。

```python
def auth(func):
    print('before run')
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
    return wrapper

@auth
def response(*args, **kwargs):
    print('this is a test function')
    print(args)
    
response(1,2)  

###### result ######
# before run
# this is a test function
# (1, 2)
```

#### 装饰器的高级用法

有时候实际使用装饰器的时候可能并不会像上面的那样简单，例如我们可能需要给装饰器本身传递参数，来让装饰器更为灵活。先尝试不改代码看看运行的结果

```python
@auth(1,2)
def response(*args, **kwargs):
    print('this is a test function')
    print(args)

response(1, 2)

###### result ######
# error:
# TypeError: auth() takes 1 positional argument but 2 were given
```

auth只有一个参数，但是传递了两个参数，这是为什么呢？我们需要先看看@auth这行代码是什么意思，@auth其实是response=auth(response)的简写，你看这样的写法就只接收一个参数，那么我们不使用这种简写方式可以吗？

```python
def auth(func, *args):
    print('before run')
    print(args)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
    return wrapper

def response(*args, **kwargs):
    print('this is a test function')
    print(args)

response = auth(response, 1)
response(1, 2)

###### result ######
# before run
# (1,)
# this is a test function
# (1, 2)
```

你看还真是实现了这个功能，只不过没办法使用简写来装饰函数了。那有没有更好的解决方法呢，我们再回到装饰器的原理上（一个闭包）那如果我们在闭包函数外面再套一层函数是不是就可以解决了呢。尝试一下

```python
def outer(*args, **kwargs):
    print('before run')
    print(args)
    def inner(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        return wrapper
    return inner

@outer(1, 2)
def response(*args, **kwargs):
    print('this is a test function')
    print(args)

response(3, 4)

###### result ######
# before run
# (1,)
# this is a test function
# (1, 2)
```

实现了和上一个一样的功能，此时的@outer(1,2)还原成本来样子就是 response = outer(1,2)(response)，我们打上断点看看装饰器是如何运行的

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190307021938395.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70)

#### 多个装饰器同时使用

先上代码看结果

```python
def decorator1(func):
    print('Decorator1')
    def wrapper(*args,**kwargs):
        print('----1----')
        func(*args, **kwargs)
    return wrapper

def decorator2(func):
    print('Decorator2')
    def wrapper(*args,**kwargs):
        print('----2----')
        func(*args, **kwargs)
    return wrapper

@decorator1
@decorator2
def test(*args):
    print(args)

test(1,2)

###### result ######
# Decorator2
# Decorator1
# ----1----
# ----2----
# (1, 2)
```

执行顺序并不是先执行完装饰器1然后在执行装饰器2，而是交替运行的，我们分析一下具体执行过程一探究竟。就装饰顺序来说还是按照decorator1、decorator2来对原函数装饰的，那么装饰的结果是什么呢，这里需要了解一下@符号的作用，在python中@会将紧跟着的函数名作为参数传给装饰函数，经过两个装饰器作用之后 test变成了 ：test = decorator1(decorator2(test))

此时在调用test的时候，就会从里往外执行，

1. 即先执行decorator2(test)，会先打印出Decorator2
2. 返回decorator2中的内函数给decorator1，然后打印Decorator1
3. 返回decorator1内函数给test
4. 在调用test函数的时候就会先执行decorator1的内函数，打印出了----1----
5. 然后运行decorator2的内函数,打印出----2----
6. 最后才会运行test原函数

![在这里插入图片描述](https://img-blog.csdnimg.cn/2019030702192439.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70)
总结来说，在装饰过程中越靠近被装饰函数越先执行，内函数恰恰相反**
#### 保留原函数的信息

回到之前一个最简单的装饰器上，我们看看直接输出被装饰的函数信息是什么?

```python
def auth(func):
    def wrapper():
        func()
    return wrapper

@auth
def response():
    pass

print(response.__name__)

###### result ######
# wrapper
```

输出的是装饰器的内函数，原因就不说了，和之前的一样@的作用，难么我们该怎么让打印函数信息能够显示的是被装饰函数本身呢？这里就要用到functools的wraps方法，用法很简单：

```python
from functools import wraps
def auth(func):
    @wraps(func)
    def wrapper():
        func()
    return wrapper

@auth
def response():
    pass

print(response.__name__)

###### result ######
# response
```
#### 总结

装饰器到此差不多都说完了，其作用就不展开说了，经过这么一连串的分析自己也对装饰器的原理有了更深的了解，算是没白浪费时间。
