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
        flagLocation = -1
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

            if flag == 0:
                flagLocation = countID
                if len(locationtmp_1) == 1:
                    flagLocation = -1

                for n in range(len(locationtmp_1)):
                    stayAttribute.append((locationtmp_1[n][0], stay[locationtmp_1[n][0]][1], stay[locationtmp_1[n][0]][1], flagLocation))

                if len(locationtmp_1) >= 2:

                    lat = 0.0
                    lng = 0.0
                    for n in range(len(locationtmp_1)):
                        lat += stay[locationtmp_1[n][0]][1]
                        lng += stay[locationtmp_1[n][0]][1]

                    lat = lat / len(locationtmp_1)
                    lng = lng / len(locationtmp_1)
                    location.append((countID, lat, lng))
                    countID += 1
                locationtmp_1 = []
            if len(locationtmp_1) == 0:
                break

        i = j

    return location, stayAttribute








if __name__ == '__main__':
    stay_semantic = np.genfromtxt("../oriData/000/end_poi.txt", dtype=[float, float, float, float, float, float, float, float, float, float,
                                                                           float, float, float, float, float, float, float, float, float])  # 将文件中数据加载到data数组里
    stay = np.genfromtxt("../oriData/000/stay.txt", dtype=[int, float, float, int , float])
    # print(stay_semantic)

    # vec1 = [1, 2, 3, 4, 5]
    # vec2 = [3, 4, 5, 6, 7]
    #
    # print(similar(vec1, vec2))


    location, stayAttribute = Location(stay, stay_semantic, 0.9)
    print(len(location))
    print(stayAttribute)




























