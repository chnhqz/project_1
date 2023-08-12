import os
import matplotlib.pyplot as plt

'''
数据集
维度 经度 高度 日期 时间
'''

plt.rcParams['font.sans-serif'] = ['SimHei']                    # 正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False                      # 正常显示负号
lat = []                                                        # 维度
lng = []                                                        # 经度
high = []
date = []
time = []
tra = []                                                        # 轨迹数据
path = os.getcwd() + "\\data" + "\\000" + "\\Trajectory"

plts_000 = os.scandir(path)

for item in plts_000:
    path_item = path + "\\" + item.name                         # 文件夹内每一个子文件的绝对路径
    with open(path_item, 'r+') as fp:
        for item in fp.readlines():
            item_list = item.split(',')
            if len(item_list) < 7:
                continue
            if float(item_list[0]) >= 39.1 and float(item_list[0]) <= 41.1 and float(item_list[1]) >= 115.4 and float(item_list[1]) <= 117.6:
                lat.append(item_list[0])
                lng.append(item_list[1])
                high.append(item_list[3])
                date.append(item_list[5])
                time.append(item_list[6])
                tra.append((item_list[0], item_list[1], item_list[3], item_list[5], item_list[6]))



print("共有{}条数据".format(len(lat)))

str_time = tra[0][3]
lat_0 = []
lng_0 = []
count = 0
for tra_ in tra:
    str_time_ = tra_[3]
    print(str_time_)
    if str_time_ != str_time:
        break
    if count % 10 == 0:
        lat_0.append(float(tra_[0]))
        lng_0.append(float(tra_[1]))
    count += 1

lat_new = [float(x) for x in lat]
lng_new = [float(x) for x in lng]
print("{}共有{}条轨迹数据".format(str_time, len(lat_0)))
plt.title("000轨迹测试")
plt.xlabel("经度")
plt.ylabel("维度")
# plt.plot(list(lng_0), list(lat_0))
plt.scatter(list(lng_0), list(lat_0))
plt.show()

