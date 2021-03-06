import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = ''
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

currentId = "0"
pos = ["0:20,200", "1:870,200"]


def threaded_client(conn):
    global currentId, pos, nid
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    while True:
        try:
            # recieves data
            data = conn.recv(2048)
            reply = data.decode('utf-8')

            # if there is no data coming in then print goodbye.
            if not data:
                conn.send(str.encode("Goodbye"))
                break

            # else acknowledge data is received.
            else:
                print("Recieved: " + reply)
                arr = reply.split(":")
                id = int(arr[0])
                pos[id] = reply

                if id == 0: nid = 1
                if id == 1: nid = 0

                # sends data from data.
                reply = pos[nid][:]
                print("Sending: " + reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Connection Closed")
    conn.close()


# Accepts new connections
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))