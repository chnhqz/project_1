import pack_tra
import os
import time
import k_means


path = os.getcwd() + "//data"
user = "000"
tra, loc = pack_tra.loadData(path, user)                                                                                # tra, loc 分别为全部轨迹，和全部位置点

print("用户{}共有{}条轨迹数据".format(user, len(tra)))
# 以下处理只针对一条轨迹来进行处理

tra = tra[100]
print("轨迹包含{}个轨迹点".format(len(tra)))


# pack_tra.drawTrajectory(tra)
# for k in range(1, len(tra)):
#     print(pack_tra.geo_distance(tra[k][0], tra[k][1], tra[k - 1][0], tra[k - 1][1]))

tra = pack_tra.traToTrajectory(tra)
# pack_tra.drawTrajectory(tra)

startTime = time.time()

# Stay, traAllStay, pointAttribute = pack_tra.stay_point(tra, 100, 1800)
stayPoint, pointAttribute = pack_tra.stayPointNew(tra, 100, 1800)
# pack_tra.drawTrajectory1(tra, Stay)

fakeTrajectory = pack_tra.addNoiseToTrueCoordinate(tra)
#
pack_tra.drawTrajectory1(tra, fakeTrajectory)

print("共有{}个停留点".format(len(stayPoint)))
# print("共有{}个停留点".format(len(Stay)))

pack_tra.save_json("jsonData/stayPoint.json", stayPoint)
pack_tra.save_json("jsonData/pointAttribute.json", pointAttribute)
endTime = time.time()

print("共用时:{}s".format(endTime - startTime))

coordinate = pack_tra.getJsonCoordinate("./jsonData/stayPoint.json")
pack_tra.drawTrajectory1(tra, coordinate)




