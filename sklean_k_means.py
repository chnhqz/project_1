from sklearn.cluster import KMeans
import pack_tra
import numpy as np
from matplotlib import pyplot
import os
from sklearn import metrics

path = os.getcwd() + "//data"
user = "000"
tra, loc = pack_tra.loadData(path, user)                                                                                # tra, loc 分别为全部轨迹，和全部位置点
print("用户{}共有{}条轨迹数据".format(user, len(tra)))
# 以下处理只针对一条轨迹来进行处理

tra_100 = tra[0]

# tra = tra[100]
# print("轨迹包含{}个轨迹点".format(len(tra)))

# x = np.array([[1, 2], [1.5, 1.8], [5, 8], [8, 8], [1, 0.6], [9, 11]])

array = pack_tra.allTraToKmeans(tra)

# array = pack_tra.traToKMeans(tra)
# 数据归一化
array = np.divide(np.subtract(array, np.min(array, axis=0)), np.subtract(np.max(array, axis=0), np.min(array, axis=0)))
# print(array)

print("轨迹包含{}个轨迹点".format(len(array)))

# 把上面数据点分为两组（非监督学习）
def testK():
    scores = []
    for i in range(2, 50):
        print("第{}次循环".format(i))
        km = KMeans(n_clusters=i, max_iter=300)
        km.fit(array)
        # 轮廓系数
        # scores.append(metrics.silhouette_score(array, km.labels_, metric='euclidean'))
        # SSE 样本距离最近的聚类中心的距离总和 （簇内误差平方和）
        scores.append(km.inertia_)

    pyplot.plot(range(2, 50), scores, marker='o')
    pyplot.xlabel('Number of clusters')
    pyplot.ylabel('silhouette_score')
    pyplot.show()

# 聚类并预测
def julei():
    # 聚类簇的数量
    k = 30
    clf = KMeans(n_clusters=k)
    clf.fit(array)  # 分组

    centers = clf.cluster_centers_  # 数据点的中心点
    labels = clf.labels_  # 每个数据点所属分组
    print("分类点的中心坐标")
    print(centers)
    print("所有点的分类标签")
    print(labels)

    colors = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond',
              'blue',
              'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue',
              'cornsilk', 'crimson',
              'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkkhaki', 'darkmagenta',
              'darkolivegreen', 'darkorange',
              'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkturquoise',
              'darkviolet', 'deeppink', 'deepskyblue',
              'dimgray', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite',
              'gold', 'goldenrod',
              'gray', 'green', 'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki',
              'lavender',
              'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan',
              'lightgoldenrodyellow', 'lightgreen', 'lightgray', 'lightpink',
              'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightsteelblue', 'lightyellow', 'lime',
              'limegreen', 'linen', 'magenta',
              'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen',
              'mediumslateblue', 'mediumspringgreen', 'mediumturquoise']

    # 计算每个分类的频率

    sumPoint = len(array)
    proPoint = np.zeros((k,), dtype=np.int64)
    print(proPoint.shape)
    for i in range(len(labels)):
        proPoint[labels[i]] += 1

    probabilityPoint = np.zeros((k,))
    for i in range(k):
        probabilityPoint[i] = proPoint[i] / sumPoint

    pointAttribute = []
    count = 0

    arrayTra100 = pack_tra.traToKMeans(tra_100)
    arrayTra100 = np.divide(np.subtract(arrayTra100, np.min(arrayTra100, axis=0)),
                      np.subtract(np.max(arrayTra100, axis=0), np.min(arrayTra100, axis=0)))

    label = clf.predict(arrayTra100)
    for tra_ in tra_100:

        pointAttributeTmp = {
            'id': count,
            'lat': tra_[0],
            'lng': tra_[1],
            'frequency': probabilityPoint[label[count]]
        }
        count += 1
        pointAttribute.append(pointAttributeTmp)
    # print(pointAttribute)
    pack_tra.save_json("jsonData/pointFrequency.json", pointAttribute)

    print(probabilityPoint)

    for i in range(len(labels)):
        if i % 100 == 0:
            pyplot.scatter(array[i][0], array[i][1], c=colors[labels[i]])
    pyplot.scatter(centers[:, 0], centers[:, 1], marker='*', s=100)

    # 预测
    # predict = [[40.00823937, 116.31899055], [39.98616056, 116]]
    # label = clf.predict(predict)
    # for i in range(len(label)):
    #     pyplot.scatter(predict[i][0], predict[i][1], c=colors[labels[i]], marker='x')

    pyplot.show()

julei()

