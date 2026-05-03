---
title: Transformer:我所知道的一切
tags:
  - Attention
  - Transformer
  - 模型结构
categories: 大模型学习
date: 2025-04-01 00:02:12
---
## 前言

- 从那节“数据科学实践”开始，自己曾多次尝试理解Transformer的原理。但这么多年过去了，对其仍然只是大概知道是个什么东西，理解完全称不上深入。但是现在计划往大模型方向转型，Transformer是一个绕不开的概念，于是痛定思痛，决定好好学习一下Transformer的原理。
- 之前对Transformer的理解太浅薄了，以为之只是一个类似于AlexNet这样的很好理解的模型，每次都没有花费很多的时间去看。另一方面，Transformer的论文写的很简短，网上的解释质量也参差不齐，学起来十分痛苦。
- 本次学习自认为把自己对Transformer的理解从20%提升到了70%。对于还没有理解的部分，我也会标注出来，并在不久后进行补充。

## Reference

1. [Transformer-知乎](https://zhuanlan.zhihu.com/p/403433120)
2. [位置编码追根溯源-苏剑林](https://kexue.fm/archives/8231)
3. [Transformer-菜鸟教程](https://www.runoob.com/pytorch/transformer-model.html)
4. [Transformer-harvard](https://nlp.seas.harvard.edu/2018/04/03/attention.html#greedy-decoding)
5. [Transformer论文精读-李沐](https://www.bilibili.com/video/BV1pu411o7BE)
6. [Attention is All You Need-论文](https://arxiv.org/abs/1706.03762)

---

![Transformer架构图](https://nlp.seas.harvard.edu/images/the-annotated-transformer_14_0.png)

## 模型流程

> 笔者将使用一个简单的例子顺一遍完整的Transformer模型的流程。也就是上面这张图。
> 在下面的表达中，我会用如此处一样的标注块来表示数据的变化

- 假设我们需要进行一个机器翻译任务，目标是将“我喜欢吃苹果”翻译成“i like to eat apple”。

### 分词

- 模型并不直接处理文本，而是将文本进行分词处理。分词的方式有很多种，最常用的有BPE（Byte Pair Encoding）和WordPiece。这里我们使用BPE进行分词。
- 简单来讲，BPE的分词方式是将文本中的单词进行切分，切分的方式是将文本中出现频率最高的字母组合进行替换。比如“我喜欢吃苹果”可以被分成“我/喜欢/吃/苹果”。
- 分词后，我们得到的文本是“我/喜欢/吃/苹果”，我们将其转换为数字表示，得到“1/2/3/4”。
- 这里的数字表示是一个词表（Vocabulary），词表是一个字典，字典的key是单词，value是单词对应的数字表示。比如“我”对应的数字表示是1，“喜欢”对应的数字表示是2。
- 词表的大小是一个超参数，通常设置为10000。也就是说，我们的模型只能处理10000个单词，如果文本中出现了不在词表中的单词，那么我们就将其替换为一个特殊的token，比如“[UNK]”。除了不在词表中的单词之外，我们还需要处理一些特殊的token，比如“[PAD]”、“[START]”、“[END]”。这些token也在词表之中，有其对应的数字表示。这些token在模型处理过程中是不可或缺的，他们的作用是：

|token|作用|数字表示|
|---|---|---|
|[PAD]|填充token，用于填充文本，使得文本长度一致。|0|
|[START]|开始token，用于标记文本的开始。|5|
|[END]|结束token，用于标记文本的结束。|6|
|[UNK]|未知token，用于替换不在词表中的单词。|7|
- 除此之外，还有一些其他的特殊token，他们常用于满足特定的模型需求，此处不做赘述。至此，我们建立了一个长度为8的中文词表，相对应的，我们可以建立一个英文词表如下：
  
|token|数字表示|
|---|---|
|[PAD]|0|
|i|1|
|like|2|
|to|3|
|eat|4|
|apple|5|
|[START]|6|
|[END]|7|
|[UNK]|8|

- Transformer模型的输入输出是定长的，为了适应不同长度文本的翻译需求，我们需要将不足长的部分进行占位填充。以上述翻译任务为例，假设模型的输入输出长度分别是6和7，那么我们需要将“我/喜欢/吃/苹果”进行填充，得到“我/喜欢/吃/苹果/[PAD]/[PAD]”，同时将“i like to eat apple”进行填充，得到“i like to eat apple [PAD] [END]”。
- 换句话说，模型的任务就是将中文词表下的：“1/2/3/4/0/0” 翻译成英文词表下的：“1/2/3/4/5/0/7”。
- 接下来，数据终于要进入模型了！让我们从Encoder开始！

### Encoder

> 输入：$x_0=[1,2,3,4,0,0]$

- Embedding
  - 我们并不喜欢上面的数表示方法，数字间的大小关系并没有实际意义。数据输入模型时，将会从上面的数字表示转换为one-hot向量表示，即`1->[0,1,0,0,0,0,0,0]`，`2->[0,0,1,0,0,0,0,0]`(上述中文词表长度为8)。
  
  - > one-hot向量表示：（矩阵$X$的角标仅为辅助理解数据传递流程使用）
    > $X_1= [[0,1,0,0,0,0,0,0], [0,0,1,0,0,0,0,0], ......, [1,0,0,0,0,0,0,0]] $ 
    > $X_1.shape=(6,8)=(token数目,词表长度)=(n,vocab\_size)$

  - 但显然这样的表示有两大问题： 
    - 没有体现词之间的关系，向量表示不含有词意信息
    - 向量维度过高：目前市面上的大模型(如deepseek等)词表一般在10W左右，one-hot向量的维度也就10W，无法直接进行计算
  - Embedding层的作用就是将one-hot向量转换为低维稠密向量表示。该层维护一个矩阵，矩阵的大小是`(vocab\_size, embedding\_dim)`，其中`embedding\_dim`是一个超参数，通常设置为512。Embedding层的作用就是将one-hot向量乘以这个矩阵，得到低维稠密向量表示，称之为词向量。
  
  - > Embedding 参数矩阵：$E_1.shape=(8,512)$
    > $X_2=X_1E_1$ $X_2.shape=(6,512)=(token数目,embedding\_dim)=(n,d_{model})$

  - 明明说是转化为低维稠密向量但为什么维度变高了？因为我们此处仅为距离，设计的词表大小非常小，实际应用中词表大小要大得多的多，但embedding\_dim不会再大太多了
- Positional Encoding
  - 笔者在此处不加解释的给出下述两个公式：

    $PE_{(pos,2i)}=sin(pos/10000^{2i/d_{model}})$

    $PE_{(pos,2i+1)}=cos(pos/10000^{2i/d_{model}})$

    $pos \in [0,1,2,...,n-1], 2i\in [0,2,...,d_{model}/2-1]$

  - > 位置编码矩阵：$P.shape=(6,512)$ 
    > - 使用$P$而非$PE$表示该矩阵以避免歧义，并非参数矩阵而是由上述公式计算得出
    >
    > $X_3=X_2E_1+P$
    > $X_3.shape=(6,512)=(token数目,embedding\_dim)=(n,d_{model})$
  - Transformer的Attention结构并不能从文本中提取位置信息，因此需要通过位置编码来为文本增加位置信息。详细解释将在[位置编码](#位置编码)章节进行

- Multi-Head Attention
  - 多头自注意力机制是Transformer的核心，也就是论文题目《Attention is All You Need》中的Attention。此处过程复杂、难以理解，笔者将在后续章节做详细解释，此处仅给出数据流动过程：
  
  - > 单层多头自注意力机制：$W_Q,W_K,W_V,W_M$，$W_{[Q,K,V]}.shape=(d_{model},d_{[Q,K,V]}*n_{heads})$，$W_M.shape=(d_V*n_{heads},d_{model})$
    >
    > 1. $Q= X_3W_Q$， $K= X_3W_K$， $V= X_3W_V$
    > 2. $Q,K,V.view(-1,n_{heads},d_{[Q,K,V]})$
    > 1. $Q,K,V.shape=(6,n_{heads},d_{[Q,K,V]})$
    > 1. $X_4=Softmax(\frac{QK^T}{\sqrt{d_{model}}}\odot Mask)V$
    > 1. $X_4.shape=(6,n_{heads},d_V)$
    > 1. $X_4.view(-1,d_{model})$
    > 1. $X_5= X_4W_M$
    > 1. $X_5.shape=(6,512)=(n,d_{model})$
    > 1. output: $X_6=LayerNorm(X_5+X_3)$

  - 上述过程涉及了以下内容，皆会在后续章节进行详细解释
    - [4.自注意力机制](#自注意力机制)
    - [1.多头注意力机制](#多头注意力机制)
    - [4.掩码(Mask)](#掩码)
    - [9.层归一化(LayerNorm)](#层归一化)
    - [9.残差连接](#残差连接)
  - 简单来讲，多头自注意力层将输入的词向量数据进行一些变化，输出一个具有更加丰富词义的词向量数据。这一过程的主要作用是提取文本中词与词之间的关系。如将“我喜欢吃苹果”中的“我”和“苹果”联系起来。

- Feed-forward network
  - 该层的作用是将多头自注意力层输出的词向量数据进行一些变化，输出一个具有更加丰富词义的词向量数据。该层包含两个线性变换和一个ReLU激活函数。该层的输入是多头自注意力层的输出，输出是一个新的词向量数据。
  
  - > Feed-forward network：$W_1,W_2,b_1,b_2$，$W_1.shape=(d_{model},d_{ff})$，$W_2.shape=(d_{ff},d_{model})$，$b_1.shape=(d_{ff})$，$b_2.shape=(d_{model})$
    >
    > $X_7=ReLU(X_6W_1+b_1)$
    > $X_8=X_7W_2+b_2$
    > output: $X_9=LayerNorm(X_8+X_6)$

- 一个多头自注意力层和一个前馈网络层组成了一个Encoder层。Transformer的Encoder部分由多个Encoder层堆叠而成，通常设置为6层。每一层的输入是上一层的输出，第一层的输入是Embedding层的输出。记数据在Encoder层循环N次之后的输出为$X_E$，此时：
  
  - $X_E.shape=(6,512)=(n,d_{model})$

### Decoder

- 在对Decoder进行描述之前，我们先描述一下Decoder层的输入与输出是什么。
  - 输入：
    - Encoder的输出$X_E$，形状为$(6,512)$
    - 模型的当前翻译结果$X_D$，形状为$(7,512)$，7为我们前面设置的模型输出长度，512为embedding\_dim。
  - 输出：
    - 模型对输入结果的所有词的“下一个词”预测结果$X_O$，形状为$(7,512)$
  - 模型将根据encoder的输出，并行地**依据每个词的前序信息**预测整个输入文本7个词的全部“下一个词”，如：
    - 输入："i like to eat [PAD] [PAD] [PAD]"
    - 输出："like to eat apple [PAD] [PAD] [PAD]"
  - 每个词都是预测结果而非输入数据的复制，每个词都**仅依据前序信息**进行预测，如上例中输出的"eat"是依据"i like to"进行预测的;"apple"是依据"i like to eat"进行预测的;而再之后的"[PAD]"是依据"i like to eat [PAD]"进行预测的。这样的预测行为被成为"Right Shift"，仅依据前序信息是通过[掩码](#掩码)实现的。
  - 对于上例中的模型输出，我们只取"apple"作为模型的预测结果，并拼接到输入的"i like to eat"后面，得到"i like to eat apple"。这是因为只有这个词是对“当前翻译结果的下一个词”的预测结果，其他的输出我们并不需要。接下来我们进入数据流动过程

> 输入：$x_D=[6,0,0,0,0,0,0]$ 模型还未开始翻译，将第一个位置置为[START]，其他位置置为[PAD]。模型第一步将预测'[START]'的下一个词。
> 转化为one-hot向量表示:$X_D.shape=(7,9)=(token数目,词表长度)=(n,vocab\_size)$

- Embedding与Positional Encoding
  - 与Encoder部分相同，模型将输入的one-hot向量表示转换为低维稠密向量表示，并添加位置编码。
  
  - > Embedding 参数矩阵：$E_2.shape=(9,512)$
    > 位置编码矩阵：$P_D.shape=(7,512)$ 
    > $X_2=X_DE_2+P_D$
    > $X_2.shape=(7,512)=(token数目,embedding\_dim)=(n,d_{model})$

- Masked Multi-Head Attention
  - 该层与Encoder部分的多头自注意力层几乎一致，唯一的区别在于mask的形状不同，读者仅需要注意这一点即可，具体形式将在[掩码](#掩码)章节进行详细描述。
  
  - > Masked Multi-Head Attention：$W_Q,W_K,W_V,W_M$，$W_{[Q,K,V]}.shape=(d_{model},d_{[Q,K,V]}*n_{heads})$，$W_M.shape=(d_V*n_{heads},d_{model})$
    >
    > 1. $Q= X_2W_Q$， $K= X_2W_K$， $V= X_2W_V$
    > 2. $Q,K,V.view(-1,n_{heads},d_{[Q,K,V]})$
    > 1. $Q,K,V.shape=(7,n_{heads},d_{[Q,K,V]})$
    > 1. $X_4=Softmax(\frac{QK^T}{\sqrt{d_{model}}}\odot Mask)V$
    > 1. $X_4.shape=(7,n_{heads},d_V)$
    > 1. $X_4.view(-1,d_{model})$
    > 1. $X_5= X_4W_M$
    > 1. $X_5.shape=(7,512)=(n,d_{model})$
    > 1. output: $X_6=LayerNorm(X_5+X_2)$

- Encoder-Decoder Multi-Head Attention
  - 与前面不同的是，本步不再是自注意力层，输入的QKV不再是相同的矩阵，而是Q来自Decoder，K和V为Encoder的输出$X_E$。这一步的作用是将Decoder的当前信息与Encoder所分析的文本信息进行结合，将双语信息进行联系。
  
  - > Encoder-Decoder Multi-Head Attention：$W_Q,W_K,W_V,W_M$，$W_{[Q,K,V]}.shape=(d_{model},d_{[Q,K,V]}*n_{heads})$，$W_M.shape=(d_V*n_{heads},d_{model})$
    >
    > 1. $Q= X_6W_Q$， $K= X_EW_K$， $V= X_EW_V$
    > 2. $Q,K,V.view(-1,n_{heads},d_{[Q,K,V]})$
    > 1. $Q.shape=(7,n_{heads},d_Q)$；   $\quad K,V.shape=(6,n_{heads},d_{[K,V]})$
    > 1. $X_7=Softmax(\frac{QK^T}{\sqrt{d_{model}}}\odot Mask)V$
    > 1. $X_7.shape=(7,n_{heads},d_V)$
    > 1. $X_7.view(-1,d_{model})$
    > 1. $X_8= X_7W_M$
    > 1. $X_8.shape=(7,512)=(n,d_{model})$
    > 1. output: $X_9=LayerNorm(X_8+X_6)$

- Feed-forward network
  - 与Encoder一致
  
  - > Feed-forward network：$W_1,W_2,b_1,b_2$，$W_1.shape=(d_{model},d_{ff})$，$W_2.shape=(d_{ff},d_{model})$，$b_1.shape=(d_{ff})$，$b_2.shape=(d_{model})$
    >
    > $X_{10}=ReLU(X_9W_1+b_1)$
    > $X_{11}=X_{10}W_2+b_2$
    > output: $X_{12}=LayerNorm(X_{11}+X_9)$

- 如最上面的图所示，数据将在上述三层中循环N次，N通常设置为6。每一层的输入是上一层的输出。记数据在Decoder层循环N次之后的输出为$X_O$，此时：
  
  - > $X_O.shape=(7,512)=(n,d_{model})$
  
- Projection
  - 该层的作用是将Decoder的输出$X_O$转换为模型的预测结果$X_{pred}$。该层包含一个线性变换和一个softmax激活函数。该层的输入是Decoder的输出，输出是一个新的词向量数据。
  
  - > Projection：$W_P,b_P$，$W_P.shape=(d_{model},vocab\_size)$，$b_P.shape=(vocab\_size)$
    >
    > $X_{pred}=Softmax(X_OW_P+b_P)$
    > $X_{pred}.shape=(7,vocab\_size)=(n,vocab\_size)$

- Prediction
  - 该层的作用是将模型的预测结果$X_{pred}$转换为模型的最终输出$X_{out}$。该层包含一个argmax操作。该层的输入是模型的预测结果，输出是一个新的词向量数据。至此，整个模型的数据流动流程就结束了，模型完成了一次预测。
  
  - > Prediction：$X_{out}=argmax(X_{pred})$
    > $X\_{out}.shape=(7)$

---

## 自注意力机制

## 多头注意力机制

## 掩码

## 解码器

## 位置编码

## 层归一化

## 残差连接

## 激活函数
