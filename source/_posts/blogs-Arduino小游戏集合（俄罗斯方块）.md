
<h2>一：前期准备</h2>
<p>用到的硬件材料Arduino Mega2560 &#43; LCD4884 Joystick Shiled&nbsp;</p>
<p>屏幕分辨率为48*84</p>
<p>软件平台&nbsp;Arduino IDE， 需要用到的库&nbsp;U8glib &#43;MsTime2</p>
<p><br>
</p>
<h2>二：设计思路</h2>
<h3>1：游戏整体界面</h3>
<div><span style="font-size:10px">标准的俄罗斯方块为<span style="color:rgb(51,51,51); font-family:arial,'宋体',sans-serif; text-indent:28px">行宽为10，列高为20，结合屏幕大小每个最小单位点设为2*2像素，共计七种方块，19种形状，使用[10][20]的二维数组存放方块位置信息，需要显示则将相应位置的数组&#20540;改为1，空白则为0。</span><span style="color:rgb(51,51,51); font-family:arial,宋体,sans-serif; text-indent:28px">并在左侧显示下一个方块形状，右侧显示当前分数和等级</span></span></div>
<div><br>
</div>
<div>游戏界面如图所示</div>
<div><span style="color:rgb(51,51,51); font-family:arial,'宋体',sans-serif; text-indent:28px"><span style="font-size:10px"><img src="https://img-blog.csdn.net/20180211160807423?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
</span></span></div>
<div><br>
</div>
<h3>2：方块的产生、变换和移动</h3>
<div>我没有采用使用整体存放方块图形信息的方法，因为不知道怎么使用U8glib库旋转单个图形，采用的是一种比较笨的方法。</div>
<div>每一种方块选取一个中心点，围绕这个中心点来绘制方块，移动的时候也是直接移动中心点然后重新在中心点绘制方块，总共有16种方块图形这里选取其中一种来做例子说明</div>
<div><br>
</div>
<h3>(1)&nbsp;方块的产生</h3>
<div>例如Z形方块</div>
<div><img src="https://img-blog.csdn.net/20180211161946252?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
</div>
<div>选取B为中心点，只需要获取B的坐标信息，设为(x,y)那么其他几个方块的坐标也能相应求出来，然后将二维数组中的这几个对应&#20540;设为1，循环绘制的时候就能显示出方块图形了</div>
<div><br>
</div>
<div><img src="https://img-blog.csdn.net/20180211162042026?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
</div>
<h3>(2)方块的变换和移动</h3>
<div>我们想要控制方块旋转的时候就需要重新获取方块生成的方式</div>
<div><img src="https://img-blog.csdn.net/20180211161946252?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><img src="https://img-blog.csdn.net/20180211163039154?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><img src="https://img-blog.csdn.net/20180211162938994?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
</div>
<div><br>
</div>
<div><img src="https://img-blog.csdn.net/20180211162042026?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><img src="https://img-blog.csdn.net/20180211163039154?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><img src="https://img-blog.csdn.net/20180211162947414?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
</div>
<div>在方块移动和变换的时候在这之前都需要先在二维数组中清空原有的方块信息，然后重新按照新的生成方式写入数组里面</div>
<div><br>
</div>
<h3>(3):方块检测</h3>
<div>每一次在移动和和变换的过程中还需要判断是否能够移动和变换，需要检测方块周围是否有足够的空间</div>
<div>检测方法如下</div>
<div><img src="https://img-blog.csdn.net/20180211163729222?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
</div>
<div>由于方块无法向上移动，所以上部不需要判断，我们只知道B的坐标，1-7号坐标可以根据B的坐标推断出来</div>
<div>当我们需要右移动的时候就需要判断 2、4、6号位置是否已有方块阻挡或者到达边界，同理下移则需判断5、7号位置</div>
<div><br>
</div>
<h2>三：详细设计</h2>
<h3>1：按键检测</h3>
<div>LCD4884 Joystick Shiled带有一个摇杆按键，并且和A0脚连接，所以读取A0引脚&#20540;即可。</div>
<div>
<pre class="cpp">void Control()
{
  switchVoltage = analogRead(0);
  if ( switchVoltage &gt; 600 &amp;&amp; switchVoltage &lt; 800 )            //上
    dir = 1 ;
  else if ( switchVoltage &gt; 180 &amp;&amp; switchVoltage &lt; 400 )       //下
    dir = 3;
  else if ( switchVoltage == 0 )                               //左
    dir = 4;
  else if ( switchVoltage &gt; 400 &amp;&amp; switchVoltage &lt; 600 )       //右
    dir = 2;
  else if ( switchVoltage &gt; 0 &amp;&amp; switchVoltage &lt; 180 )        //确认
    dir = 5;
}</pre>
为了防止按键粘连，使用了MsTime2库定时扫描</div>
<div>
<pre class="cpp">  MsTimer2::set(100, Control);                /*定时器中断按键的扫描*/
  MsTimer2::start();</pre>
<div><br>
</div>
<h3>2：初始化</h3>
在游戏运行之前，初始化屏幕亮度、游戏等级、随机数种子(防止每一次方块出现次数都相同、清空数组&#20540;以及方块中心点位置，</div>
<div>
<pre class="cpp">  randomSeed(analogRead(1));   <span style="white-space:pre">		</span>/*随机产生随机数序列以免方块的顺序为固定的*/
  block_num = random(1, 20);<span style="white-space:pre">		</span>/*生成第一个方块信息
  block_num_next = random(1, 20) ; <span style="white-space:pre">	</span>/*生成第二个方块
  x = 5 , y = 2;
  block_state_right = 0 ;
  block_state_left = 0;
  block_state_down = 0;
  level_now = 300;
  light_value = 50;    <span style="white-space:pre">			</span> /*设置背光亮度*/
  pinMode(LCD_BACKLIGHT_PIN , OUTPUT);
  analogWrite(LCD_BACKLIGHT_PIN, light_value);</pre>
<br>
<h3>3：绘制游戏界面背景</h3>
<div>显示当前等级和分数，以及下一个方块形状，游戏的等级设置的是每次自动向下移动时延时的毫秒数，move_speed越小等级越高，方块向下移动也越来越快</div>
<div>
<pre class="cpp">void interface()
{
  u8g.setFont(u8g_font_timR08);
  u8g.drawStr(57, 10, &quot;Score&quot;);
  u8g.drawStr(57, 30, &quot;Grade&quot;);
  u8g.drawStr(0, 10, &quot;Next&quot;);
  u8g.setPrintPos(70, 20);
  /*显示分数*/
  u8g.print(score);
  /*显示等级*/
  if ( move_speed &lt;= 300)
    u8g.drawBox(60, 42, 3, 6);
  if ( move_speed &lt;= 250)
    u8g.drawBox(65, 39, 3, 9);
  if ( move_speed &lt;= 200)
    u8g.drawBox(70, 36, 3, 12);
  if ( move_speed &lt;= 150)
    u8g.drawBox(75, 33, 3, 15);
  if (move_speed &lt;= 100)
    u8g.drawBox(80, 30, 3, 18);
  /*显示下一个方块*/
  create_box_next(1);
  for (int m = 0 ; m &lt; 5 ; m&#43;&#43;)
    for (int n = 0 ; n &lt; 5 ; n&#43;&#43;)
    {
      if ( block_next[m][n] == 1)
        u8g.drawBox(3 * m &#43; 5, 3 * n &#43; 15, 3, 3);
    }
  create_box_next(0);
}</pre>
</div>
<div><br>
</div>
<h3>4：方块的生成</h3>
<div>形状太多，代码复用率太高只截取部分，每次移动或者变换的时候都需要调用这个函数来清除上一个方块的位置信息</div>
<div>
<pre class="cpp">void create_box(int a )  /*调整block数组中的&#20540;，参数为0的时候清除，参数为1时写入*/
{
  switch (block_num)
  {
    case 1:
      block[x][y &#43; 1] = a;
      block[x][y - 1] = a;
      block[x - 1][y] = a;
      block[x][y] = a;
      break ;
  }
｝</pre>
<br>
<h3>5：方块的移动和变换</h3>
</div>
<div>每次移动和变换之前都得判断方块能否移动，能够移动还需要在移动之前清空原有的，不能移动的时候需要产生新的方块，这时候方块的中心点需要重置，并且当前形状的标号改为block_num_next的&#20540;，再重新随机生成一个数给block_num_next</div>
<div>
<pre class="cpp">void block_go()             /*方块的移动和变形*/
{
  block_fixed();
  if (block_state_down == 1 )    /*方块不能下降的时候生成新的方块*/
  {
    for (int m = 0; m &lt; 10; m&#43;&#43;)
    {
      if (block[m][3] == 1) /*判断游戏是否结束*/
      {
        game_over();
        break;
      }
    }
    x = 5 , y = 2;    /*设置初始中心点位置*/
    block_num = block_num_next ;
    block_num_next = random(1, 20) ;
    block_state_right = 0 ;
    block_state_left = 0;
    block_state_down = 0;
    create_box(0);
  }}</pre>
变换方块形状，需要注意的是方块标号是连续的，每次变换的时候实际只是更改了当前方块的标号，为了防止从一个类型调到另一个类型需要做一些判断来限制标号更改的范围</div>
<div>
<pre class="cpp">switch (dir)
  {
    case 1:           /*变换方块形状*/
      create_box(0);
      if ( block_num &gt;= 1 &amp;&amp; block_num &lt;= 4)   /*防止变换的时候方块形状发生变换*/
      {
        block_num&#43;&#43;;
        if (block_num &gt; 4)
          block_num = 1;
      }
  }</pre>
<br>
<h3>6：判断方块能否移动</h3>
每一种方块的判断方法都不同，需要根据当前方块标号做出不同的判断，判断结束会返回三个状态，block_state_left、block_state_down、block_state_right，这三个&#20540;为0的时候是可以向这个方向移动的</div>
<div>
<pre class="cpp">void block_fixed()      /*判断方块是否能够移动*/
{
  switch (block_num)
  {
    case 1:
      if (block[x - 2][y] == 1 || block[x - 1][y - 1] == 1 || block[x - 1][y &#43; 1] == 1 || x &lt;= 1)
        block_state_left = 1;
      else
        block_state_left = 0;
      if (block[x &#43; 1][y] == 1 || block[x &#43; 1][y - 1] == 1 || block[x &#43; 1][y &#43; 1] == 1 || x &gt;= 9)
        block_state_right = 1;
      else
        block_state_right = 0;
      if (block[x - 1][y &#43; 1] == 1 || block[x][y &#43; 2] == 1 || y &gt;= 18)
        block_state_down = 1;
      else
        block_state_down = 0;
      break;
  }
}</pre>
<div><br>
</div>
<h3>7：绘制方块</h3>
<div>遍历二维数组，当&#20540;为1的时候则显示最小像素点</div>
<div>
<pre class="cpp">void draw_block()     /*绘制方块*/
{
  int block_x , block_y;
  for (block_x = 0 ; block_x &lt; 10 ; block_x &#43;&#43;)
    for (block_y = 0 ; block_y &lt; 20 ; block_y &#43;&#43;)
    {
      if (block[block_x][block_y] == 1)
        u8g.drawBox(2 * block_x &#43; 28 , 2 * block_y &#43; 4 , 2 , 2);
    }
}</pre>
<br>
<br>
</div>
<h3>8：计算得分</h3>
</div>
<div>遍历整个二维数组，判断有多少行全为1，然后再将数组中每一行都往下挪多少行</div>
<div>
<pre class="cpp">void remove_block()
{
  int sum = 0, m, n, i = 0 , h;       /*i：需要消除的行数，h:记录是哪一行需要消除*/
  /*判断有多少行需要消除*/
  for ( m = 19 ; m &gt; 4; m--)
  {
    for ( n = 0 ; n &lt; 10 ; n&#43;&#43;)
      sum &#43;= block[n][m];
    if (sum == 10)
    {
      i&#43;&#43;;
      score &#43;= 10;
      h = m;
      block_state_down = 1 ;
    }
    else
      sum = 0;
  }
  /*当存在消行的情况下数组每一行都向下移动i个单位*/
  for (i; i &gt; 0; i--)
    for ( m = h; m &gt;= 3; m--)
      for ( n = 0; n &lt; 10; n&#43;&#43;)
        block[n][m] = block[n][m - 1];
}</pre>
<br>
<br>
</div>
<h2>四：结语</h2>
<div>这个游戏是在一年前完成的，到今天很多细节忘得差不多了，只能凭借印象来大致的说明一下主要的流程和思路，代码中有很大一部分重用导致看起来很臃肿现在也懒得改了，有想折腾的可以尝试完善完善，另外其他的屏幕也是能适用的，只需要更改按键控制那个函数和u8glib那个头文件即可，但是分辨率就没办法了</div>
<div>源码连接，喜欢的还请赏个Star</div>
<div><strong><span style="color:#ff0000">https://github.com/FanMLei/Arduino_Games</span></strong><br>
</div>
<div>试玩视频</div>
<div><strong><span style="color:#ff0000">http://v.youku.com/v_show/id_XMzM5NjA0NjY2OA==.html?spm=a2h3j.8428770.3416059.1</span></strong><br>
</div>
<div><br>
</div>
&nbsp;</div>
<div><br>
<br>
</div>
<div><br>
</div>
<p><br>
</p>
