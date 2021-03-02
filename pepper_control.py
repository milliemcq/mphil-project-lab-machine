from naoqi import ALProxy
import qi
import time

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


        self.speed = 1
        self.inverse_movements = []


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
        codes = {'U' :[-1.0, 0.0], 'D' :[1.0, 0.0], 'R' :[0.0, 1.0], 'L' :[0, -1.0]}
        inverse_codes =  {'U': 'D', 'D' :'U', 'R' :'L', 'L' :'R'}

        # Speed is inverse
        self.speed = self.speed - speed_change

        movement = codes[action]
        self.inverse_movements.append(inverse_codes[action])

        self.move_service.moveAlong(["Holonomic", ["Line", movement], 0.0, self.speed])
        return True

    def return_to_start(self):

        for i in range(len(self.inverse_movements)):
            self.move_pepper()

        self.inverse_movements = []


    def pepper_hand_movement(self):

        pass

    def face_detection(self):
        pass

    def pepper_speak(self, str):
        self.tts_service.say("Hello, world!")
        return

    def animate(self):
        animation_player_service = self.session.service("ALAnimationPlayer")
        animation_player_service.run("animations/Stand/Gestures/ShowTablet_3")


if __name__ == '__main__':
    IP = "127.0.0.1"
    port = 35493

    pepper = PepperControl(IP, port)
    pepper.pepper_speak("Hello World")
    pepper.animate()