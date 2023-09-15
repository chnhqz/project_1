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
data_stay_point = np.genfromtxt("../txtData/stayPoint.txt", dtype=[int, float, float, int])
print("读取到停留点！")

matrix = np.zeros((len(data_stay_point), 19))
count = [0] * 19

startTime1 = time.time()
# 停留点区域 即半径r
r = 100
len_data_stay_point = len(data_stay_point)
len_POI_matrix = len(POI_matrix)
for i in range(len_data_stay_point):
    # 停留点经纬度
    lat = data_stay_point[i][0]
    lng = data_stay_point[i][1]
    startTime = time.time()
    for j in range(len_POI_matrix):
        s = 1 + 1
        if POI_matrix[j][0] > 0.0:
            if math.sqrt((lat - POI_matrix[j][0]) ** 2 + (lng - POI_matrix[j][1]) ** 2) <= r:
                 count[0] += 1
            # if geodesic((lat, lng), (POI_matrix[j][0], POI_matrix[j][1])).m <= r:
            #     count[0] += 1
            # s = s + 1
        #
        # if POI_matrix[j][2] > 0.0:
        #     if geo_distance(lat, lng, POI_matrix[j][2], POI_matrix[j][3]) <= r:
        #         count[1] += 1
        #
        # if POI_matrix[j][4] > 0.0:
        #     if geo_distance(lat, lng, POI_matrix[j][4], POI_matrix[j][5]) <= r:
        #         count[2] += 1
        #
        # if POI_matrix[j][6] > 0.0:
        #     if geo_distance(lat, lng, POI_matrix[j][6], POI_matrix[j][7]) <= r:
        #         count[3] += 1
        #
        # if POI_matrix[j][8] > 0.0:
        #     if geo_distance(lat, lng, POI_matrix[j][8], POI_matrix[j][9]) <= r:
        #         count[4] += 1
        #
        # if POI_matrix[j][10] > 0.0:
        #     if geo_distance(lat, lng, POI_matrix[j][10], POI_matrix[j][11]) <= r:
        #         count[5] += 1
        #
        # if POI_matrix[j][12] > 0.0:
        #     if geo_distance(lat, lng, POI_matrix[j][12], POI_matrix[j][13]) <= r:
        #         count[6] += 1
        #
        # if POI_matrix[j][14] > 0.0:
        #     if geo_distance(lat, lng, POI_matrix[j][14], POI_matrix[j][15]) <= r:
        #         count[7] += 1
        #
        # if POI_matrix[j][16] > 0.0:
        #     if geo_distance(lat, lng, POI_matrix[j][16], POI_matrix[j][17]) <= r:
        #         count[8] += 1
        #
        # if POI_matrix[j][18] > 0.0:
        #     if geo_distance(lat, lng, POI_matrix[j][18], POI_matrix[j][19]) <= r:
        #         count[9] += 1
        #
        # if POI_matrix[j][20] > 0.0:
        #     if geo_distance(lat, lng, POI_matrix[j][20], POI_matrix[j][21]) <= r:
        #         count[10] += 1
        #
        # if POI_matrix[j][22] > 0.0:
        #     if geo_distance(lat, lng, POI_matrix[j][22], POI_matrix[j][23]) <= r:
        #         count[11] += 1
        #
        # if POI_matrix[j][24] > 0.0:
        #     if geo_distance(lat, lng, POI_matrix[j][24], POI_matrix[j][25]) <= r:
        #         count[12] += 1
        #
        # if POI_matrix[j][26] > 0.0:
        #     if geo_distance(lat, lng, POI_matrix[j][26], POI_matrix[j][27]) <= r:
        #         count[13] += 1
        #
        # if POI_matrix[j][28] > 0.0:
        #     if geo_distance(lat, lng, POI_matrix[j][28], POI_matrix[j][29]) <= r:
        #         count[14] += 1
        #
        # if POI_matrix[j][30] > 0.0:
        #     if geo_distance(lat, lng, POI_matrix[j][30], POI_matrix[j][31]) <= r:
        #         count[15] += 1
        #
        # if POI_matrix[j][32] > 0.0:
        #     if geo_distance(lat, lng, POI_matrix[j][32], POI_matrix[j][33]) <= r:
        #         count[16] += 1
        #
        # if POI_matrix[j][34] > 0.0:
        #     if geo_distance(lat, lng, POI_matrix[j][34], POI_matrix[j][35]) <= r:
        #         count[17] += 1
        #
        # if POI_matrix[j][36] > 0.0:
        #     if geo_distance(lat, lng, POI_matrix[j][36], POI_matrix[j][37]) <= r:
        #         count[18] += 1

        # for k in range(len(count)):
        #     matrix[i][k] = count[k]
        #     count[k] = 0

    endTime = time.time()
    print("完成第{}次计算,用时{}s,剩余{}次计算,预计用时{}h".format(i, endTime - startTime, len(data_stay_point) - i, (endTime * startTime) * (len(data_stay_point) - i) / 3600))
endTime1 = time.time()

print("构建完成matrix！用时：{}".format(endTime1 - startTime1))











