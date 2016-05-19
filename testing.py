import numpy as np
# # from iotdata import IOTData
# # from ShimmerBluetooth import ShimmerBluetooth


# # test = ShimmerBluetooth("COM9", 256)
# # test.getFrame()

# data = np.array([[4, 3, 2, 1],[3,2,4,5]])
# print data

# print data.shape, type(data.shape[0])

# print data.shape[0]/2

# a = np.reshape(data,(1,-1))
# a = a[0]
# print a

# tempdata = np.array(data)
# data2d = np.zeros([3, 1])
# data2d[0,0] = data[0]
# data2d[1,0] = data[1]
# data2d[2,0] = data[2]

# print data2d

# a = [[1,2,4],[1,4,7]]
# an = np.array(a)
# print an

# from ShimmerBluetooth import ShimmerBluetooth as sb
# from calibration import calibrateInertialSensorData


# some test code for calibration

# print calibrateInertialSensorData([2033,2035,1237],AMa,SMa,OVa)

# print calibrateInertialSensorData([-129,62,-13],AMg,SMg,OVg)

# from iotdata import IOTData
# from ShimmerBluetooth import ShimmerBluetooth

# sensor = ShimmerBluetooth("COM9", 256)
# df = sensor.getFrame()
# print df[0]


# print 'a' is not 'a'

# a = np.array([5, 4, 3, 5])

# c = np.argsort(a)
# print c
# # expected: c = np.array([2, 1, 0, 3])
# for i in range(len(a)):
#     print a[c[i]]

# loc = np.where(c==5)
# print loc[0]
# print loc[0].size is 0

# from peakdetect2 import locatePeaks as lpk
# import matplotlib.pyplot as plt
# testData = np.array([0,1,1,1,2,3,2,1,1,2,2,2,1,1,4,1,2,1])
# plt.plot(testData)
# print lpk(testData,2,1,2)
# plt.show()

a = np.array([1,1,2]).reshape(-1,1)
b = np.array([2,3,1]).reshape(-1,1)
c = np.square(a)+np.square(b)
print c

