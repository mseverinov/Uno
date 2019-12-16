import numpy as np
arrays = np.array([np.array(range(5)) for i in range(10)])

a = np.average(arrays, axis = 0)
print(a)
