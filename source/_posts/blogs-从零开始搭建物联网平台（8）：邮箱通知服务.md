<p>关于触发器的通知，最开始有三种打算 微信公众号、 邮箱、 HTTP，最后发现微信公众号平台无法主动向用户推送消息，所以微信公众号暂时不做了，看看有没有其他的解决方案</p>

<h3>搭建SMTP服务</h3>

<p style="text-indent:0;">发送邮件可以借助第三方平台如163、QQ等等，但是使用个人账户去做都是有最大发送数量限制的，为了稳妥起见还是决定搭建自己的STMP服务来发送邮件。</p>

<p style="text-indent:0;">以ubuntu 14.04为例：借助于postfix搭建SMTP服务</p>

<ol><li>安装
	<pre class="has">
<code>apt-get install mailutils</code></pre>

	<p>在设置页面选择Internet site<br /><img alt="" class="has" height="269" src="https://img-blog.csdnimg.cn/20181227134333835.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70" width="500" /></p>
	</li>
	<li style="text-indent:0px;"> 配置
	<pre class="has">
<code class="language-bash">vim  /etc/postfix/main.cf


# 修改以下内容
myhostname = mail.youraddress
mydomain = youraddress
myorigin = admin@youraddress

mydestination = $myhostname, localhost.$mydomain, $mydomain</code></pre>

	<p> </p>
	</li>
	<li style="text-indent:0px;">重启服务
	<pre class="has">
<code>service postfix restart</code></pre>
	</li>
	<li style="text-indent:0px;">测试
	<pre class="has">
<code>echo “This is the body of the email” | mail -s “This is the subject line” your_email_address

</code></pre>

	<p>检查是否能够收到邮件，如果没有请检查服务器25端口是否开放，（腾讯云的默认是关闭的需要去申请解封）</p>
	</li>
</ol><h3 style="text-indent:0px;">邮箱服务</h3>

<p style="text-indent:0px;">python 自带两个模块可以实现发送邮件的功能，email和 smtplib，email负责构造邮件内容，smtplib用来发送邮件<br />
下面是最简单的一个发送示例</p>

<pre class="has">
<code class="language-python">import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send(receiver,payload):
    sender = 'admin@iotforfml.cn'
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(payload, 'plain', 'utf-8')
    # 邮件标题
    subject = '触发器报警通知'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtp_obj = smtplib.SMTP('localhost')
        smtp_obj.sendmail(sender, receiver, message.as_string())
    except smtplib.SMTPException:
        pass

send('1193589986@qq.com','aaaa')</code></pre>

<p style="text-indent:0px;">结果：<br /><img alt="" class="has" height="217" src="https://img-blog.csdnimg.cn/20181227161551150.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70" width="599" /></p>

<p style="text-indent:0px;">何时发送，怎么判断是否需要发送报警邮件，这个问题会放到持久化服务里面去判断，接受消息后就应该判断是否触发，具体的实现我想放到后面整合的时候在说，这里只是简单的实现一个发送邮件的接口</p>