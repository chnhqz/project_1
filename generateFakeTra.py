import pack_tra
import os
import time
import random
from scipy.special import lambertw
import numpy as np
import math
import matplotlib.pyplot as plt
'''
这里主要考虑停留点、频率、停留时间对隐私预算分配的影响
'''

# 读取txt文件



data = np.genfromtxt("txtData/000/1.txt", dtype=[int, float, float, int, int, float])  # 将文件中数据加载到data数组里
# print(data)
'''
data:
[(id, lat, lng, staypoint, staytime, frequency)]
'''
'''
对数据进行标准化
'''
staytime = []
frequency = []

for i in range(len(data)):
    staytime.append(data[i][4])
    frequency.append(data[i][5])

staytime = np.array(staytime)
frequency = np.array(frequency)

staytime = np.divide(np.subtract(staytime, np.min(staytime, axis=0)),
                      np.subtract(np.max(staytime, axis=0), np.min(staytime, axis=0)))

frequency = np.divide(np.subtract(frequency, np.min(frequency, axis=0)),
                      np.subtract(np.max(frequency, axis=0), np.min(frequency, axis=0)))

def computeDifferentEpsilon(data, staytime, frequency, w_staypoint, w_staytime, w_frequency):
    point = []
    for i in range(len(data)):
        if data[i][3] == 1:
            epsilon = w_staypoint + w_staytime * staytime[i] + w_frequency * frequency[i] + 1000
        else :
            epsilon = w_staytime * staytime[i] + w_frequency * frequency[i] + 1000

        point.append((data[i][0], data[i][1], data[i][2], epsilon))

    return point

point = computeDifferentEpsilon(data, staytime, frequency, 100, 5000, 5000)
# print(point)

# 计算r，其中r代表扰动后发布位置与真实位置之间的距离
def r_compute(epsilon):
    t = random.uniform(0, 1)
    '''
    Lambert W 函数（也称为产品对数函数）是一个特殊的数学函数，用来解决形如 x = y * e^y 这样的方程，其中 x 和 y 是实数。
    Lambert W 函数的定义域为 [-1/e, +∞)，并且在该范围内有无穷多个分支，其中主支（Branch 0）用 W₀(x) 表示，其他分支用 Wₖ(x) 表示，其中 k 是整数。
    负支（negative branch）是指 Lambet W 函数在主支之外的分支，其函数值可能为负数。负支的计算通常需要数值计算方法，例如迭代或数值优化，因为没有通用的封闭形式来表达负支。
    '''
    r = - (1 / epsilon) * (lambertw(((t - 1) / epsilon + 1), k=-1))
    return r

# 计算极坐标中的角度
def theta_compute():
    theta = random.uniform(0, 2 * math.pi)
    return theta

# 坐标转换
def coordinateTranslate(lat, lng, dis, theta):
    latTranslate = lat + dis * math.cos(theta)
    lngTranslate = lng + dis * math.sin(theta)
    return latTranslate, lngTranslate

def addNoiseToTrueCoordinate(point):
    fakeTrajectory = []
    trueTrajectory = []
    for i in range(len(point)):
        epsilon = point[i][3]
        r = r_compute(epsilon)
        theta = theta_compute()
        lat, lng = coordinateTranslate(point[i][1], point[i][2], r, theta)
        fakeTrajectory.append((lat, lng))
        trueTrajectory.append((point[i][1], point[i][2]))

    return fakeTrajectory, trueTrajectory

fakeTrajectory, trueTrajectory = addNoiseToTrueCoordinate(point)

# 绘制虚假轨迹和原始轨迹点的距离直方图
def disTrueFake(fakeTrajectory, trueTrajectory):
    dis = []
    y = []
    for i in range(len(fakeTrajectory)):
        disTmp = pack_tra.geo_distance(fakeTrajectory[i][0], fakeTrajectory[i][1], trueTrajectory[i][0], trueTrajectory[i][1])
        dis.append(disTmp)
        y.append(i)
    plt.scatter(list(y), list(dis), color='blue', alpha=0.5)

    plt.show()


disTrueFake(fakeTrajectory, trueTrajectory)
# 绘制对比图象

# pack_tra.drawTrajectory1(trueTrajectory, fakeTrajectory)













