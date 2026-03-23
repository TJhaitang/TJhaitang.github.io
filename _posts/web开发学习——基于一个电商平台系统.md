---
title: web开发学习——基于一个电商平台系统
date: 2021-10-25 00:35:19
tags: 
- '普罗米修斯'
- '作业的奴隶'
categories: '数据库大作业'
---
## 前言
本学期的数据库大作业是一个电商系统，老师发布的文档指出可以选择自己喜欢的编程语言写用户界面(C++，java，python，JavaScript等等)。本着想触及一些好奇但未知的领域(如上学期的Java课对面向接口、编程模式、git、网络、多线程等等了解了一点，这个学期也想有这样的体验)，同时想让自己的GitHub仓库里面多点语言(好看)而不是现在的Java、Java、Java，以及有点想装逼的念头，对开发方式探索来探索去。   
道路漫长，本学期的回归分析、机器学习、数据库、人生哲学以及不知道有没有的抽样技术大作业让人担惊受怕，估计后半学期八成是以毁灭为主旋律了，所以我准备把这几个的摸索过程记录下来，不过不知道什么时候就鸽掉了。

## Reference

- [菜鸟教程-JavaScript](https://www.runoob.com/js/js-tutorial.html)
- [Apache+PHP环境搭建](https://www.cnblogs.com/godlei/p/6445391.html)

## 目录
> ! 以下页面已失效
- [数据库作业要求](https://TJhaitang.github.io/2021/10/26/数据库大作业要求/)
- [JavaScript学习笔记](https://TJhaitang.github.io/2021/10/26/JavaScript学习笔记)
- [Vue学习笔记](https://TJhaitang.github.io/2021/10/26/Vue学习笔记)
- [数据表](https://TJhaitang.github.io/2021/10/25/数据库大作业-数据表/)
- [分工](https://TJhaitang.github.io/2021/10/26/数据库大作业-分工)
- [功能设计](https://TJhaitang.github.io/2021/10/28/数据库大作业-功能设计)
- [平台本体](https://TJhaitang.github.io/Shopping-System)

## 开发模式
也就是前端和后端的开发方式选择，最近简单了解了一下php、Node.js(typeScript\javaScript)以及在研究Node.js的时候回忆起来的java，几个方式各有不同，但都没有实质上实现上面说的**好奇且未知**这件事。
前端目前准备用vue，但还没有开始了解，所以先简述一下后端的几个方式的区别   

|开发方式|特点|
|:--:|:-----:|
|php|学习成本适中<br>可以嵌入到html文档中<br>可以前端后端放在不同服务上<br>apache后配置后即可自动运行<br>不酷|
|JavaScript+Node.js|学习成本较低<br>服务需要手动开启，但可以开一个screen跑<br>虽然如此，这样网站更改时需要重启服务<br>听名字一般酷|
|TypeScript+Node.js|学习成本较高<br>特征同上<br>名字比较酷(但需要翻译成JavaScript运行，其实一般酷)<br>学习内容多|
|Java/Python|学习成本很低<br>比较不酷<br>特征同上|
|C/C++|别闹|
|其他|还在想要不要继续看|

总结来说php似乎是最好的选择，相对于其他几个“发送请求-返回数据”的方式，php可以在环境配置之后一劳永逸，每次更新只需要刷新页面就可以查看效果。同时使用php可以选择将静态网站放置在Github Pages上面，将动态部分由服务器提供运算。其他几种应该也可以实现这样的功能但便捷性上要差一点。   
但php最大的问题在于，真的不酷，不如TypeScript+Node.js酷   
目前选择`Vue+JavaScript+php+SqlServer`作为数据库大作业的开发方式
## 所需要的知识
- Javascript、php在网页中的意义是什么
- php如何连接到SqlServer
- php程序如何嵌入到网站中
- Vue的网站设计方式
- 各语言的基本语法   
- 想不到了

## 期待能学到的东西
- 不同编程语言之间的不同点是什么，为什么将他们分为不同的语言
- 一些html方面的知识
- 多人共同开发的经验以及自己如何立足其中的经验
- 一些功能的设计方式

## 卷法
- UI设计
- 推荐系统
- 积分
- 签到
- 折扣活动
- 防sql注入
- 高并发安全性
- 信息系统
- ......