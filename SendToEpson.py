# Python library to send command to EPSON VT6 via TCP/IP
# by Judhi Prasetyo April 2023

import socket
from time import sleep
import numpy as np

ip_adddress = "192.168.150.2" # real robot
# ip_adddress = "127.0.0.1" # simulator robot

## Create a client socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
## Connect to the EPSON robot
clientSocket.connect((ip_adddress,2001))
#clientSocket.connect(("127.0.0.1",2001)) # this is simulator address, change this according to your robot address
#clientSocket.connect(("192.168.150.2",2001)) # this is the EPSON RC7+ simulator on localhost

# format of the coordinate is "x y z u" where u is the wrist rotation angle
# so we will keep the z axis the same and only take values for the x and y values
# example:
# places = ["100 400 600 0", "0 500 500 0", "-100 600 400 0"]


def sendToEpson(command):
    # Send data to robot
    msg_tx = command + "\r\n"
    print("Sending: " + command)
    clientSocket.send(msg_tx.encode())
    msg_rx = clientSocket.recv(1023) # waiting for confirmation from robot
    print("Result: ", msg_rx , "\r\n")
    return msg_rx
    sleep(0.5)

def Home():
    sendToEpson(0, 450, 850, 90) # change this to default home or camera position

clientSocket.close # close the connection
