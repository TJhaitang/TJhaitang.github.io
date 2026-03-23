---
title: 博客重启！！！
date: 2026-03-23
tags: 我的来时路
---

## 发生了什么

- 实际上自25年初重启博客之后，自己一个字都没写。主要原因是当时的latex编译出了点问题，极大的影响了我的写作热情
- 但现在可能已经好了！！并且最近就业压力巨大，准备重新开始写博客，记录一下算法学习的路程

## 下面测试一下latex的能力

### PDAS(2013)

对于如下优化问题

$$
\begin{aligned}
    \hat{\beta}&=\arg \min_\beta -l_n(\beta)+\lambda\|\beta\|_0 \\
    &=\arg \min_\beta \frac{1}{2}\|y-X\beta\|_2^2+\lambda\|\beta\|_0
\end{aligned}
$$

该方法首先对矩阵 $X^\top X$ 进行调整，通过增加一个 $\alpha E$ 矩阵以保证其正定。进而得到其增广拉格朗日函数：

$$
L(\beta,v,\gamma)=\frac{1}{2}\|y-X\beta\|_2^2+\frac{\alpha}{2}\beta^\top\beta+\lambda\|v\|_0+\gamma^T(\beta-v)+\frac{1}{2}(\beta-v)^\top\Lambda(\beta-v)
$$

其中，$\Lambda=diag\{\Lambda_1,\Lambda_2,\cdots,\Lambda_p\}$, $\Lambda_i=X_i^\top X_i+\alpha$以保证其强凸。从而可以获得其更新公式，分析其更新公式可以得出其收敛点满足如下方程：

$$
\begin{cases}
    X^\top(X\beta-y)+\alpha\beta+\gamma=0 \\
    \gamma_i=0 \quad when \quad (\gamma_i+\Lambda_i \beta_i)^2 > 2\lambda\Lambda_i\\
    \beta_i=0 \quad when \quad (\gamma_i+\Lambda_i \beta_i)^2 \leq 2\lambda\Lambda_i
\end{cases}
$$

由此得到迭代更新算法 PDAS：

$$
\begin{aligned}
    &\gamma_i^{(t+1)}=0 \quad when \quad (\gamma_i^{(t)}+\Lambda_i \beta_i^{(t)})^2 > 2\lambda\Lambda_i \\
    &\beta_i^{(t+1)}=0 \quad when \quad (\gamma_i^{(t)}+\Lambda_i \beta_i^{(t)})^2 \leq 2\lambda\Lambda_i \\
    &solve \quad X^\top(X\beta^{(t+1)}-y)+\alpha\beta^{(t+1)}+\gamma^{(t+1)}=0
\end{aligned}
$$

由于前两个式子为第三行的方程减少了p个变量，使得其化为一个pxp的方程，故方程有解。记$S=\{i:\gamma_i=0\}$,则实际上该解即为

$$
\begin{cases}
    \beta_S^{(t+1)}=(X_S^\top X_S+\alpha E_S)^{-1}X_S^\top y  \\
    \gamma_S^{(t+1)}=0  \\
    \beta_{S^c}^{(t+1)}=0  \\
    \gamma_{S^c}^{(t+1)}=X_{S^c}^\top(y-X_S\beta_S^{(t+1)})
\end{cases}
$$

显然，上述算法必收敛。