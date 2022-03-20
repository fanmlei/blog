
首先说一下项目预期的目标，通过板载的WiFi模块联网获取天气信息，使用屏幕将信息显示出来，配合板载的语音模块播放当天天气状况。<br style="word-wrap:break-word; margin:0px; padding:0px; color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">
<span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">总体的设计思路：天气获取的网站是心知天气网免费的API（需要注册），400次/小时的请求足够日常使用了，当然也可以使用付费接口那样能获取更多的信息。当开发板通过API接口发送请求时网站会返回json&#26684;式的信息，然后再通过json库将有用的信息解析出来，就能得到当天的天气信息了。然后将获取到的数据发送给屏幕进行处理，根据数据控制语音模块播放相应的语音文件。</span><br style="word-wrap:break-word; margin:0px; padding:0px; color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">
<br style="word-wrap:break-word; margin:0px; padding:0px; color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">
<span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">下面简单的介绍一下心知天气的API</span><br style="word-wrap:break-word; margin:0px; padding:0px; color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">
<span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">这个链接是获取实时天气状况</span><br style="word-wrap:break-word; margin:0px; padding:0px; color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">
<span style="word-wrap:break-word; margin:0px; padding:0px; color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px"><span style="color:#4169e1; word-wrap:break-word; margin:0px; padding:0px">https://api.seniverse.com/v3/weather/now.json?key=</span></span><span style="color:#000000; word-wrap:break-word; margin:0px; padding:0px; font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px"><span style=""><span style="word-wrap:break-word; margin:0px; padding:0px; font-weight:700">APIPASSWORD</span></span></span><span style="word-wrap:break-word; margin:0px; padding:0px; color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px"><span style="color:#4169e1; word-wrap:break-word; margin:0px; padding:0px">&amp;location=</span></span><span style="color:#000000; word-wrap:break-word; margin:0px; padding:0px; font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px"><span style=""><span style=""><span style="word-wrap:break-word; margin:0px; padding:0px; font-weight:700">地址</span></span></span></span><span style="word-wrap:break-word; margin:0px; padding:0px; color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px"><span style="color:#457ffd; word-wrap:break-word; margin:0px; padding:0px"><span style="">&amp;language=</span></span><span style="word-wrap:break-word; margin:0px; padding:0px; font-weight:700"><span style="color:#000000; word-wrap:break-word; margin:0px; padding:0px">返回的数据语言&#26684;式</span></span><span style="color:#457ffd; word-wrap:break-word; margin:0px; padding:0px"><span style="">&amp;unit=</span></span></span><span style="word-wrap:break-word; margin:0px; padding:0px; font-weight:700; color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">温度单位</span><br style="word-wrap:break-word; margin:0px; padding:0px; color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">
<span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">黑色加粗的部分是需要根据自己情况进行修改的。</span><br style="word-wrap:break-word; margin:0px; padding:0px; color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">
<span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">当发送正确的请求后将会收到服务器返回的json数据</span><br style="word-wrap:break-word; margin:0px; padding:0px; color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">
<span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">{&quot;results&quot;:[{&quot;location&quot;:{&quot;id&quot;:&quot;WX4FBXXFKE4F&quot;,&quot;name&quot;:&quot;北京&quot;,&quot;country&quot;:&quot;CN&quot;,&quot;path&quot;:&quot;北京,北京,中国&quot;,&quot;timezone&quot;:&quot;Asia/Shanghai&quot;,&quot;timezone_offset&quot;:&quot;&#43;08:00&quot;},&quot;now&quot;:</span><span style="word-wrap:break-word; margin:0px; padding:0px; font-weight:700; color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">{&quot;text&quot;:&quot;多云&quot;,&quot;code&quot;:&quot;4&quot;,&quot;temperature&quot;:&quot;25&quot;}</span><span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">,&quot;last_update&quot;:&quot;2017-04-14T12:20:00&#43;08:00&quot;}]}</span><br style="word-wrap:break-word; margin:0px; padding:0px; color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">
<span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">黑色加粗就是我们需要解析的天气信息，本次需要用到的就这些了。更加详细的介绍请看</span><a target="_blank" href="https://www.seniverse.com/api" target="_blank" style="word-wrap:break-word; margin:0px; padding:0px; color:rgb(85,85,85); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">心知天气-天气数据API</a><br style="word-wrap:break-word; margin:0px; padding:0px; color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">
<br style="word-wrap:break-word; margin:0px; padding:0px; color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">
<span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">这次我们用到的库有</span><span style="word-wrap:break-word; margin:0px; padding:0px; font-weight:700; color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">ArduinoJson、ArduinoHttpClient、WiFi</span><br style="word-wrap:break-word; margin:0px; padding:0px; color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">
<p><span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">首先我们需要在setup中连接上WiFi</span></p>
<p><span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px"><br>
</span></p>
<p><span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px"></span></p>
<pre name="code" class="cpp">Serial.begin(9600);
&nbsp;Serial.print(&quot;connect....&quot;);
&nbsp;while (WiFi.begin(ssid, pass) != WL_CONNECTED)
&nbsp;Serial.println(&quot;connected&quot;);</pre><span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px"></span>
<p></p>
<p><span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px"><span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px"><br>
</span></span></p>
WiFi连接后发送API请求，并解析数据
<p><span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px"><br>
</span></p>
<p><span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px"></span><pre name="code" class="cpp">int httpCode = 0;
  String httpData;
  //发送http请求
  httpCode = http.get(&quot;/v3/weather/now.json?key=&quot; + APIPASSWORD + &quot;&amp;location=zhengzhou&amp;language=en&amp;unit=c&quot;);
  //若是有返回就接收数据
  if ( httpCode == 0)
  {
    Serial.println(&quot;startedRequest ok&quot;);
    httpCode = http.responseStatusCode();
    if (httpCode &gt;= 0)
    {
      int bodyLen = http.contentLength();
      //将接收到的字符存入string中，直到数据接收完毕
      while ( (http.connected() || http.available()) &amp;&amp; (!http.endOfBodyReached()))
      {
        if (http.available())
        {
          char c = http.read();
          httpData += c;
        }
        else
          delay(1000);
      }
      //提取出关于天气的那一段字符串
      data = httpData.substring((httpData.indexOf(&quot;\&quot;now\&quot;:&quot;) + 6), httpData.indexOf(&quot;,\&quot;last&quot;)); 
      //通过json库解析出相应的数据
      DynamicJsonBuffer jsonBuffer;
      JsonObject&amp; root = jsonBuffer.parseObject(data);
      temperature = root[String(&quot;temperature&quot;)];
      code = root[String(&quot;code&quot;)];
    }
  }
  else
    Serial.print(&quot;Connect failed&quot;);
  http.stop();
  //串口打印出温度
  Serial.print(&quot;temperature is :&quot;):
  Serial.println(temperature);
  Serial.print(&quot;end&quot;);</pre><span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px"></span></p>
<p><span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px"><span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px"><br>
</span></span></p>
关于json库的使用我了解的不是很多，就不做详细的说明。我在做的时候发现若是将整个返回的数据进行解析并得不到正确的信息，我猜测是因为返回的数据包含有其他的信息并不是json库所能解析的&#26684;式，因此我将接收到的字符存入到一个String类型的字符串中，然后截取其中一段（也就是上面黑色加粗的那一段）进行解析。需要注意的是json解析String类型的方式和char类型是不同的，具体还请参考ArduinoJson的示例。<br style="word-wrap:break-word; margin:0px; padding:0px; color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">
<span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px">最后的结果</span>
<p><span style="color:rgb(68,68,68); font-family:&quot;Microsoft Yahei&quot;,Simsun; font-size:14px"><img src="https://img-blog.csdn.net/20171214164623695?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center" alt=""><br>
</span></p>
<br>
<br>
<br>
