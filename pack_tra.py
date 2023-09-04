import os
import matplotlib.pyplot as plt
from geopy.distance import geodesic
import json
import math
import numpy as np
import matplotlib.colors as colors
import matplotlib.cm as cmx
import random
from scipy.special import lambertw


# 读取数据
def loadData(path, user):
    '''
    数据集
    维度 经度 高度 日期 时间
    '''
    lat = []                                        # 维度
    lng = []                                        # 经度
    high = []                                       # 高度
    date = []                                       # 日期
    time = []                                       # 时间
    loc = []                                        # 位置点数据
    tra = []                                        # 轨迹数据
    path = path + "//" + user + "//Trajectory"
    plts = os.scandir(path)
    for item in plts:
        # 这里边item是指文件夹内的文件
        path_item = path + "//" + item.name  # 文件夹内每一个子文件的绝对路径
        with open(path_item, 'r+') as fp:
            for item in fp.readlines():
                # 这里是打开了单个文件内每一行数据
                item_list = item.split(',')
                if len(item_list) < 7:
                    continue
                if float(item_list[0]) >= 39.1 and float(item_list[0]) <= 41.1 and float(item_list[1]) >= 115.4 and float(item_list[1]) <= 117.6:
                    # 意思是只需要位于北京区域的位置点
                    lat.append(item_list[0])
                    lng.append(item_list[1])
                    high.append(item_list[3])
                    date.append(item_list[5])
                    time.append(item_list[6])
                    loc.append((item_list[0], item_list[1], item_list[3], item_list[5], item_list[6]))
                    # loc指的是当个文件内的所有轨迹数据点
            tra.append(loc)
    return tra, loc

# 绘制轨迹图
def drawTrajectory(tra):
    '''
    :param tra: 轨迹点
    :return: 轨迹图
    '''
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
    colors = ['mistyrose', 'lightcoral', 'salmon', 'tomato', 'cyan', 'deepskyblue', 'red']
    lat = []
    lng = []

    plt.title("轨迹图")
    plt.xlabel("维度-lat")
    plt.ylabel("经度-lng")

    for tra_ in tra:
        lat.append(float(tra_[0]))
        lng.append(float(tra_[1]))

    plt.plot(list(lat), list(lng), color=colors[4])
    plt.scatter(list(lat), list(lng), color=colors[6])
    print("轨迹绘制结束！")
    plt.show()


# 绘制原始轨迹和停留点轨迹对比
def drawTrajectory1(ori_truple, stay_truple):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

    colors = ['mistyrose', 'lightcoral', 'salmon', 'tomato', 'cyan', 'deepskyblue', 'red']

    lat_ori = []
    lng_ori = []
    for tra_ in ori_truple:
        lat_ori.append(float(tra_[0]))
        lng_ori.append(float(tra_[1]))

    lat_stay = []
    lng_stay = []

    for tra_ in stay_truple:
        lat_stay.append(float(tra_[0]))
        lng_stay.append(float(tra_[1]))


    plt.title("轨迹测试")
    plt.xlabel("维度-lat")
    plt.ylabel("经度-lng")
    plt.scatter(list(lat_stay), list(lng_stay), color='red')
    plt.scatter(list(lat_ori), list(lng_ori), color='blue', alpha=0.5)
    plt.plot(list(lat_stay), list(lng_stay), color='red', linewidth=2.5)
    plt.plot(list(lat_ori), list(lng_ori), color='blue', linewidth=0.5)

    plt.show()
    plt.savefig('img/my_plot_1000dpi.png', dpi=1000)

# 计算两个时间之间相差多少秒
def dis_time(time1, time2):
    '''
    :param time1: XX:XX:XX
    :param time2: XX:XX:XX
    :return: int
    '''
    time1_s = int(time1[6:8])
    time1_m_to_s = int(time1[3:5]) * 60
    time1_h_to_s = int(time1[0:2]) * 3600
    time1_sum_s = time1_s + time1_m_to_s + time1_h_to_s

    time2_s = int(time2[6:8])
    time2_m_to_s = int(time2[3:5]) * 60
    time2_h_to_s = int(time2[0:2]) * 3600
    time2_sum_s = time2_s + time2_m_to_s + time2_h_to_s
    return abs(time1_sum_s - time2_sum_s)

# 计算两个轨迹点之间的欧式距离
def geo_distance(lat1, lng1, lat2, lng2):
    distance = geodesic((lat1, lng1), (lat2, lng2)).m
    return distance

# 将原始轨迹数据转化为计算停留点所需要的轨迹数据
def traToTrajectory(tra):
    '''
    :param tra: 原始轨迹数据集([lat, lng, high, date, time])
    :return: trajectory:停留点计算所需要的轨迹数据集([lat, lng, time])
    '''
    trajectory = []
    id = 0
    for tra_ in tra:
        trajectory.append((float(tra_[0]), float(tra_[1]), tra_[4], id))
        id = id + 1
    return trajectory

# 将轨迹数据集改为适合k-means聚类方法的数据
def traToKMeans(tra):
    '''
    :param tra:  原始轨迹数据集([lat, lng, high, date, time])
    :return: array:[[lat, lng]]
    '''
    count = 0
    arrayTmp = []
    for tra_ in tra:
        # count += 1
        # if count % 10 == 0:
        arrayTmp.append((float(tra_[0]), float(tra_[1])))
    return np.array(arrayTmp)

def allTraToKmeans(allTra):
    '''
    :param allTra: 单个用户所有轨迹数据集
    :return: array:[[lat, lng]]
    '''
    arrayTmp = []

    count = 0
    for i in range(len(allTra)):
        tra = allTra[i]
        for tra_ in tra:
            count += 1
            if count % 50 == 0:
                arrayTmp.append((float(tra_[0]), float(tra_[1])))
    return np.array(arrayTmp)



# 计算停留点
def stay_point(trajectory, distance, time):
    '''
    :param trajectory: 轨迹 ([lat, lng, time, id])
    :param distance: 停留点距离阈值
    :param time: 停留点时间阈值
    :return: 停留点，所有停留点的集合，用来显示都哪些原始节点构成了该停留点
    '''
    Stay = []
    # s = stack.Stack()
    len_tra = len(trajectory)
    # s.push((trajectory[0][1], trajectory[0][2], trajectory[0][3]))
    tra_tmp = []
    traAllStay = []  # 所有停留点的集合，用来显示都哪些原始节点构成了该停留点
    pointAttribute = []  # 用json文件存储所有位置点的性质

    flag = 1    # flag = 1 代表这个点被纳入停留点
    i = 0
    while i < len_tra:
        tra_tmp.append((trajectory[i][0], trajectory[i][1], trajectory[i][2], trajectory[i][3]))  # 临时的停留点团
        j = i + 1   # 判断停留点，首先从第二个节点和第一个节点开始
        while j < len_tra:
            flag = 0
            for k in range(len(tra_tmp)):
                # print(float(geo_distance(tra_tmp[k][0], tra_tmp[k][1], trajectory[j][0], trajectory[j][1])))
                if float(geo_distance(tra_tmp[k][0], tra_tmp[k][1], trajectory[j][0], trajectory[j][1])) < distance:
                    # print(geo_distance(tra_tmp[k][0], tra_tmp[k][1], trajectory[j][0], trajectory[j][1]))
                    if dis_time(tra_tmp[0][2], trajectory[j][2]) > time:
                        flag = 1
                        tra_tmp.append((trajectory[j][0], trajectory[j][1], trajectory[j][2], trajectory[j][3]))
                if flag == 1:   # 代表此时这个点被纳入停留点集合,判断下一个点
                    j += 1
                    break
            if flag == 0:   # 这个点没有被纳入停留点 确定此时tra_tmp为这个停留点所有的原始节点和集合
                lat_temp = 0
                lng_temp = 0
                traAllStayTmp = []
                stayTime = dis_time(tra_tmp[len(tra_tmp) - 1][2], tra_tmp[0][2])    # 计算在一个停留点团内的停留时间
                for z in range(len(tra_tmp)):
                    lat_temp += tra_tmp[z][0]
                    lng_temp += tra_tmp[z][1]
                    traAllStayTmp.append((tra_tmp[z][0], tra_tmp[z][1]))
                    pointAttributeTmp = {
                        'id': tra_tmp[z][3],
                        'lat': tra_tmp[z][0],
                        'lng': tra_tmp[z][0],
                        'stayPoint': 'True',
                        'stayTime': stayTime
                    }
                    pointAttribute.append(pointAttributeTmp)
                traAllStay.append(traAllStayTmp)
                Stay.append((lat_temp / len(tra_tmp), lng_temp / len(tra_tmp), tra_tmp[0][2]))
                tra_tmp = []
                break
            if len(tra_tmp) == 0:
                break
        i = j

    return Stay, traAllStay, pointAttribute

# 新的计算停留点方法
# 计算停留点
def stayPointNew(trajectory, distance, time):
    '''
    :param trajectory: 轨迹 ([lat, lng, time, id])
    :param distance: 停留点距离阈值
    :param time: 停留点时间阈值
    :return: 停留点，所有停留点的集合，用来显示都哪些原始节点构成了该停留点
    '''
    stayPoint = [] # 用来存储停留点信息
    '''
    stayPoint : {
        stayId:
        stayLat:
        stayLng:
        StayTime:
        sonPoint:
    }
    '''
    tra_tmp = []
    lenTrajectory = len(trajectory)
    pointAttribute = []  # 用json文件存储所有位置点的性质

    i = 0
    countId = 0

    while i < lenTrajectory:
        tra_tmp.append((trajectory[i][0], trajectory[i][1], trajectory[i][2], trajectory[i][3]))
        j = i + 1
        stayPointLat = float(trajectory[i][0])
        stayPointLng = float(trajectory[i][1])
        stayPointTime = trajectory[i][2]
        while j < lenTrajectory:
            flag = 0
            if float(geo_distance(stayPointLat, stayPointLng, trajectory[j][0], trajectory[j][1])) < distance:
                if dis_time(stayPointTime, trajectory[j][2]) < time:
                    flag = 1
                    tra_tmp.append((trajectory[j][0], trajectory[j][1], trajectory[j][2], trajectory[j][3]))
                    latTmp = 0.0
                    lngTmp = 0.0
                    for k in range(len(tra_tmp)):
                        latTmp += tra_tmp[k][0]
                        lngTmp += tra_tmp[k][1]
                    stayPointLat = latTmp / len(tra_tmp)
                    stayPointLng = lngTmp / len(tra_tmp)

                    j += 1

            if flag == 0:
                sonPoint = []
                stayTime = dis_time(tra_tmp[len(tra_tmp) - 1][2], tra_tmp[0][2])    # 计算在一个停留点团内的停留时间
                stayPointFlag = "True"
                if len(tra_tmp) == 1:
                    stayPointFlag = "False"
                    stayTime = 0
                for k in range(len(tra_tmp)):
                    sonPoint.append((tra_tmp[k][3], tra_tmp[k][0], tra_tmp[k][1], stayTime))
                    pointAttributeTmp = {
                        'id': tra_tmp[k][3],
                        'lat': tra_tmp[k][0],
                        'lng': tra_tmp[k][1],
                        'stayPoint': stayPointFlag,
                        'stayTime': stayTime
                    }
                    pointAttribute.append(pointAttributeTmp)
                if len(tra_tmp) >= 5:
                    stayPointTmp = {
                        'stayId': countId,
                        'stayLat': stayPointLat,
                        'stayLng': stayPointLng,
                        'stayTime': stayTime,
                        'sonPoint': list(sonPoint),
                    }
                    stayPoint.append(stayPointTmp)
                    countId += 1
                tra_tmp = []
            if len(tra_tmp) == 0:
                break

        i = j

    return stayPoint, pointAttribute



# 将数据存储为json文件
def save_json(save_path, data):
    assert save_path.split('.')[-1] == 'json'
    with open(save_path, 'w') as file:
        json.dump(data, file)

# 加载json文件
def load_json(file_path):
    assert file_path.split('.')[-1] == 'json'
    with open(file_path, 'r') as file:
        data = json.load(file)
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

# 坐标转换
def coordinateTranslate(lat, lng, dis, theta):
    latTranslate = lat + dis * math.cos(theta)
    lngTranslate = lng + dis * math.sin(theta)
    return latTranslate, lngTranslate

# 对不同的坐标点计算不同的epsilon
def computeDifferentEpsilon(truePoint):




    return random.uniform(1000, 2000)

# 对读取到的用户真实轨迹添加噪声生成虚假轨迹
def addNoiseToTrueCoordinate(trueTrajectory):
    fakeTrajectory = []
    for trueTrajectory_ in trueTrajectory:
        epsilon = computeDifferentEpsilon(trueTrajectory_)
        r = r_compute(epsilon)
        theta = theta_compute()
        lat, lng = coordinateTranslate(trueTrajectory_[0], trueTrajectory_[1], r, theta)
        fakeTrajectory.append((lat, lng))
    return fakeTrajectory

# 将json文件中的轨迹坐标读出来
def getJsonCoordinate(path):
    coordinate = []
    oriCoordinate = load_json(path)
    for oriCoordinate_ in oriCoordinate:
        # print(oriCoordinate_)
        lat = oriCoordinate_['stayLat']
        lng = oriCoordinate_['stayLng']
        coordinate.append((lat, lng))

    return coordinate


# 读取用户轨迹点信息

def loadPoint1(path):
    coor = []
    oriCoordinate = load_json(path)
    for oriCoordinate_ in oriCoordinate:
        id = oriCoordinate_['id']
        lat = oriCoordinate_['lat']
        lng = oriCoordinate_['lng']
        staypoint = 1 if oriCoordinate_['stayPoint'] == "True" else 0
        staytime = oriCoordinate_['stayTime']
        coor.append((id, lat, lng, staypoint, staytime))

    return coor

# 读取用户轨迹点频率信息

def loadPoint2(path):
    coor = []
    oriCoordinate = load_json(path)

    for oriCoordinate_ in oriCoordinate:
        id = oriCoordinate_['id']
        lat = oriCoordinate_['lat']
        lng = oriCoordinate_['lng']
        frequency = oriCoordinate_['frequency']
        coor.append((id, lat, lng, frequency))

    return coor


# 用户子串生成



# 所有用户字串生成



































