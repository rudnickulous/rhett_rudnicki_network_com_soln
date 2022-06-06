import socket
import zmq
import pickle
import numpy as np

headerSize = 10

#  set up client side ZeroMQ socket
context = zmq.Context()
ZMQsocket  = context.socket(zmq.REQ)
ZMQsocket.connect("tcp://localhost:5555")

#set up client side Websocket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 1310))

while True:
    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            print(f"new message length: {msg[:headerSize]}")
            msglen = int(msg[:headerSize])
            new_msg = False
        full_msg += msg
        if len(full_msg) - headerSize == msglen:
            print("full message received ")
            mesh_object = pickle.loads(full_msg[headerSize:])
            print(mesh_object)
            new_msg = True
            full_msg = b''
            break
    points  = np.unique(mesh_object.vectors.reshape([int(mesh_object.vectors.size/3), 3]), axis=0)
    points  = np.around(points,decimals=4)
    message = pickle.dumps(points)
    ZMQsocket.send(message)