from geopy.distance import geodesic
import numpy as np
import time
import math


def geo_distance(lat1, lng1, lat2, lng2):
    distance = geodesic((lat1, lng1), (lat2, lng2)).m
    return distance

def function_1(matrix, i, j, lat, lng, r):
    lat_1 = matrix[i][j]
    lng_1 = matrix[i][j + 1]


def function_2(data_1, data_stay_point, r):
    count = 0
    for i in range(len(data_1)):
        lat = data_1[i][0]
        lng = data_1[i][1]
        for j in range(len(data_stay_point)):
            lat_1 = data_stay_point[j][0]
            lng_1 = data_stay_point[j][1]
            if geo_distance(lat, lng, lat_1, lng_1) <= r:
                count += 1
    return count

POI_matrix = np.genfromtxt("../txtData/POI_matrix_service.txt", dtype=[float, float, float, float, float, float, float, float, float, float,
                                                                           float, float, float, float, float, float, float, float, float, float,
                                                                           float, float, float, float, float, float, float, float, float, float,
                                                                           float, float, float, float, float, float, float, float])  # 将文件中数据加载到data数组里

print("读取到POI_matrix!")
POI_matrix = np.array(POI_matrix)

# 读取停留点
data_stay_point = np.genfromtxt("../txtData/pointAttribute.txt", dtype=[int, float, float, int])
print("读取到停留点！")

matrix = np.zeros((len(data_stay_point), 19))

startTime = time.time()
# 停留点区域 即半径r
r = 100
for i in range(len(data_stay_point)):








