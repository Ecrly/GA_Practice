# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea
from stock.transport import *

"""
初始化：
3个决策窗口，大小为5
5种物料，初始剩余[25, 20, 20, 10, 30]，消耗速度为[5, 3, 6, 4, 5]
5*3个决策变量，每个决策变量xi选自[0, 10, 20, 30]

目标函数：
f += self.c[i] + r[:, [i]] - self.u[i] * self.num_dw * self.t
其中r根据get_arrive_time和get_arrived_mt得到

约束条件：
for i in range(self.num_mt):
    cv1 = self.c[i] + r[:, [i]] - self.u[i] * self.num_dw * self.t
for i in range(self.num_mt):
    cv2 = self.c[i] - t[0][:, [i]] * self.u[i]
for i in range(self.num_mt):
    cv3 = self.c[i] + r[0][:, [i]] - t[1][:, [i]] * self.u[i]
for i in range(self.num_mt):
    cv4 = self.c[i] + r[0][:, [i]] + r[1][:, [i]] - t[2][:, [i]] * self.u[i]
把以上全部加入cv中，共4*5个

"""


class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self):
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        M = 1  # 初始化M（目标维数）
        maxormins = [-1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        self.var_set = np.array([0, 10, 20, 30])  # 设定一个集合，要求决策变量的值取自于该集合
        Dim = 3 * 5  # 初始化Dim（决策变量维数, 3是决策窗口，5是物料数)
        varTypes = [1] * Dim  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0] * Dim  # 决策变量下界
        ub = [3] * Dim  # 决策变量上界
        lbin = [1] * Dim  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [1] * Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)
        self.c = [25, 20, 50, 40, 30]  # 剩余库存
        self.u = [5, 3, 6, 4, 5]  # 消耗速率
        self.t = 5  # 决策窗口时间大小
        self.num_dw = 3  # 决策窗口数
        self.num_mt = 5 # 物料种类数


    def aimFunc(self, pop):  # 目标函数
        Vars = pop.Phen.astype(np.int32)  # 强制类型转换确保元素是整数
        x = []  # 存一下决策变量(补货量)，X1、X2、X3，其中每个X均是5列代表物料种类
        for i in range(self.num_dw):
            x.append(self.var_set[Vars[:, [_ for _ in range(self.num_mt * i, self.num_mt * (i + 1))]]])

        # 将对应的补货量发送给运输侧，运输侧需要返回一个到达时间
        t = get_arrive_time(x)

        # 对时间进行判定，从而得出Ri
        sum_r, r = get_arrived_mt(t, x)
        sum_r = np.asarray(sum_r)

        # 计算目标函数
        f, cv, cv1 = 0, [], 0
        for i in range(self.num_mt):
            cv1 = self.c[i] + sum_r[:, [i]] - self.u[i] * self.num_dw * self.t
            cv.append(-cv1)
            f += cv1

        # 通过物料到达时间确定约束条件
        t = np.asarray(t)
        r = np.asarray(r)
        cv2, cv3, cv4 = 0, 0, 0
        for i in range(self.num_mt):
            cv2 = self.c[i] - t[0][:, [i]] * self.u[i]
            cv.append(-cv2)
        for i in range(self.num_mt):
            cv3 = self.c[i] + r[0][:, [i]] - t[1][:, [i]] * self.u[i]
            cv.append(-cv3)
        for i in range(self.num_mt):
            cv4 = self.c[i] + r[0][:, [i]] + r[1][:, [i]] - t[2][:, [i]] * self.u[i]
            cv.append(-cv4)

        pop.ObjV = f  # 计算目标函数值，赋值给pop种群对象的ObjV属性
        pop.CV = np.hstack(cv)
