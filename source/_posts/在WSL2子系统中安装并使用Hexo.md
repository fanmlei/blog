---
title: 在WSL2子系统中安装并使用Hexo
date: 2022-12-13 00:06:59
tags:
---

下面以 Ubuntu22.04 子系统为例，介绍如何安装并使用Hexo博客框架。
<!--more-->

hexo 依赖 nodejs 和 npm,  需要提前安装。

### 安装 nvm、node.js 和 npm

和 python 一样，在不同的项目里面可能会在多个 nodejs 版本之间来回切换，此时一般需要借助版本管理器来实现，可以选择安装 nvm 

```shell
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash

# 如果没有 curl 命令，需要手动安装
# sudo apt-get install curl
```

安装完成可以通过 `nvm ls` 命令列出当前安装的所有 nodejs 版本

```shell
> nvm ls
iojs -> N/A (default)
node -> stable (-> N/A) (default)
unstable -> N/A (default)
```

 此时应该是没有安装任何版本的，可以通过 `nvm install --lts` 来安装最新的LTS版本

安装完成之后通过 `node --version` `npm --version` 查看相应的版本号，在项目目录使用 `nvm use <version id> `  来切换 nodejs 的版本

### 安装 Hexo

全局安装

```shell
npm install -g hexo-cli
```

安装成功后通过 `hexo --version` 即可查看 hexo 的版本



### Hexo 的使用

##### 常见命令
| 命令         | 说明 |
| ------------ | -------- |
| hexo init `folder`            | Hexo 将会在指定文件夹中初始化一个博客项目 |
| hexo new `layout` `title`     | 创建一篇新文章或者新的页面，layout:post文章、page页面、draft草稿 |
| hexo publish `layout` `title` | 将草稿中的 `title` 移动到 post 或者 page |
| hexo generate | 使用 Hexo 生成静态文件 |
| hexo server | 运行服务，本地预览 |


