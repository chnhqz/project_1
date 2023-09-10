from geopy.distance import geodesic
import numpy as np
import time
import math


def geo_distance(lat1, lng1, lat2, lng2):
    distance = geodesic((lat1, lng1), (lat2, lng2)).m
    return distance

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

# 读取POI兴趣点
data_1 = np.genfromtxt("../txtData/POI/交通设施服务.txt", dtype=[float, float])  # 将文件中数据加载到data数组里
data_2 = np.genfromtxt("../txtData/POI/住宿服务.txt", dtype=[float, float])  # 将文件中数据加载到data数组里
data_3 = np.genfromtxt("../txtData/POI/体育休闲服务.txt", dtype=[float, float])  # 将文件中数据加载到data数组里
data_4 = np.genfromtxt("../txtData/POI/公共设施.txt", dtype=[float, float])  # 将文件中数据加载到data数组里
data_5 = np.genfromtxt("../txtData/POI/公司企业.txt", dtype=[float, float])  # 将文件中数据加载到data数组里
data_6 = np.genfromtxt("../txtData/POI/医疗保健服务.txt", dtype=[float, float])  # 将文件中数据加载到data数组里
data_7 = np.genfromtxt("../txtData/POI/商务住宅.txt", dtype=[float, float])  # 将文件中数据加载到data数组里
data_8 = np.genfromtxt("../txtData/POI/摩托车服务.txt", dtype=[float, float])  # 将文件中数据加载到data数组里
data_9 = np.genfromtxt("../txtData/POI/政府机构及社会团体.txt", dtype=[float, float])  # 将文件中数据加载到data数组里
data_10 = np.genfromtxt("../txtData/POI/汽车服务.txt", dtype=[float, float])  # 将文件中数据加载到data数组里
data_11 = np.genfromtxt("../txtData/POI/汽车维修.txt", dtype=[float, float])  # 将文件中数据加载到data数组里
data_12 = np.genfromtxt("../txtData/POI/汽车销售.txt", dtype=[float, float])  # 将文件中数据加载到data数组里
data_13 = np.genfromtxt("../txtData/POI/生活服务.txt", dtype=[float, float])  # 将文件中数据加载到data数组里
data_14 = np.genfromtxt("../txtData/POI/科教文化服务.txt", dtype=[float, float])  # 将文件中数据加载到data数组里
data_15 = np.genfromtxt("../txtData/POI/购物服务.txt", dtype=[float, float])  # 将文件中数据加载到data数组里
data_16 = np.genfromtxt("../txtData/POI/道路附属设施.txt", dtype=[float, float])  # 将文件中数据加载到data数组里
data_17 = np.genfromtxt("../txtData/POI/金融保险服务.txt", dtype=[float, float])  # 将文件中数据加载到data数组里
data_18 = np.genfromtxt("../txtData/POI/风景名胜.txt", dtype=[float, float])  # 将文件中数据加载到data数组里
data_19 = np.genfromtxt("../txtData/POI/餐饮服务.txt", dtype=[float, float])  # 将文件中数据加载到data数组里
# 读取停留点
data_stay_point = np.genfromtxt("../txtData/pointAttribute.txt", dtype=[int, float, float, int])

'''
先处理整个数据集，得到一个大数组
停留点ID lat lng POI1 POI2 POI3 .... POIn
1        23  43   10   3   5   ....  10
'''
print("len(data_1):{}\nlen(data_2):{}\nlen(data_3):{}\nlen(data_4):{}\nlen(data_5):{}\n"
      "len(data_6):{}\nlen(data_7):{}\nlen(data_8):{}\nlen(data_9):{}\nlen(data_10):{}\n"
      "len(data_11):{}\nlen(data_12):{}\nlen(data_13):{}\nlen(data_14):{}\nlen(data_15):{}\n"
      "len(data_16):{}\nlen(data_17):{}\nlen(data_18):{}\nlen(data_19):{}\n".format(len(data_1), len(data_2), len(data_3), len(data_4), len(data_5)
                                                                                , len(data_6), len(data_7), len(data_8), len(data_9), len(data_10)
                                                                                , len(data_11), len(data_12), len(data_13), len(data_14), len(data_15)
                                                                                , len(data_16), len(data_17), len(data_18), len(data_19)))

'''
交通设施服务: len(data_1):23537
住宿服务: len(data_2):8527
体育休闲服务: len(data_3):11703
公共设施: len(data_4):20703
公司企业: len(data_5):64711
医疗保健服务: len(data_6):17249
商务住宅: len(data_7):34068
摩托车服务: len(data_8):849
政府机构及社会团体: len(data_9):28551
汽车服务: len(data_10):9329
汽车维修: len(data_11):5857
汽车销售: len(data_12):1838
生活服务: len(data_13):57445
科教文化服务: len(data_14):23652
购物服务: len(data_15):90985
道路附属设施: len(data_16):733
金融保险服务: len(data_17):16267
风景名胜: len(data_18):3336
餐饮服务: len(data_19):49309
'''

matrix_service = np.zeros((len(data_15), 38))
# 将这些服务组成一个矩阵
for i in range(len(data_15)):
    if i < len(data_1):
        matrix_service[i][0] = data_1[i][0]
        matrix_service[i][1] = data_1[i][1]
    if i < len(data_2):
        matrix_service[i][2] = data_2[i][0]
        matrix_service[i][3] = data_2[i][1]

    if i < len(data_3):
        matrix_service[i][4] = data_3[i][0]
        matrix_service[i][5] = data_3[i][1]

    if i < len(data_4):
        matrix_service[i][6] = data_4[i][0]
        matrix_service[i][7] = data_4[i][1]

    if i < len(data_5):
        matrix_service[i][8] = data_5[i][0]
        matrix_service[i][9] = data_5[i][1]

    if i < len(data_6):
        matrix_service[i][10] = data_6[i][0]
        matrix_service[i][11] = data_6[i][1]

    if i < len(data_7):
        matrix_service[i][12] = data_7[i][0]
        matrix_service[i][13] = data_7[i][1]

    if i < len(data_8):
        matrix_service[i][14] = data_8[i][0]
        matrix_service[i][15] = data_8[i][1]

    if i < len(data_9):
        matrix_service[i][16] = data_9[i][0]
        matrix_service[i][17] = data_9[i][1]

    if i < len(data_10):
        matrix_service[i][18] = data_10[i][0]
        matrix_service[i][19] = data_10[i][1]

    if i < len(data_11):
        matrix_service[i][20] = data_11[i][0]
        matrix_service[i][21] = data_11[i][1]

    if i < len(data_12):
        matrix_service[i][22] = data_12[i][0]
        matrix_service[i][23] = data_12[i][1]

    if i < len(data_13):
        matrix_service[i][24] = data_13[i][0]
        matrix_service[i][25] = data_13[i][1]

    if i < len(data_14):
        matrix_service[i][26] = data_14[i][0]
        matrix_service[i][27] = data_14[i][1]

    if i < len(data_15):
        matrix_service[i][28] = data_15[i][0]
        matrix_service[i][29] = data_15[i][1]

    if i < len(data_16):
        matrix_service[i][30] = data_16[i][0]
        matrix_service[i][31] = data_16[i][1]

    if i < len(data_17):
        matrix_service[i][32] = data_17[i][0]
        matrix_service[i][33] = data_17[i][1]

    if i < len(data_18):
        matrix_service[i][34] = data_18[i][0]
        matrix_service[i][35] = data_18[i][1]

    if i < len(data_19):
        matrix_service[i][36] = data_19[i][0]
        matrix_service[i][37] = data_19[i][1]


print("matrix_service以构建完成！matrix_service.shape:{}".format(matrix_service.shape))
np.savetxt('../txtData\\'+'POI_matrix_service.txt', np.c_[matrix_service], fmt='%.10f', delimiter=' ')
print("matrix_service已存储到txt文件内！")


matrix = np.zeros((len(data_stay_point), 19))

startTime = time.time()
# 停留点区域 即半径r
r = 100
for i in range(len(data_stay_point)):
    # 停留点经纬度
    lat = data_stay_point[i][0]
    lng = data_stay_point[i][1]
    # matrix[i][0] = i
    # matrix[i][1] = lat
    # matrix[i][2] = lng

    # 首先遍历交通设施服务
    count = 0
    for j_1 in range(len(data_1)):
        lat_1 = data_1[j_1][0]
        lng_1 = data_1[j_1][1]
        if geo_distance(lat, lng, lat_1, lng_1) <= r:
            count += 1

    matrix[i][0] = count

    # 住宿服务
    count = 0
    for j_2 in range(len(data_2)):
        lat_2 = data_2[j_2][0]
        lng_2 = data_2[j_2][1]
        if geo_distance(lat, lng, lat_2, lng_2) <= r:
            count += 1

    matrix[i][1] = count

    # 体育休闲服务
    count = 0
    for j_3 in range(len(data_3)):
        lat_3 = data_3[j_3][0]
        lng_3 = data_3[j_3][1]
        if geo_distance(lat, lng, lat_3, lng_3) <= r:
            count += 1

    matrix[i][2] = count

    # 公共设施
    count = 0
    for j_4 in range(len(data_4)):
        lat_4 = data_4[j_4][0]
        lng_4 = data_4[j_4][1]
        if geo_distance(lat, lng, lat_4, lng_4) <= r:
            count += 1

    matrix[i][3] = count

    # 公司企业
    count = 0
    for j_5 in range(len(data_5)):
        lat_5 = data_5[j_5][0]
        lng_5 = data_5[j_5][1]
        if geo_distance(lat, lng, lat_5, lng_5) <= r:
            count += 1

    matrix[i][4] = count

    # 医疗保健服务
    count = 0
    for j_6 in range(len(data_6)):
        lat_6 = data_6[j_6][0]
        lng_6 = data_6[j_6][1]
        if geo_distance(lat, lng, lat_6, lng_6) <= r:
            count += 1

    matrix[i][5] = count

    # 商务住宅
    count = 0
    for j_7 in range(len(data_7)):
        lat_7 = data_7[j_2][0]
        lng_7 = data_7[j_2][1]
        if geo_distance(lat, lng, lat_7, lng_7) <= r:
            count += 1

    matrix[i][6] = count

    # 摩托车服务
    count = 0
    for j_8 in range(len(data_8)):
        lat_8 = data_8[j_8][0]
        lng_8 = data_8[j_8][1]
        if geo_distance(lat, lng, lat_8, lng_8) <= r:
            count += 1

    matrix[i][7] = count

    # 政府机构及社会团体
    count = 0
    for j_9 in range(len(data_9)):
        lat_9 = data_9[j_9][0]
        lng_9 = data_9[j_9][1]
        if geo_distance(lat, lng, lat_9, lng_9) <= r:
            count += 1

    matrix[i][8] = count

    # 汽车服务
    count = 0
    for j_10 in range(len(data_10)):
        lat_10 = data_10[j_10][0]
        lng_10 = data_10[j_10][1]
        if geo_distance(lat, lng, lat_10, lng_10) <= r:
            count += 1

    matrix[i][9] = count

    # 汽车维修
    count = 0
    for j_11 in range(len(data_11)):
        lat_11 = data_11[j_11][0]
        lng_11 = data_11[j_11][1]
        if geo_distance(lat, lng, lat_11, lng_11) <= r:
            count += 1

    matrix[i][10] = count

    # 汽车销售
    count = 0
    for j_12 in range(len(data_12)):
        lat_12 = data_12[j_12][0]
        lng_12 = data_12[j_12][1]
        if geo_distance(lat, lng, lat_12, lng_12) <= r:
            count += 1

    matrix[i][11] = count

    # 生活服务
    count = 0
    for j_13 in range(len(data_13)):
        lat_13 = data_13[j_13][0]
        lng_13 = data_13[j_13][1]
        if geo_distance(lat, lng, lat_13, lng_13) <= r:
            count += 1

    matrix[i][12] = count

    # 科教文化服务
    count = 0
    for j_14 in range(len(data_14)):
        lat_14 = data_14[j_14][0]
        lng_14 = data_14[j_14][1]
        if geo_distance(lat, lng, lat_14, lng_14) <= r:
            count += 1

    matrix[i][13] = count

    # 购物服务
    count = 0
    for j_15 in range(len(data_15)):
        lat_15 = data_15[j_15][0]
        lng_15 = data_15[j_15][1]
        if geo_distance(lat, lng, lat_15, lng_15) <= r:
            count += 1

    matrix[i][14] = count

    # 道路附属设施
    count = 0
    for j_16 in range(len(data_16)):
        lat_16 = data_16[j_16][0]
        lng_16 = data_16[j_16][1]
        if geo_distance(lat, lng, lat_16, lng_16) <= r:
            count += 1

    matrix[i][15] = count

    # 金融保险服务
    count = 0
    for j_17 in range(len(data_17)):
        lat_17 = data_17[j_17][0]
        lng_17 = data_17[j_17][1]
        if geo_distance(lat, lng, lat_17, lng_17) <= r:
            count += 1

    matrix[i][16] = count

    # 风景名胜
    count = 0
    for j_18 in range(len(data_18)):
        lat_18 = data_18[j_18][0]
        lng_18 = data_18[j_18][1]
        if geo_distance(lat, lng, lat_18, lng_18) <= r:
            count += 1

    matrix[i][17] = count

    # 餐饮服务

    count = 0
    for j_19 in range(len(data_19)):
        lat_19 = data_19[j_19][0]
        lng_19 = data_19[j_19][1]
        if geo_distance(lat, lng, lat_19, lng_19) <= r:
            count += 1

    matrix[i][18] = count



matrix_1 = np.zeros((19, 1))

# 交通设施服务
matrix_1[0][0] = math.log(len(data_stay_point) / function_2(data_1, data_stay_point, r))
# 住宿服务
matrix_1[1][0] = math.log(len(data_stay_point) / function_2(data_2, data_stay_point, r))
# 体育休闲服务
matrix_1[2][0] = math.log(len(data_stay_point) / function_2(data_3, data_stay_point, r))
# 公共设施
matrix_1[3][0] = math.log(len(data_stay_point) / function_2(data_4, data_stay_point, r))
# 公司企业
matrix_1[4][0] = math.log(len(data_stay_point) / function_2(data_5, data_stay_point, r))
# 医疗保健服务
matrix_1[5][0] = math.log(len(data_stay_point) / function_2(data_6, data_stay_point, r))
# 商务住宅
matrix_1[6][0] = math.log(len(data_stay_point) / function_2(data_7, data_stay_point, r))
# 摩托车服务
matrix_1[7][0] = math.log(len(data_stay_point) / function_2(data_8, data_stay_point, r))
# 政府机构及社会团体
matrix_1[8][0] = math.log(len(data_stay_point) / function_2(data_9, data_stay_point, r))
# 汽车服务
matrix_1[9][0] = math.log(len(data_stay_point) / function_2(data_10, data_stay_point, r))
# 汽车维修
matrix_1[10][0] = math.log(len(data_stay_point) / function_2(data_11, data_stay_point, r))
# 汽车销售
matrix_1[11][0] = math.log(len(data_stay_point) / function_2(data_12, data_stay_point, r))
# 购物服务
matrix_1[12][0] = math.log(len(data_stay_point) / function_2(data_13, data_stay_point, r))
# 科教文化服务
matrix_1[13][0] = math.log(len(data_stay_point) / function_2(data_14, data_stay_point, r))
# 购物服务
matrix_1[14][0] = math.log(len(data_stay_point) / function_2(data_15, data_stay_point, r))
# 道路附属设施
matrix_1[15][0] = math.log(len(data_stay_point) / function_2(data_16, data_stay_point, r))
# 金融保险服务
matrix_1[16][0] = math.log(len(data_stay_point) / function_2(data_17, data_stay_point, r))
# 风景名胜
matrix_1[17][0] = math.log(len(data_stay_point) / function_2(data_18, data_stay_point, r))
# 餐饮服务
matrix_1[18][0] = math.log(len(data_stay_point) / function_2(data_19, data_stay_point, r))

print(matrix)
print(matrix_1)

matrix_2 = np.zeros((len(data_stay_point), 19))

for i in range(len(matrix)):
    POI_count = 0
    for j in range(19):
        POI_count += matrix[i][j]
    for j in range(19):
        matrix_2[i][j] = (matrix[i][j] / POI_count) * matrix_1[j][0]

np.savetxt('../txtData\\'+'POI.txt', np.c_[matrix_2], fmt='%.10e', delimiter=' ')


endTime = time.time()

print("共用时:{}s".format(endTime - startTime))





