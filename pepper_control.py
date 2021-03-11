from naoqi import ALProxy
import qi
import time
import numpy as np
import cv2
import random

class PepperControl:

    def __init__(self, IP, PORT):
        self.PORT = PORT
        self.IP = IP

        self.session = qi.Session()
        self.session.connect("tcp://" + str(self.IP) + ":" + str(self.PORT))

        # Setup Services for Project
        # self.face_detection_service = self.session.service("ALFaceDetection")
        # self.asr_service = self.session.service("ALSpeechRecognition")
        # self.setup_speech_recog()

        self.tts_service = self.session.service("ALTextToSpeech")
        self.move_service = self.session.service("ALNavigation")
        self.motion_service = self.session.service("ALMotion")
        self.camera_service = self.session.service("ALVideoDevice")
        self.anim_speech_service = self.session.service("ALAnimatedSpeech")


        self.speed = 3
        self.inverse_movements = []
        self.movement_codes = {'U' :[-0.2, 0.0], 'D' :[0.2, 0.0], 'R' :[0.0, 0.2], 'L' :[0, -0.2]}
        self.all_episode_phrases = self.get_all_episode_phrases()
        self.animations = self.get_animations()

    def get_all_episode_phrases(self):
        episode_1_phrases = ["Hello and welcome to Pepper's diner, I hope you enjoy your service today. {} I will be right back to take your order",
            "Thank you for choosing to eat at Pepper's diner today I hope you enjoy your service. {} Please choose something from the menu and I will return to take your order.",
            " Welcome today to Pepper's diner. I hope you enjoy your service today. {} I will be back in a minute to take your order."]

        episode_2_phrases = ["Thank you for your patience, {} what would you like to order today?",
                             "Have you decided on something to order? {} What would you like to eat today?",
                             "Can I get you something to order? {} What would you like from the menu?"]

        episode_3_phrases = ["{} Here is your food, I hope you enjoy!",
                             "{} I have brought you your food, I hope you like it!",
                             "Thank you for your patience, {} here is the food you ordered."]

        episode_4_phrases = ["Did you enjoy your meal? {} Thank you for eating here today!",
                             "I hope that you enjoyed your meal! {} Thank you for eating at Pepper's diner",
                             "{} Thank you for eating here today, I hope you enjoyed your meal."]

        return [episode_1_phrases, episode_2_phrases, episode_3_phrases, episode_4_phrases]

    def get_animations(self):
        potential_speaking_gestures = ["^start(animations/Stand/Emotions/Positive/Happy_4)",
                                       "^start(animations/Stand/Gestures/Choice_1)",
                                       "^start(animations/Stand/Gestures/Excited_1)",
                                       "^start(animations/Stand/Gestures/Explain_1)",
                                       "^start(animations/Stand/Gestures/Explain_10)",
                                       "^start(animations/Stand/Gestures/Explain_11)",
                                       "^start(animations/Stand/Gestures/Explain_2)",
                                       "^start(animations/Stand/Gestures/Explain_3)",
                                       "^start(animations/Stand/Gestures/Explain_4)",
                                       "^start(animations/Stand/Gestures/Explain_5)",
                                       "^start(animations/Stand/Gestures/Explain_6)",
                                       "^start(animations/Stand/Gestures/Explain_7)",
                                       "^start(animations/Stand/Gestures/Explain_8)",
                                       "^start(animations/Stand/Gestures/Give_3)",
                                       "^start(animations/Stand/Gestures/Give_4)",
                                       "^start(animations/Stand/Gestures/Give_5)",
                                       "^start(animations/Stand/Gestures/Give_6)",
                                       "^start(animations/Stand/Gestures/Me_1)",
                                       "^start(animations/Stand/Gestures/Me_2)",
                                       "^start(animations/Stand/Gestures/Me_4)",
                                       "^start(animations/Stand/Gestures/Me_7)",
                                       "^start(animations/Stand/Gestures/Yes_1)",
                                       "^start(animations/Stand/Gestures/Yes_2)",
                                       "^start(animations/Stand/Gestures/Yes_3)"]
        return potential_speaking_gestures

    def run_camera(self):
        print("Also running Camera")
        self.videoDeviceProxy = ALProxy("ALVideoDevice", self.IP, self.PORT)
        subscriber = self.videoDeviceProxy.subscribe("python_Pepper_Camera_device", 2, 11, 30)
        camID = 0  # Top camera ID is 0; Bottom camera ID is 1; Depth camera is 2
        print("Subscriber made")
        self.videoDeviceProxy.setActiveCamera(camID)

        # print(videoDeviceProxy.getCameraName())
        self.videoDeviceProxy.openCamera(camID)
        self.videoDeviceProxy.startCamera(camID)
        print("Camera Started: ", self.videoDeviceProxy.isCameraStarted(camID))

        # filecount = 0 # initialize file count to save img files
        # sess_id = "/VR_images/HC1_12Feb_img"
        while self.videoDeviceProxy.isCameraStarted(camID):
            print('Entering while loop')
            naoImage = self.videoDeviceProxy.getImageRemote(subscriber)
            # print(naoImage)
            imageWidth = naoImage[0]
            imageHeight = naoImage[1]
            array = naoImage[6]
            # image_string = str(bytearray(array))
            print("Image Width: ", imageWidth)
            print("Image Height: ", imageHeight)
            # Create a PIL Image from our pixel array.
            img = (np.reshape(np.frombuffer(naoImage[6], dtype='%iuint8' % naoImage[2]),
                                 (naoImage[1], naoImage[0], naoImage[2])))
            img = np.hstack([img, img[:, 50:]])
            # img = Image.fromstring("RGB", (imageWidth, imageHeight), image_string)

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # filename = sess_id + str(filecount) + '.png'
            # cv2.imwrite(filename, img)
            # filecount += 1
            img = cv2.resize(img, (2160, 1200), interpolation=cv2.INTER_CUBIC)
            cv2.namedWindow("window", cv2.WINDOW_NORMAL)
            cv2.moveWindow("window", 1920, 1080)
            # cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow("window", img)
            if cv2.waitKey(int(5)) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                self.camera_service.unsubscribe(subscriber)
                break

    def setup_speech_recog(self):
        self.asr_service.setLanguage("English")

        # Example: Adds "yes", "no" and "please" to the vocabulary (without wordspotting)
        vocabulary = ["yes", "no", "please"]
        self.asr_service.setVocabulary(vocabulary, False)

    def speech_recognition(self):
        self.asr_service.subscribe("Test_ASR")
        print 'Speech recognition engine started'
        time.sleep(20)
        self.asr_service.unsubscribe("Test_ASR")


    def move_pepper(self, curr_x, curr_y, action, speed_change=0):

        inverse_codes =  {'U': 'D', 'D' :'U', 'R' :'L', 'L' :'R'}

        # Speed is inverse
        self.speed = self.speed - speed_change

        movement = self.movement_codes[action]
        self.inverse_movements.append(inverse_codes[action])

        self.move_service.moveAlong(["Holonomic", ["Line", movement], 0.0, self.speed])
        return 'finished_movement'


    def animate_speech(self, text, animation):

        final_text = animation + text

        self.anim_speech_service.say(final_text)
        return True

    def return_to_start(self):

        for i in range(len(self.inverse_movements)):
            self.move_pepper()

        self.inverse_movements = []

    def reset_robot_position(self):

        for item in self.inverse_movements:
            movement = self.movement_codes[item]
            self.move_service.moveAlong(["Holonomic", ["Line", movement], 0.0, self.speed])

        self.inverse_movements = []

        return "Pepper position reset"


    def pepper_hand_movement(self):

        pass

    def face_detection(self):
        pass

    def pepper_speak(self, str):
        self.tts_service.say(str)
        return

    def animate(self):
        animation_player_service = ALProxy("ALAnimationPlayer", self.IP, self.PORT)
        animation_player_service.run("animations/Stand/Gestures/ShowTablet_3")

    def record_video(self):
        video_recorder_service = self.session.service('ALVideoRecorder')
        video_recorder_service.startRecording('home/nao/recordings/cameras', "test")
        print('Recording Started')
        time.sleep()

    def video_device(self):
        video_service = self.session.service('ALVideoDevice')
        SID = "test"
        pass


    def play_animation_for_episode(self, episode_num):
        if episode_num == -1:
            self.tts_service.say("Ready to goooooo!!!")
            return "Ready to goooooo!!!"

        speech = random.choice(self.all_episode_phrases[episode_num])
        animation = random.choice(self.animations)

        speech_str = speech.format(animation)

        self.anim_speech_service.say(speech_str)

        return speech_str

# if __name__ == '__main__':
#     IP = "pepper.local"
#     port = 9559
#
#     pepper = PepperControl(IP, port)
#     pepper.pepper_speak("Hello World")
#     pepper.run_camera()

hello_animations = []
generic_animations = []




explicit_service_questions = ["How are you finding your service so far?", "Are you enjoying the service?",
                              "Did you find my placement ok?", "Did you like the way I approached you?",
                              "Did you find my movement ok today?", "Do you think the service is ok today?"]
