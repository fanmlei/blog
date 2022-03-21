
<h4>安装</h4>
<div>RabbitMQ是使用Erlang开发的，因此我们需要首先安装Erlang。<a target="_blank" href="http://www.erlang.org/downloads">http://www.erlang.org/downloads</a>下载对应的版本，安装完成后即可进入下一步。</div>
<div>下载RabbitMQ&nbsp;<a target="_blank" href="http://www.rabbitmq.com/download.html">http://www.rabbitmq.com/download.html</a>&nbsp;选择默认安装即可，安装完成后可在开始菜单中找到</div>
<div><img src="https://img-blog.csdn.net/20180419202452158?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""></div>
<div>点击 RabbitMQ Service - start就开始运行了</div>
<h4>使用Python进行操作</h4>
<div>这里我们需要用到pika这个模块来实现，安装好之后我们就可以实现最简单的例子了</div>
<h6>第一个程序Hello world</h6>
<p>下面两个例子都来自于官方示例</p>
<p>消息传递模型</p>
<p><img src="https://img-blog.csdn.net/20180421160239802?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" alt=""><br>
</p>
<div>send.py</div>
<div>
<pre class="python">import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(&quot; [x] Sent 'Hello World!'&quot;)
connection.close()</pre>
receive.py</div>
<div>
<pre class="python">import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(&quot; [x] Received %r&quot; % body)

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL&#43;C')
channel.start_consuming()</pre>
依次运行这两个函数结果如下</div>
<div><img src="https://img-blog.csdn.net/20180419203216036?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""></div>
<div><img src="https://img-blog.csdn.net/20180419203343047?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""></div>
<div>下面我们再来具体看一看每条语句的具体作用</div>
<div>
<pre class="python">connection = pika.BlockingConnection（pika.ConnectionParameters（'localhost'））
channel = connection.channel（）</pre>
第一句是建立连接的，rabbitmq支持本地连接也支持连接到其他机器上，在这里我们选择本地连接。</div>
<div>第二句是创建一个新的管道，之后的所有操作都是在这个管道上进行的。<br>
<pre class="python">channel.queue_declare(queue='hello')</pre>
<div>声明一个队列名为hello，如果你确认这个队列存在那么不声明也是可以的，但是最好声明一下以免造成其他的麻烦。</div>
</div>
<div>
<pre class="python">channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')</pre>
</div>
<div>向队列中发送一条消息，其中routing_key指定队列名，body为消息内容</div>
<pre class="python">connection.close()</pre>
<p>关闭连接</p>
<p>receive.py中前面几句和send中的作用是一样的，这里不再赘述。&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</p>
<pre class="python">def callback(ch, method, properties, body):
    print(&quot; [x] Received %r&quot; % body)</pre>
<p>callback是回调函数，当程序从队列中获取消息后都会执行回调函数来处理消息&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</p>
<pre class="python">channel.basic_consume(callback,
                      queue='hello',
                      #no_ack=True
                      )</pre>
<p>从队列中获取消息，callback指定回调函数，queue指定获取的队列名，no_ack在以后再说明&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;</p>
<pre class="python">channel.start_consuming()</pre>
<p>让程序进入到一个死循环中，不断从队列中取出消息</p>
<h6>消息队列的循环调度</h6>
<p>消息传递模型</p>
<p><img src="https://img-blog.csdn.net/20180421160404952?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" alt=""></p>
<p>当我们启动多个程序从同一个队列中接收消息的时候，默认是依次接收，即第一个启动的程序首先接收到然后是第二个启动的程序,直到最后一个程序收到之后又从第一个开始，但是这样会造成一个后果就是，可能每个程序或者机器的处理速度不同，造成有的在等待有的消息过多。如下图启动两个接收程序，并发送从0-4数字，两个程序接收的消息依次为：</p>
<p><img src="https://img-blog.csdn.net/20180421141241831?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" alt=""><img src="https://img-blog.csdn.net/20180421141300490?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" alt=""><br>
</p>
<h6>消息确认</h6>
<p>在实际应用中一般程序接收消息后处理需要时间，如果在处理的过程中程序崩溃了那么那个消息就会从消息队列中消失了，这当然不是我们想要的结果，我们需要在程序崩溃之后将那条消息转发到另一个程序中执行，这时候我们需要设置只有在消息被确认后才将消息从队列中删除，RabbitMQ默认消息确认是打开的，但是我们可以添加参数no_ack = True来取消，这样即使消息为处理完成也不会再次发送了，会直接从队列中去除。我们还可以使用手动消息确认即在callback中添加一句：</p>
<pre class="sourcecode python hljs" style="padding:.5em; background-color:rgb(35,35,35); color:rgb(230,225,220); font-size:14px; white-space:pre-wrap; letter-spacing:.16px; text-align:left"><span style="vertical-align:inherit">ch.basic_ack（delivery_tag = method.delivery_tag）</span></pre>
<h6>消息持久化</h6>
<p>上面我们已经说了如何保证消费者崩溃时还保留消息，现在我们将介绍如何在RabbitMQ服务终止后还会保留消息队列。这里需要我们在声明这个队列的时候添加一个参数来实现</p>
<pre class="sourcecode python hljs" style="padding:.5em; background-color:rgb(35,35,35); color:rgb(230,225,220); font-size:14px; white-space:pre-wrap; letter-spacing:.16px; text-align:left"><span style="vertical-align:inherit">channel.queue_declare（queue = </span><span class="hljs-string" style="color:rgb(165,194,97)">'hello'</span><span style="vertical-align:inherit">，durable = </span><span class="hljs-keyword" style="color:rgb(194,98,48)">True</span><span style="vertical-align:inherit">）</span></pre>
<p>但是这只是保证了hello队列的持久化（下次重启服务的时候队列依然存在），但是队列中消息内容依然是不会被保留下来的，我们想要同时将消息保留下来还需要在channel.basic_publish()函数中添加下面这个参数</p>
<pre class="sourcecode python hljs" style="padding:.5em; background-color:rgb(35,35,35); color:rgb(230,225,220); font-size:14px; white-space:pre-wrap; letter-spacing:.16px; text-align:left"> properties=pika.BasicProperties(delivery_mode = <span class="hljs-number" style="color:rgb(165,194,97)">2</span>)</pre>
<p>需要注意的是消息内用只会暂存于缓存中，并未正真写入磁盘中永久保留，还有就是要实现消息持久化的前提是当前队列也是持久化的（不会报错，但是消息并没有被保留下来）</p>
<h6>公平派遣</h6>
<p></p>
<p>实际应用场景中，有些程序或者是机器处理消息的能力强一些，有些会弱一些，那么按照上面的操作所有的消息都是循环分发的这样就会导致有些机器空闲而有些会出现消息过多处理不过来的情况，为了解决这个问题我们可以在消费者中设置最多可容纳多少条消息，当消息数目满了之后就不会再接收新的消息，直到消息被处理完了留有空余才会再次接收消息。</p>
<pre class="sourcecode python hljs" style="padding:.5em; background-color:rgb(35,35,35); color:rgb(230,225,220); font-size:14px; white-space:pre-wrap; letter-spacing:.16px; text-align:left"><span style="vertical-align:inherit">channel.basic_qos（prefetch_count = </span><span class="hljs-number" style="color:rgb(165,194,97)">1</span><span style="vertical-align:inherit">）</span></pre>
<p>需要注意的是prefetch_count参数&#20540;并未实际意义，只要为True即可，也就是设置后消费者每次只能接收一个消息与参数&#20540;无关。</p>
<h6>广播模式</h6>
<div>消息传递模型</div>
<p><img src="https://img-blog.csdn.net/2018042117585856?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" alt=""></p>
<p>上面所有的都是一对一的消息传递，下面将说一说一对多的传递模型，即广播模式，就好比收音机收听广播一样，需要一个发布者，其他的都是订阅者，发布者发布消息只要订阅者订阅了这个频道那么所有的订阅者都能收到消息。这里的消息传递模型就与之前的略有不同。消息并不是直接发送到队列中，而是经过一个交易所来分发到不同的队列中如上图所示。那么有人会问了，交易所是如何知道要分发到哪一个队列呢，其实只需要将队列和交易所绑定在一起就可以了，每一次消息过来的时候交易所会将消息转发到所有和他绑定的队列中。</p>
<pre class="python">channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

message = &quot;info: Hello World!&quot;
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)</pre>
<p><span style="font-family:'Microsoft YaHei'; font-size:14px">其中exchange_type类型有direct、topic、headers、fanout<span style="letter-spacing:.16px; text-align:left; white-space:pre-wrap"><span style="color:#333333">这四种，下面主要说明fanout类型。</span></span>上面这段程序指定了一个名为logs的交易所，类型为fanout，下面向这个exchange里面publish一条message消息，routing_key为空表示使用默认操作或称为无名交换。完成了发送程序，下面再来说说接收程序。</span></p>
<pre class="python">channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs',
                   queue=queue_name)</pre>
<p><span style="font-family:'Microsoft YaHei'; font-size:14px">在第四行代码中声明了一个随机名称的队列，exclusive=True将会让程序在消费者断开连接的时候删除这个队列&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 在第七行代码中我们将生成的随机队列和我们之前的交换所绑定在一起，这样当一个消息过来的时候交易所会将消息分发到我们绑定过的队列中</span></p>
<h6><span style="font-family:'Microsoft YaHei'; font-size:14px">路由</span></h6>
<p><img src="https://img-blog.csdn.net/20180423153004240?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" alt=""></p>
<p>如上图所示</p>
<p><br>
</p>
<p></p>
<div><br>
</div>
<div><br>
</div>
<div><br>
</div>
<div><br>
</div>
<div><br>
</div>
<div><br>
</div>
<div><br>
</div>
<div><br>
</div>
<div><br>
</div>
<div><br>
</div>
<div><br>
</div>
<div><br>
</div>
<div><br>
</div>
<p></p>
<p></p>
<p></p>
<p><br>
</p>
<p></p>
<p><br>
</p>
