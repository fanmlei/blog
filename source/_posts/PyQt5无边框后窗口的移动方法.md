---
title: PyQt5无边框后窗口的移动方法
date: 2017-11-20 02:21:08
categories: 
- 未分类
tags:
- PyQt
---
<p>由于隐藏了标题栏无法通过点击标题栏来实现窗口的移动，这时候我们可以通过鼠标事件来移动窗口</p>
<p>第一步：判断鼠标左键是否被按下，如果按下则将flag设为True并获取当前的位置</p>
<p>第二步：判断鼠标是否移动并且左键被按下，若移动了计算移动的距离在移动窗口</p>
<p>第三步：若鼠标释放了则将flag设为False</p>
<p>具体做法：重写窗口类自带的三个函数</p>
<p><pre name="code" class="python">    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  #更改鼠标图标
            
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:  
            self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
            QMouseEvent.accept()
            
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))</pre><br>
最后最小化和关闭可以设置两个按钮，通过点击按钮来触发</p>
<p><pre name="code" class="python">    @pyqtSlot()
    def on_pushButton_clicked(self):
        &quot;&quot;&quot;
        关闭窗口
        &quot;&quot;&quot;
        self.close()
    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        &quot;&quot;&quot;
        最小化窗口
        &quot;&quot;&quot;
        self.showMinimized()</pre></p>
<p><br>
</p>
<p>ps :设置无边框和背景透明</p>
<p><pre name="code" class="python"># 设置窗体无边框
# self.setWindowFlags(Qt.FramelessWindowHint)
# 设置背景透明
# self.setAttribute(Qt.WA_TranslucentBackground)</pre><br>
效果图</p>
<p><img src="https://img-blog.csdn.net/20180303221110347" alt=""><br>
</p>
<p>win10自带的录屏只能录当前软件那个区域。。。。。。。</p>
<p>就这样吧</p>
