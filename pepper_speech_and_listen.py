# https://medium.com/@blogemtech/pepper-facial-recognition-43e24b10cea2
from naoqi import ALBroker, ALProxy
import cv2
import numpy as np


IP = "127.0.0.1"
port = 37847

# get NAOqi module proxy
videoDevice = ALProxy('ALVideoDevice', IP, port)

# subscribe top camera
AL_kTopCamera = 0
AL_kQVGA = 1            # 320x240
AL_kBGRColorSpace = 13
captureDevice = videoDevice.subscribeCamera(
    "test", AL_kTopCamera, AL_kQVGA, AL_kBGRColorSpace, 10)

# create image
width = 320
height = 240
image = np.zeros((height, width, 3), np.uint8)

while True:

    # get image
    result = videoDevice.getImageRemote(captureDevice);

    if result == None:
        print 'cannot capture.'
    elif result[6] == None:
        print 'no image data string.'
    else:

        # translate value to mat
        values = map(ord, list(result[6]))
        i = 0
        for y in range(0, height):
            for x in range(0, width):
                image.itemset((y, x, 0), values[i + 0])
                image.itemset((y, x, 1), values[i + 1])
                image.itemset((y, x, 2), values[i + 2])
                i += 3

        # show image
        cv2.imshow("pepper-top-camera-320x240", image)

    # exit by [ESC]
    if cv2.waitKey(33) == 27:
        break