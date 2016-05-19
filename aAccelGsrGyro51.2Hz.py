#!/usr/bin/python
import sys, struct, serial
import numpy as np
from calibration import calibrateInertialSensorData

AMa = np.array([[0,-1.0,0],[-1.0,0,0],[0,0,-1.0]])
SMa = np.array([[83.0,0,0],[0,83.0,0],[0,0,83.0]])
OVa = np.array([[2047.0],[2047.0],[2047.0]])

AMg = np.array([[0,-1.0,0],[-1.0,0,0],[0,0,-1.0]])
SMg = np.array([[65.5,0,0],[0,65.5,0],[0,0,65.5]])
OVg = np.array([[0.0],[0.0],[0.0]])

AMm = np.array([[-1.0,0,0],[0,1.0,0],[0,0,-1.0]])
SMm = np.array([[1100.0,0,0],[0,1100.0,0],[0,0,980.0]])
OVm = np.array([[0.0],[0.0],[0.0]])

def wait_for_ack():
   ddata = ""
   ack = struct.pack('B', 0xff)
   while ddata != ack:
      ddata = ser.read(1)
   return

# parameters come in as a list called sys.argv
if len(sys.argv) < 2:
   print "No device specified."
   print "Specify the serial port of the device you wish to connect to."
   print "Example:"
   print "   aAccelGsrGyro51.2Hz.py Com12"
   print "or"
   print "   aAccelGsrGyro51.2Hz.py /dev/rfcomm0"
else:
   ser = serial.Serial(sys.argv[1], 115200)
   ser.flushInput()
# send the set sensors command
   ser.write(struct.pack('BBBB', 0x08, 0xA0, 0x00, 0x00))  #analog accel, gsr, MPU9150 gyro
   wait_for_ack()
# send the set sampling rate command
   ser.write(struct.pack('BBB', 0x05, 0x80, 0x02)) #51.2Hz (32768/640=51.2Hz: 640 -> 0x0280; has to be done like this for alignment reasons.)
   wait_for_ack()
# send start streaming command
   ser.write(struct.pack('B', 0x07))
   wait_for_ack()

# read incoming data
   ddata = ""
   numbytes = 0
   framesize = 15 # 1byte packet type + 2byte timestamp + 3x2byte Analog Accel + 3x2byte LSM Mag

   print "Packet Type,Timestamp,Analog AccelX,Analog AccelY,Analog AccelZ,MagX,MagY,MagZ"
   try:
      while True:
         while numbytes < framesize:
            ddata += ser.read(framesize)
            numbytes = len(ddata)

         data = ddata[0:framesize]
         ddata = ddata[framesize:]
         numbytes = len(ddata)

         (packettype,) = struct.unpack('B', data[0:1])
         timestamp = struct.unpack('H', data[1:3])
         (analogacceyx, analogacceyy, analogacceyz) = struct.unpack('HHH', data[3:9])
         # (timestamp, analogacceyx, analogacceyy, analogacceyz) = struct.unpack('HHHH', data[1:9])
         # (timestamp, analogacceyx, analogacceyy, analogacceyz, magx, magz, magy) = struct.unpack('HHHHHHH', data[1:framesize])
         (magx, magz, magy) = struct.unpack('>hhh', data[9:15]) # why on earth are these unpacked out of order?

# gsrrange = (gsr & 0xC000) >> 14
         # gsr &= 0xFFF
         # print "0x%02x,%5d,\t%4d, %4d, %4d,\t%d, %4d,\t%4d, %4d, %4d" % (packettype, timestamp, analogacceyx, analogacceyy, analogacceyz, gsrrange, gsr, gyrox, gyroy, gyroz)

         # print calibrateInertialSensorData([analogacceyx,analogacceyy,analogacceyz],AMa,SMa,OVa), calibrateInertialSensorData([gyrox,gyroy,gyroz],AMg,SMg,OVg),calibrateInertialSensorData([magx,magy,magz],AMm,SMm,OVm)

         print [magx,magy,magz],calibrateInertialSensorData([magx,magy,magz],AMm,SMm,OVm)

   except KeyboardInterrupt:
#send stop streaming command
      ser.write(struct.pack('B', 0x20))
      wait_for_ack()
#close serial port
      ser.close()
      print
      print "All done!"
