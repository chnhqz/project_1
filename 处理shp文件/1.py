import numpy as np

mattrix = np.zeros((3, 3))
np.savetxt('../txtData\\'+'POI.txt', np.c_[mattrix], fmt='%d', delimiter='\t')