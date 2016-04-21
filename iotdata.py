# # Internet of Things Project
# unix timestamp,  ax,ay,az,  gx,gy,gz,  temperature,  mx,my,mz,


import matplotlib.pyplot as plt
import numpy as np
import datetime
import csv
import matlab.engine
import matlab
from scipy import signal
import scipy
import pickle

class IOTData():
    ''' A class to help pull and format data from Shimmer devices
        The data is basically stored as a linked list, so
        operations that are not simply sequential, or that operate
        just on the end of the dataset will be slow.
    ''' 

    def __init__(self, devices, location = "Good_Shimmer_data/3_7_16/3_7_16_Data/"):
        self.location= location
        self.matlabinit = False
        #self.pre = "Treadmill"
        self.post = ".csv" 
        self.devices = devices
        self.dataset = devices[0]
        self.deviceInfo = []
        self.initdata(self.dataset)
        self.window = []
        self.windowSize = 256
        self.windowFeatures = []

    def getDeviceInfo(self):
        ''' TODO: Get the device info embedded in the first 3 lines of the CSV File '''
        pass

    def getDeviceID(self):
        ''' Returns the string representing the device's ID eg. E123'''
        return self.deviceInfo[1][1].split("_")[1]

    def getWindow(self, index):
        while self.windowIndex < index:
            self.getNextWindow()
        return self.window

    def getNextWindow(self):
        ''' returns an array with all variables, of length windowSize '''
        self.window = [[] for k in range(self.columnCount)]
        for k in range(self.windowSize):
            temp = self.reader.next()
            for k in range(len(temp)):
                try:
                    self.window[k].append(float(temp[k])) # add np.float32here
                except:
                    self.window[k].append(temp[k])
        self.windowIndex += 1
        self.dataIndex += self.windowSize
        return self.window

    def getSelection(self, start, end):
        ''' returns an array with all variables, starting and ending at  '''
        if self.dataIndex > start:
            self.initdata(self.dataset)
        while self.dataIndex < start:
            self.reader.next()
            self.dataIndex+=1
        self.window = [[] for k in range(self.columnCount)]
        while self.dataIndex < end:
            temp = self.reader.next()
            for k in range(len(temp)):
                try:
                    self.window[k].append(float(temp[k])) #np.float32 here
                except:
                    self.window[k].append(temp[k])
            self.dataIndex +=1

        for k in range(len(self.window)):
            self.window[k] = np.array(self.window[k])
            # self.window[k] = np.array(self.window[k], np.float32)   

        return self.window

    def initdata(self, which, windowSize = 256):
        ''' A function to reset the internal state of this class, and open the next file'''
        self.dataset = which
        self.windowSize = windowSize
        self.csvfile = open(self.location + which + self.post)
        self.reader = csv.reader(self.csvfile, delimiter = ',')
        #remove first 3 pieces of data as identifiers
        self.info = [[] for k in range(20)]
        temp = self.reader.next()
        for i in range(2):
            temp = self.reader.next()
            self.columnCount = len(temp)
            # print self.columnCount, temp

            #print temp, len(temp)
            self.deviceInfo.append(temp)
            for k in range(len(temp)):
                self.info[k].append(temp[k])
        self.windowIndex = 0
        self.dataIndex = 0
        # print self.info

    def getUpdateRate(self):
        ''' Get the sensor update rate in Hz '''
        return len(self.window[0])/((float(self.window[0][-1]) - float(self.window[0][0]))/1000)

    def featurePowerSpectrumMean(self):
        temp = []
        for dimension in self.window:
            try:
                power = signal.welch(dimension, nperseg=self.windowSize) # nperseg=self.windowSize
                temp.append(np.mean(power[1]))
            except:
                pass
        return temp

    def featurePowerSpectrumStdev(self):
        temp = []
        for dimension in self.window:
            try:
                power = signal.welch(dimension, nperseg=self.windowSize) # nperseg=self.windowSize
                temp.append(np.std(power[1]))
            except:
                pass
        return temp

    def featurePowerSpectrumMax(self):
        temp = []
        for dimension in self.window:
            try:
                power = signal.welch(dimension, nperseg=self.windowSize) # nperseg=device.windowSize
                current = -99999
                maxindex = 0
                for k in range(len(power[0])):
                    if power[1][k] > current:
                        current = power[1][k]
                        maxindex = power[0][k]
                temp.append(maxindex)
            except:
                pass
        return temp

    def featureFrequencySpectrumMean(self):
        temp = []
        for dimension in self.window:
            try:
                frequency = scipy.fftpack.fft(dimension).real # nperseg=device.windowSize
                temp.append(np.mean(frequency))
            except:
                pass
        return temp

    def featureFrequencySpectrumStdev(self):
        temp = []
        for dimension in self.window:
            try:
                frequency = scipy.fftpack.fft(dimension).real # nperseg=device.windowSize
                temp.append(np.std(frequency))
            except:
                pass
        return temp

    def featureFrequencySpectrumMax(self):
        temp = []
        for dimension in self.window:
            try:
                frequency = scipy.fftpack.fft(dimension).real # nperseg=device.windowSize
                current = -99999
                maxindex = 0
                for k in range(len(frequency)):
                    if frequency[k] > current:
                        current = frequency[k]
                        maxindex = k
                temp.append(maxindex)
            except:
                pass
        return temp

    def featurezcr(self):
        temp = []
        for dimension in self.window:
            try:
                mean = np.mean(dimension)
                normalized = []
                for datum in dimension:
                    normalized.append(datum - mean) 
                count = 0
                for k in range(len(normalized)-1):
                    if normalized[k] > 0 and normalized[k+1] <0:
                        count = count + 1

                temp.append(count)
            except:
                pass

        return temp


    def featureWindowMean(self):
        temp = []
        for dimension in self.window:
            try:
                temp.append(np.mean(dimension))
            except:
                pass

        return temp

    def featureWindowStdev(self):
        temp = []
        for dimension in self.window:
            try:
                temp.append(np.std(dimension))
            except:
                pass

        return temp


    def getLength(self):
        ''' Returns the number of data lines in the CSV '''
        sum = 0
        while True:
            try:
                self.reader.next()
                self.dataIndex+=1
                sum +=1
            except:
                break
        return sum
                
    def annotateARFF(self, labels):
        ''' Write the current window to an ARFF File given labels, which
            is an array of dictionaries containing an in
            eg. {'Begin': 1458998110.329, 'End':1458998155.595, 'Label':'walking'}
            (this currently assumes only one class per datapoint )
        '''
        file = open(self.dataset + 'annotated.arff', 'w')
        file.write('@RELATION ' + self.dataset + '\n\n')
        for k in range(self.columnCount -1):
            file.write('@ATTRIBUTE' + self.info[k][0] + '\n')

        file.write('@ATTRIBUTE class {not_walking,walking,running}\n')
        file.write('\n')
        file.write('@DATA\n')

        for k in range(len(self.window[0])):
            currentclass = 'not_walking'
            for interval in labels: 
                if np.float32(self.window[0][k])/1000 > interval['Begin'] and np.float32(self.window[0][k])/1000 < interval['End']:
                    currentclass = interval['Label']
                    break
            file.write("%.2f"%self.window[0][k] +',')
            for i in range(self.columnCount-2):
                file.write(str(self.window[i+1][k])+',')
            file.write(currentclass + '\n')

        file.close()

    def generateAllFeaturesToARFF(self, labels, startindex, endindex):
        # 0 7 14 15
        self.getSelection(startindex, startindex)
        file = open(self.dataset + 'featuresannotated.arff', 'w')
        file.write('@RELATION ' + self.dataset + '\n\n')
        
        # names of each attribute
        features = [self.featurePowerSpectrumMean,
                    self.featurePowerSpectrumStdev,
                    self.featurePowerSpectrumMax,
                    self.featureFrequencySpectrumMean,
                    self.featureFrequencySpectrumStdev,
                    self.featureFrequencySpectrumMax,
                    self.featurezcr,
                    self.featureWindowMean,
                    self.featureWindowStdev]

        featureStrings = ['featurePowerSpectrumMean',
                        'featurePowerSpectrumStdev',
                        'featurePowerSpectrumMax',
                        'featureFrequencySpectrumMean',
                        'featureFrequencySpectrumStdev',
                        'featureFrequencySpectrumMax',
                        'featurezcr',
                        'featureWindowMean',
                        'featureWindowStdev']

        for feature in featureStrings:
            for k in range(16):
                file.write('@ATTRIBUTE ' + feature + str(k) + ' NUMERIC' + '\n')

        file.write('@ATTRIBUTE class {not_walking,walking,running}\n')
        file.write('\n')
        file.write('@DATA\n')

        for k in range((endindex - startindex)/self.windowSize):
            self.getNextWindow()

            for k in range(len(features)):
                data = features[k]()
                for datum in data:
                    file.write(str(datum) + ',')

            #write label
            currentclass = 'not_walking'
            for interval in labels: 
                if np.float32(self.window[0][self.windowSize/2])/1000 > interval['Begin'] and np.float32(self.window[0][self.windowSize/2])/1000 < interval['End']:
                    currentclass = interval['Label']
                    break
            file.write(currentclass)
            file.write('\n')
        file.close()


    def generateWindowFeatures(self):
        ''' calculate the feature vector for the current window of data
            This will be passed 
        '''
        self.windowFeatures = []
        features = [self.featurePowerSpectrumMean,
                    self.featurePowerSpectrumStdev,
                    self.featurePowerSpectrumMax,
                    self.featureFrequencySpectrumMean,
                    self.featureFrequencySpectrumStdev,
                    self.featureFrequencySpectrumMax,
                    self.featurezcr,
                    self.featureWindowMean,
                    self.featureWindowStdev]

        for k in range(len(features)):
            data = features[k]()
            for datum in data:
                self.windowFeatures.append(datum)

    def generateAllFeatures(self, labels, startindex, endindex):
        self.getSelection(startindex, startindex)
        file = open(self.dataset + 'featuresannotated.arff', 'w')
        file.write('@RELATION ' + self.dataset + '\n\n')
        
        # names of each attribute
        features = [self.featurePowerSpectrumMean,
                    self.featurePowerSpectrumStdev,
                    self.featurePowerSpectrumMax,
                    self.featureFrequencySpectrumMean,
                    self.featureFrequencySpectrumStdev,
                    self.featureFrequencySpectrumMax,
                    self.featurezcr,
                    self.featureWindowMean,
                    self.featureWindowStdev]

        featureStrings = ['featurePowerSpectrumMean',
                        'featurePowerSpectrumStdev',
                        'featurePowerSpectrumMax',
                        'featureFrequencySpectrumMean',
                        'featureFrequencySpectrumStdev',
                        'featureFrequencySpectrumMax',
                        'featurezcr',
                        'featureWindowMean',
                        'featureWindowStdev']

        for feature in featureStrings:
            for k in range(16):
                file.write('@ATTRIBUTE ' + feature + str(k) + ' NUMERIC' + '\n')

        file.write('@ATTRIBUTE class {not_walking,walking,running}\n')
        file.write('\n')
        file.write('@DATA\n')

        for k in range((endindex - startindex)/self.windowSize):
            self.getNextWindow()

            for k in range(len(features)):
                data = features[k]()
                for datum in data:
                    file.write(str(datum) + ',')

            #write label
            currentclass = 'not_walking'
            for interval in labels: 
                if np.float32(self.window[0][self.windowSize/2])/1000 > interval['Begin'] and np.float32(self.window[0][self.windowSize/2])/1000 < interval['End']:
                    currentclass = interval['Label']
                    break
            file.write(currentclass)
            file.write('\n')
        file.close()



    ###############################
    #
    # Classification Functions
    #
    ###############################

    def loadClassifier(self, filename):
        ''' loads a classifier saved pickle '''

    def saveClassifier(self, filename):
        ''' saves the generated classifier as a pickle object '''

    def classifyWindow(self):
        ''' Pass the data through the give Decision Tree '''



    ###############################
    #
    # Start Matlab Functionality
    #
    ###############################

    def startMatlab(self):
        self.eng = matlab.engine.start_matlab()
        self.matlabinit = True


    def getMatlabFeature(self):
        if not self.matlabinit:
            return False
        pass
        # self.eng.workspace

    def getSteps(self, data):
        if not self.matlabinit:
            print "Not initialized"
            return
        # self.eng.load('d:/iot/DataExaminer.m')
        print self.eng.path('d:/iot/')
        # self.eng.addpath('d:/iot/');
        self.eng.workspace['data'] = data[1].tolist()
        # self.eng.importdata('countSteps.m')

        data2 = self.eng.eval('countSteps(data)')
        print(data2)
        return data2
