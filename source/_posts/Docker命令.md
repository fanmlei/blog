---
title: Docker命令
date: 2018-12-14 19:42:49
categories: 
- Docker
tags:
- 笔记
---
安装 apt-get install docker.io

获取镜像：docker pull <name>

运行一个容器： docker run <参数> <image name>
常见的参数
1. -d, --detach=false 指定容器运行于前台还是后台，默认为false
2. -i, --interactive=false， 打开STDIN，用于控制台交互
3. -t, --tty=false， 分配tty设备，该可以支持终端登录，默认为false
4. -u, --user=""， 指定容器的用户
5. -a, --attach=[]， 登录容器（必须是以docker run -d启动的容器）
6. -w, --workdir=""， 指定容器的工作目录
7. -c, --cpu-shares=0， 设置容器CPU权重，在CPU共享场景使用
8. -e, --env=[]， 指定环境变量，容器中可以使用该环境变量
9. -m, --memory=""， 指定容器的内存上限
10. -P, --publish-all=false， 指定容器暴露的端口
11. -p, --publish=[]， 指定容器暴露的端口
12. -h, --hostname=""， 指定容器的主机名
13。 -v, --volume=[]， 给容器挂载存储卷，挂载到容器的某个目录

将容器变为镜像 ： docker commit -a "creator name" -m "information"  containerID   imagename:tag

删除单个容器：docker rm containerID 

删除所有容器：docker rm $(docker ps -a -q)

删除镜像：docker rmi imageID  /  docker rmi imageName:Tag