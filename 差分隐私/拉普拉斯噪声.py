import random
import numpy as np
from scipy.special import lambertw
import matplotlib.pyplot as plt

# 计算基于拉普拉斯分布的噪声
def laplace_noisy(sensitivety, epsilon):
    n_value = np.random.laplace(0, sensitivety / epsilon, 1)
    return n_value


# 计算基于拉普拉斯加噪的混淆值
def laplace_mech(data, sensitivety, epsilon):
    for i in range(len(data)):
        data[i] += laplace_noisy(sensitivety, epsilon)
    return data

# 计算r，其中r代表扰动后发布位置与真实位置之间的距离
def r_compute(epsilon):
    t = random.uniform(0, 1)
    r = (1 / epsilon) * (lambertw((t - 1) / epsilon) + 1)
    return r

# 计算极坐标中的角度
def theta_compute():
    theta = random.uniform(0, 360)
    return theta

# 绘制图像
def draw():
    epsilons = []

    for i in range(100):
        epsilons.append(random.uniform(0.1, 10))


    r = []
    for epsilon in epsilons:
        r.append(r_compute(epsilon))
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
    colors = ['mistyrose', 'lightcoral', 'salmon', 'tomato', 'cyan', 'deepskyblue', 'red']

    plt.title("发布位置与真实位置之间的距离图")
    plt.xlabel("epsilon")
    plt.ylabel("r")

    plt.scatter(list(epsilons), list(r), color=colors[4])
    plt.show()





# 基于拉普拉斯分布的特性，如果想要分布震荡较小，需要将隐私预算epsilon的值设置较大
if __name__ == '__main__':

    lat_lng = [31.3, 141.2]  # 坐标

    data = [1., 2., 3.]
    sensitivety = 1
    epsilon = 100
    r = r_compute(epsilon)
    theta = theta_compute()
    print(r, theta)
    data_noisy = laplace_mech(data, sensitivety, epsilon)
    for j in data_noisy:
        print("Final Resulet = %.16f" % j)

    draw()






# 输出结果
# (tensorflow)  dubaokun@ZBMAC-C02D5257M  ~ python laplace_apply.py
# Final Resulet = 1.1131262345421142
# Final Resulet = 1.9423797734301973
# Final Resulet = 3.0605257391487291
