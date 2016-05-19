#!/usr/bin/python
import sys, struct, serial
import numpy as np
from calibration import calibrateInertialSensorData

class ShimmerBluetooth():

   def __init__(self, comport, windowsize):
      ''' initialize a connection to a shimmer, and '''
      self.comport = comport
      self.windowsize = windowsize

      self.AMa = np.array([[0,-1.0,0],[-1.0,0,0],[0,0,-1.0]])
      self.SMa = np.array([[83.0,0,0],[0,83.0,0],[0,0,83.0]])
      self.OVa = np.array([[2047.0],[2047.0],[2047.0]])
      self.AMg = np.array([[0,-1.0,0],[-1.0,0,0],[0,0,-1.0]])
      self.SMg = np.array([[65.5,0,0],[0,65.5,0],[0,0,65.5]])
      self.OVg = np.array([[0.0],[0.0],[0.0]])
      self.AMm = np.array([[-1.0,0,0],[0,1.0,0],[0,0,-1.0]])
      self.SMm = np.array([[1100.0,0,0],[0,1100.0,0],[0,0,980.0]])
      self.OVm = np.array([[0.0],[0.0],[0.0]])

      # this is the number of values expected to be recived (accelx,accely,accelz,magx,magy,magz)
      self.numSensorVals = 6

      # Bluetooth Setup Operations
      self.ser = serial.Serial(self.comport, 115200)
      self.ser.flushInput()
      # send the set sensors command
      self.ser.write(struct.pack('BBBB', 0x08, 0xA0, 0x00, 0x00))  #analog accel, LSM303DLHC Magnetometer
      self.wait_for_ack()
      # send the set sampling rate command
      self.ser.write(struct.pack('BBB', 0x05, 0xA2, 0x00)) #51.2Hz (32768/640=51.2Hz: 640 -> 0x0280; has to be done like this for alignment reasons.)
      self.wait_for_ack()
      # send start streaming command
      self.ser.write(struct.pack('B', 0x07))
      self.wait_for_ack()




   def wait_for_ack(self):
      ddata = ""
      ack = struct.pack('B', 0xff)
      while ddata != ack:
         ddata = self.ser.read(1)
      return

   def getFrame(self):
      ''' get window number of lines from the shimmer'''

      # read incoming data
      # datavec = [[] for k in range(9)]
      datavec = np.zeros((self.windowsize,self.numSensorVals))
      ddata = ""
      framesize = 15 # 1byte packet type + 2byte timestamp + 3x2byte Analog Accel + 3x2byte LSM303DLHC Magnetometer

      try:
         for k in range(self.windowsize):
            numbytes = 0
            while numbytes < framesize:
               ddata += self.ser.read(framesize)
               numbytes = len(ddata)
            data = ddata[0:framesize]
            ddata = ddata[framesize:]
            numbytes = len(ddata) # this is probably redundant

            (packettype,) = struct.unpack('B', data[0:1])
            (timestamp, analogacceyx, analogacceyy, analogacceyz) = struct.unpack('HHHH', data[1:9])
            # (gyrox, gyroy, gyroz) = struct.unpack('>hhh', data[9:15])
            (magx, magy, magz) = struct.unpack('>hhh', data[9:15])

            [ax,ay,az] = calibrateInertialSensorData([analogacceyx,analogacceyy,analogacceyz],self.AMa,self.SMa,self.OVa)
            # [gx,gy,gz] = calibrateInertialSensorData([gyrox,gyroy,gyroz],self.AMg,self.SMg,self.OVg)
            [mx,my,mz] = calibrateInertialSensorData([magx,magy,magz],self.AMm,self.SMm,self.OVm)
            # reading = [ax,ay,az,gx,gy,gz,mx,my,mz]
            reading = [ax,ay,az,mx,my,mz]
            datavec[k,:] = reading
            # for d in range(len(reading)):
            #    datavec[d].append(reading[d])


      except KeyboardInterrupt:
         self.closeDevice()

      return datavec

   def closeDevice(self):
      #send stop streaming command
      self.ser.write(struct.pack('B', 0x20))
      self.wait_for_ack()
      #close serial port
      self.ser.close()
      print self.comport, "closed"
