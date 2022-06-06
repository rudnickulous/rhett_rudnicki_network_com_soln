import socket
import zmq
import pickle
import numpy as np
from stl import mesh
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import pathlib

#file save location
saveLoc    = str(pathlib.Path(__file__).parent.resolve())

#set up server side ZeroMQ socket
context = zmq.Context()
ZMQsocket = context.socket(zmq.REP)
ZMQsocket.bind("tcp://*:5555")

#set up server side Websocket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 1310))
s.listen(5)

#file selector (works on Mac or Windows)
# create the root window
root = tk.Tk()
root.title('Once File Has Been Opened, Close This Window')
root.resizable(False, False)
root.geometry('500x150')
def select_file():
    filetypes = (('STL Files', '*.stl'),
        ('All Files', '*.*')
    )
    global filename
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    showinfo(
        title='Selected File',
        message=filename
    )
# open button
open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_file
)
open_button.pack(expand=True)
# run the application
root.mainloop()
mesh_object = mesh.Mesh.from_file(filename)

#buffer size for socket
headerSize = 10
while True:
    clientsocket,address = s.accept()
    print(f"Connection from {address}")
    #file stuff here
    msg = pickle.dumps(mesh_object)
    msg = bytes(f'{len(msg):<{headerSize}}',"utf-8") + msg
    clientsocket.send(msg)
    message = ZMQsocket.recv()
    points = pickle.loads(message)
    np.savetxt(saveLoc+'/output.csv', points, fmt='%.4e', delimiter=",")
    print("output.csv is saved")