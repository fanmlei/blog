
<p><span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">这篇我们会讲如何使用板载的语音模块播放</span></p>
<p><span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">这次用到的是串口语音模块，首先我们需要使用语音合成工具合成我们想要的语音存入内存卡中，然后呢当我们获取数据后发送相应的指令控制语音模块来播放对于的音频文件。</span></p>
<p><span style="font-family:Microsoft Yahei,Simsun; color:#444444"><span style="font-size:14px">在这里不再说明如何合成音频文件了，直接切入正题。</span></span></p>
<p><span style="font-family:Microsoft Yahei,Simsun; color:#444444"><span style="font-size:14px">这次我们主要用到的只有一条命令&nbsp; ———————&gt;&nbsp; &nbsp;<span style="font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:12px">播放指定目录下的文件&nbsp;&nbsp;0x7E, 0x04, 0x44, 文件夹号, 文件号, 0xEF</span></span></span></p>
<p><span style="font-family:Microsoft Yahei,Simsun; font-size:12px; color:#444444">因此音频文件存放位置和命名需要有一定的&#26684;式：例如 01号文件夹中存放诸如描述天气情况的语音，02号文件夹存放温度语音等等。命名也是有技巧的，例如我们可以根据天气代码来描述天气的语音，例如“今天天气晴”可命名为001，正好我们获取到的天气代码也是1这样我们就不用来处理这部分对于关系了。</span></p>
<p><span style="font-family:Microsoft Yahei,Simsun; font-size:12px; color:#444444">还需要一点是在播放语音的过程中需要判断当前是否没有播放，这个可以通过模块上的一个引脚电平来判断，具体需要根据你自己的模块来设定，我的这个是当没有播放时电平为低，这样我们可以将引脚接入到Arduino的引脚上，通过读取引脚电压来判断。</span></p>
<p><span style="font-family:Microsoft Yahei,Simsun; font-size:12px; color:#444444">这部分代码就不拿出来单独说明了，因为太简单了，而且会和硬件有较大的关系难免有人在使用的时候出现问题。</span></p>
<p><span style="font-family:Microsoft Yahei,Simsun; font-size:12px; color:#444444"><br>
</span></p>
<p><span style="font-family:Microsoft Yahei,Simsun; font-size:12px; color:#444444">其实呢整个项目到这里已经完成了，但是我还想说一下有人可能直接烧代码会出现很多问题，那是因为我是用的并不是标准的Arduino开发板而是Fireduino使用Arduino平台开发而已，这块板子价&#26684;有点高只是做这个有点浪费而且我的也给弄坏了，理解了整个制作流程其实可以用更廉价的开发板来代替，例如NodeMCU、Arduino&#43;esp8266，而且所有的功能都能实现。</span></p>
<p><span style="font-family:Microsoft Yahei,Simsun; font-size:12px; color:#444444"><br>
</span></p>
<p><br>
</p>
<p><span style="font-family:Microsoft Yahei,Simsun; color:#444444"><a target="_blank" href="http://v.youku.com/v_show/id_XMjc1NTUzOTE5Mg==.html" style=""><span style="font-size:14px"><strong>完整的项目演示</strong></span></a><br>
</span></p>
<p><span style="font-family:Microsoft Yahei,Simsun; font-size:12px; color:#444444">参考代码</span></p>
<p><span style="font-family:Microsoft Yahei,Simsun; font-size:12px; color:#444444"><a target="_blank" href="https://github.com/FanMLei/Weather_Station">https://github.com/FanMLei/Weather_Station</a><br>
</span></p>
<p><span style="font-family:Microsoft Yahei,Simsun; font-size:12px; color:#444444"><br>
</span></p>
<p><span style="font-family:Microsoft Yahei,Simsun; font-size:12px; color:#444444"><br>
</span></p>
