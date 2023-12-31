import random
import numpy as np
from scipy.special import lambertw
import matplotlib.pyplot as plt
import math
import geopy
from geopy.distance import geodesic

# 计算基于拉普拉斯分布的噪声
def laplace_noisy(sensitivety, epsilon):
    n_value = np.random.laplace(0, sensitivety / epsilon, 1)
    return n_value


# 计算基于拉普拉斯加噪的混淆值
def laplace_mech(data, sensitivety, epsilon):
    for i in range(len(data)):
        data[i] += laplace_noisy(sensitivety, epsilon)
    return data

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

# 绘制图像
def draw():
    epsilons = []

    for i in range(100):
        epsilons.append(random.uniform(0.1, 1))
    r = []
    for epsilon in epsilons:
        r.append(r_compute(epsilon))
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
    colors = ['mistyrose', 'lightcoral', 'salmon', 'tomato', 'cyan', 'deepskyblue', 'red']

    plt.title("发布位置与真实位置之间的距离图")
    plt.xlabel("epsilon")
    plt.ylabel("r")

    plt.scatter(list(epsilons), list(r), color=colors[1])
    plt.show()

def draw_x_y(x, y):
    colors = ['mistyrose', 'lightcoral', 'salmon', 'tomato', 'cyan', 'deepskyblue', 'red']
    plt.xlabel("epsilon")
    plt.ylabel("r")
    plt.scatter(x, y, color=colors[1])
    plt.show()

# 坐标转换
def coordinateTranslate(lat, lng, dis, theta):
    latTranslate = lat + dis * math.cos(theta)
    lngTranslate = lng + dis * math.sin(theta)
    return latTranslate, lngTranslate

# 衡量两个坐标之间的距离
def geoDistance(lat1, lng1, lat2, lng2):
    distance = geodesic((lat1, lng1), (lat2, lng2)).m
    return distance

# 测量不同的epsilon值对两点之间距离的影响
def experimentEpsilon():
    epsilons = []
    for i in range(100, 1000):
        epsilons.append(i)
    epsilons = list(epsilons)

    lat = 31.2
    lng = 141.2
    distance = []
    for epsilon in epsilons:
        r = r_compute(epsilon)
        theta = theta_compute()
        latTranslate, lngTranslate = coordinateTranslate(lat, lng, r, theta)
        distance.append(geoDistance(lat, lng, latTranslate, lngTranslate))
    draw_x_y(epsilons, distance)


# 计算停留点
# def stayPoint(trajectory, distance, time):
#     '''
#     :param trajectory: 轨迹 ([lat, lng, time, id])
#     :param distance: 停留点距离阈值
#     :param time: 停留点时间阈值
#     :return: 停留点，所有停留点的集合，用来显示都哪些原始节点构成了该停留点
#     '''
#     stayPoint = [] # 用来存储停留点信息
#     '''
#     stayPoint : {
#         stayId:
#         stayLat:
#         stayLng:
#         StayTime:
#         sonPoint:
#     }
#     '''
#     tra_tmp = []
#     lenTrajectory = len(trajectory)
#     pointAttribute = []  # 用json文件存储所有位置点的性质
#
#     i = 0
#     countId = 0
#
#     while i < lenTrajectory:
#         tra_tmp.append((trajectory[i][0], trajectory[i][1], trajectory[i][2], trajectory[i][3]))
#         j = i + 1
#         stay = (trajectory[i][0], trajectory[i][1], trajectory[i][2])
#         while j < lenTrajectory:
#             flag = 0
#             if float(geo_distance(stay[0], stay[1], trajectory[j][0], trajectory[j][1])) < distance:
#                 if dis_time(stay[3], trajectory[j][2]) > time:
#                     flag = 1
#                     tra_tmp.append((trajectory[j][0], trajectory[j][1], trajectory[j][2], trajectory[j][3]))
#                     latTmp = 0.0
#                     lngTmp = 0.0
#                     for k in range(len(tra_tmp)):
#                         latTmp += tra_tmp[k][0]
#                         lngTmp += tra_tmp[k][1]
#                     stay[0] = latTmp
#                     stay[1] = lngTmp
#
#
#             j += 1
#             if flag == 0:
#                 sonPoint = []
#                 stayTime = dis_time(tra_tmp[0][2], tra_tmp[len(tra_tmp) - 1][2])
#                 for k in range(len(tra_tmp)):
#                     sonPoint.append((tra_tmp[k][3], tra_tmp[k][0], tra_tmp[k][1], stayTime))
#                     pointAttributeTmp = {
#                         'id': tra_tmp[k][3],
#                         'lat': tra_tmp[k][0],
#                         'lng': tra_tmp[k][0],
#                         'stayPoint': 'True',
#                         'stayTime': stayTime
#                     }
#                     pointAttribute.append(pointAttributeTmp)
#                 stayPointTmp = {
#                     'stayId' : countId,
#                     'stayLat' : stay[0],
#                     'stayLng' : stay[1],
#                     'stayTime' : stayTime,
#                     'sonPoint' : sonPoint,
#                 }
#                 stayPoint.append(stayPointTmp)
#                 countId += 1
#                 tra_tmp = []
#             if len(tra_tmp) == 0:
#                 break
#
#         i = j
#
#     return stayPoint, pointAttribute






















# 基于拉普拉斯分布的特性，如果想要分布震荡较小，需要将隐私预算epsilon的值设置较大
if __name__ == '__main__':

    lat_lng = [31.3, 141.2]  # 坐标

    data = [1., 2., 3.]
    sensitivety = 1
    epsilon = 100
    # r = r_compute(epsilon)
    # theta = theta_compute()
    # latTranslate, lngTranslate = coordinateTranslate(lat_lng[0], lat_lng[1], r, theta)
    # print("latTranslate, lngTranslate = ({},{})".format(latTranslate, lngTranslate))
    # print("两点之间的距离：{}m".format(geoDistance(lat_lng[0], lat_lng[1], latTranslate, lngTranslate)))
    #
    #
    #
    # print(r, theta)
    experimentEpsilon()
    data_noisy = laplace_mech(data, sensitivety, epsilon)
    for j in data_noisy:
        print("Final Resulet = %.16f" % j)

    # draw()






# 输出结果
# (tensorflow)  dubaokun@ZBMAC-C02D5257M  ~ python laplace_apply.py
# Final Resulet = 1.1131262345421142
# Final Resulet = 1.9423797734301973
# Final Resulet = 3.0605257391487291
