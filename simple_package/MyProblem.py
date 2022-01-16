# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea

"""
一个带约束的多目标背包问题：
    假设有5类物品，每类物品中包含着四个具体的物品，要求从这五种类别的物品中分别选择一个物品放进背包，
使背包内的物品总价最高，总体积最小，且背包的总质量不能超过92kg。用矩阵P代表背包中物品的价值；
矩阵R代表背包中物品的体积；矩阵C代表物品的质量。P,R,C的取值如下:

cap = 8
v=[3,4,5,6]       w=[2,3,4,5]
t=[2,3,4,9]
分析：
    这是一个0-1背包问题，但如果用一个元素为0或1的矩阵来表示哪些物品被选中，则不利于后面采用进
化算法进行求解。可以从另一种角度对背包问题进行编码：由于问题要求在每类物品均要选出一件，这里我
们可以用0, 1, 2, 3来表示具体选择哪件物品。因此染色体可以编码为一个元素属于{0, 1, 2, 3}的1x5行向量，
比如：[0,0,0,0,0]表示从这五类物品中各选取第一个物品。



"""


class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self, M=1):
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        maxormins = [-1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = 4  # 初始化Dim（决策变量维数）
        varTypes = [1] * Dim  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0] * Dim  # 决策变量下界
        ub = [1] * Dim  # 决策变量上界
        lbin = [1] * Dim  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [1] * Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)
        # 添加几个属性来存储P、R、C
        self.v = np.array([3, 4, 5, 6])
        self.w = np.array([2, 3, 4, 5])
        self.t = np.array([2, 3, 4, 9])

    def aimFunc(self, pop):  # 目标函数
        x = pop.Phen  # 得到决策变量矩阵
        row, col = x.shape
        x1 = x[:, [0]]
        x2 = x[:, [1]]
        x3 = x[:, [2]]
        x4 = x[:, [3]]
        f = x1 * self.v[0] + x2 * self.v[1] + x3 * self.v[2] + x4 * self.v[3]
        g = x1 * self.w[0] + x2 * self.w[1] + x3 * self.w[2] + x4 * self.w[3]
        h = x1 * self.t[0] + x2 * self.t[1] + x3 * self.t[2] + x4 * self.t[3]

        # # 采用可行性法则处理约束
        pop.CV = np.hstack([g - 8, h - 10])
        pop.ObjV = f  # 把求得的目标函数值赋值给种群pop的ObjV
