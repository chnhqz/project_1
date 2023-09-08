import geopandas as gpd
from matplotlib import pyplot as plt

data = gpd.read_file(r'../POIdata/商务住宅.shp')#读取磁盘上的矢量文件
# data = gpd.read_file('shapefile/china.gdb', layer='province')#读取gdb中的矢量数据
# print(data.crs)  # 查看数据对应的投影信息

'''
if float(item_list[0]) >= 39.1 and float(item_list[0]) <= 41.1 and float(item_list[1]) >= 115.4 and float(item_list[1]) <= 117.6:

data.geometry = POINT (115.67472321194444 41.663950925277774) 经度 - 维度
type(data_) = <class 'shapely.geometry.point.Point'>
'''

def getCoordinate(coordinateStr):
    tmp = 0
    for i in range(6 ,len(coordinateStr)):
        if coordinateStr[i] == ' ':
            tmp = i
    return coordinateStr[7:tmp], coordinateStr[tmp + 1: len(coordinateStr) - 1]

coordinate = []
for data_ in data.geometry:
    coordinateStr = str(data_)
    lngStr, latStr = getCoordinate(coordinateStr)

    lng = float(lngStr)
    lat = float(latStr)

    if lat >= 39.1 and lat <= 41.1 and lng >= 115.4 and lng <= 117.6:
        coordinate.append((lat, lng))

with open("../txtData/POI/商务住宅.txt", 'w') as f:
    for coordinate_ in coordinate:
        strAll = str(coordinate_[0]) + " " + str(coordinate_[1]) + "\n"
        f.write(strAll)

# print(data.head())  # 查看前5行数据
# data.plot()
# plt.show()#简单展示

























