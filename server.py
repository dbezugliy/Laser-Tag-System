import time
import socket
from _thread import *

fires = []
takes = []

hits = []

s = socket.socket()
host = '127.0.0.1' # host ip
port = 1000 # port no
ThreadCount = 0
try:
    s.bind((host, port))
except socket.error as e:
    print(str(e))
print('Socket is listening..')
s.listen(5)

def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)
        data = data.decode('utf-8')
        msg_type, uid, t = data.rstrip().split()
        sec = sum(x * int(t) for x, t in zip([3600, 60, 1], time.split(":")))
        print("Data received:{}".format(data))
        found = -1
        if msg_type == 'Shot':
            for i, item in enumerate(takes):
                if item[1] == sec:
                    hits.append([uid, item[0]])
                    print("{} hits {}".format(uid, item[0]))
                    found = i
                    break
            if found == -1:
                fires.append([uid, sec])
            else:
                del takes[found]
        else:
            for i, item in enumerate(fires):
                if item[1] == sec:
                    hits.append([item[0], uid])
                    print("{} hits {}".format(item[0], uid))
                    found = i
                    break
            if found == -1:
                takes.append([uid, sec])
            else:
                del fires[found]
        if not data:
            break
    connection.close()

while True:
    Client, address = s.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
s.close()