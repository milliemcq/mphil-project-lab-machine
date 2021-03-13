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
from emotion_detection import EmotionDetection
import numpy as np

def get_rolling_avg(lst, roll=3):
    if len(lst) < roll:
        return np.mean(lst)
    else:
        return np.mean(lst[-roll:])



cap = cv2.VideoCapture(0)
#cap.open(0)

if cap.isOpened():  # try to get the first frame
    rval, f = cap.read()
else:
    rval = False

emotion_detector = EmotionDetection()
valence_values = []
arousal_values = []

while(True):
    # Capture frame-by-frame

        rval, frame = cap.read()

        valence, arousal = emotion_detector.get_arousal_valence_for_image(frame)
        valence_values.append(valence)
        arousal_values.append(arousal)

        rolling_valence = get_rolling_avg(valence_values)
        rolling_arousal = get_rolling_avg(arousal_values)

        print "rolling valence", rolling_valence
        print "rolling arousal", rolling_arousal

cap.release()
# cv2.destroyAllWindows()