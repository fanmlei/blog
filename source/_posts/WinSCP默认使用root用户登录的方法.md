
<p><span style="white-space:pre"></span><span style="font-size:18px">使用WinSCP远程登录ubuntu系统后，再进行文件的拖拽操作的时候会提示错误&nbsp;</span>&nbsp;</p>
<h2><span style="white-space:pre"></span><img src="https://img-blog.csdn.net/20171229194959072?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center" alt=""><br>
<p><span style="white-space:pre"></span><span style="font-size:18px; font-weight:normal">原因是没有这个权限，需要我们使用root用户进行操作，但是WinSCP并不能默认使用root用户进行登录，解决方法是：</span></p>
<p><span style="font-size:18px; font-weight:normal"><span style="white-space:pre"></span>1：使用 sudo passwd root 设置好密码（已设置可忽略这步）。</span></p>
<p><span style="font-size:18px; font-weight:normal"><span style="white-space:pre"></span>2：然后在/etc/ssh/sshd_config中找到PermitRootLogin 这一行将后面的参数改为yes 保存退出。</span></p>
<p><span style="font-size:18px; font-weight:normal"><span style="white-space:pre"></span>3：重启service ssh restart 。</span></p>
<p><span style="font-size:18px; font-weight:normal"><span style="white-space:pre"></span>4：重新打开winscp 重新编辑登录信息，使用root用户登录就可以直接拖拽文件。</span></p>
</h2>
