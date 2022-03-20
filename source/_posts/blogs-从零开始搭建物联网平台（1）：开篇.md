<h3>前言：</h3>

<p style="text-indent:50px;">读大学的时候学的是物联网工程，大概是在大二的时候开始接触单片机，那时候特喜欢捣鼓那些东西，就觉得特别酷有极客范。还记得第一次做物联网相关的是一个远程控制的开关，第一次调通的时候真的很兴奋，啥也没干就挂在那用手机控制继电器听咔嗒咔哒的声音，现在想想真的好小儿科，明明只是按照人家的教程改改代码却也能兴奋那么就。但是有一句话不是说所有的编程语言第一个代码都是Hello World，一切都要从最基础的开始，当我们有能力的时候才能做更大的事。</p>

<p style="text-indent:50px;">言归正传，之前也用过一些很成熟的物联网平台例如移动的OneNET、 Yeelink，做的都很好功能也很强大，我也做过一些扩展功能，例如那时候OneNET是没有手机端的，于是就根据OneNET提供的API实现了微信公众号的访问和控制（最开始的几篇博客有介绍），可是觉得这些一点也不极客，无非是在调用API。搭建一个个人的物联网平台这个想法很久之前就有了，只是一直迟迟未开始，现在我觉得是时候开始着手实现这个想法了。关于这个物联网平台我的想法是够用就好，也许它很简单，功能有点low，设计不合理等等，毕竟是我自己做出来的，开心就好【手动滑稽】，当然呢我也会尽力去完善。立一个Flag半年之内完成。</p>

<p style="text-indent:50px;"><span style="color:#f33b45;">最后也是最重要的一点，这不是一个教程，只是我个人的一些开发记录，里面可能会有很多漏洞，不合理的地方，而且之前的操作可能会在后面给推翻重做，所以啊，参考就行了不要当真。</span></p>

<h3>整体构思：</h3>

<p style="text-align:center;"><img alt="" class="has" height="431" src="https://img-blog.csdnimg.cn/20181104024403255.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70" width="805" /></p>

<p style="text-indent:0;">图画的有点low不要介意，简单说一下<br />
        硬件：这里选择Arduino平台开发，之所以不先考虑stm32或者51之类的，是因为那两个我都没完整的了解过，等以后会提供更多的连接例程，目前手上现有一个NodeMCU、和一个ArduinoMEGA2560，考虑到Arduino和ESP8266连线太麻烦了，就以NodeMCU为例。<br />
        平台：协议就使用MQTT好了，后台用Django，数据库MySQL。<br />
        手机：还是借助微信公众号之前也有一些经验，最主要的是APP开发不会。<br />
        电脑：应该会和OneNET类似，前端大概率会用vue开发，这个应该会放到最后实现，vue还在学习阶段。<br />
        大致功能包括： 用户注册、添加设备、上传数据、查看历史数据、发送控制指令、微信提醒，目前想到的就只有这么多了，以后还有新的再来添加。</p>

<p style="text-indent:0;"> </p>

<h3 style="text-indent:0px;"><strong>更新一下：</strong></h3>

<p><strong>项目差不多完成了75%左右，在制作过程中对原有的一些设计做了优化和调整目前项目的整个架构图如下</strong></p>

<p><img alt="" class="has" height="567" src="https://img-blog.csdnimg.cn/20190218132744174.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0Zhbk1MZWk=,size_16,color_FFFFFF,t_70" width="918" /></p>