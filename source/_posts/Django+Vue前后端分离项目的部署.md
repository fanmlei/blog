<p>前后端分离项目的部署主要使用Nginx和uwsgi来实现，把Nginx换成Apache也是可以的，看个人喜好。Nginx主要处理静态文件，uwsgi用来部署Django项目，处理其他请求</p>

<p><strong>安装uwsgi:</strong></p>

<pre class="has">
<code>pip3 install uwsgi</code></pre>

<p><strong>测试uwsgi：</strong></p>

<p>首先创建一个test.py文件</p>

<pre class="has">
<code class="language-python">def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
return [b"Hello World"]</code></pre>

<p>在文件目录下使用命令：</p>

<pre class="has">
<code>uwsgi --http :80 --wsgi-file test.py</code></pre>

<p>访问我们的网站，能够得到Hello World，则uwsgi安装成功<img alt="" class="has" height="88" src="https://img-blog.csdnimg.cn/20181217150734770.png" width="687" /></p>

<p><strong>部署django项目：</strong></p>

<p>为了以后使用方便，可先创建一个目录存放uwsgi配置文件</p>

<pre class="has">
<code>mkdir website_uwsgi
cd website_uwsgi
vim uwsgi.ini</code></pre>

<p>配置文件内容如下</p>

<pre class="has">
<code class="language-bash">[uwsgi]
chdir = /home/iot/IOTPlatform   #项目根目录
module = IOTPlatform.wsgi:application  # wsgi
http = :8000
master = True
Processes = 4  #最大进程数
harakiri = 60  # 
max-requests = 5000

# socket = 127.0.0.1:8000

uid = 1000
gid = 2000

pidfile = /home/iot/website_uwsgi/master.pid
daemonize = /home/iot/website_uwsgi/mysite.log
vacuum = True</code></pre>

<p>部分选项的含义：<br />
chdir : 项目根目录路径<br />
module： 入口文件<br />
http：监听的IP和端口，socket也是，如果使用Nginx做反向代理就应该选择socket方式，因为nginx反向代理使用的是socket方式，在这个项目中没有使用方向代理所以选用了http的方式<br />
master：是否启动主进程<br />
processes:  设置进程数目<br />
harakiri: 请求超时时间<br />
max-requests:每个工作进程设置请求数的上限<br />
pidfile:指定pid文件<br />
daemonize: 日志文件</p>

<p>uwsgi配置文件写好了，使用命令启动： </p>

<pre class="has">
<code>uwsgi --ini uwsgi.ini</code></pre>

<p style="margin-left:0pt;">启动完成之后，使用ps -aux | grep uwsgi 查看是否有4个进程来判断uwsgi是否启动成功，另外可以使用接口工具访问接口看是否有正常的数据</p>

<p style="margin-left:0pt;">其他的一些命令：<br />
uwsgi --reload master.pid 重启服务<br />
uwsgi --stop master.pid 停止服务</p>

<p style="margin-left:0pt;"><strong>部署静态文件：</strong></p>

<p style="margin-left:0pt;">静态文件有两种方式<br />
1：通过django路由访问<br />
2：通过nginx直接访问</p>

<p style="margin-left:0pt;"><strong>方式1：</strong></p>

<p style="margin-left:0pt;">需要在根目录的URL文件中增加 url(r'^$', TemplateView.as_view(template_name="index.html")),作为入口，在setting中更改静态资源位置</p>

<p>STATIC_URL = '/static/'</p>

<p>STATICFILES_DIRS = (<br />
    os.path.join(BASE_DIR, "dist/static"),  # 静态文件目录位置<br />
)</p>

<p><strong>方式2：</strong></p>

<p style="margin-left:0pt;">安装nginx:   apt-get install nginx<br />
配置nginx:   cd /etc/nginx<br />
首先在 nginx的可用配置目录下新建我们的配置文件</p>

<pre class="has">
<code class="language-bash">cd sites-available/
vim mysite.conf</code></pre>

<pre class="has">
<code class="language-bash">server {
    listen 80;
    server_name iotplatform;
    charset utf-8;
    client_max_body_size 75M;   
    location /static {
        alias /home/iot/IOTPlatform/dist/static;
    }    
    location /media {
        alias /home/iot/media;
    }   
    location / {
        root /home/iot/IOTPlatform/dist;  
	    index index.html;
        try_files $uri $uri/ /index.html;
    }
}
</code></pre>

<p>再使用命令测试我们的配置文件是否有问题</p>

<pre class="has">
<code>ln -s /etc/nginx/sites-available/mysite.conf   /etc/nginx/sites-enabled/mysite.conf
nginx -t</code></pre>

<p>没有问题使用  service nginx restart重启nginx服务，这样就能访问到静态文件了</p>

<p> </p>

<p><strong>关于反向代理的问题</strong><br />
反向代理的配置文件：</p>

<pre class="has">
<code>server {
    listen 80;
    server_name iotplatform;
    charset utf-8;
    client_max_body_size 75M;
    location /static {
        alias /home/iot/IOTPlatform/dist/static
    }
    location /media {
        alias /home/iot/media
    }
    location / {
        uwsgi_pass 127.0.0.1:8000;
        include /etc/nginx/uwsgi_params;
    }
}</code></pre>

<p>使用nginx -t测试的时候出现</p>

<p style="margin-left:0pt;">nginx: [emerg] open() "/etc/nginx/conf/uwsgi_params" failed (2: No such file or directory) in /etc/nginx/nginx.conf:81</p>

<p style="margin-left:0pt;">nginx: configuration file /etc/nginx/nginx.conf test failed</p>

<p style="margin-left:0pt;">提示说没有找到uwsgi_params文件我的解决方法是：手动新建一个conf目录并将uwsgi_params文件复制过去</p>