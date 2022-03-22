---
title: Django 实现Websocket
date: 2018-09-21 14:42:49
categories: 
- Django
tags:
- Django
- WebSocket
---

django实现websocket大致上有两种方式，一种channels，一种是dwebsocket。channels依赖于redis，twisted等，相比之下使用dwebsocket要更为方便一些。

### 安装
```
pip install dwebsocket
```

### 配置
```python
# setting.py

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
```
### 简单使用

模拟文件下载的简单示例
```python
from dwebsocket.decorators import accept_websocket
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
            request.websocket.send('下载完成'.encode('utf-8'))
```

效果图
![](1.png)

### 其他

dwebsocket有两种装饰器：require_websocket和accept_websocekt，使用require_websocket装饰器会导致视图函数无法接收导致正常的http请求，一般情况使用accept_websocket方式就可以了。

dwebsocket的一些内置方法：
1. request.is_websocket（）：判断请求是否是websocket方式，是返回true，否则返回false
2. request.websocket： 当请求为websocket的时候，会在request中增加一个websocket属性。
3. WebSocket.wait（） 返回客户端发送的一条消息，没有收到消息则会导致阻塞。
4. WebSocket.read（） 和wait一样可以接受返回的消息，只是这种是非阻塞的，没有消息返回None。
5. WebSocket.count_messages（）返回消息的数量。
6. WebSocket.has_messages（）返回是否有新的消息过来。
7. WebSocket.send（message）像客户端发送消息，message为byte类型。
