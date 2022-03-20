
<p>这篇主要说说如何通过微信公众号来查看室内传感器数据，至于硬件部分和物联网平台以后再详细说明。</p>
<p><br>
</p>
<h2>准备工作：</h2>
<p>1：申请微信公众号</p>
<p>2：搭建云服务器</p>
<p><br>
</p>
<p>首先说明一下整体流程：用户发送相应的指令到公众号后台，服务器根据指令的内容调用OneNET的API获取传感器数据在返回给用户</p>
<p><br>
</p>
<h2>详细步骤：</h2>
<h3><span style="font-size:10px; font-weight:normal"><span style="white-space:pre"></span>申请公众号后我们需要启用服务器配置，具体步骤请看微信的开发者文档，这个地方需要注意一下在填写URL的时候不要添加端口号，这样会导致验证不通过的（开发者文档上这个是错误的）</span></h3>
<div><span style="font-size:10px; font-weight:normal"><span style="white-space:pre"></span>在云服务器上安装运行环境：</span></div>
<div><br>
</div>
<div><span style="font-size:10px; font-weight:normal"><span style="white-space:pre"></span>安装pip</span></div>
<div><span style="font-size:10px; font-weight:normal"><span style="white-space:pre"><img src="https://img-blog.csdn.net/20171217162858414?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center" alt=""></span></span></div>
<div><span style="font-size:10px; font-weight:normal"><span style="white-space:pre"><span style="white-space:pre"></span></span></span></div>
<div><span style="font-size:10px; font-weight:normal"><span style="white-space:pre"></span>安装libxml2</span></div>
<div><span style="font-size:10px; font-weight:normal"><span style="white-space:pre"><img src="https://img-blog.csdn.net/20171217162935160?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center" alt=""></span></span></div>
<div><span style="font-size:10px; font-weight:normal"><span style="white-space:pre"><br>
</span></span></div>
<div><span style="font-size:10px; font-weight:normal"><span style="white-space:pre"><span style="white-space:pre"></span>安装lxml</span></span></div>
<div><span style="font-size:10px; white-space:pre"><span style="font-size:10px; white-space:pre"><img src="https://img-blog.csdn.net/20171217162943429?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center" alt=""></span></span><span style="font-size:10px">&nbsp;&nbsp;</span></div>
<div><span style="white-space:pre"></span></div>
<div><span style="white-space:pre"></span>安装web.py</div>
<div><span style="white-space:pre"></span><img src="https://img-blog.csdn.net/20171217163002373?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center" alt="" style="font-size:10px"></div>
<div><br>
</div>
<div><span style="white-space:pre"></span>我们使用的物联网平台是中国移动的OneNet，它提供了很多API接口可以让我们获取数据、发送指令，在GitHub上有人用python写了常用的API调用示例，这里我们拿来直接使用就好了<a target="_blank" target="_blank" href="https://github.com/jiangxiaobai1989/pythonOneNetAPI">https://github.com/jiangxiaobai1989/pythonOneNetAPI</a></div>
<div><span style="white-space:pre"></span>首先呢我们需要能够接收用户发过来的消息，使用者发送消息后后台收到的为lxml&#26684;式</div>
<div><span style="white-space:pre"></span><pre name="code" class="html">&lt;xml&gt;
&lt;ToUserName&gt;&lt;![CDATA[粉丝号]]&gt;&lt;/ToUserName&gt;
&lt;FromUserName&gt;&lt;![CDATA[公众号]]&gt;&lt;/FromUserName&gt;
&lt;CreateTime&gt;1460541339&lt;/CreateTime&gt;
&lt;MsgType&gt;&lt;![CDATA[text]]&gt;&lt;/MsgType&gt;
&lt;Content&gt;&lt;![CDATA[test]]&gt;&lt;/Content&gt;
&lt;/xml&gt;</pre><br>
</div>
<div><span style="white-space:pre"></span>然后呢我们需要解析这些内容</div>
<div><span style="white-space:pre"></span><pre name="code" class="python"># -*- coding: utf-8 -*-
# filename: receive.py
import xml.etree.ElementTree as ET

def parse_xml(web_data):
    if len(web_data) == 0:
        return None
    xmlData = ET.fromstring(web_data)
    msg_type = xmlData.find('MsgType').text
    if msg_type == 'text':
        return TextMsg(xmlData)
    elif msg_type == 'image':
        return ImageMsg(xmlData)
    elif msg_type == 'voice':
	return VoiceMsg(xmlData)

class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text
	

class TextMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.Content = xmlData.find('Content').text.encode(&quot;utf-8&quot;)

class VoiceMsg(Msg):
	def __init__(self, xmlData):
		Msg.__init__(self, xmlData)
		self.Recognition = xmlData.find('Recognition').text.encode(&quot;utf-8&quot;)</pre><br>
</div>
<div><span style="white-space:pre"></span>获取消息后我们需要服务器做出相应的反应，首先需要判断消息类型和消息内容，然后通过API获取数据后再返回个用户，例如下面这段获取室内温湿度的例子</div>
<div><pre name="code" class="python"># -*- coding: utf-8 -*-
# filename: handle.py
import hashlib
import reply
import receive
import web
from getData import *
class Handle(object):
    def POST(self):
        try:
            webData = web.data()
            print &quot;Handle Post webdata is &quot;, webData   #后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.MsgType == 'text':
                	if recMsg.Content == '温度':
				content = str(getData_time('temperature'))+'\n室内温度为'+str(getData_value('temperature')) +'℃'
		  	elif recMsg.Content == '湿度':
				content = str(getData_time('humidity'))+'\n室内湿度为'+str(getData_value('humidity')) +'%'
			else:
				content = '抱歉尚未开通这项指令功能，你可以尝试发送‘温度’、‘湿度’来查看最新的室内信息,或者发送相应的语音消息 '
                   	replyMsg = reply.TextMsg(toUser, fromUser, content)
                   	return replyMsg.send()
                if recMsg.MsgType == 'voice':
                    	if recMsg.Recognition =='温度。':
				content = str(getData_time('temperature'))+'\n室内温度为'+str(getData_value('temperature')) +'℃'
			elif recMsg.Recognition =='湿度。':
				content = str(getData_time('humidity'))+'\n室内湿度为'+str(getData_value('humidity')) +'%'
			else:
				content =recMsg.Recognition+'\n无法识别这条语音消息'
                    	replyMsg = reply.TextMsg(toUser, fromUser, content)
                    	return replyMsg.send()
                else:
                    	return reply.Msg().send()
            else:
                print &quot;暂且不处理&quot;
                return reply.Msg().send()
        except Exception, Argment:
            return Argment</pre><br>
<span style="white-space:pre"></span>通过API调用我们获取到的json数据，这样是不能直接给用户发送过去的，还需要对json进行处理提取主要的数据，例如提取温湿度数据和数据节点时间</div>
<div><pre name="code" class="python"># -*- coding: UTF-8

from OneNetApi import *
import json

def getData_value(datastreamid):
    test = OneNetApi(&quot;***************************&quot;) #  your API
    datastream_id = datastreamid
    limit = 1
    res3 = test.datapoint_get(device_id = &quot;6975064&quot;, limit = limit, datastream_id = datastream_id)
    data = json.loads(res3.content.replace(']',' ').replace('[',' '))
    value = data['data']['datastreams']['datapoints']['value']
    return value
	
	
def getData_time(datastreamid):
    test = OneNetApi(&quot;***************************&quot;) #  your API
    datastream_id = datastreamid
    limit = 1
    res3 = test.datapoint_get(device_id = &quot;6975064&quot;, limit = limit, datastream_id = datastream_id)
    data = json.loads(res3.content.replace(']',' ').replace('[',' '))
    time = data['data']['datastreams']['datapoints']['at'][0:19]
    return time</pre><br>
<span style="white-space:pre"></span>至于返回用户消息呢，依然是按照lxml&#26684;式，将我们获取到的数据和需要返回的用户信息添加进去就可以了<pre name="code" class="python">class TextMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
        XmlForm = &quot;&quot;&quot;
        &lt;xml&gt;
        &lt;ToUserName&gt;&lt;![CDATA[{ToUserName}]]&gt;&lt;/ToUserName&gt;
        &lt;FromUserName&gt;&lt;![CDATA[{FromUserName}]]&gt;&lt;/FromUserName&gt;
        &lt;CreateTime&gt;{CreateTime}&lt;/CreateTime&gt;
        &lt;MsgType&gt;&lt;![CDATA[text]]&gt;&lt;/MsgType&gt;
        &lt;Content&gt;&lt;![CDATA[{Content}]]&gt;&lt;/Content&gt;
        &lt;/xml&gt;
        &quot;&quot;&quot;
        return XmlForm.format(**self.__dict)</pre><br>
</div>
<div><span style="white-space:pre"></span><span style="white-space:pre"></span>微信后天还提供了语音识别接口，默认是打开的，当用户发送的是语音命令的时候后台接收的lxml中会比text消息多出<span style="color:rgb(51,51,51); font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif; font-size:14px">Recognition这项，把识别结果当做text一样处理就能让公众号处理语音消息了，再次不再赘述了。</span></div>
<div><span style="white-space:pre"></span>至此整个流程就结束了，当编写所有的代码后使用 python main.py 80 即可打开这项服务了，下面是效果图</div>
<div><span style="white-space:pre"></span><img src="https://img-blog.csdn.net/20171217173126601?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center" alt=""><br>
</div>
<div><br>
</div>
<div>国际惯例：<a target="_blank" href="https://github.com/FanMLei/wx">源码</a></div>
<p><br>
</p>
