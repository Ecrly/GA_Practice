import random

'''
关于运输侧主要是通过一个订单量确定路线
对于库存侧的影响主要体现在了到达时间上
因此通过get_arrive_time函数随机生成物料达到时间
'''

def get_arrive_time(x):
    '''
    先给每种物料一个随机的到达时间，实际中某几种物料可能是同时到达的
    :param x: 每次补货指令发出后的物料需求表
    :return: 物料到达的时间
    '''
    random_t = [1, 2, 3, 4, 5, 6, 8]
    ret = []
    for i in range(len(x)):
        tx = x[i]
        tmp = []
        for j in range(len(tx)):
            tmp.append([(i + 1) * random_t[random.randint(0, 6)] for _ in range(len(tx[0]))])
        ret.append(tmp)
    ans = ret
    return ret


def is_arrived(dw_t, t):
    '''
    判断是否在窗口内到达
    :param dw_t:
    :param t:
    :return:
    '''
    if t <= dw_t:
        return True
    return False

def get_arrived_mt(t, x):
    '''
    计算时间窗口内能够到达的物料数
    :param t: 物料到达时间
    :param x: 物料需求量
    :return: 规定时间内到达的物料量
    '''
    for i in range(len(t)):
        tt = t[i]
        for j in range(len(tt)):
            for k in range(len(tt[0])):
                if is_arrived(5 * 3, tt[j][k]):
                    pass
                else:
                    x[i][j][k] = 0
    ret = x[0]
    for i in range(1, len(x)):
        for j in range(len(x[0])):
            for k in range(len(x[0][0])):
                ret[j][k] += x[i][j][k]
    return ret, x




# test
b = [
[
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 5],
],
[
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 5],
],
[
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 5],
]
]
# get_arrive_time(x)