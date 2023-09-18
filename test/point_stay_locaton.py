from geopy.distance import geodesic
import math
import numpy as np
import random
from scipy.special import lambertw
import matplotlib.pyplot as plt


def r_compute(epsilon):
    t = random.uniform(0, 1)
    while (((t - 1) / float(epsilon)) + 1) < - (1 / math.e):
        t = random.uniform(0, 1)
    r = - (1 / epsilon) * (lambertw((((t - 1) / epsilon) + 1), k=-1))
    # print(int(r))
    return int(r)

# r = r_compute(100000)
# print(r)


# 计算极坐标中的角度
def theta_compute():
    theta = random.uniform(0, 2 * math.pi)
    return theta




# 对不同的坐标点计算不同的得分
def score(point, w_staydis, w_staytime, w_locationdis, bias):
    staydis = point[12]
    staytime = point[6]
    locationdis = point[13]
    score = w_staydis * staydis + w_staytime * staytime + w_locationdis * locationdis + bias
    return score

# 对不同的坐标点计算不同的epsilon
def computeDifferentEpsilon(point, epsilon):
    epsilon1 = epsilon * (1.0 - float(point[15]))
    # print("epsilon:{}".format(epsilon))
    # print(0.1 * (1 - float(point[15])) * 10)
    # print("epsilon1:{}".format(epsilon1))
    if float(epsilon1) == 0.0:
        epsilon1 = 0.02
    return float(epsilon1)

# 坐标转换
def coordinateTranslate(lat, lng, dis, theta):
    latTranslate = lat + (dis / 85234.2896058041) * math.cos(theta)
    lngTranslate = lng + (dis / 85234.2896058041) * math.sin(theta)
    return latTranslate, lngTranslate


# 对读取到的用户真实轨迹添加噪声生成虚假轨迹
def addNoiseToTrueCoordinate(point_martix, epsilon):
    fakeTrajectory = []
    fakeTrajectorytmp = []
    for i in range(len(point_martix)):
        if point_martix[i][8] == -1:
            fakeTrajectorytmp.append(point_martix[i][1])
            fakeTrajectorytmp.append(point_martix[i][2])
            for j in range(8):
                fakeTrajectorytmp.append(-1)
            fakeTrajectory.append(fakeTrajectorytmp)
            fakeTrajectorytmp = []

            continue
        epsilonend = computeDifferentEpsilon(point_martix[i], epsilon)
        # print("epsilonend:{}".format(epsilonend))
        r = r_compute(epsilonend)
        # print(type(r))'
        for j in range(5):
            theta = theta_compute()
            lat, lng = coordinateTranslate(point_martix[i][1], point_martix[i][2], r, theta)
            fakeTrajectorytmp.append(lat)
            fakeTrajectorytmp.append(lng)
        fakeTrajectory.append(fakeTrajectorytmp)
        fakeTrajectorytmp = []
    return fakeTrajectory

# 计算两个向量之间的角度
def comculate_angle(lat1, lng1, lat2, lng2):

    vec1 = np.array([float(lat1), float(lng1)])
    vec2 = np.array([float(lat2), float(lng2)])

    # 分别计算两个向量的模：
    l_vec1 = np.sqrt(vec1.dot(vec1))
    l_vec2 = np.sqrt(vec2.dot(vec2))

    # 计算两个向量的点积
    dian = vec1.dot(vec2)

    # 计算夹角的cos值：
    cos_ = dian / (l_vec1 * l_vec2)

    # 求得夹角（弧度制）：
    angle = np.arccos(cos_)


    return angle

# 数值标准化

def min_max(vec1):
    vec = np.array(vec1)

    min_vec = min(vec)
    max_vec = max(vec)

    min_max_vec = []
    for i in range(len(vec)):
        min_max_vec.append((vec[i] - min_vec) / (max_vec - min_vec))

    return min_max_vec



# 选择最优的混淆位置
def select_min_dis_tra(fakeTrajectory):
    tra_start = []
    tra_end = []

    obs_tra_start = []
    obs_tra_end = []


    obs_tra = []
    obs_tra.append((fakeTrajectory[0][0], fakeTrajectory[0][1]))

    for i in range(1, len(fakeTrajectory)):

        tra_start.append((fakeTrajectory[i - 1][0], fakeTrajectory[i - 1][1]))
        tra_end.append((fakeTrajectory[i][0], fakeTrajectory[i][1]))

        if fakeTrajectory[i][4] == -1.0:
            obs_tra.append((fakeTrajectory[i][0], fakeTrajectory[i][1]))
            continue
        for j in range(5):
            obs_tra_end.append((fakeTrajectory[i][2 * j + 2], fakeTrajectory[i][2 * j + 3]))

        vec_L = []
        vec_angle = []
        for k in range(len(obs_tra_end)):
            # 原始轨迹距离
            L = geodesic((tra_start[0][0], tra_start[0][1]), (tra_end[0][0], tra_end[0][1]))

            # 目前混淆轨迹距离
            L_obs = geodesic((obs_tra[i - 1][0], obs_tra[i - 1][1]), (obs_tra_end[k][0], obs_tra_end[k][1]))
            vec_L.append(abs(L_obs - L))
            vec_angle.append(comculate_angle(obs_tra_end[k][0] - obs_tra[i - 1][0], obs_tra_end[k][1] - obs_tra[i - 1][1], tra_end[0][0] - tra_start[0][0], tra_end[0][1] - tra_start[0][1]))

        vec_L_min_max = min_max(vec_L)
        vec_angle_min_max = min_max(vec_angle)

        dis = 3
        flag_obs_tra = 0

        for k in range(len(vec_L_min_max)):
            if vec_angle_min_max[k] + vec_angle_min_max[k] < dis:
                dis = vec_angle_min_max[k] + vec_angle_min_max[k]
                flag_obs_tra = k
        # print(flag_obs_tra)
        obs_tra.append((fakeTrajectory[i][2 * flag_obs_tra + 2], fakeTrajectory[i][2 * flag_obs_tra + 3]))

        tra_start = []
        tra_end = []
        obs_tra_end = []


    return obs_tra




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

# 计算epsilon


'''
组建一个所有点的信息矩阵
'''
'''
location : ID lat lng
stayAttribute : ID lat lng locationID
pointAttribute : ID lat lng stayID staytime
'''
location = np.genfromtxt("../oriData/000/location.txt", dtype=[int, float, float])
stayAttribute = np.genfromtxt("../oriData/000/stayAttribute.txt", dtype=[int, float, float, int])
pointAttribute = np.genfromtxt("../oriData/000/pointAttribute.txt", dtype=[int, float, float, int, int])


'''
                0  1   2    3       4       5       6        7        8          9            10          11        12         13       14      15
point_martix : ID lat lng stayID stayLat stayLng staytime staydis LocationID LocationLat LocationLng Locationdis staydis1 Locationdis1 score  score1

后边两列的 staydis1 Locationdis1 指的是标准化后的距离 score1 指的是标准化后的得分
'''
point_martix = np.zeros((len(pointAttribute), 16))

for i in range(len(pointAttribute)):
    for j in range(16):
        point_martix[i][j] = -1




for i in range(len(pointAttribute)):
    point_martix[i][0] = i
    point_martix[i][1] = pointAttribute[i][1]
    point_martix[i][2] = pointAttribute[i][2]
    # 判断该点是停留点
    if pointAttribute[i][3] != -1:
        # 该点是停留点接着判断这个点是否是语义位置点
        point_martix[i][3] = pointAttribute[i][3]
        point_martix[i][4] = stayAttribute[pointAttribute[i][3]][1]
        point_martix[i][5] = stayAttribute[pointAttribute[i][3]][2]
        point_martix[i][6] = pointAttribute[i][4]
        staydis = geodesic((pointAttribute[i][1], pointAttribute[i][2]), (point_martix[i][4], point_martix[i][5])).m
        point_martix[i][7] = staydis
        # 该点既是属于停留点 又是语义位置点
        if stayAttribute[pointAttribute[i][3]][3] != -1:
            point_martix[i][8] = stayAttribute[pointAttribute[i][3]][3]
            point_martix[i][9] = location[stayAttribute[pointAttribute[i][3]][3]][1]
            point_martix[i][10] = location[stayAttribute[pointAttribute[i][3]][3]][2]
            staydis1 = geodesic((pointAttribute[i][1], pointAttribute[i][2]), (point_martix[i][9], point_martix[i][10])).m
            point_martix[i][11] = staydis1

# 标准化停留点距离
distmp = []
flag = -1
for i in range(len(point_martix)):
    if point_martix[i][3] != -1:
        flag = point_martix[i][3]
        break

for i in range(len(point_martix)):
    if point_martix[i][3] == -1:
        continue

    if flag == int(point_martix[i][3]):
        distmp.append((i, point_martix[i][7]))

    else:
        flag = int(point_martix[i][3])
        distmp_ = []
        for j in range(len(distmp)):
            distmp_.append(distmp[j][1])

        min1 = min(distmp_)
        max1 = max(distmp_)
        for j in range(len(distmp)):
            # print((distmp[j][1] - min1) / (max1 - min1))
            point_martix[distmp[j][0]][12] = (distmp[j][1] - min1) / (max1- min1)

        distmp = []


# 标准化语义位置距离
distmp = []
flag = -1
for i in range(len(point_martix)):
    if point_martix[i][8] != -1:
        flag = point_martix[i][8]
        break

for i in range(len(point_martix)):
    if point_martix[i][8] == -1:
        continue

    if flag == int(point_martix[i][8]):
        distmp.append((i, point_martix[i][11]))

    else:
        flag = int(point_martix[i][8])
        distmp_ = []
        for j in range(len(distmp)):
            distmp_.append(distmp[j][1])
        min1 = min(distmp_)
        max1 = max(distmp_)
        for j in range(len(distmp)):
            point_martix[distmp[j][0]][13] = (distmp[j][1] - min1) / (max1- min1)

        distmp = []

for i in range(len(point_martix)):
    if point_martix[i][8] == -1:
        continue
    point_martix[i][14] = score(point_martix[i], 1, 0.01, 1, 10)

scoreSum = []
for i in range(len(point_martix)):
    if point_martix[i][14] == -1:
        continue
    scoreSum.append(point_martix[i][14])

min1 = min(scoreSum)
max1 = max(scoreSum)
for i in range(len(point_martix)):
    if point_martix[i][14] == -1:
        continue
    point_martix[i][15] = (point_martix[i][14] - min1) / (max1 - min1)



fakeTrajectory = addNoiseToTrueCoordinate(point_martix, 1.0)

# print(len(fakeTrajectory[0]))

fake_true_trajectory = np.genfromtxt("../oriData/000/fake_true_trajectory.txt", dtype=[float, float, float, float, float, float,
                                                                                       float, float, float, float, float, float])

min_tra = select_min_dis_tra(fake_true_trajectory)

drawTrajectory1(point_martix, min_tra)









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

saveTxt(point_martix, "../oriData/000/point_stay_location.txt")



with open("../oriData/000/fake_true_trajectory.txt", 'w') as f:
    for i in range(len(point_martix)):
        loc_str = str(point_martix[i][1]) + " " + str(point_martix[i][2]) + " "\
                  + str(fakeTrajectory[i][0]) + " " + str(fakeTrajectory[i][1]) + " " + str(fakeTrajectory[i][2]) + " " + str(fakeTrajectory[i][3]) + " " + str(fakeTrajectory[i][4]) +\
                " " + str(fakeTrajectory[i][5]) + " " + str(fakeTrajectory[i][6]) + " " + str(fakeTrajectory[i][7]) + " " + str(fakeTrajectory[i][8]) + " " + str(fakeTrajectory[i][9]) + "\n"

        f.write(loc_str)
        loc_str = []











