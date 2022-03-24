---
title: virtualenv和virtualenvwrapper的安装和使用
date: 2018-03-09 02:21:08
categories: 
- 未分类
---

<p><span style="white-space:pre"></span>virtualenv可以让用户创建独立的python环境，每个环境互不干扰。<span style="white-space:pre">virtualenvwrapper则可以让我们更方便的管理每个环境。</span></p>
<p><span style="white-space:pre"><span style="white-space:pre"></span>1：安装virtualenv 和 virtualenvwrapper</span></p>
<p><span style="white-space:pre"><span style="white-space:pre"></span>pip install virtualenv</span></p>
<p><span style="white-space:pre"><span style="white-space:pre"></span>pip install<span style="white-space:pre">virtualenvwrapper</span></span></p>
<p><span style="white-space:pre"><span style="white-space:pre"><span style="white-space:pre"></span>2：配置<span style="white-space:pre">virtualenvwrapper环境</span></span></span></p>
<p><span style="white-space:pre"><span style="white-space:pre"><span style="white-space:pre"><span style="white-space:pre"></span>打开/etc目录，找到bash.bashrc</span></span></span></p>
<p><span style="white-space:pre"><span style="white-space:pre"><span style="white-space:pre"><span style="white-space:pre"><img src="https://img-blog.csdn.net/20171229203750937?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center" alt=""></span></span></span></span></p>
<p><span style="white-space:pre"><span style="white-space:pre"><span style="white-space:pre"><span style="white-space:pre"><span style="white-space:pre"></span>使用vim 打开 ，在最后加入</span></span></span></span></p>
<p><span style="white-space:pre"><span style="white-space:pre"><span style="white-space:pre"><span style="white-space:pre"><span style="white-space:pre"><img src="https://img-blog.csdn.net/20171229203829946?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center" alt=""></span></span></span></span></span></p>
<p><span style="white-space:pre"><span style="white-space:pre"><span style="white-space:pre"><span style="white-space:pre"><span style="white-space:pre"><span style="white-space:pre"></span></span></span></span></span></span></p>
<p><span style="white-space:pre"></span></p>
<p>保存退出，使用source bash.bashrc命令就完成了</p>
<p>安装完成后我们可以使用</p>
<p>常用的几个命令</p>
<br>
<img src="https://img-blog.csdn.net/20180310124426258?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRmFuTUxlaQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" alt=""><br>
