# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea  # import geatpy
import matplotlib.pyplot as plt
from tsp.MyProblem import MyProblem  # 导入自定义问题接口

def get_path(places):
    """================================实例化问题对象============================"""
    problem = MyProblem(places)  # 生成问题对象
    """==================================种群设置=============================="""
    Encoding = 'P'  # 编码方式，采用排列编码
    NIND = 20  # 种群规模
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
    population = ea.Population(Encoding, Field, NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    """================================算法参数设置============================="""
    myAlgorithm = ea.soea_SEGA_templet(problem, population)  # 实例化一个算法模板对象
    myAlgorithm.MAXGEN = 20  # 最大进化代数
    myAlgorithm.mutOper.Pm = 0.5  # 变异概率
    myAlgorithm.logTras = 1  # 设置每隔多少代记录日志，若设置成0则表示不记录日志
    myAlgorithm.verbose = False  # 设置是否打印输出日志信息
    myAlgorithm.drawing = 0  # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制目标空间过程动画；3：绘制决策空间过程动画）
    """===========================调用算法模板进行种群进化========================"""
    [BestIndi, population] = myAlgorithm.run()  # 执行算法模板，得到最优个体以及最后一代种群
    BestIndi.save()  # 把最优个体的信息保存到文件中
    """==================================输出结果=============================="""
    # print('评价次数：%s' % myAlgorithm.evalsNum)
    # print('时间已过 %s 秒' % myAlgorithm.passTime)
    if BestIndi.sizes != 0:
        # print('最短路程为：%s' % BestIndi.ObjV[0][0])
        # print('最佳路线为：')
        best_journey = np.hstack([0, BestIndi.Phen[0, :], 0])
    else:
        print('没找到可行解。')
        return [0, 0]
    return [BestIndi.ObjV[0][0], [int(best_journey[i]) for i in range(len(best_journey))]]

places = np.array([
            [40, 40],
            [45, 20],
            [10, 15],
            [20, 5],
            [15, 30]
        ])
# get_path(places)
