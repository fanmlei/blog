<p>安装 apt-get install docker.io</p>

<p>获取镜像：docker pull &lt;name&gt;</p>

<p>运行一个容器： docker run &lt;参数&gt; &lt;image name&gt; <br />
参数</p>

<ul><li><code>-d, --detach=false</code>， 指定容器运行于前台还是后台，默认为false</li>
	<li><code>-i, --interactive=false</code>， 打开STDIN，用于控制台交互</li>
	<li><code>-t, --tty=false</code>， 分配tty设备，该可以支持终端登录，默认为false</li>
	<li><code>-u, --user=""</code>， 指定容器的用户</li>
	<li><code>-a, --attach=[]</code>， 登录容器（必须是以docker run -d启动的容器）</li>
	<li><code>-w, --workdir=""</code>， 指定容器的工作目录</li>
	<li><code>-c, --cpu-shares=0</code>， 设置容器CPU权重，在CPU共享场景使用</li>
	<li><code>-e, --env=[]</code>， 指定环境变量，容器中可以使用该环境变量</li>
	<li><code>-m, --memory=""</code>， 指定容器的内存上限</li>
	<li><code>-P, --publish-all=false</code>， 指定容器暴露的端口</li>
	<li><code>-p, --publish=[]</code>， 指定容器暴露的端口</li>
	<li><code>-h, --hostname=""</code>， 指定容器的主机名</li>
	<li><code>-v, --volume=[]</code>， 给容器挂载存储卷，挂载到容器的某个目录</li>
</ul><p>将容器变为镜像 ： docker commit -a "creator name" -m "information"  containerID   imagename:tag</p>

<p>删除单个容器：docker rm containerID </p>

<p>删除所有容器：docker rm $(docker ps -a -q)</p>

<p>删除镜像：docker rmi imageID  /  docker rmi imageName:Tag</p>