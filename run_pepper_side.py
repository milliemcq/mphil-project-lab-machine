
import socket, sys
from pepper_control import PepperControl




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

        affect = str(make_up_affect())

        c.sendall(affect)
        c.close()






if __name__ == "main":
    IP = "127.0.0.1"
    PORT = 34723

    pepper = PepperControl(IP, PORT)




    connect_and_wait()