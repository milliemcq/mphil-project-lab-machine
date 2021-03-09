# This test demonstrates how to use the ALVideoRecorder module.

import os
import sys
import time
from naoqi import ALProxy
import math, ctypes
import numpy
import cv2
import stream
#import Image
# Replace this with your robot's IP address
# WGB
# IP = "192.168.202.21"

#LAN
# IP = "169.254.50.227"

#TP-LINK
IP = "pepper.local"
PORT = 9559

# Create a proxy to ALVideoDevice
print("STARTING PROGRAM")
videoDeviceProxy = ALProxy("ALVideoDevice", IP, PORT)
cam_list = videoDeviceProxy.getCameraIndexes()
# subscribe(const std::string& Name, const int& resolution, const int& colorSpace, const int& fps)
# Resolution:
# Parameter ID Name 	ID Value 	Description
# AL::kQQQQVGA 				8 		Image of 40*30px
# AL::kQQQVGA 				7 		Image of 80*60px
# AL::kQQVGA 				0 		Image of 160*120px
# AL::kQVGA 				1 		Image of 320*240px
# AL::kVGA 					2 		Image of 640*480px
# AL::k4VGA 				3 		Image of 1280*960px
# AL::k16VGA 				4 		Image of 2560*1920px


# Limitations
#
# Currently on ATOM CPU, requesting more than 5fps 1280x960 HD images remotely (getImageRemote) is bringing some frame drops. So we recommend not to go over 5fps HD images if you want to get them through the network. If all modules processing HD images are calling them locally (getImageLocal), there is no such limitation.
#
# Here are the observed framerates when requesting uncompressed YUV422 images on NAO v4 (*).
#   				local 	Gb Ethernet 	100Mb Ethernet 	WiFi g
# 40x30 (QQQQVGA) 	30fps 	30fps 			30fps 			30fps
# 80x60 (QQQVGA) 	30fps 	30fps 			30fps 			30fps
# 160x120 (QQVGA) 	30fps 	30fps 			30fps 			30fps
# 320x240 (QVGA) 	30fps 	30fps 			30fps 			11fps
# 640x480 (VGA) 	30fps 	30fps 			12fps 			2.5fps
# 1280x960 (4VGA) 	29fps 	10fps 			3fps 			0.5fps
subscriber = videoDeviceProxy.subscribe("python_Pepper_Camera_device", 2, 11, 30)
camID = 0 # Top camera ID is 0; Bottom camera ID is 1; Depth camera is 2

videoDeviceProxy.setActiveCamera(camID)

# print(videoDeviceProxy.getCameraName())
videoDeviceProxy.openCamera(camID)
videoDeviceProxy.startCamera(camID)
print("Camera Started: ", videoDeviceProxy.isCameraStarted(camID))

# filecount = 0 # initialize file count to save img files
# sess_id = "/VR_images/HC1_12Feb_img"
while videoDeviceProxy.isCameraStarted(camID):
	naoImage = videoDeviceProxy.getImageRemote(subscriber)
	# print(naoImage)
	imageWidth = naoImage[0]
	imageHeight = naoImage[1]
	array = naoImage[6]
	#image_string = str(bytearray(array))
	print("Image Width: ", imageWidth)
	print("Image Height: ", imageHeight)
	# Create a PIL Image from our pixel array.
	img = (numpy.reshape(numpy.frombuffer(naoImage[6], dtype='%iuint8' % naoImage[2]), (naoImage[1], naoImage[0], naoImage[2])))
	img = numpy.hstack([img, img[:, 50:]])
	#img = Image.fromstring("RGB", (imageWidth, imageHeight), image_string)

	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	# filename = sess_id + str(filecount) + '.png'
	# cv2.imwrite(filename, img)
	# filecount += 1
	img = cv2.resize(img, (2160, 1200), interpolation=cv2.INTER_CUBIC)
	cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
	cv2.moveWindow("window", 1920, 1080)
	cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
	cv2.imshow("window", img)
	if cv2.waitKey(int(5)) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		videoDeviceProxy.unsubscribe(subscriber)
		break
	# # print(img_data[0])
	# time.sleep(10)