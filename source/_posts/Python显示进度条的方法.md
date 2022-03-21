
<p>使用&nbsp;progressive&nbsp;库实现</p>
<p>第一步&nbsp;导入模块</p>
<p><span style="background-color:rgb(240,240,240)">from progressive.bar import Bar</span></p>
<p>第二步&nbsp;实例化</p>
<p><span style="background-color:rgb(240,240,240)">&nbsp; &nbsp; bar = Bar(title=&quot;Progress&quot;, max_value=MAX_VALUE, fallback=True)</span></p>
在源文件中可以<br>
可以自定义标题、宽度、颜色等等、、、
<p><img src="https://img-blog.csdn.net/20180210212015819" alt=""><br>
</p>
<p>第三步&nbsp;初始化的一些操作</p>
<p><span style="background-color:rgb(240,240,240)">bar.cursor.clear_lines(1)</span></p>
<p><span style="background-color:rgb(240,240,240)">bar.cursor.save()</span></p>
<p><span style="background-color:rgb(240,240,240)">bar.cursor.restore()</span></p>
<p>第四步&nbsp;显示进度条</p>
<p><span style="background-color:rgb(240,240,240)">bar.draw(value=NOW_VALUE, newline=False)</span></p>
在draw这个方法里面value是指当前进度条位置，newline可设置是否在新的一行里面重新显示
<p>显示效果</p>
<p><img src="https://img-blog.csdn.net/20180210212729278" alt=""><br>
</p>
<p><br>
</p>
<br>
<br>
<p><br>
</p>
