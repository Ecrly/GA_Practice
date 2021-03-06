# -*- coding: utf-8 -*-
import geatpy as ea  # import geatpy
from MyProblem import MyProblem  # 导入自定义问题接口
import numpy as np
import matplotlib.pyplot as plt
from tsp.tsp import get_path
from tools.track import show_track

if __name__ == '__main__':
    """===============================实例化问题对象==========================="""
    problem = MyProblem()  # 生成问题对象
    problem.set_order([50, 30, 40, 20, 60])
    """=================================种群设置=============================="""
    Encoding = 'RI'  # 编码方式
    NIND = 20  # 种群规模
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
    population = ea.Population(Encoding, Field, NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    """================================算法参数设置============================="""
    myAlgorithm = ea.soea_DE_rand_1_bin_templet(problem, population)  # 实例化一个算法模板对象
    myAlgorithm.MAXGEN = 25  # 最大进化代数
    myAlgorithm.mutOper.F = 0.5  # 差分进化中的参数F
    myAlgorithm.recOper.XOVR = 0.2  # 重组概率
    myAlgorithm.trappedValue = 1e-6  # “进化停滞”判断阈值
    myAlgorithm.maxTrappedCount = 10  # 进化停滞计数器最大上限值，如果连续maxTrappedCount代被判定进化陷入停滞，则终止进化
    myAlgorithm.logTras = 1  # 设置每隔多少代记录日志，若设置成0则表示不记录日志
    myAlgorithm.verbose = True  # 设置是否打印输出日志信息
    myAlgorithm.drawing = 1  # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制目标空间过程动画；3：绘制决策空间过程动画）
    """===========================调用算法模板进行种群进化======================="""
    [BestIndi, population] = myAlgorithm.run()  # 执行算法模板，得到最优个体以及最后一代种群
    BestIndi.save()  # 把最优个体的信息保存到文件中
    """==================================输出结果=============================="""
    print('用时：%f 秒' % myAlgorithm.passTime)
    print('评价次数：%d 次' % myAlgorithm.evalsNum)
    if BestIndi.sizes != 0:
        print('最优的目标函数值为：%s' % BestIndi.ObjV[0][0])
        print('最优的控制变量值为：')
        gen = []
        for i in range(BestIndi.Phen.shape[1]):
            gen.append(BestIndi.Phen[0, i].astype(int))
        print(gen)
        # 画一下路径
        paths = [[problem.start.copy()] for i in range(problem.num_car)]
        for i in range(len(gen)):
            paths[gen[i]].append(problem.places[i].tolist())
        track = []
        print(paths)
        for i in paths:
            if len(i) > 1:
                track.append(get_path(np.asarray(i))[1])
        show_track(paths, track)
        print(paths)
        print(track)

    else:
        print('没找到可行解。')
