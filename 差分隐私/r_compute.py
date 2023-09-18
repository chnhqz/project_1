import math
import random
from scipy.special import lambertw
import matplotlib.pyplot as plt
from geopy.distance import geodesic
import numpy as np






def r_compute(epsilon):
    t = random.uniform(0, 1)
    while (((t - 1) / epsilon) + 1) < - (1 / math.e):
        t = random.uniform(0, 1)

    r = - (1 / epsilon) * (lambertw((((t - 1) / epsilon) + 1), k=-1))
    print(r)
    return int(r)

# r = r_compute(100000)
# print(r)




#
# epsilon = []
# r = []
#
#
# for i in range(1000):
#     tmp = random.uniform(0.01, 1)
#     epsilon.append(tmp)
#     r.append(r_compute(tmp))
#
#
#
# plt.title("epsilon-r")
# plt.xlabel("epsilon")
# plt.ylabel("r")
#
# plt.scatter(list(epsilon), list(r), color='red', linewidth=2.5)
# plt.show()

def coordinateTranslate(lat, lng, dis, x, theta):
    latTranslate = lat + (dis / x) * math.cos(theta)
    lngTranslate = lng + (dis / x) * math.sin(theta)
    return latTranslate, lngTranslate

lat, lng = 40.00633, 116.321461

x = 1000
lat1, lng1 = 41.00633, 117.321461
print("x:{}".format(x))
print("dis:{}".format(geodesic((lat, lng), (lat1, lng1)).m))
while float(geodesic((lat, lng), (lat1, lng1)).m - 100.0) > 1.0:
    x = random.uniform(0, 100000)
    lat1, lng1 = coordinateTranslate(lat, lng, 100, x, random.uniform(0, 2 * math.pi))


print("x:{}".format(x))
print("dis:{}".format(geodesic((lat, lng), (lat1, lng1)).m))

'''
x:85234.2896058041
dis:100.68134078515084
'''



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

print(comculate_angle(-1, -1, 0, 1) * 180 / np.pi)








