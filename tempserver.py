#!/usr/bin/python

import socket, threading

class client_thread(threading.Thread):

    def __init__(self, ip, port, socket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        print("[+] new thread started for " + ip + ":" + str(port))

    def run(self):

        print("connection from: " + ip + ":" + str(port))
        message = "\nwelcome to the server\n\n"
        self.socket.send(message.encode())
        data = "dummydata" # @debug: can also configure do-while

        while len(data) > 0:
            data = self.socket.recv(2048)
            print("client sent: " + str(data))
            print("length of data client sent" + str(len(data)))
            message = "you sent me: ".encode()
            self.socket.send(message + data)

        print("client disconnected...")

host = "0.0.0.0"
port = 7000

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# note: specify the option name as well as level below;
# below option is effectively workaround for "ADDR ALREADY IN USE"
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcpsock.bind((host,port))
threads = []

tcpsock.listen(4) # arg: max # of queued connections allowed

while True: # server keeps running
    print("\nlistening for incoming connections...")
    (clientsock, (ip, port)) = tcpsock.accept()
    newthread = client_thread(ip, port, clientsock)
    newthread.start() # start thread to handle client
    threads.append(newthread)

for t in threads:
    t.join()
