
import socket, sys
# from pepper_control import PepperControl
from threading import Thread

class Run:

    def __init__(self, IP, PORT, BASELINE, explicit=True):
        self.IP = IP
        self.PORT = PORT
        self.BASELINE = BASELINE
        self.explicit = explicit

    def run_camera(self):
        # pepper.run_camera()
        return

    def get_affect_and_convert(self):
        arousal = str(0)
        valence = str(1)
        return arousal + '_' + valence




    def affect_reward(self):
        valence_arousal = pepper.get_rolling_valence_arousal()
        # TODO - CALCULATE REWARD HERE
        reward = 0
        return reward


    def get_data_meaning(self, data):

        print(data[:2])
        print(data)

        if data == 'AV':
            return self.get_affect_and_convert()
        elif data == 'RE':
            return self.reset_pepper_behaviour()
        elif data[:2] == 'EP':
            return self.pepper_behaviour_for_episode(int(data[-1]))
        elif data == 'REWARD':
            if self.explicit:
                pass
            else:
                return self.affect_reward()

            else: pass
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


IP = "pepper.local"
PORT = 9559
BASELINE = [5.71207145601511, -3.350907772562803]
explicit = True

# global pepper
# pepper = PepperControl(IP, PORT)
run = Run(IP, PORT, BASELINE)


if __name__ == '__main__':
    # Thread(target=run_camera).start()
    Thread(target=run.connect_and_wait).start()


