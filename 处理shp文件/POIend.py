import os
import numpy as np

POI_matrix = np.genfromtxt("../txtData/matrix_poi.txt", dtype=[int, int, int, int, int, int, int, int, int, int,
                                                               int, int, int, int, int, int, int, int, int, int,])  # 将文件中数据加载到data数组里

# log_matrix = np.genfromtxt("../txtData/a.txt", dtype=[float, float, float, float, float, float, float, float, float, float,
#                                                       float, float, float, float, float, float, float, float, float,])

log_matrix = [1.0986122887, 2.4849066498, 1.6094379124, 1.6094379124, 1.9459101491, 2.1972245773, 0.6931471806, 8.6896327484, 1.0986122887, 3.4965075615, 4.0430512678, 4.7957905456,
              1.0986122887, 0.6931471806, 1.3862943611, 7.3031700512, 1.9459101491, 3.663561646, 1.3862943611]

end_matrix = np.zeros((len(POI_matrix), 19))

for i in range(len(POI_matrix)):
    for j in range(len(POI_matrix[0]) - 1):
        count_poi = POI_matrix[i][len(POI_matrix[0]) - 1]
        if count_poi == 0:
            count_poi = 1
        end_matrix[i][j] = POI_matrix[i][j] / count_poi * log_matrix[j]

print(end_matrix)
np.savetxt('../txtData\\'+'end_matrix.txt', np.c_[end_matrix], fmt='%.10f', delimiter=' ')













