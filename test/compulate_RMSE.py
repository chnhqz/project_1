import numpy as np
import math








fake_true_trajectory = np.genfromtxt("../oriData/000/fake_true_trajectory.txt", dtype=[float, float, float, float])


def RMSE(trajectory):
    RMSEnumber = 0.0
    for i in range(len(trajectory)):
        RMSEnumber += pow((trajectory[i][0] - trajectory[i][2]), 2) + pow((trajectory[i][1] - trajectory[i][3]), 2)

    return math.sqrt(RMSEnumber / len(trajectory))

print(RMSE(fake_true_trajectory))


















