---
title: php配置sqlserver驱动
date: 2021-10-27 00:50:23
tags: '普罗米修斯'
categories: '数据库大作业'
---
## 前言
配置数据库大作业的环境是一个漫长且艰苦的过程，从最开始的Apache到给Apache加上php，再到ubuntu服务器上配置git仓库配置apache+php，再到尝试各种后端开发方式时配置npm、nodejs、typescript环境，然后今天配置php的sqlserver驱动，一路上可以说十分坎坷，由于时效性的问题很多博客已经失去了指示意义，但总是需要尝试后才能体会到这一点。   
apache+php使用者较多相对便利，php的sqlserver驱动属实时对我这个小白太不友好，在很久的一段挣扎之后我才知道有sqlserver的驱动这么一回事，在之前一直以为是一个开启就可以用的功能(使用了php5.4的配置教程)。   
后来渐渐摸索到了解决的关键，一个比较新的教程博客和官方文档给了我极大的帮助，但还是遇到了一些问题，遂记录。

## Reference
- [php+sqlserver之如何连接sqlserver数据库](https://blog.csdn.net/xiaozhegaa/article/details/53741623)
- [Microsoft Drivers for PHP for SQL Server](https://docs.microsoft.com/zh-cn/sql/connect/php/microsoft-php-driver-for-sql-server?redirectedfrom=MSDN&view=sql-server-ver15)

## 操作环境
- Win11 22000 家庭版
- httpd-2.4.49-o111l-x64-vc15
- php 7.4.25-win32-VC15-x64

## 驱动下载
- [php_pdo_sqlsrv_74_ts_x64.dll](http://60.205.226.43/repo/php_pdo_sqlsrv_74_ts_x64.dll)
- [php_sqlsrv_74_ts_x64.dll](http://60.205.226.43/repo/php_sqlsrv_74_ts_x64.dll)

驱动下载后放在`php/ext`文件夹下，如在我电脑上即为`U:\下载\php-7.4.25-Win32-vc15-x64\ext`   
若下载失败或版本不对应(74对应php版本为7.4)，可以在上面的微软官方文档的连接中获取相应资源   

## php.ini配置
使用你喜欢的文本编辑器打开php.ini文件(`php/php.ini`)   
在有很多的extension处写入这两行(在哪里其实关系不太大，主要是好看)
```ini
extension=sqlsrv_74_ts_x64
extension=pdo_sqlsrv_74_ts_x64
```
之后保存文件、重启apache即可   
重启apache可以在`计算机管理-服务-Apache-重启动`实现

## 验证是否成功
- 查看phpinfo
新建index.php,输入以下内容
```php
<?php
    echo phpinfo;
?>
```
保存退出，通过localhost访问此文件，下拉菜单应该看到这样的页面
![sql驱动显示](https://raw.githubusercontent.com/TJhaitang/TJhaitang.github.io/refs/heads/master/_posts/images/php配置sqlserver驱动/1.png)
这样应该就成功了

- 连接sqserver
使用以下php代码连接sqlserver
```php
<?php
    $serverName = "localhost";
    $connectionOptions = array(
        "Database" => "TPCH",
        "Uid" => "sa", "PWD" => "123456"
    );
    $conn = sqlsrv_connect($serverName, $connectionOptions);
    if ($conn == false)
        echo "连接失败";
    else
        echo "连接成功";
?>
```
如果成功那就成功了！恭喜你！

## 总结
按照这个流程的话配置应该是相对顺利的，如果还是有问题可以在评论区联系我(现在我还没用过评论区呢呜呜想尝鲜)   
以上

