<p>之前使用vue构建的前端页面每次加载都需要十几秒的时间，最初的时候因为浏览器有缓存一直没有发现这个问题，后来换用设备访问的时候才发现。不想花费太多的时间去优化vue的代码，感觉作用不大，毕竟服务器带宽只有1M，再怎么压缩文件大小都需要很长时间传输，所以使用CDN去加速静态资源</p>

<p>先看一下之前的加载速度，简直惨不忍睹<img alt="" class="has" height="69" src="https://img-blog.csdnimg.cn/20181217200021726.png" width="850" /></p>

<p>首先需要在云服务商那购买CDN服务，我的服务器是腾讯云的正好腾讯云也有免费的CDN可以试用，购买环节跳过。</p>

<p>要使用CDN服务首先需要在域名管理处添加域名：</p>

<p><img alt="" class="has" height="103" src="https://img-blog.csdnimg.cn/20181217200522978.png" width="800" /></p>

<p>域名配置需要按照自己的服务器填写，加速服务的配置看自己的需求了，一般来说选择css、js、和图片资源就够了<img alt="" class="has" height="407" src="https://img-blog.csdnimg.cn/20181217200806211.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70" width="700" /></p>

<p>提交配置等待几分钟后在域名管理处查看CNAME<img alt="" class="has" height="61" src="https://img-blog.csdnimg.cn/20181217201433716.png" width="850" /></p>

<p>接下来需要配置DNS解析服务<br />
在开启的时候如果出现冲突，按照提示关闭另外的一个即可<br /><img alt="" class="has" height="56" src="https://img-blog.csdnimg.cn/20181217201655175.png" width="850" /></p>

<p>至此CDN的配置完成了，如果访问还是很慢先去CDN刷新缓存检查一下</p>

<p>最后的成果：1.16秒</p>

<p><img alt="" class="has" height="106" src="https://img-blog.csdnimg.cn/20181217202537753.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70" width="850" /></p>

<p> </p>