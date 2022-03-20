<h3>基础知识</h3>

<p>想要弄清楚rest framework的执行过程首先需要明白Django中CBV和FBV执行流程，http请求最最本质的就是一个socket，一个请求过来第一步就是做路由匹配，在FBV中因为视图本身就是一个函数，所以直接调用函数就可以了，但是CBV中视图是一个类而在这个类里面是我们编写的视图函数，所以比FBV多了一步如何找到那个函数并且执行它。</p>

<p style="text-indent:0;">CBV中是基于反射实现请求方式不同执行不同的方法，我们在使用CBV来实现的时候，通常都是在路由中使用as_view方法。<br /><img alt="" class="has" height="29" src="https://img-blog.csdnimg.cn/20181127162910526.png" width="608" /></p>

<p>这个方法存在于我们继承的父类View中，在as_view内部又会调用dispatch方法通过反射去找到对应的函数<br /><img alt="" class="has" src="https://img-blog.csdnimg.cn/20181127163104969.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70" /><br /><img alt="" class="has" src="https://img-blog.csdnimg.cn/20181127164045587.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70" /></p>

<p>所以总得来说，在CBV中一个请求过来的具体流程：url  → view → as_view → dispatch</p>

<p><img alt="" class="has" src="https://img-blog.csdnimg.cn/20181127164908520.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70" /></p>

<h3>源码分析</h3>

<p>有了上面的基础接下来就比较容易理解了</p>

<p>首先在使用rest framework框架的时候 CBV不在是继承django的View了而是 rest framework的APIView，只是这个APIView也是继承django的View的，只不过是在原有的View中增加了很多功能而已，依然还是通过反射来实现的，所以跳过前面的内容直接到dispatch这部分</p>

<p><img alt="" class="has" height="458" src="https://img-blog.csdnimg.cn/20181127170329362.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70" width="984" /></p>

<p><img alt="" class="has" height="328" src="https://img-blog.csdnimg.cn/20181127170932609.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70" width="774" /></p>

<p>正式进入正题，restframework主要包含认证、解析器、分页和序列化四个大的部分，就对应上图框框内的几个部分，这几个部分流程大致相同，所以就以认证为例来具体说说他的流程</p>

<p>咱们接着上图继续往下一步一步走，首先会获取所有认证类的实例化对象。<br /><img alt="" class="has" height="142" src="https://img-blog.csdnimg.cn/20181128000047237.png" width="981" /></p>

<p>如果自己写的类里面没有认证类，就会到基类中继续寻找，默认使用rest framework的配置文件中的认证类<br /><img alt="" class="has" height="30" src="https://img-blog.csdnimg.cn/20181128000109794.png" width="821" /><br />
拿到了认证所需要的类的对象，就继续返回到dispatch中，这时候request已经是增加内容了的request</p>

<p>返回dispatch之后回调用initial方法，在这个方法里面会执行所有之前我们添加的认证类、解析类<br /><img alt="" class="has" height="375" src="https://img-blog.csdnimg.cn/20181128002438807.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70" width="793" /></p>

<p>initial方法里面跳转比较频繁，这里截图就重叠到一起方便看，经过一路的跳转最终是执行了request对象的_authenticate方法</p>

<p><img alt="" class="has" height="426" src="https://img-blog.csdnimg.cn/20181128002611464.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70" width="882" /></p>

<p>在_authenticate方法里面，会依次执行所有认证类的authenticate方法（由此我们也能知道如果我们想编写自己的认证类，那么认证部分需要放在authenticate方法里面），同时会将返回值赋值给request的user和auth属性<br /><img alt="" class="has" height="445" src="https://img-blog.csdnimg.cn/20181128004850888.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70" width="849" /></p>

<p>所以rest framework的认证流程总得来说就是：<br /><img alt="" class="has" height="535" src="https://img-blog.csdnimg.cn/20181128005730158.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70" width="1033" /></p>