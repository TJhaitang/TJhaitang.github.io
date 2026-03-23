---
title: 使用SMB实现远程桌面
date: 2022-08-12 13:57:31
tags: '普罗米修斯'
---
## 前言
实际上这是一个鸽了很久的文，因为实在是对我来说有些过于麻烦了。   
但确实很好用，可以说是捣鼓到现在最好用的一个小东西了。所以还是记录一下。

## Reference
1. [Rdpwrap.ini-github](https://github.com/sebaxakerhtc/rdpwrap.ini)   
2. [Rdpwarpper-github](https://github.com/stascorp/rdpwrap)

## 操作环境
DELL g15 5511 ： win11家庭版
Redmibook15pro ： ubuntu22.04

## 目录
> [Windows端](#Windows端)   
> 1. [开启SMB服务](#1开启smb服务)
> 2. [访问远程桌面](#2访问远程桌面)   
>
> [Ubuntu端](#ubuntu端)   
> 1. [访问远程桌面](#1访问远程桌面)
> 2. [开启SMB远程桌面服务](#2开启smb远程桌面服务)
> 
> [iPad OS端](#ipad-os端)
> 1. [连接远程桌面](#1连接远程桌面)

---

## Windows端   

### 1.开启SMB服务

如果你的windows是专业版，则只需打开`开始菜单` -> `搜索栏搜索` -> `远程桌面设置` -> `打开远程桌面服务`即可。   
然而对于大多笔记本用户或整机用户来说可能windows家庭版更加常见，而在家庭版windows上并没有开放远程桌面功能，如果尝试打开上述页面会看到如下提示:
{% asset_img 1.1.png 功能不可用 %}   
你可以选择通过合法不合法的方式升级你的windows来获取这一服务，也可以使用[Rdpwarpper](https://github.com/stascorp/rdpwrap/releases/tag/v1.6.2)来获取这一服务。   
下载解压后，使用管理员身份运行install.bat即可安装，这一脚本会为你设置一些配置文件。   
{% asset_img 1.2.png 以管理员身份运行 %}     
安装完毕后，双击打开RDPConf.exe，如果程序显示 [fully supported] 则代表远程桌面服务已开启。然而十有八九是不可以的，还需要对Rdpwrap.ini进行配置。   
{% asset_img 1.3.png 检验通过 %}     
下载此链接中的[rdpwrap.ini](https://github.com/sebaxakerhtc/rdpwrap.ini)文件的最新版本，将此文件移动到`C:\Program Files\RDP Wrapper\`目录下对原文件进行覆盖即可。   
检查RDPConf.exe是否运行正常，此时十有八九是可以的，如果仍然不能三行全绿，可以尝试重启电脑。

### 2.访问远程桌面

在开始菜单搜索`远程桌面连接`并打开相应程序，在`计算机`栏输入目标电脑ip地址即可，此处支持ipv6网络。   
若目标计算机与本机在同一局域网下，可以通过输入计算机名称来进行连接。    
{% asset_img 1.4.png 远程桌面连接 %}   
`远程桌面连接`程序可以对远程桌面进行一些设置，此处不再赘述。

## Ubuntu端

### 1.访问远程桌面

ubuntu下可以通过Remmina来访问远程桌面，此程序在系统安装时会自动安装。若不存在此程序，可以通过`apt-get install remmina`来安装。   

### 2.开启SMB远程桌面服务

实际上在linux间远程桌面通过VNC来实现是一个更加方便的选择，但是若访问端为windows系统，则使用SMB远程桌面服务来实现远程桌面更加方便。由于各种原因，这一部分过段时间再写吧。   

## iPad OS端

### 1.连接远程桌面

在app store中搜索`RD Client`并下载，该软件为iPad端的远程桌面客户端，可以通过输入电脑的ip地址来进行连接。(其他移动端都可以使用这一软件)



