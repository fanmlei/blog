---
title: Arduino语音天气预报（二）
date: 2017-12-14 16:49:21
categories: 
- Arduino
tags:
- 硬件
- Arduino
---

咱们接着上一篇来讲

作为天气预报的装置，若是只能在串口显示信息，那就没什么卵用了，还不如拿个手机看看省事，因此这篇将会讲一下如何使用外接屏幕显示信息。所用到的屏幕为串口彩屏，相较于普通的彩屏来说，串口屏的操作更为方便，也能更简单的制作画面较为复杂的界面，而且对于mcu没有任何要求只要能进行串口通信即可，因为串口屏内部本身是有主控的，串口屏可以根据指令自己绘图、操作控件。我们可以在页面上添加各种功能的控件，然后通过各种控件来显示信息达到我们想要的效果，如下图一样

![](1.png)

举一个简单的例子：如果我们t5显示“1234”我们只需让mcu串口发送“t5.txt="1234"”就可以了

当我们将所有的信息都发送后就能得到下面这样的效果图

![](2.png)

看到这里我们应该能够知道上一篇从心知天气获取到的信息远远没有这么多，这一次我们还需要从另外的地址获取更多的信息。
```
https://api.seniverse.com/v3/weather/daily.json?key=APIPASSWORD&location=地址&language=返回的数据语言格式&unit=温度单位&start=起始时间（0：当天、1明天···）&days=获取多少天的信息（从起始时间开始，免费的最多只有三天）
```

还是和上一篇一样黑色加粗的部分是需要根据自己情况进行修改的。这里由于Arduino处理中文很麻烦，因此语言我们最好选择英文，然后再同过其它代码转换成中文或其它。
还需要提醒一下最好一天一天的获取信息，如start=0&days=1，因为Arduinojson貌似是处理不了一个字符串包含多个json的数据格式。
当连接成功后我们将会得到这样的数据：
```json
{"results":[{"location":{"id":"WX4FBXXFKE4F","name":"Beijing","country":"CN","path":"Beijing,Beijing,China","timezone":"Asia/Shanghai","timezone_offset":"+08:00"},"daily":[{"date":"20170417","text_day":"Cloudy","code_day":"4","text_night":"Cloudy","code_night":"4","high":"27","low":"13","precip":"","wind_direction":"SW","wind_direction_degree":"225","wind_speed":"15","wind_scale":"3"}],"last_update":"2017-04-17T18:00:00+08:00"}]}
```
这些信息里面包括白天天气、夜晚天气、最高气温、最低气温、风向、风速和风力等级，按照我们上一篇将的操作即可。这里我们只是获取了当天的全天天气，我们还要重复这样的操作获取第二天和第三的信息，好了到这里我们所有信息的获取就完成了，接下来就是如何将获取的信息传给屏幕并转化成中文。

```cpp
data_day1 = httpData_day1.substring((httpData_day1.indexOf("\"daily\"") + 9), httpData.indexOf("],\"last"));
DynamicJsonBuffer jsonBuffer;
JsonObject& root = jsonBuffer.parseObject(data_day1);
date1 = root[("date")].as<String>();
temperature_low_day1 = root[String("low")];
temperature_high_day1 = root[String("high")];
code_day1 = root[String("code_day")];
code_night1 = root[String("code_night")];
wind_direction_day1 = root[("wind_direction")].as<String>();
wind_scale_day1 = root[String("wind_scale")];
```

数据的发送：
我们所用到的指令大概有切图、控件的赋值这三种指令，切图指令是让屏幕显示当前天气的图片信息，天气图片可以在心知天气上下载，由于目前串口屏的上位机并不支持矢量图，因此我们需要将天气图片和背景图P在一起然后按照顺序导入这些图片。切图指令为picq x,y,w,h,pic_id  pic_id为我们导入的图片序号，由于是显示天气实况pic_id的值应该是上一篇我们解析出来的天气代码“code”

![](3.png)

天气图片的显示就完成了，下面就是发送其他的信息了。
我们用到的大部分是文本控件使用到的指令为控件ID.txt=" "和控件ID.txt=控件ID.txt+" "前一种会将以前的字符给覆盖掉，后一种则是在原有的基础上增加。由于Arduino解析中文、发送中文字符比较麻烦，所以我选择是发送数字和字符，然后通过让串口屏进行处理并组合成中文，
举个例子
```cpp
//假设白天为晴天，对应的天气代码为0，夜晚为多云，对应天气代码为4，那么整天的天气情况用中文表示应该是晴转多云
if(code_day1==0)
{
        if(code_night1==4)
                g0.txt="晴转多云";
}
```

总共大概有30中天气情况，这样就会有几百种组合了，看似麻烦其实只需要写一遍然后Ctrl+c 、Ctrl+v再稍微调整一下就行了，风向风力同样是这样处理的。（如果嫌麻烦，直接下载链接的tft文件直接烧进屏幕即可），关于屏幕显示的东西就这么多了，其他的以后再补充吧！！！

[演示视频（增加了loading动画）](http://v.youku.com/v_show/id_XMjcxNTk0MzIyOA==.html)

