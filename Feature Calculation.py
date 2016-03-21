
# coding: utf-8

# # Internet of Things Project

# # The Data
# 

# The data is recorded at 50Hz and is formatted as follows:
# 
# unix timestamp,  ax,ay,az,  gx,gy,gz,  temperature,  mx,my,mz,
# 

import matplotlib.pyplot as plt
import numpy as np
import datetime
import csv

class IOTData():

    def __init__(self):
        self.location = "Good_Shimmer_data/3_7_16/3_7_16_Data/"
        self.pre = "Treadmill"
        self.post = ".csv" 
        self.devices = ["1B", "1F", "2B", "3B", "4B","5F"]
        this.dataset = "1B"
        self.loadDataSet()
        self.window = []
        self.windowSize =1024


    def getWindow(self, index):
        while self.windowIndex < index:
            self.getNextWindow()
        return self.window

    def getNextWindow(self):
        self.window = []
        for k in range(self.windowSize):
            window.append(self.reader.next())
        self.windowIndex += 1
        return self.window

    def initdata(self, which):
        self.csvfile = open(self.location + self.pre + which + self.post)
        self.reader = csv.reader(csvfile, delimiter = ',')

        #remove first 3 pieces of data as identifiers
        for i in range(3):
            reader.next()
        self.windowIndex = 0



# data = [[] for k in range(10)]
# for k in range(10):
#     csvfile = open(location2 + pre2 + devices[k] + post2)
#     reader = csv.reader(csvfile, delimiter = ',')
    
#     # Get rid of tag info
#     for i in range(3):
#         reader.next()

#     for row in reader:
#         data[k].append(row)

#     print len(data[k])


# # In[5]:


# for k in range(10):
#     timedata = []
#     toPlot = [[],[],[]]
#     numsamples = len(data[k])
#     x = np.linspace(0,1,numsamples)
#     timedata = []
#     for i in range(numsamples):
#         timedata.append(data[k][i][0])
#         toPlot[0].append(data[k][i][1])
#         toPlot[1].append(data[k][i][2])
#         toPlot[2].append(data[k][i][3])

#     toPlot[0] = np.array(toPlot[0]).astype(np.float)
#     toPlot[1] = np.array(toPlot[1]).astype(np.float)
#     toPlot[2] = np.array(toPlot[2]).astype(np.float)
#     plt.figure(k)
#     plt.plot(timedata,toPlot[0])
#     plt.plot(timedata,toPlot[1])
#     plt.plot(timedata,toPlot[2])

#     #print the timestamp
#     print "Start Time:"
#     print(datetime.datetime.fromtimestamp(
#             float(data[k][0][0])/1000).strftime('%Y-%m-%d %H:%M:%S'))
#     print "End Time"
#     print(datetime.datetime.fromtimestamp(
#             float(data[k][numsamples -1][0])/1000).strftime('%Y-%m-%d %H:%M:%S'))

#     plt.title('Accelerometer Data for ' + devices[k])


# # I'm Writing a helpler function here to better display the plots for the accelerometer Data

# # In[6]:

# def plotSection(index, start, end):
#     tempdata = [[],[],[]]
#     xdata = np.linspace(start,end, end-start)
#     for k in range(start,end):
#         tempdata[0].append(data[index][k][1])
#         tempdata[1].append(data[index][k][2])
#         tempdata[2].append(data[index][k][3])
#     print len(xdata), len(tempdata[0])
#     #print the timestamp
#     print "Start Time:"
#     print(datetime.datetime.fromtimestamp(
#             float(data[index][start][0])/1000).strftime('%Y-%m-%d %H:%M:%S'))
#     print "End Time"
#     print(datetime.datetime.fromtimestamp(
#             float(data[index][end][0])/1000).strftime('%Y-%m-%d %H:%M:%S'))

#     plt.plot(xdata,tempdata[0])
#     plt.plot(xdata,tempdata[1])
#     plt.plot(xdata,tempdata[2])


# # In[7]:

# plotSection(2, 22000,22200 )


# # This graph looks pretty nice - It shows there are a few peaks that definitely look like steps

# # # Filtering
# # Steps will have a very high instantaneous rate of change. Hopefully, the acceleration of the z data stream will show some very high peaks, although this may require a bit of filtering before it will be pretty.

# # In[8]:

# class lowpassfilter:

#     def __init__(self,RC,initialtime):
#         "use RC for tuning the smoothmness"
#         self.RC=RC
#         self.t = initialtime
#         self.x_old=0
#         self.y_old=0
#         self.z_old=0

#     def filter(self,x,y,z,t):
#         "return the low pass filtered valus -dt delta time current step"
#         dt = t -self.t
#         self.t = t
#         k=dt / (self.RC + dt)
#         res_x= self.x_old + k * (x - self.x_old)
#         res_y= self.y_old + k * (y - self.y_old)
#         res_z= self.z_old + k * (z - self.z_old)
#         self.x_old=res_x
#         self.y_old=res_y
#         self.z_old=res_z
#         return t, res_x,res_y,res_z


# # In[9]:

# # initialize a lowpass filter
# # The value can be increased to filter out more information, but the data
# # will need to be scaled up later (or normalized)
# filter = lowpassfilter(50, float(data[2][0][0]) -1)
# tempdata = []
# for point in data[2]:
#     tempdata.append(filter.filter(float(point[1]), float(point[2]), float(point[3]), float(point[0])))

# # format and plot
# newdata = []
# for k in tempdata[22000:22200]:
#     newdata.append(k[3])
# plt.plot(range(len(newdata)), newdata - np.average(newdata))
# plt.ylim([-2, 2])


# # Definitely smoother, but more information is probably needed before throwing this in a learning algorithm
# # 

# # ## Welch
# # power spectrum the signal

# # In[21]:

# from scipy import signal

# envelope = np.abs(hilbert(newdata - np.average(newdata)))
# powerSpectrum = signal.welch(range(len(newdata)) )
# plt.plot(range(len(newdata)), newdata - np.average(newdata))
# plt.plot(range(len(envelope)), envelope )
# plt.ylim([-2, 2])


# # ## Correlating the front and back of a treadmill
# # For this, I will need to sync up the data between two of the shimmers that are on the same Treadmill based on their timestamps
# # 
# # I will use E8E3 and E887 (Treadmill 1, indexes 2 and 7) to look at how they line up
# # 
# # then E84F E833 (Treadmills 5 and 4) to see how the signal carries between treadmills.

# # In[11]:

# print data[2][22000][0]
# print data[7][22000][0]


# # E887 seems to have been started later, so i will use the first dataset to find a common point

# # In[12]:

# i = 0
# while(data[2][i][0] < data[7][0][0]):
#     i += 1
# print i 
# print data[2][i][0]
# print data[7][i][0]


# # ## Or not...
# # The time values seem to be off, so i will find a common event and compare their timestamps

# # In[13]:

# timedata = [[],[]]
# for row in data[2]:
#     timedata[0].append(row[0])
# for row in data[7]:
#     timedata[1].append(row[0])

# plt.plot(range(len(timedata[0])), timedata[0])
# plt.plot(range(len(timedata[1])), timedata[1])


# # Time should be increasing at the same rate, but time is clearly different between each device...

# # In[14]:

# print "Start Time:"
# print(datetime.datetime.fromtimestamp(
#         float(data[2][0][0])/1000).strftime('%Y-%m-%d %H:%M:%S'))
# print "End Time"
# print(datetime.datetime.fromtimestamp(
#         float(data[2][10000][0])/1000).strftime('%Y-%m-%d %H:%M:%S'))

# print "Start Time:"
# print(datetime.datetime.fromtimestamp(
#         float(data[7][0][0])/1000).strftime('%Y-%m-%d %H:%M:%S'))
# print "End Time"
# print(datetime.datetime.fromtimestamp(
#         float(data[7][10000][0])/1000).strftime('%Y-%m-%d %H:%M:%S'))
# print ""
# print "Update rate for E8E3", 10000/((float(data[2][10000][0]) - float(data[2][0][0]))/1000), "Hz"
# print "Update rate for E887", 10000/((float(data[7][10000][0]) - float(data[7][0][0]))/1000), "Hz"


# # It seems one device is recording at 140Hz, while the other is recording at 51 Hz, since they both end at the same time

# # In[15]:

# tempdata1 = [[],[],[]]
# for row in data[2]:
#         tempdata1[0].append(row[1])
#         tempdata1[1].append(row[2])
#         tempdata1[2].append(row[3])
        
# tempdata2 = [[],[],[]]

# for row in data[7]:
#         tempdata2[0].append(row[1])
#         tempdata2[1].append(row[2])
#         tempdata2[2].append(row[3])

# print len(timedata[0]), len(tempdata1)
# plt.plot(timedata[0], tempdata1[2])
# plt.plot(timedata[1], tempdata2[2])


# # In[16]:

# plt.plot(timedata[0][60000:60150], tempdata1[2][60000:60150])
# plt.plot(timedata[1][21965:22020], tempdata2[2][21965:22020], color='red')


# # ## Envelope
# # Envelope of our filtered signal

# # In[17]:

# from scipy.signal import hilbert

# analytic_signal = hilbert(signal)

