# iterate through the values from greatest to some minimum value:
# if there is resonable delta on both sides, call the point a maximum and zero out the points around it

import numpy as np

# this implementation of peak finding is inefficient.  Keep that in mind

def locatePeaks(data, delta, mindist, minamp = 0):
    # data: data to apply peakfinding to
    # delta: minimum
    # mindist: minimum number of indicies between peaks
    # minvalue: minimum peak amplitude
    peakInds = []
    correspondingInds = np.argsort(data)
    for i in (len(correspondingInds)-1 - np.arange(len(correspondingInds))):
        curInd = correspondingInds[i]
        # if the value of data at curInd is smaller than the threshold, break the loop
        if curInd != -1 and curInd != len(data)-1: # if the current index has been nullified (ie it is too close to a peak), ignore it
            if data[curInd] > data[curInd+1] + delta and data[curInd] > data[curInd-1] + delta:
                # max found
                peakInds.append(curInd)
                # nullify surrounding indicies
                for k in (np.arange(mindist*2)-mindist+curInd):
                    # if value k exists in correspondingInds, change it to -1
                    loc = np.where(correspondingInds==k)
                    if loc[0].size != 0:
                        correspondingInds[loc[0]] = -1
    return peakInds
