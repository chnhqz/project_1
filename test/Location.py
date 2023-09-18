import sys
import math
import time
import random
import numpy as np
from geopy import distance
import matplotlib.pyplot as plt

'''
将停留点聚类，得到语义位置，其中主要是考察停留点之间的语义相似度
两组向量之间的语义相似度主要是用停留点语义特征向量之间的余弦相似度来衡量
'''

def similar(vec1, vec2):

    vec1_1 = []
    vec2_2 = []
    for i in range(1, len(vec1)):
        vec1_1.append(vec1[i])
    for i in range(len(vec2)):
        vec2_2.append(vec2[i])

    vec1_1 = np.array(vec1_1)
    vec2_2 = np.array(vec2_2)
    # print(vec1_1)
    # print(vec2_2)
    return np.sum(vec1_1 * vec2_2) / (np.linalg.norm(vec1_1) * np.linalg.norm(vec2_2))


def Location(stay, stay_senmantic, senmantic_threshold):
    countID = 0
    location = []
    locationtmp = []
    locationtmp_1 = []
    stayAttribute = []

    len_stay_senmantic = len(stay_senmantic)

    i = 0
    while i < len_stay_senmantic:

        # 在每一次循环中首先添加一个停留点的语义信息，及其停留点ID
        locationtmp.append(i)
        for z in range(len(stay_senmantic[i])):
            locationtmp.append(float(stay_senmantic[i][z]))
        locationtmp_1.append(locationtmp)

        locationtmp = []

        # 下一个停留点语义特征向量
        j = i + 1
        flag = 1
        while j < len_stay_senmantic:
            # 停留点所处语义位置的ID

            # 该点是否处于一个语义位置
            # locationtmp_1 临时存储位于一个语义位置的停留点集合
            for p in range(len(locationtmp_1)):

                # print(similar(locationtmp_1[p], stay_senmantic[j]))
                # 如果stay_senmantic[j]和该语义位置内所有停留点的语义相似度都大于一定阈值，则他们所处同一语义位置
                if similar(locationtmp_1[p], stay_senmantic[j]) > senmantic_threshold:
                    continue
                else:
                    flag = 0
                    break

            if flag == 1:
                locationtmp.append(j)
                for k in range(len(stay_senmantic[j])):
                    locationtmp.append(stay_senmantic[j][k])
                locationtmp_1.append(locationtmp)
                # print(locationtmp)
                locationtmp = []
                j += 1

            if flag == 0 or j == len_stay_senmantic:
                flagLocation = countID
                if len(locationtmp_1) == 1:
                    flagLocation = -1

                for n in range(len(locationtmp_1)):
                    stayAttribute.append((locationtmp_1[n][0], stay[locationtmp_1[n][0]][1], stay[locationtmp_1[n][0]][2], flagLocation))

                if len(locationtmp_1) >= 2:

                    lat = 0.0
                    lng = 0.0
                    for n in range(len(locationtmp_1)):
                        lat += stay[locationtmp_1[n][0]][1]
                        lng += stay[locationtmp_1[n][0]][2]

                    lat = lat / len(locationtmp_1)
                    lng = lng / len(locationtmp_1)
                    location.append((countID, lat, lng))
                    countID += 1
                locationtmp_1 = []
            if len(locationtmp_1) == 0:
                break
        i = j

    return location, stayAttribute


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
    stay_semantic = np.genfromtxt("../oriData/000/end_poi.txt", dtype=[float, float, float, float, float, float, float, float, float, float,
                                                                           float, float, float, float, float, float, float, float, float])  # 将文件中数据加载到data数组里
    stay = np.genfromtxt("../oriData/000/stay.txt", dtype=[int, float, float, int , float])

    location, stayAttribute = Location(stay, stay_semantic, 0.95)



    # print(len(location))
    # print(stayAttribute)

    with open('../oriData/000/location.txt', 'w') as f:
        for i in range(len(location)):
            loc_str = str(location[i][0]) + " " + str(location[i][1]) + " " + str(location[i][2]) + "\n"
            f.write(loc_str)

    with open('../oriData/000/stayAttribute.txt', 'w') as f:
        for i in range(len(stayAttribute)):
            loc_str = str(stayAttribute[i][0]) + " " + str(stayAttribute[i][1]) + " " + str(stayAttribute[i][2]) + " " + str(stayAttribute[i][3]) + "\n"
            f.write(loc_str)

    drawTrajectory1(stayAttribute, location)





    # np.savetxt('../oriData/000\\' + 'location.txt', np.c_[location], fmt='%.10f', delimiter=' ')
    # np.savetxt('../oriData/000\\' + 'stayAttribute.txt', np.c_[stayAttribute], fmt='%.10f', delimiter=' ')


























