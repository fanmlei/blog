<p>使用QMoive方法实现</p>

<p>导入库文件</p>

<p> </p>

<pre class="has">
<code class="language-python">from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie</code></pre>

<p><br />
创建一个带label控件的窗口，label作为GIF的显示窗体</p>

<p> </p>

<pre class="has">
<code class="language-python">class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(517, 361)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 0, 500, 300))
        self.label.setObjectName("label")
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))</code></pre>

<p><br />
在setupUi()函数里面加入</p>

<p> </p>

<pre class="has">
<code class="language-python">self.gif = QMovie('qq.gif')
self.label.setMovie(self.gif)
self.gif.start()</code></pre>

<p>第一行 实例化一个QMovie对象，传入GIF图片地址</p>

<p>第二行 使用label的setMovie方法导入QMovie对象</p>

<p>第三行 开始播放GIF动画</p>

<p> </p>

<p>效果图：</p>

<p><img alt="" class="has" src="https://img-blog.csdn.net/20180303221947962?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center" /></p>

<p> </p>

<p>PyQt的一些其他功能<br />
#设置窗体无边框<br />
self.setWindowFlags(Qt.FramelessWindowHint)</p>

<p># 设置背景透明<br />
# self.setAttribute(Qt.WA_TranslucentBackground)</p>

<p># 显示输入对话框<br />
# 字符串类型，标题、提示信息、默认输入<br />
# text,ok=QInputDialog.getText(self, "title", "User name:", QLineEdit.Normal, '&gt;&gt;&gt;:')</p>

<p># 整型类型  标题、提示信息、默认值，（最小值，最大值）可选<br />
# num,ok = QInputDialog.getInt(self,"输入整数",'输入0-100范围内的数字',30,0,100)</p>

<p><br />
# 下拉框<br />
# my_list = ['1','2','3']<br />
# my_str,ok = QInputDialog.getItem(self,"下拉框",'提示',my_list)<br />
 </p>