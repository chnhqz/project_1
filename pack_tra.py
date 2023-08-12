import os
import matplotlib.pyplot as plt
from geopy.distance import geodesic
import json
import math
import numpy
import matplotlib.colors as colors
import matplotlib.cm as cmx


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
    path = path + "\\" + user + "\\Trajectory"
    plts = os.scandir(path)
    for item in plts:
        path_item = path + "\\" + item.name  # 文件夹内每一个子文件的绝对路径
        with open(path_item, 'r+') as fp:
            for item in fp.readlines():
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
            tra.append(loc)
    return tra, loc

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
    plt.savefig('img/my_plot_1000dpi.png', dpi=1000)
    plt.show()


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

def geo_distance(lat1, lng1, lat2, lng2):
    distance = geodesic((lat1, lng1), (lat2, lng2)).m
    return distance

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



def stay_point(trajectory, distance, time):
    '''
    :param trajectory: 轨迹 ([lat, lng, time])
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
                    if dis_time(tra_tmp[k][2], trajectory[j][2]) < time:
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


def save_json(save_path, data):
    assert save_path.split('.')[-1] == 'json'
    with open(save_path, 'w') as file:
        json.dump(data, file)


def load_json(file_path):
    assert file_path.split('.')[-1] == 'json'
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data





































