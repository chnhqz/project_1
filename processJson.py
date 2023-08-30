'''
用户000的第100条轨迹共有157646个轨迹点。



'''
import os
import pack_tra




path = os.getcwd() + "//data"
user = "000"
tra, loc = pack_tra.loadData(path, user)                                                                                # tra, loc 分别为全部轨迹，和全部位置点

print("用户{}共有{}条轨迹数据".format(user, len(tra)))
# 以下处理只针对一条轨迹来进行处理

tra = tra[0]
print("轨迹包含{}个轨迹点".format(len(tra)))

tra = pack_tra.traToTrajectory(tra)

# stayPoint, pointAttribute = pack_tra.stayPointNew(tra, 100, 1800)
# pack_tra.drawTrajectory1(tra, stayPoint)

# print("共有{}个停留点".format(len(stayPoint)))

# 读取停留点内的json文件



# coordinate = pack_tra.getJsonCoordinate("jsonData/stayPoint.json")
# pack_tra.drawTrajectory1(tra, coordinate)


coor1 = pack_tra.loadPoint1("jsonData/pointAttribute.json")
coor2 = pack_tra.loadPoint2("jsonData/pointFrequency.json")

allAttribute = []
# print(len(coor1))
for i in range(len(coor2)):
    if i < len(coor1):
        if coor1[i][0] == coor2[i][0]:
            allAttribute.append((coor1[i][0], coor1[i][1], coor1[i][2], coor1[i][3], coor1[i][4], coor2[i][3]))
    else:
        id = coor2[i][0]
        lat = coor2[i][1]
        lng = coor2[i][2]
        staypoint = 0
        staytime = 0
        frequency = coor2[i][3]
        allAttribute.append((id, lat, lng, staypoint, staytime, frequency))

with open("txtData/000/1.txt", 'w') as f:
    for allAttribute_ in allAttribute:
        strall = str(allAttribute_[0]) + " " + str(allAttribute_[1]) + " " + str(allAttribute_[2]) + " " + str(allAttribute_[3]) + " " + str(allAttribute_[4]) + " " + str(allAttribute_[5]) + "\n"
        f.write(strall)


# jsonPath = "allJsonData/000/" + tra[0][3]
#
# pack_tra.save_json(jsonPath, pointAttribute)











































