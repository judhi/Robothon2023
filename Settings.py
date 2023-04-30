import arduino_communication
import cv2
import datetime
import math
from time import sleep
import numpy as np
from SendToEpson import sendToEpson # connect to EPSON Robot and send command via TCP/IP

#port = "COM3" # Judhi's PC
port = "COM9" # desktop PC
baudrate = 9600
# Create an instance of the ArduinoCommunication class
print("Opening connection with Arduino")
arduino = arduino_communication.ArduinoCommunication(port, baudrate)
sleep(1)

def gripper(n):
    arduino.communicate("g"+str(n))
    print("Gripper ",n)
    sleep(1)    
    return(n)

def calculateXY(xc, yc):
    # take values from calibration result
    tl_x, tl_y = 280, 330 # take from cal_image_corrected
    tr_x, tr_y = 1259, 329
    bl_x, bl_y = 279, 821
    br_x, br_y = 1262, 819
    
    x_ctr = int(1920/2)
    y_ctr = int(1080/2)
    
    dx = (xc - x_ctr)/100
    dy = (yc - y_ctr)/170
    
    xc = xc + dx
    yc = yc + dy
    
    print("dx,dy=",dx,dy)

    Y_len = 200
    X_len = 100

    gradX = (tr_x - tl_x) / Y_len
    gradY = (bl_y - tl_y) / X_len

    # print("gradX", gradX)
    # print("gradY", gradY)

    xc = xc - tl_x # top left X pixel
    yc = yc - tl_y # top left Y pixel
    calc_wx = -550 + round( yc / gradY, 2) # Y robot is x pixel
    calc_wy = 50.955 + round( xc / gradX, 2) # X robot is y pixel 
    return calc_wx, calc_wy

