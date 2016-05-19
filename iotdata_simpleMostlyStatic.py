from scipy import signal
import scipy
import numpy as np
import pdb

class IOTData_simple():
    ''' A class to help pull and format data from Shimmer devices
        The data is basically stored as a linked list, so
        operations that are not simply sequential, or that operate
        just on the end of the dataset will be slow.
    '''

    def __init__(self, windowsize = 256):
        self.windowSize = windowsize

    def featurePowerSpectrumMean(self, data):
        temp = []
        try:
            power = signal.welch(data, nperseg=self.windowSize) # nperseg=self.windowSize
            temp = (np.mean(power[1]))
        except:
             pass
        return temp

    def featurePowerSpectrumStdev(self, data):
        temp = []
        try:
             power = signal.welch(data, nperseg=self.windowSize) # nperseg=self.windowSize
             temp=(np.std(power[1]))
        except:
             pass
        return temp

    def featurePowerSpectrumMax(self, data):
        temp = []
        try:
            power = signal.welch(data, nperseg=self.windowSize) # nperseg=device.windowSize
            current = -99999
            maxindex = 0
            for k in range(len(power[0])):
                if power[1][k] > current:
                    current = power[1][k]
                    maxindex = power[0][k]
            temp = (maxindex)
        except:
            pass
        return temp

    def featureFrequencySpectrumMean(self, data):
        temp = []
        try:
            frequency = scipy.fftpack.fft(data).real # nperseg=device.windowSize
            temp = np.mean(frequency)
        except:
            pass
        return temp

    def featureFrequencySpectrumStdev(self, data):
        temp = []
        try:
            frequency = scipy.fftpack.fft(data).real # nperseg=device.windowSize
            temp = np.std(frequency)
        except:
            pass
        return temp

    def featureFrequencySpectrumMax(self, data):
        temp = []
        try:
            frequency = scipy.fftpack.fft(data).real # nperseg=device.windowSize
            current = -99999
            maxindex = 0
            for k in range(len(frequency)):
                if frequency[k] > current:
                    current = frequency[k]
                    maxindex = k
            temp = maxindex
        except:
            pass
        return temp

    def featurezcr(self, data):
        temp = []
        try:
            mean = np.mean(data)
            normalized = []
            for datum in data:
                normalized.append(datum - mean)
            count = 0
            for k in range(len(normalized)-1):
                if normalized[k] > 0 and normalized[k+1] <0:
                    count = count + 1

            temp = count
        except:
            pass

        return temp


    def featureWindowMean(self, data):
        temp = (np.mean(data))
        return temp

    def featureWindowStdev(self, data):
        temp = []
        try:
            temp = (np.std(data))
        except:
             pass

        return temp

    def generateWindowFeatures(self, dataMatrix):
        ''' calculate the feature vector for the current window of data
            This will be passed
        '''
        windowFeatures = [] # this will be a vector that stores all of the features
        features = [self.featurePowerSpectrumMean,
                    self.featurePowerSpectrumStdev,
                    self.featurePowerSpectrumMax,
                    self.featureFrequencySpectrumMean,
                    self.featureFrequencySpectrumStdev,
                    self.featureFrequencySpectrumMax,
                    self.featurezcr,
                    self.featureWindowMean,
                    self.featureWindowStdev]

        # for each column of dataMatrix perform the following (the outer loop should iterate 6 times)
        # pdb.set_trace()
        for i in range(dataMatrix.shape[1]):
            curCol = dataMatrix[:,i];
            for k in range(len(features)):
                data = features[k](curCol) # why is data blank
                # pdb.set_trace()
                windowFeatures.append(data)
        windowFeatures = np.reshape(windowFeatures,(1,-1))
        windowFeatures = np.reshape(windowFeatures,(1,-1))
        windowFeatures = windowFeatures[0]
        return windowFeatures


