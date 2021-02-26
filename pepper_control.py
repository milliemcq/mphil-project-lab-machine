from naoqi import ALProxy

class PepperControl:
    IP = "127.0.0.1"
    port = 40947
    def __init__(self, IP, PORT):
        self.PORT = PORT
        self.IP = IP
        self.tts_proxy = ALProxy("ALTextToSpeech", self.IP, self.port)
        self.move_proxy = ALProxy("ALNavigation", self.IP, self.port)
        self.motion_proxy = ALProxy('ALMotion', self.IP, self.port)
        self.speed = 1
        self.reverse_movements = []

    def move_pepper(self, curr_x, curr_y, action, speed_change=0):
        codes = {'U' :[-1.0, 0.0], 'D' :[1.0, 0.0], 'R' :[0.0, 1.0], 'L' :[0, -1.0]}
        inverse_codes =  {'U': 'D', 'D' :'U', 'R' :'L', 'L' :'R'}

        # Speed is inverse
        self.speed = self.speed - speed_change

        movement = codes[action]
        self.inverse_movements.append(inverse_codes[action])

        self.move_proxy.moveAlong(["Holonomic", ["Line", movement], 0.0, self.speed])
        return True

    def return_to_start(self):

        for i in range(len(self.inverse_movements)):
            self.move_pepper()

        self.inverse_movements = []
