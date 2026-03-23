---
title: Communication-Efficient Distributed Statistical Inference
tags:
  - 联邦学习
  - 阅读难度：困难
categories: 文献阅读
date: 2023-12-27 14:26:41
---

## 前言
这篇文章实在对我来说过于难以理解，破防了，所以边读边写

## Reference

# Part 2

## 跳过

- 算法介绍
    
- 应用案例介绍
    
- 启发式说明有效性（没看懂
    

## 几个Remarks

- 该算法是中心化的，只有一个机器被选作中心机器。原则上可以不中心化的每个机器上都执行相同的操作，但作者说明在实际实验中这样一方面极大增加通信量，另一方面对估计效果的提升有限
    
- 与其这样做，不如将增加的通信量用在更好的初值估计上
    
- 前人的工作为我们权衡通信成本与统计准确性方面提供了帮助
    
- 我们对数据分布的要求是，中心机器上的数据与全局的数据要同质，其他机器上是无所谓的（当然了
    

# Part3

## M-Estimators in Low Dimensions

### Assumption

1. 参数空间紧且凸，优点在内点，且定义了参数空间的半径
    
2. 全局风险函数的海瑟矩阵在最优点可逆，且特征值有上下界。有解、没有线性关系
    
3. 对于经验风险函数，当n足够大时可以保证
    
    1. 全局最优点是该函数的最优点
        
    2. 最优点处的函数值足够小
        
4. 在一个球内，经验风险函数
    
    1. 梯度有界
        
    2. 海瑟矩阵与全局风险函数的海瑟矩阵差异的最大特征值有界
        
    3. 海瑟矩阵变化率不足够大
        

### Theorem

1. 估计值与不使用替代loss的估计值的差异可以被bound住
    
    1. 大约是n^-1数量级
        
    2. with high probability
        
2. 估计值与真实值的差异的期望可以被bound住
    
3. 全局最优也就1/N
    
    1. 所以这个很好
        

### One-step approximation

二次替代函数-一步求解

    Theorem

    当初值足够近的时候，在一个大概率下，估计值与全局估计的差异也是1/n

### Iterative local estimation algorithm

n^-1/2的收敛速率

### Confidence region construction

对于估计值的分布，我们可以给出一个plug-in的估计

两种估计方式

    使用本地最优估计和全局plug-in估计

Corollary

    为上述说法提供了理论支持，说明了估计器的一致性

## Regularized Estimators with L_1-Regularizer

### Assumption

1. 在某个不太明白的区域内，local的risk函数强凸
    
2. restricted Lipschitz Hessians
    

### Theorem

# Part4

## Distributed M-Estimators in Logistic Regression

### 本地比较

- 符合想法的，估计精度很好
    
- 当N定n小的时候估计效果差，因为使用本地数据估计全局的海瑟阵的精度变差了
    
- 对于右边的两幅图，为什么为什么ave没有随着k的变大而变小？这一点论文中提到，前人研究过。也就是需要k<<n才有这个结论（还是好奇怪
    
- 提到了当k大的时候误差会变大，但实验中其实还好？？
    

### 和其他方法比较

- 横坐标为数据遍历次数？
    
- 仅仅使用一阶信息的弱鸡对手收敛的太慢辣！（在用遍历次数当横轴这是有些不公平的评价，但可以想象到这样的评价倒没什么问题
    
- 居然叫二阶信息noisy？
    
- communication efficient如是说
    

### 区间估计

- 对$\theta$ 的第一个分量进行区间估计，使用plug in estimators
    
- 小n时候差，和上面一样
    
- 其他情况基本就是95%
    
- 带撇的稍微好一点点
    

## Distributed Sparse Linear Regression

### 数值模拟，和平均进行比较

- 基本是线性的，也就是说数据的分布对算法的估计效果影响不大。与之相对的全局平均受分布散度影响很大
    
- 第二张图相当于把第一章图斜过来了，说明二者受N的影响都是线性的
    

### 本地、一步、全局进行比较，比较变量选择的准确性（感觉需要联系一下DITS

- 一步CSL和全局Lasso效果差别不大
    
- 左边是平均选中且对的，右边是平均选中且错的（选中的数量没有限定——软阈值
    

## Distributed Bayesian Inference
