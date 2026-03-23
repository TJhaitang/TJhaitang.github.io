---
title: >-
  A robust fusion-extraction procedure with summary statistics in the presence
  of biased sources
tags:
  - 迁移学习
  - 阅读难度：简单
categories: 文献阅读
date: 2024-01-03 15:38:24
---

## 前言

概述吧？包括对于其摘要与introduction的理解：
- 本文建立在数据分块的框架下，因此该方法原生的可以应用到分布式框架下。
- 本文的目标在对多个数据块进行综合估计，而这多个数据块的数据质量难以保证，且数据块之间**没有明确的优先级**,这一点是与迁移学习中的方法是有区别的，但其中思想**好像不同**（有点像样本选择）
- 数据块包含的数据可能存在异常状态，给出不利与总体估计的影响。同时，对总体数据进行分块本身就会导致数据块的数据分布与总体数据分布不一致，这也会导致不利于总体估计。
- 从摘要来看，本文给出的方法大抵是要选择出那个更好的数据块，在上面进行估计。这样的方法有更好的鲁棒性和准确性（好像样本选择
- 本文所提到的方法可以用在迁移学习中的相同数据源选择上，实现相同数据源、相似数据源与不相关数据源的分离

## Reference

- Ruoyu Wang, Qihua Wang, Wang Miao, A robust fusion-extraction procedure with summary statistics in the presence of biased sources, Biometrika, Volume 110, Issue 4, December 2023, Pages 1023–1040, https://doi.org/10.1093/biomet/asad013

# Introduction

# Estimation in the presence of biased sources
## identification
- 有些数据块是biased,也就是其参数估计值的极限不是总体参数的极限。有些是unbiased
- 不知道哪些有偏，哪些无偏
- 偏差定义为参数差的二范数
### proposition 1

这个定理有些强劲啊？   

- 如果无偏的数据源所包含数据量占总数据的量大于一定的阈值——该阈值表示为`不同数据源的偏差方向的加权累加和`
- 那么，真实参数可以被无偏估计

### Estimation
- 由Proposition 1，可以直观的给出估计量
- 问题是效果不好，因此选择了IVW估计量
- IVW需要给定一些条件，但我们没有 $K_0$ ，所以用 $K$ 替代一下。
- 因此该估计量可能不一致，所以加入 $b^*$ 项使其一致
- $b^*$ 也未知，将其加进去一起估计效果很大可能没那么好，所以要加一个惩罚
- 将相同的压缩为0,不同的不施加惩罚？


# Theoretical properties

## Consistency and oracle properties
> Oracle属性（Oracle Properties）：(generate from copilot)
> 在统计学和机器学习中，Oracle属性是指一个理想的模型选择过程，它知道真实的数据生成过程，并因此能够选择最佳的模型。在现实中，我们通常不知道数据的真实生成过程，因此不能实现Oracle选择。然而，我们可以设计算法来近似Oracle选择，通过选择最佳的模型来最大化预测性能。在编程中，我们经常寻求设计具有Oracle属性的算法，尽管这在实践中可能很困难。

### Theorem 1
- 当比例条件满足，且 $\delta^{-1} \max_k \|\tilde{\theta}_k - \theta^*_k\| \to 0$ in probability, then $\|\tilde{\theta}-\theta_0\| \to 0$ in probability
- 比例足够且不要太小，且 $\tilde{\theta}_k$ **一致收敛**

### Conditions
1. 有无偏的数据源
2. 没看懂，给 $V_k$ 定了一些限制，并且单位矩阵满足这个限制（没有对好坏的评价吗
3. K不要太大，局部收敛速度不要太慢

### Theorem 2
- 展示了一个和oracle estimator的bias的收敛速度
- K不需要给定，也不需要知道一个已知的目标数据源

### Conditions
4. 还是很温和

### Thheorem 3
- 对$ \mathcal{K}_0 $的估计很好
- 咋证的啊？感觉在到时候证明自己的性质的时候会有用

## Asymptotic normality

### Conditions
5. 没看懂

### Theorem 4
- 在一些没看懂的条件下
- 给出了一个超级复杂的式子
- 给出了一个渐进正态的性质




# Simulation
## generated data
- 比较了初始值(好像是使用一阶信息的估计量)、oracle estimator(需要 $k_0$ 吧)、iFusion estimator(需要知道一个无偏的量)、本算法的估计结果
- 比较了有偏差和无偏差情况下的估计效果
- 具体效果没仔细看还

## real data
### Effects of a surgical procedure on the treatment of moderate periodontal disease

### Effects of smoking and alcohol on head and neck cancer