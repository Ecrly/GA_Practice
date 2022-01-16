# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea
from tsp.tsp import get_path

"""
    一个带约束的单目标旅行商问题：
    有十座城市：A, B, C, D, E, F, G, H, I, J，坐标如下：
        X      Y
    [[0.4,  0.4439],
     [0.2439,0.1463],
     [0.1707,0.2293],
     [0.2293,0.761],
     [0.5171,0.9414],
     [0.8732,0.6536],
     [0.6878,0.5219],
     [0.8488,0.3609],
     [0.6683,0.2536],
     [0.6195,0.2634]]
    某旅行者从A城市出发，想逛遍所有城市，并且每座城市去且只去一次，最后要返回出发地，
而且需要从G地拿重要文件到D地，另外要从F地把公司的车开到E地，那么他应该如何设计行程方案，才能用
最短的路程来满足他的旅行需求？
    分析：在这个案例中，旅行者从A地出发，把其他城市走遍一次后回到A地，因此我们只需要考虑中间途
径的9个城市的访问顺序即可。这9个城市需要排列组合选出满足约束条件的最优的排列顺序作为最终的路线方案。

仓库位置[25, 25]
物料点[
    [40, 40],
    [45, 20],
    [10, 15],
    [20, 5],
    [15, 30]
]

"""


class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self):
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        M = 1  # 初始化M（目标维数）
        maxormins = [1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = 5  # 初始化Dim（决策变量维数）
        varTypes = [1] * Dim  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0] * Dim  # 决策变量下界
        ub = [1] * Dim  # 决策变量上界
        lbin = [1] * Dim  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [1] * Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)
        # 物料存储地点坐标
        self.places = np.array([
                                [40, 40],
                                [45, 20],
                                [10, 15],
                                [20, 5],
                                [15, 30]
                            ])
        self.start = [25, 25]
        # 货车规格
        self.num_car = 2
        self.cars = [100, 120]
        # 物料种数
        self.num_mt = 5


    def set_order(self, order):
        self.order = order

    def aimFunc(self, pop):  # 目标函数
        Vars = pop.Phen.astype(np.int32)  # 得到决策变量矩阵

        # 目标函数（路程）这里需要将路过的点传入另一个专门求解Tsp问题的模块来处理比较好
        f = []
        track = []  # 记录轨迹，以便画路径图
        for gen in Vars:
            paths = [[self.start.copy()] for i in range(self.num_car)]
            for i in range(len(gen)):
                paths[gen[i]].append(self.places[i].tolist())
            dis = 0
            print(paths)
            for i in paths:
                if len(i) > 1:
                    dis += get_path(np.asarray(i))[0]
            f.append([dis])

        # 约束条件：保证不超过货车的载重和体积（暂时先只用载重，即一个约束）
        cv = []
        for j in range(len(Vars)):
            cv.append([-self.cars[i] for i in range(self.num_car)])
        for i in range(self.num_mt):
            v = Vars[:, [i]]
            for j in range(len(v)):
                cv[j][v[j][0]] += self.order[i]
        cv = np.asarray(cv)
        pop.ObjV = np.asarray(f)
        pop.CV = cv





