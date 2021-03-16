# Useful website on SpeechRecognition
import socket, sys
# from pepper_control import PepperControl
from threading import Thread
from emotion_detection import EmotionDetection
import cv2
import numpy as np
import speech_recognition as sr
from keras import backend as K

class Run:

    def __init__(self, IP, PORT, BASELINE, explicit=True):
        self.IP = IP
        self.PORT = PORT
        self.BASELINE = BASELINE
        self.explicit = explicit

        self.valence_values = []
        self.arousal_values = []
        self.rolling_average_valence = 0
        self.rolling_average_arousal = 0

        self.emotion_detection = EmotionDetection()
        self.mic = sr.Microphone()
        self.r = sr.Recognizer()
        # self.curr_explicit_reward
        self.explicit_rewards = []

    def run_camera(self):
        # pepper.run_camera()
        return

    def get_affect_and_convert(self):
        arousal = str(0)
        valence = str(1)
        return arousal + '_' + valence



    def get_reward_implicit(self):
        # valence_arousal = pepper.get_rolling_valence_arousal()
        # TODO - CALCULATE REWARD HERE
        print "Rolling average valence", self.rolling_average_valence
        print "Rolling average arousal", self.rolling_average_arousal

        reward = str(int((self.rolling_average_valence - self.BASELINE[0]) + \
                 (self.rolling_average_arousal - self.BASELINE[1])))

        return reward

    def get_reward_explicit(self):
        with self.mic as source:
            print('Speak Now')
            audio = self.r.record(source, duration=5)

        self.explicit_rewards.append(0)

        try:
            speech = self.r.recognize_google(audio)
            print speech
        except Exception as e:
            print "Nothing detected"



    def get_data_meaning(self, data):

        print(data[:2])
        print(data)

        if data == 'RE':
            return self.reset_pepper_behaviour()
        elif data[:2] == 'EP':
            return self.pepper_behaviour_for_episode(int(data[-1]))
        elif data == 'REWARD':
            if self.explicit:
                return str(self.explicit_rewards[-1])
            else:
                return self.get_reward_implicit()
        else:
            split = data.split('_')
            print('Pepper Moving')
            print(split[1])
            # finished = pepper.move_pepper(0, 0, split[1])
            return 'moved'



    def pepper_behaviour_for_episode(self, episode):
        print("Looking for episode: ", episode)
        phrase = "animation for episode: " + str(episode)
        # phrase = pepper.play_animation_for_episode(episode)
        self.get_reward_explicit()

        return phrase

    def reset_pepper_behaviour(self):

        # result = pepper.reset_robot_position()
        result = "Reset"
        return result


    def connect_and_wait(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
        PORT = 65431
        s.bind((HOST, PORT))
        s.listen(5)
        while True:
            print "Listening..."
            c, addr = s.accept()
            print 'Connection from ', addr

            data = c.recv(1024)
            print "Recieved: ", data

            completed = self.get_data_meaning(data.decode('utf-8'))

            c.sendall(completed)
            c.close()

    def get_rolling_avg(self, lst, roll=3):
        if len(lst) < roll:
            return np.mean(lst)
        else:
            return np.mean(lst[-roll:])

    def run_local_camera(self):
        cap = cv2.VideoCapture(0)
        # cap.open(0)

        # if cap.isOpened():  # try to get the first frame
        #     rval, f = cap.read()
        # else:
        #     rval = False

        while True:
            # Capture frame-by-frame

            rval, frame = cap.read()
            # K.clear_session()
            valence, arousal = self.emotion_detection.get_arousal_valence_for_image(frame)
            # K.clear_session()
            self.valence_values.append(valence)
            self.arousal_values.append(arousal)

            rolling_valence = self.get_rolling_avg(self.valence_values)
            rolling_arousal = self.get_rolling_avg(self.arousal_values)

            # print "rolling valence", rolling_valence
            # print "rolling arousal", rolling_arousal

            self.rolling_average_valence = rolling_valence
            self.rolling_average_arousal = rolling_arousal





IP = "pepper.local"
PORT = 9559
BASELINE = [5.71207145601511, -3.350907772562803]
explicit = False

# global pepper
# pepper = PepperControl(IP, PORT)
run = Run(IP, PORT, BASELINE, explicit=explicit)


if __name__ == '__main__':
    Thread(target=run.run_local_camera).start()
    # Thread(target=run.connect_and_wait).start()
    run.connect_and_wait()
    # run.run_local_camera()



# run.get_reward_explicit()