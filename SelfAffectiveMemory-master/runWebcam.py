"""
Emotion Recognition - Vision-Frame-Based Face Channel

__author__ = "Pablo Barros"

__version__ = "0.1"
__maintainer__ = "Pablo Barros"
__email__ = "barros@informatik.uni-hamburg.de"

More information about the implementation of the model:

Barros, P., Churamani, N., & Sciutti, A. (2020). The FaceChannel: A Light-weight Deep Neural Network for Facial Expression Recognition. arXiv preprint arXiv:2004.08195.

Barros, P., & Wermter, S. (2016). Developing crossmodal expression recognition based on a deep neural model. Adaptive behavior, 24(5), 373-396.
http://journals.sagepub.com/doi/full/10.1177/1059712316664017

"""

import cv2
from Utils import imageProcessingUtil, modelDictionary, modelLoader, GUIController
import numpy

import AffectiveMemory

import tensorflow as tf
config = tf.ConfigProto()
config.gpu_options.allow_growth=True
sess = tf.Session(config=config)

finalImageSize = (1024,768) # Size of the final image generated by the demo
categoricalInitialPosition = 460 # Initial position for adding the categorical graph in the final image
faceSize = (64,64) # Input size for both models: categorical and dimensional
faceDetectionMaximumFrequency = 20 # Frequency that a face will be detected: every X frames.

affectiveMemory = AffectiveMemory.AffectiveMemory() # Affective Memory

modelDimensional = modelLoader.modelLoader(modelDictionary.DimensionalModel)

imageProcessing = imageProcessingUtil.imageProcessingUtil()

GUIController = GUIController.GUIController()

cap = cv2.VideoCapture(0)
#cap.open(0)

if cap.isOpened():  # try to get the first frame
    rval, f = cap.read()
else:
    rval = False


while(True):
    # Capture frame-by-frame

        rval, frame = cap.read()

        # detect faces
        facePoints, face = imageProcessing.detectFace(frame)

        # create display image and copy the captured frame to it
        image = numpy.zeros((finalImageSize[1], finalImageSize[0], 3), numpy.uint8)

        y = int((frame.shape[0]-480)/2)
        x = int((frame.shape[1]-720)/2)
        image[0:480, 0:640] = frame[y:y+480, x:x+640]
        frame = image

         # If a face is detected
        if not len(face) == 0:
            # pre-process the face
            face = imageProcessing.preProcess(face, faceSize)

            # Obtain dimensional classification
            dimensionalRecognition = numpy.array(modelDimensional.classify(face))

            # ----------- Affective Memory ----------------------

            # Obtain the affective memory input / output of the dense layer of the network
            #affectiveMemoryInput = numpy.squeeze(numpy.array(modelDimensional.getDense(face)),1)

            # Otherwise use arousal/valence as input to the affective memory
            affectiveMemoryInput = numpy.array(dimensionalRecognition[:,0,0]).flatten()

            # If affective memory is not built, build it.
            if not affectiveMemory.isBuilt:
                # print ("BUild")
                affectiveMemory.buildModel(affectiveMemoryInput)
            # if affective memory is already built, train it with the new facial expression
            else:
                # print("train")
                affectiveMemory.train(affectiveMemoryInput)

            affectiveMemoryNodes, affectiveMemoryNodesAges = affectiveMemory.getNodes()


            # print the affective memory plot

            frame = GUIController.createAffectiveMemoryGUI(affectiveMemoryNodes, affectiveMemoryNodesAges, frame)

            # # ----------- Affective Memory ----------------------


            # Print the square around the categorical face
            frame = GUIController.createDetectedFacGUI(frame,facePoints)

            # Create the dimensional graph
            frame = GUIController.createDimensionalEmotionGUI(dimensionalRecognition, frame)



        # Display the resulting frame
        cv2.imshow('frame',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()