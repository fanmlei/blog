---
title: ESP-IDF 在 WSL2中的安装和使用
date: 2022-11-18 23:59:37
tags:
---

以 Ubuntu22.04 子系统为例，下面介绍 ESP-IDF 的安装、 VS Code 的配置，以及 USB 的相关设置。
<!--more-->
### 安装系统依赖

```shell
sudo apt-get install git wget flex bison gperf python3 python3-pip python3-setuptools cmake ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0
```

### 获取ESP-IDF

打开终端，执行以下命令，默认安装在用户目录下 `%userprofile%/esp`

```shell
mkdir ~/esp && cd ~/esp
# 这里可以根据自己选择安装不同的版本，github 需要梯子才能访问
git clone -b v4.4.3 --recursive https://github.com/espressif/esp-idf.git
```

### 安装ESP-IDF

等待下载完成之后，进入到 ~/esp/esp-idf 下面，执行脚本自动安装

```shell
cd ~/esp/esp-idf
./install.sh
```

可以指定需要安装的芯片，例如 esp32s3、esp32c3 等等，默认安装为所有芯片都安装

### 配置命令行工具

一般来说我们只需要执行 export.sh 即可激活 esp-idf 的命令行工具

```shell
. ~/esp/esp-idf/export.sh
```

但是每次都需要手动执行，如果使用了类似于zsh的工具，可以通过配置来简化步骤，以 zsh 为例

```shell
vim ~/.zshrc

# 增加下面这行可以在启动终端的时候默认激活idf
. ~/esp/esp-idf/export.sh

# 或者增加别名，通过别名手动激活（更为推荐）
alias get_idf=". ~/esp/esp-idf/export.sh"

```

保存后需要重启终端或者执行 `source ~/.zshrc` 才会生效

### VS Code插件安装

一般来说不会直接在 WSL2 里面编写代码，借助于 IDE 可以更方便的进行开发，乐鑫官方提供了 VS Code 插件，只需要在扩展里面搜索 ESP-IDF 即可安装，需要注意的是，ESP-IDF 安装在 WSL2 里面，所有需要提前安装 WSL 插件，进入到 WSL2 环境里面再安装 ESP-IDF 插件，插件安装成功后会自动识别 ESP-IDF 安装路径进行配置，



### 让 WSL2 能够连接 USB 设备

此时 WSL2 是没办法识别到我们插入的开发板，可以参考微软的官方文档来解决这个问题  https://learn.microsoft.com/zh-cn/windows/wsl/connect-usb

可以在 WSL2 终端通过 `uname -a` 命令查看内核版本，如果低于 `5.10.60.1` 可以执行 `wsl  --update` 来更新到最新的内核

#### 在 Windows 安装 USBIPD

通过 winget 命令安装

```bash
winget install --interactive --exact dorssel.usbipd-win
```

或者直接下载 msi 文件安装，地址为 https://github.com/dorssel/usbipd-win/releases/download/v2.4.1/usbipd-win_2.4.1.msi

安装完成后需要重新打开终端，否则 usbipd 命令会找不到。

#### 在 WSL2 安装 USBIP 工具

按照官网上面的命令，可能会报如下错误

```shell
sudo apt install linux-tools-5.4.0-77-generic hwdata


Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
E: Unable to locate package linux-tools-5.4.0-77-generic
E: Couldn't find any package by glob 'linux-tools-5.4.0-77-generic'
```

参考：https://github.com/dorssel/usbipd-win/wiki/WSL-support 来解决上面的问题

```shell
sudo apt install linux-tools-virtual hwdata
sudo update-alternatives --install /usr/local/bin/usbip usbip `ls /usr/lib/linux-tools/*/usbip | tail -n1` 20
```

将 USB 设备添加到 WSL2 中

```bash
# Windows 系统
# 需要使用管理员身份运行
> usbipd wsl list

BUSID  VID:PID    DEVICE                                                        STATE
1-2    1462:7d97  USB 输入设备                                                  Not attached
1-9    1a86:7523  USB-SERIAL CH340 (COM5)                                       Not attached
1-14   8087:0033  英特尔(R) 无线 Bluetooth(R)                                   Not attached
4-3    046d:c52b  USB 输入设备                                                  Not attached
4-4    05ac:024f  USB 输入设备                                                  Not attached

# BUSID 为 1-9 是目标设备

usbipd wsl attach --busid 1-9 

# WSL2 子系统
> lsusb
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 001 Device 002: ID 1a86:7523 QinHeng Electronics CH340 serial converter
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub

# 可以看到 CH340 已经挂载成功
```

如果使用完成想要将 USB 设备从 WSL2 断开，只需要执行下面命令即可

```bash
usbipd wsl detach --busid <busid>
```

### 编译&烧录示例项目

通过自带的 hello_world 项目，进行编译和烧录来测试安装是否成功

```shell
# 激活idf虚拟环境
get_idf 
# 创建一个工作目录
mkdir ~/workspace $$ cd ~/workspace
# 复制hello_world工程
cp -r $IDF_PATH/examples/get-started/hello_world .
cd hello_world
# 编译
idf.py build
```

通过 VS Code 打开对应的目录，通过底部菜单栏，根据自己的开发板依次设置 端口、芯片型号、烧录方式，最后点击🔥图标 ESP-IDF Build, Flash and Monitor，如果能在终端窗口看到串口输出内容，那么就说明整个安装过程是没有问题的。

