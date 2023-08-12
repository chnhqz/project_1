import math
import os
from geographiclib.geodesic import Geodesic
import stack
import matplotlib.pyplot as plt

lat = []  # 维度
lng = []  # 经度
high = []  # 海拔
date = []  # 日期
time = []  # 时间
tra = []  # 轨迹数据
path = os.getcwd() + "\\data" + "\\000" + "\\Trajectory"

plts_000 = os.scandir(path)

for item in plts_000:
    path_item = path + "\\" + item.name  # 文件夹内每一个子文件的绝对路径
    with open(path_item, 'r+') as fp:
        for item in fp.readlines():
            item_list = item.split(',')
            if len(item_list) < 7:
                continue
            if float(item_list[0]) >= 39.1 and float(item_list[0]) <= 41.1 and float(item_list[1]) >= 115.4 and float(
                    item_list[1]) <= 117.6:
                lat.append(item_list[0])
                lng.append(item_list[1])
                high.append(item_list[3])
                date.append(item_list[5])
                time.append(item_list[6])
                tra.append((item_list[0], item_list[1], item_list[3], item_list[5], item_list[6]))

print("共有{}条数据".format(len(lat)))
# 这里是取其中一天的数据
str_time = tra[0][3]
lat_0 = []
lng_0 = []
time_0 = []
tra_0 = []
i = 0
for tra_ in tra:
    str_time_ = tra_[3]
    if str_time_ != str_time:
        break
    lat_0.append(float(tra_[0]))
    lng_0.append(float(tra_[1]))
    time_0.append(tra_[4])
    tra_0.append((float(tra_[0]), float(tra_[1]), tra_[4]))
    # print(tra_[4])

print("{}共有{}条轨迹数据".format(str_time, len(lat_0)))

# 计算两个经纬度坐标之间的距离

# geoDict = Geodesic.WGS84.Inverse()

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

def geo_distance(x1, y1, x2, y2):
    return  math.sqrt(pow(abs(x1 - x2), 2) + pow(abs(y1 - y2), 2))


def angleDistance(x1, y1, x2, y2):
    dDistance = y2 - y1
    lDistance = geo_distance(x1, y1, x2, y2)
    angle = math.asin((dDistance / lDistance)) * 180 / math.pi
    return angle

angle = angleDistance(0, 0, 1, 1)
# print(angle)



def stay_point(trajectory, distance, time):
    Stay = []
    # s = stack.Stack()
    len_tra = len(trajectory)
    # s.push((trajectory[0][1], trajectory[0][2], trajectory[0][3]))
    tra_tmp = []
    traAllStay = []  # 所有停留点的集合，用来显示都哪些原始节点构成了该停留点

    flag = 1    # flag = 1 代表这个点被纳入停留点
    i = 0
    while i < len_tra:
        tra_tmp.append((trajectory[i][0], trajectory[i][1], trajectory[i][2]))  # 临时的停留点团
        j = i + 1   # 判断停留点，首先从第二个节点和第一个节点开始
        while j < len_tra:
            flag = 0
            for k in range(len(tra_tmp)):
                print(float(geo_distance(tra_tmp[k][0], tra_tmp[k][1], trajectory[j][0], trajectory[j][1])) * 1000000)
                if float(geo_distance(tra_tmp[k][0], tra_tmp[k][1], trajectory[j][0], trajectory[j][1])) * 1000000 < distance:
                    # print(geo_distance(tra_tmp[k][0], tra_tmp[k][1], trajectory[j][0], trajectory[j][1]))
                    if dis_time(tra_tmp[k][2], trajectory[j][2]) < time:
                        flag = 1
                        tra_tmp.append((trajectory[j][0], trajectory[j][1], trajectory[j][2]))
                if flag == 1:   # 代表此时这个点被纳入停留点集合,判断下一个点
                    j += 1
                    break
            if flag == 0:   # 这个点没有被纳入停留点 确定此时tra_tmp为这个停留点所有的原始节点和集合
                lat_temp = 0
                lng_temp = 0
                traAllStayTmp = []
                for z in range(len(tra_tmp)):
                    lat_temp += tra_tmp[z][0]
                    lng_temp += tra_tmp[z][1]
                    traAllStayTmp.append((tra_tmp[z][0], tra_tmp[z][1]))
                traAllStay.append(traAllStayTmp)
                Stay.append((lat_temp / len(tra_tmp), lng_temp / len(tra_tmp), tra_tmp[0][2]))
                tra_tmp = []
                break
            if len(tra_tmp) == 0:
                break
        i = j

    return Stay, traAllStay

def stayAnglePoint(trajectory, angle):
    Stay = []
    # s = stack.Stack()
    len_tra = len(trajectory)
    # s.push((trajectory[0][1], trajectory[0][2], trajectory[0][3]))
    tra_tmp = []


    flag = 1  # flag = 1 代表这个点被纳入停留点
    i = 0
    while i < len_tra:
        tra_tmp.append((trajectory[i][0], trajectory[i][1], trajectory[i][2]))  # 临时的停留点团
        j = i + 1  # 判断停留点，首先从第二个节点和第一个节点开始
        while j < len_tra:
            flag = 0
            for k in range(len(tra_tmp)):
                if float(angleDistance(tra_tmp[k][0], tra_tmp[k][1], trajectory[j][0], trajectory[j][1])) > angle:
                    flag = 1
                    tra_tmp.append((trajectory[j][0], trajectory[j][1], trajectory[j][2]))
                if flag == 1:  # 代表此时这个点被纳入停留点集合,判断下一个点
                    j += 1
                    break
            if flag == 0:  # 这个点没有被纳入停留点 确定此时tra_tmp为这个停留点所有的原始节点和集合
                lat_temp = 0
                lng_temp = 0

                for z in range(len(tra_tmp)):
                    lat_temp += tra_tmp[z][0]
                    lng_temp += tra_tmp[z][1]

                Stay.append((lat_temp / len(tra_tmp), lng_temp / len(tra_tmp), tra_tmp[0][2]))
                tra_tmp = []
                break
            if len(tra_tmp) == 0:
                break
        i = j

    return Stay, traAllStay





stayDis, traAllStay = stay_point(tra_0, 100, 60)
# print(traAllStay)
print("共有{}个原始停留点".format(len(stayDis)))
stayAngle = stayAnglePoint(stayDis, 0)
print("共有{}个角度停留点".format(len(stayAngle)))


def plot_show(ori_truple, stay_truple, traAllStay):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

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


    plt.title("000轨迹测试")
    plt.xlabel("经度")
    plt.ylabel("维度")
    plt.scatter(list(lat_stay), list(lng_stay), color='red')
    plt.scatter(list(lat_ori), list(lng_ori), color='blue', alpha=0.5)
    # plt.plot(list(lat_stay), list(lng_stay), color='red', linewidth=2.5)
    plt.plot(list(lat_ori), list(lng_ori), color='blue', linewidth=0.5)

    # print(len(traAllStay[0]))

    for i in range(len(stayDis)):
        x = []
        y = []
        for j in range(len(traAllStay[i])):
            x.append(traAllStay[i][j][0])
            y.append(traAllStay[i][j][1])
        plt.plot(list(x), list(y), color='yellow', linewidth=0.5)



    plt.show()
    plt.savefig('img/my_plot_1000dpi.png', dpi=1000)



plot_show(tra_0, stayDis, traAllStay)









