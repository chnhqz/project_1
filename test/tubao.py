'''
一般有两种算法来计算平面上给定n个点的凸包：Graham扫描法(Graham’s scan)，
时间复杂度为O(nlgn)；Jarvis步进法(Jarvis march)，时间复杂度为O(nh)，
其中h为凸包顶点的个数。这两种算法都按逆时针方向输出凸包顶点。
'''
import sys
import math
import time
import random
import numpy as np
from geopy import distance
import matplotlib.pyplot as plt

# 获取基准点的下标，基准点是p[k]

def get_leftbottompoint(p):
    k = 0
    for i in range(1, len(p)):
        if p[i][1] < p[k][1] or (p[i][1] == p[k][1] and p[i][0] < p[k][0]):
            k = i
    return k

# 叉乘计算方法

def multiply(p1, p2, p0):
    return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1])

# 获取极角，通过求反正切得出，考虑pi/2的情况

def get_arc(p1, p0):
    # 兼容sort_points_tan的考虑
    if (p1[0] - p0[0]) == 0:
        if (p1[1] - p0[1]) == 0:
            return -1
        else:
            return math.pi / 2

    tan = float((p1[1] - p0[1])) / float((p1[0] - p0[0]))
    arc = math.atan(tan)

    if arc >= 0:
        return arc
    else:
        return math.pi + arc

# 对极角进行排序，排序结果list不包含基准点

def sort_points_tan(p, pk):
    p2 =[]
    for i in range(0, len(p)):
        p2.append({"index" : i, "arc" : get_arc(p[i], pk)})
    p2.sort(key=lambda  k: (k.get('arc')))
    p_out = []
    for i in range(0, len(p2)):
        p_out.append(p[p2[i]["index"]])

    return p_out

def convex_hull(p):
    p = list(set(p))
    k = get_leftbottompoint(p)
    pk = p[k]
    p.remove(p[k])

    p_sort = sort_points_tan(p, pk)
    p_result = [pk, p_sort[0]]

    top = 2

    for i in range(1, len(p_sort)):
        while (multiply(p_result[-2], p_sort[i], p_result[-1]) > 0):
            p_result.pop()
        p_result.append(p_sort[i])
    return p_result

def HeronGetAreaOfPolyGonbyVector(points):
    # 基于海伦公式计算多边形面积
    area = 0
    if(len(points) < 3):
        raise Exception("error")

    pb = ((points[-1][0] + points[0][0]) / 2, (points[-1][1] + points[0][1]) / 2)   # 基准点选为第一个点和最后一个点连线边上的中点

    for i in range(0, len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]

        db1 = distance.geodesic((pb[0], pb[1]), (p1[0], p1[1])).m
        d12 = distance.geodesic((p1[0], p1[1]), (p2[0], p2[1])).m
        d2b = distance.geodesic((p2[0], p2[1]), (pb[0], pb[1])).m

        # db1 = distance.Geodesic(pb, p1).meters   #根据维度转化成经纬度距离
        # d12 = distance.Geodesic(p1, p2).meters
        # d2b = distance.Geodesic(p2, pb).meters

        hc = (db1 + d12 + d2b) / 2   # db1是基准点和p1的距离，d12是p1和p2的距离，d2b是p2和基准点距离
        # print("hc:{}, db1:{}, d12:{}, d2b:{}".format(hc, db1, d12, d2b))

        triArea = math.sqrt(abs(hc * (hc - db1) * (hc - d12) * (hc - d2b)))
        area += triArea

    return area


def tubaomianjie(tra):
    result = convex_hull(tra)
    area = HeronGetAreaOfPolyGonbyVector(result)
    return area

'''
停留点算法：
输入：轨迹点、面积阈值、时间阈值
输出：停留点坐标集合，坐标点性质集合
停留点坐标集合:(ID lat lng time 停留点面积)
坐标点性质集合：(ID stayPointID lat lng time)
'''
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

def stayPoint(trajectory, area_min, area_max, time):
    stay = []  # 存储停留点信息
    tra_tmp = []
    lenTrajectory = len(trajectory)
    pointAttribute = []  # 存储所有位置点
    i = 0
    countId = 0

    while i < lenTrajectory:
        tra_tmp.append((trajectory[i][0], trajectory[i][1], trajectory[i][2], trajectory[i][3]))
        if (i + 1) < lenTrajectory:
            i = i + 1
            tra_tmp.append((trajectory[i][0], trajectory[i][1], trajectory[i][2], trajectory[i][3]))
        if (i + 1) < lenTrajectory:
            i = i + 1
            tra_tmp.append((trajectory[i][0], trajectory[i][1], trajectory[i][2], trajectory[i][3]))
        j = i + 1


        stayPointTime = trajectory[i][2]

        while j < lenTrajectory:
            flag = 0
            points = []
            for tra_tmp_ in tra_tmp:
                points.append((tra_tmp_[0], tra_tmp_[1]))
            points.append((trajectory[j][0], trajectory[j][1]))

            if tubaomianjie(points) <= area_max and tubaomianjie(points) >= area_min:
                if dis_time(stayPointTime, trajectory[j][2]) < time:
                    flag = 1
                    tra_tmp.append(((trajectory[j][0], trajectory[j][1], trajectory[j][2], trajectory[j][3])))
                    j = j + 1

            # 当前点不是停留点，那么需要将tra_tmp内的点保存下来，如果len(tra_tmp) <= 10,
            # 那么说明只有这10以内的点符合，明显数量不够，所以把他们都记为非停留点。
            # 如果len(tra_tmp) > 10 数量足够，则把他们记为停留点
            if flag == 0:
                pointsend = []
                for i in range(len(points) - 1):
                    pointsend.append((points[i][0], points[i][1]))
                stayPOintFlag = -1
                stayTime = 0
                if len(tra_tmp) > 10:
                    stayTime = dis_time(tra_tmp[len(tra_tmp) - 1][2], tra_tmp[0][2])
                    stayPOintFlag = countId
                    latTmp = 0.0
                    lngTmp = 0.0
                    for k in range(len(tra_tmp)):
                        latTmp += tra_tmp[k][0]
                        lngTmp += tra_tmp[k][1]
                    stayPointLat = latTmp / len(tra_tmp)
                    stayPointLng = lngTmp / len(tra_tmp)
                    stay.append((countId, stayPointLat, stayPointLng, stayTime, tubaomianjie(pointsend)))
                    countId = countId + 1

                for tra_tmp_ in tra_tmp:
                     pointAttribute.append((tra_tmp_[3], tra_tmp_[0], tra_tmp_[1], stayPOintFlag, stayTime))
                tra_tmp = []

            if len(tra_tmp) == 0:
                break
        i = j
        if len(tra_tmp) != 0:
            pointAttribute.append((tra_tmp_[3], tra_tmp_[0], tra_tmp_[1], -1, 0))
    return stay, pointAttribute

def loadData():
    f = open('../oriData/000/trajectory.txt', encoding='gbk')
    trajectory_data = []
    for line in f:
        s = ""
        trajectory_data_tmp = []
        for i in range(len(line)):
            if (line[i] != " " and line[i] != '\n'):
                s = s + line[i]
            else:
                trajectory_data_tmp.append(s)
                s = ""

        trajectory_data.append(trajectory_data_tmp)

    trajectory = []
    for i in range(len(trajectory_data)):
        if trajectory_data[i][3] == trajectory_data[0][3]:
            trajectory.append((float(trajectory_data[i][0]), float(trajectory_data[i][1]), float(trajectory_data[i][2]),
                               trajectory_data[i][3], trajectory_data[i][4]))

    return trajectory

def saveTxt(data, path):
    with open(path, 'w') as f:
        for i in range(len(data)):
            loc_str = ""
            for j in range(len(data[0])):
                if j != (len(data[0]) - 1):
                    loc_str += str(data[i][j]) + " "
                else:
                    loc_str += str(data[i][j]) + "\n"
            f.write(loc_str)

# 绘制原始轨迹和停留点轨迹对比
def drawTrajectory1(ori_truple, stay_truple):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

    colors = ['mistyrose', 'lightcoral', 'salmon', 'tomato', 'cyan', 'deepskyblue', 'red']

    lat_ori = []
    lng_ori = []
    for tra_ in ori_truple:
        lat_ori.append(float(tra_[1]))
        lng_ori.append(float(tra_[2]))

    lat_stay = []
    lng_stay = []

    for tra_ in stay_truple:
        lat_stay.append(float(tra_[1]))
        lng_stay.append(float(tra_[2]))


    plt.title("轨迹测试")
    plt.xlabel("维度-lat")
    plt.ylabel("经度-lng")
    plt.scatter(list(lat_stay), list(lng_stay), color='red')
    plt.scatter(list(lat_ori), list(lng_ori), color='blue', alpha=0.5)
    plt.plot(list(lat_stay), list(lng_stay), color='red', linewidth=2.5)
    plt.plot(list(lat_ori), list(lng_ori), color='blue', linewidth=0.5)

    plt.show()




if __name__ == '__main__':
    trajectory = loadData()
    trajectory = traToTrajectory(trajectory)
    stay, pointAttribute = stayPoint(trajectory, 0.001, 1000, 3600)
    print(len(stay))
    print(pointAttribute)
    drawTrajectory1(stay, pointAttribute)


    saveTxt(stay, "../oriData/000/stay.txt")
    saveTxt(pointAttribute, "../oriData/000/pointAttribute.txt")






    # test_data = [(12, 100), (0,0), (40, 170), (34, 50), (54, 150), (32, 150)]
    # print(test_data)
    #
    # result = convex_hull(test_data)
    # print(result)
    # area = HeronGetAreaOfPolyGonbyVector(result)
    # print("面积：{}平方米".format(area))



























