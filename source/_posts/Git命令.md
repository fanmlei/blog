---
title: Git命令
date: 2018-05-21 14:42:49
categories: 
- 未分类
tags:
- 笔记
---
1. git init 初始化版本库
2. git config --global user.name (your name) 
3. git config --global user.email (your email)
4. git add (file name)  将文件放置到缓存区
5. git commit -m (describe) 将缓存区的文件提交到分支上
6. git status 查看版本库状态
1. git diff 查看具体修改内容
2. git log 查看提交记录
3. git reset  -- hard HEAD^ 退回上一次提交、  HEAD^^ 退回前两次、  HEAD~n 退回到前n次 、 commit id  退回到指定的位置
4.  git reflog 查看命令记录
5.  git checkout -- (file name)  撤销修改
6.  git rm (file name)  删除文件
7.  git remote set-url origin [URL] 修改远程仓库地址
8.  git config --global credential.helper store 永久记录Https用户名密码
