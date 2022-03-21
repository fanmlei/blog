<p>django实现websocket大致上有两种方式，一种channels，一种是dwebsocket。channels依赖于redis，twisted等，相比之下使用dwebsocket要更为方便一些。</p>

<h3>安装： </h3>

<pre class="has">
<code>pip install dwebsocket</code></pre>

<h3>配置：</h3>

<pre class="has">
<code class="language-python"># setting.py

INSTALLED_APPS = [
    .....
    .....
    'dwebsocket',
]

MIDDLEWARE_CLASSES = [
    ......
    ......
    'dwebsocket.middleware.WebSocketMiddleware'  # 为所有的URL提供websocket，如果只是单独的视图需要可以不选

]
WEBSOCKET_ACCEPT_ALL=True   # 可以允许每一个单独的视图实用websockets</code></pre>

<h3>简单使用：</h3>

<p>模拟文件下载的简单示例</p>

<pre class="has">
<code class="language-python">from dwebsocket.decorators import accept_websocket
@accept_websocket
def test(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        return render(request, 'websocket.html')
    else:
        download = Haproxy()
        t = threading.Thread(target=download.run)
        t.start()
        sent = []
        while download.status:
            if len(download.res_dict) &gt; len(sent):
                for i in download.res_dict.keys():
                    if i not in sent:
                        sent.append(i)
                request.websocket.send(str(sent[-1]+str(download.res_dict[sent[-1]])).encode('utf-8'))  # 发送消息到客户端
        if not download.status:
            request.websocket.send('下载完成'.encode('utf-8'))</code></pre>

<p>效果图：<br /><img alt="" class="has" src="https://img-blog.csdn.net/20180921152624468?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" /></p>

<h3>详细：</h3>

<p>dwebsocket有两种装饰器：require_websocket和accept_websocekt，使用require_websocket装饰器会导致视图函数无法接收导致正常的http请求，一般情况使用accept_websocket方式就可以了，</p>

<p><strong>dwebsocket的一些内置方法：</strong></p>

<p>request.is_websocket（）：判断请求是否是websocket方式，是返回true，否则返回false<br />
request.websocket： 当请求为websocket的时候，会在request中增加一个websocket属性，<br />
WebSocket.wait（） 返回客户端发送的一条消息，没有收到消息则会导致阻塞<br />
WebSocket.read（） 和wait一样可以接受返回的消息，只是这种是非阻塞的，没有消息返回None<br />
WebSocket.count_messages（）返回消息的数量<br />
WebSocket.has_messages（）返回是否有新的消息过来<br />
WebSocket.send（message）像客户端发送消息，message为byte类型</p>

<p> </p>