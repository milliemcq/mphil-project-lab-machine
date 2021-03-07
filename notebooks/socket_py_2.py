import socket, sys




def send_data(signal, data):
    # Create a TCP/IP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.sendall(b'Hello, world')
    data = s.recv(1024)
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65432
    s.connect((HOST, PORT))
    message = signal + '-' + data
    s.sendall(message)

    print('Received', repr(data))

def make_up_affect():
    return [0, 1]


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


connect_and_wait()