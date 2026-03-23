---
title: 在Windows电脑上运行安卓程序
date: 2021-10-21 19:29:57
tags: '普罗米修斯'
---
## 前言
今日惊闻WSA正式在Beta渠道推送了，本着有用没用先试了再说的的原则，在拿到电脑后便开始捣鼓。整体流程非常简单顺利，共计耗时一个小时，中间还打了把王者荣耀。   
用了之后感觉还是香啊，如果国内安卓pad生态再发展发展就好了。

## Reference
1. [乘风破浪，遇见最美Windows 11之新微软商店(Microsoft Store)生态 - 安卓(Android™)体验及开发兼容指南](https://www.cnblogs.com/taylorshi/p/15431615.html)

## 操作环境
Windows 11 家庭版 22000.282测试版Beta   
戴尔G5 5511
***
> 安装WSA可以搞windows测试版转美国地区然后在MS Store下载，`测试版` `转美国地区` `在MS Store下载`都有相关教程，我没有这么做。我选择的是将网友分享的WSA安装包直接安装。
> 这里我两个方向都会介绍。
## 你所必要的事情
1. 电脑操作系统为Windows11 22000及以上
2. 电脑需要开启虚拟机平台
{% asset_img xnh.png 虚拟化需要开启 %}
如果未开启，需要找到 `设置`->`应用`->`可选功能`->`更多Windows功能` 勾选 `Hyper-V`和`虚拟机平台`。之后重启系统即可。

## 下载WSA安装包
> 你可以不选择这个方案，不过我选择的是这个   
[百度网盘下载链接](https://pan.baidu.com/s/1CcC6W7jUjh-w9KTkqhv_NQ) 提取码：2sxh   
下载后双击打开点击`Install`即可   
### 若提示无法安装
- 右键点击开始菜单，选择Windows终端(管理员)
- 切换到安装包所在目录
```bash
# 切换盘符，例如切换到d盘
d:
# 查看当前目录
dir
# 切换目录
cd <文件夹名>
```
- 执行命令
```bash
add-appxpackage "MicrosoftCorporationII.WindowsSubsystemForAndroid_1.7.32815.0_neutral___8wekyb3d8bbwe.Msixbundle"
```
- 待部署操作进程完毕后即可安装了

## 进入Windows内测版获取WSA
> 若不喜欢上面的方法或上面未成功可使用此方法
- 获取Windows内测资格
`设置`->`Windows更新`->`Windows预览体验计划`   
在选择内测渠道时选择Beta渠道即可
- 切换地区为美国
`设置`->`时间和语言`->`区域和语言`
- 重启电脑后，访问以下网站
 <https://www.microsoft.com/store/productId/9P3395VX91NR>   
 或也可以Win+r，输入`ms-windows-store://pdp/?productid=9P3395VX91NR`并运行
 - 点击获取

 ## 开启WSA的adb旁加载功能
 > 由于目前WSA下载应用需要使用亚马逊应用市场，然而一方面上面应用太少了，另一方面很多人会对注册亚马逊账号感到困扰，所以adb旁加载功能显得十分重要。
 > adb旁加载可以允许你安装你电脑上的.apk文件
 - 查看adb版本
 ```bash
 adb version
 ```
 - 若没有adb命令，则下载该压缩包，将解压后的东西全复制到`C://Windows`文件夹下就可以了
 [下载链接](https://pan.baidu.com/s/15eTHKtkPIhoHHbbHNa03Hg)提取码：gr3g

 - 在开始菜单打开WSA(一个绿色图标的应用)，进入设置页面
 {% asset_img wsa.png 设置页面 %}
 - 打开开发人员模式
 - 点击第一行文件右边的小箭头，启动Android子系统
 - 打开Windows Terminal输入以下命令
```bash
adb connect 127.0.0.1:58526
# 如果失败，可以在WSA设置中选择关闭Android子系统后重启WSA
# 执行以下命令以安装.apk程序
# 首先需要切换到安装包所在文件夹下
adb install .\name.apk # name.apk为文件名
```
- 之后就可以快乐的在你的电脑上使用安卓应用程序啦

## 总结
- 虽然捣鼓流程不长，但最后的效果是很好的，体感上感觉程序的刷新率能达到90~120的水平。不过现在这个功能还比较新，问题还是很多的，比如肉眼可见的不稳定和部分窗口的适配糟糕。   
- 尝试了几个程序，目前没有真正的享受到这个工具带来的便利。一开始安装这个是为了在电脑上装一个微信读书，因为web端的微信读书我属实是不喜欢，想要一个类似iPad端的样式。但让我吃惊的是，微信读书居然没有安卓的pad版本。
- 可能这也是WSA的一个意义吧，突破Google Store的垄断，优化安卓平板生态。
- 但另一方面，在国内web环境日渐炸裂的当下，WSA的出现可能会为这一现象火上浇油
- 目前我还没有找到太多在电脑上好用的安卓应用，大家有什么想法可以卸载评论区里，虽然没有评论区。
