
import socket, sys
# from pepper_control import PepperControl
from threading import Thread

def run_camera():
    pepper.run_camera()


def get_affect_and_convert():
    arousal = str(0)
    valence = str(1)
    return arousal + '_' + valence


def get_data_meaning(data):

    print(data[:2])
    print(data)

    if data == 'AV':
        return get_affect_and_convert()
    elif data == 'RE':
        return reset_pepper_behaviour()
    elif data[:2] == 'EP':
        return pepper_behaviour_for_episode(data[-1])
    else:
        split = data.split('_')
        print('Pepper Moving')
        print(split[1])
        # pepper.move_pepper(0, 0, split[1])
        return 'moved'


def pepper_behaviour_for_episode(episode):
    # phrase = pepper.play_animation_for_episode(episode)
    return 'WELCOME TO PEPA JOINT'

def reset_pepper_behaviour():
    # result = pepper.reset_robot_position()
    result = "Reset"
    return result


def connect_and_wait():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65432
    s.bind((HOST, PORT))
    s.listen(5)
    while True:
        print "Listening..."
        c, addr = s.accept()
        print 'Connection from ', addr

        data = c.recv(1024)
        print "Recieved: ", data

        completed = get_data_meaning(data.decode('utf-8'))

        c.sendall(completed)
        c.close()


IP = "pepper.local"
PORT = 9559

global pepper
# pepper = PepperControl(IP, PORT)

if __name__ == '__main__':
    # Thread(target=run_camera).start()
    Thread(target=connect_and_wait).start()


