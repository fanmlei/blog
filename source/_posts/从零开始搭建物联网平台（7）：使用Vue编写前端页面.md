<h3>摘要：</h3>

<p style="text-indent:50px;">Vue我也是刚开始学的，看了两天的文档就开始着手做这件事了，所以对vue了解不太深入，没有能力说的的太详细万一是错误的不就误导别人了，所以只对几个相对来说比较主要的点说明一下。</p>

<h3>搭建开发环境：</h3>

<p style="text-indent:50px;">老生常谈的话题！首先自然是要安装nodejs，这个直接去官网下载安装即可，再使用命令npm install vue、npm install -g vue-cli去安装vue和脚手架工具，完成之后再使用命令vue init webpack myproject来初始化项目，初始化完成之后会在目录下生成这些文件，到这一步的话环境差不多搭建好了。<br /><img alt="" class="has" height="351" src="https://img-blog.csdnimg.cn/20181102150006888.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70" width="325" /></p>

<p style="text-indent:50px;">接下来是安装依赖，在这个项目里面我用了以下几个库， 通过命令npm install  xxx --S 安装，环境差不多搭建完成。<br />
                  "axios": "^0.18.0",         发送请求的类似ajax<br />
                  "echarts": "^4.2.0-rc.2",      可视化工具，用于绘制数据曲线图<br />
                  "element-ui": "^2.4.9",        网页UI<br />
                  "vue-router": "^3.0.1",         路由，这个一般在初始化项目的时候就安装了，如果没有自己手动安装</p>

<h3>开始我们的开发之旅：</h3>

<p style="text-indent:50px;">首先确定一下页面布局，分为三大块，其中顶栏和侧栏显示内容不变，只变主题部分，布局样式使用elementUI中的<code>&lt;el-header&gt;</code>：顶栏容器， <code>&lt;el-aside&gt;</code>：侧边栏容器，<code>&lt;el-main&gt;</code>：主要区域容器实现。</p>

<p><img alt="" class="has" src="https://img-blog.csdnimg.cn/20181121122335392.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70" /></p>

<p style="text-indent:50px;">顶栏基本没啥内容就一个图标不说了，说一下侧边导航栏，导航栏使用el-menu组件实现，将el-menu的 route属性设置为true，或者使用router-link去做跳转，不过那样显得要麻烦一些，所以还是推荐第一种</p>

<p style="text-align:center;"><img alt="" class="has" height="62" src="https://img-blog.csdnimg.cn/2018112217051257.png" width="1020" /></p>

<pre class="has">
<code class="language-javascript"> &lt;el-menu class="el-menu-vertical-demo"
                 background-color="#304156"
                 text-color="#bfcbd9"
                 active-text-color="#409eff"
                 :default-active="$route.path"
                 router &gt;
    &lt;el-menu-item index="/developer/dashboard"&gt;
      &lt;i class="el-icon-ump-18"&gt;&lt;/i&gt;
      &lt;span slot="title"&gt;主页&lt;/span&gt;
    &lt;/el-menu-item&gt;
    &lt;el-menu-item index="/developer/charts"&gt;
      &lt;i class="el-icon-ump-shuju2"&gt;&lt;/i&gt;
      &lt;span slot="title"&gt;历史数据&lt;/span&gt;
    &lt;/el-menu-item&gt;
    &lt;el-menu-item index="/developer/devices"&gt;
      &lt;i class="el-icon-ump-shebei2"&gt;&lt;/i&gt;
      &lt;span slot="title"&gt;设备管理&lt;/span&gt;
    &lt;/el-menu-item&gt;
    &lt;el-menu-item index="/developer/streams"&gt;
      &lt;i class="el-icon-ump-shuju1"&gt;&lt;/i&gt;
      &lt;span slot="title"&gt;数据流管理&lt;/span&gt;
    &lt;/el-menu-item&gt;
    &lt;el-menu-item index="/developer/triggers"&gt;
      &lt;i class="el-icon-ump-chufaqi"&gt;&lt;/i&gt;
      &lt;span slot="title"&gt;触发器管理&lt;/span&gt;
    &lt;/el-menu-item&gt;
    &lt;el-menu-item index="/developer/console"&gt;
      &lt;i class="el-icon-ump-kongzhitai1"&gt;&lt;/i&gt;
      &lt;span slot="title"&gt;控制台&lt;/span&gt;
    &lt;/el-menu-item&gt;
&lt;/el-menu&gt;</code></pre>

<p style="text-indent:50px;">最后的效果：</p>

<p style="text-indent:50px;"><img alt="" class="has" height="403" src="https://img-blog.csdnimg.cn/20181122170829897.png" width="230" /></p>

<p style="text-indent:50px;">下面开始内容主体，放个样图。</p>

<p style="text-align:center;"><img alt="" class="has" src="https://img-blog.csdnimg.cn/20181122171312133.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70" /></p>

<p style="text-indent:50px;">样式部分就不说了看个人喜好，主要说一下如何获取后台的数据，数据的获取需要用到之前安装的axios插件，通过axios的get、post等方法访问后端的接口获取json数据例如get方法，then和catch是es6的语法，具体的我也解释明白。如果数据获取正常，后端返回的数据放在res.data里面，打印到控制台看看返回结果，post同理，只是参数不同</p>

<pre class="has">
<code class="language-javascript">axios.get(url, {
　　params: { 'key': 'value' }
}).then((res)=&gt; {
　　console.log(res.data);
}).catch((error)=&gt; {
　　console.log(error);
});</code></pre>

<p style="text-indent:50px;">一般来说获取数据可以放在created()或者mounted()里面，看自己需求吧，created要先于mounted，created那时候还没有生成dom，如果需要操作dom那么还是放到mounted里面吧。</p>

<p style="text-indent:50px;"> </p>

<p style="text-indent:50px;">算了就写这么多吧，自己都不专业还是不误导别人了</p>

<p style="text-indent:50px;"> </p>

<p style="text-indent:50px;"> </p>