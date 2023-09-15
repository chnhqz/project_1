import json
import math
import numpy as np
import matplotlib.colors as colors
import matplotlib.cm as cmx
import random
from scipy.special import lambertw
import os


# 读取数据
def loadData(path, user):
    '''
    数据集
    维度 经度 高度 日期 时间
    '''
    lat = []                                        # 维度
    lng = []                                        # 经度
    high = []                                       # 高度
    date = []                                       # 日期
    time = []                                       # 时间
    loc = []                                        # 位置点数据
    path = path + "//" + user + "//Trajectory"
    plts = os.scandir(path)
    for item in plts:
        # print(item)
        # 这里边item是指文件夹内的文件
        path_item = path + "//" + item.name  # 文件夹内每一个子文件的绝对路径
        with open(path_item, 'r+') as fp:
            for item in fp.readlines():
                # 这里是打开了单个文件内每一行数据
                item_list = item.split(',')
                if len(item_list) < 7:
                    continue
                if float(item_list[0]) >= 39.1 and float(item_list[0]) <= 41.1 and float(item_list[1]) >= 115.4 and float(item_list[1]) <= 117.6:
                    # 意思是只需要位于北京区域的位置点
                    lat.append(item_list[0])
                    lng.append(item_list[1])
                    high.append(item_list[3])
                    date.append(item_list[5])
                    time.append(item_list[6])
                    loc.append((item_list[0], item_list[1], item_list[3], item_list[5], item_list[6]))
                    # loc指的是单个文件内的所有轨迹数据点
    return loc

path = "F://hqz_all_file//pythonProject//project_1//data"
user = "000"
loc = loadData(path, user)                                                                                              # loc是全部位置点

'''
loc (lat lng high date time)
'''

print(len(loc))

loc_martix = np.zeros((len(loc), 5))

with open('../oriData/000/trajectory.txt','w') as f:
    for i in range(len(loc)):
        loc_str = loc[i][0] + " " + loc[i][1] + " " + loc[i][2] + " " + loc[i][3] + " " + loc[i][4]
        f.write(loc_str)

































