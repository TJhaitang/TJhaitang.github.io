---
title: 查询-SqlServer学习
date: 2021-10-22 17:20:49
tags:  '课堂大师'
---
这里用来记录数据库相关知识
课件文件夹在   
[这里](http://10.43.12.25:81/ruc/数据库)  *需要连接ruc校园网*
***
# 查询
![数据查询](3-1ppt) 

|关键词|功能|
|:--:|:--:|
|SELECT|指定要显示的属性列|
|FROM | 制定查询对象(基本表或视图)|
|WHERE | 指定查询条件|
|GROUP BY | 对查询结果按指定列的值分组，该属性列值相等的元组为一个组。通常会在每组中作用聚集函数|
|HAVING | 只有满足指定条件的组才予以输出|
|ORDER BY | 对查询结果表安指定列值的升序或降序排序|
|DISTINCT|去掉表中重复的行|

## 单表查询
- 选择表中的若干列
```sql
-- 查询全体学生的学号与姓名
SELECT Sno,Sname
FROM Student;
-- 选取所有属性列
SELECT *
FROM Student;
-- 虚列，列别名
SELECT Sname NAME,'New row',2014-Sage,LOWER(Sdept)
FROM Student;
```
- 选择表中的若干元组
```sql
-- DISTINCT关键词，去掉表中重复的行，作用范围是所有目标列
SELECT DISTINCT Cno,Grade
FROM SC;

-- 查询满足条件的元组(条件见下表)
--查询年龄在20以下的学生姓名和年龄
SELECT Sname,Sage
FROM Student
WHERE Sage<20;
--20到23之间
WHERE Sage BETWEEN 20 AND 23;
--确定集合
WHERE Sdept IN ('CS','MA','IS')
--字符串匹配，通配符
-- _:任意单个字符
-- %:任意长度字符串，可为0长
-- [abc]:匹配abc中任意一个字符
-- [^123]:不匹配123中的左右字符
WHERE Sno LIKE '200615121';
WHERE Cname LIKE 'DB\_%i__'ESCAPE'\';
WHERE Sno LIKE '%[^235]'
--LIKE等价于 '='
--空值，逻辑连接
WHERE Grade IS NOT NULL OR Sage>10; 
```
|查询条件|谓词|
|:--:|:--:|
比较|=,>,<,>=,<=,<>,!>,!<; NOT +前述
确定范围|BETWEEN AND, NOT BETWEEN AND
确定集合|IN, NOT IN
字符匹配|LIKE, NOT LIKE
空值|IS NULL, IS NOT NULL
多重条件(逻辑运算)|AND, OR, NOT

- ORDER BY子句
```sql
-- ORDER BY
-- ASC 升序
-- DESC 降序
SELECT *
FROM Student
ORDER BY Sdept, Sage DESC;-- 系号升序，年龄降序
```
- 聚集函数

|关键词|功能|
|:--:|:--:|
COUNT(*)|统计元组个数
COUNT([DISTINCT &#124 ALL]<列名>)|计算一列中不同值的个数
SUM([DISTINCT &#124 ALL]<列名>)|计算一列值的总和
AVG([DISTINCT &#124 ALL]<列名>)|计算一列值的平均值
MIN(<列名>)|计算一列的最小值
MAX(<列名>)|计算一列的最大值

```sql
-- 实例
SELECT AVG(Grade)
FROM SC
WHERE Cno='1';
```
- GROUP BY,HAVING子句
**以后再写**

## 连接查询   
一般格式:   
`[<表名1>.]<列名1><比较运算符>[<表名2>.]<列名2>`
- 广义笛卡尔积
```sql
-- 不带连接谓词
-- 很少直接使用
SELECT Student.*,SC.*
FROM Student,SC
```
- 等值与非等值连接查询
```sql 
SELECT Student.*,Sc.*
FROM Student,SC
WHERE Student.Sno=SC.Sno
-- 等价写法
SELECT *
FROM Student inner join Sc 
on Student.Sno=Sc.Sno
-- 自然连接：在select中去掉重复字段
SELECT Student.Sno Sno,Sname,Ssex,Sage,Sdept,Cno,Grade
FROM Student,SC
WHERE Student.Sno=SC.Sno AND SC.Grade>90
```
- 自身连接
```sql
-- 需要给表起名以示区别
SELECT A.Cno,B.Cpno
FROM Course A,Course B
WHERE A.Cpno=B.Cno
```
- 外连接
外连接与普通连接的区别
> - 普通连接操作之输出满足连接条件的元组
> - 外连接操作以指定表为连接主题，将主题表中不满足连接条件的元组一并输出
> - 左外连接：列出左边关系中所有的元组
> - 右外连接：列出右边关系中所有的元组
```sql
SELECT Student.Sno,Sname,Ssex,Sage,Sdept,Cno,Grade
FROM Student LEFT JOIN SC ON
    (Student.Sno=SC.Sno); -- 左外连接
------
SELECT Student.Sno,Sname,Ssex,Sage,Sdept,Cno,Grade
FROM Student FULL JOIN SC ON
    (Student.Sno=SC.Sno); -- 外连接
```
{% asset_img 左外连接.png 左外连接 %}
- 多表连接
两个以上的表进行连接
```sql
-- 查询每个学生的学号、姓名、选修的课程名及成绩
SELECT Student.Sno,Sname,Cname,Grade
FROM Student,SC,Course
WHERE Student.Sno=SC.Sno
    AND SC.Cno=Course.Cno;
```
## 嵌套查询
> 嵌套查询概述
> - 一个 `SELECT-FROM-WHERE`语句称为一个查询块
> - 将一个查询块嵌套在另一个查询块的`WHERE`子句或`HAVING`短语的条件中的查询称为**嵌套查询**
- IN、比较运算符
```sql
-- 不相关子查询
-- 由内向外
SELECT Sname
FROM Student
WHERE Sno IN
        (SELECT Sno
        FROM SC
        WHERE Cno='2')
```
```sql
-- 相关子查询
SELECT Sno,Cno
FROM SC x
WHERE Grade >=(SELECT AVG(GRADE)
                FROM SC y
                WHERE y.Sno=x.Sno);
```
- ANY、ALL  
 
|||||
|:--:|:--:|:--:|:--:|
|> ANY|> ALL|< ANY|< ALL|
|>= ANY|>= ALL|<= ANY|<= ALL|
|= ANY|= ALL|<> ANY|!= ALL|
```sql
SELECT Sname,Sage
FROM Student
WHERE Sage<
        (SELECT MAX(Sage)
        FROM Student
        WHERE Sdept='CS')
        AND Sdept <> 'CS';
```
- EXISTS
**以后再写**


