import cv2
from time import sleep
import numpy as np
from Settings import gripper
from SendToEpson import sendToEpson # connect to EPSON Robot and send command via TCP/IP
from map_coord import get_coord
from slider_task import *


def ConnectCamera():
    print("Connecting to camera...")
    #cam_device = 3 # on Judhi's laptop
    cam_device = 0 # on lab's desktop
    #vid = cv2.VideoCapture(cam_device,cv2.CAP_DSHOW) # activate Windows Direct Show for faster camera setup
    vid = cv2.VideoCapture(0) # for other systems
    print("Camera connected")
    print("Setting video resolution")
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # max 3840 for 4K, 1920 for FHD
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # max 2160 for 4K, 1080 for FHD
    sleep(1)
    if(vid.isOpened()):
            print("=======Ready to capture=======")  
            ret, img = vid.read() # take a sample frame
            return vid

# --- click M5 button
def m5():
    gripper(80)
    sendToEpson("go_click_m5")

# --- press blue button
def bb():
    gripper(80)
    sendToEpson("go_press_blue_button")
    sleep(1)
    
# --- move sliders
def slide(cam):
    sendToEpson("go_check_display")
    # take picture here to get slider value
    if (cam.isOpened()):
        print("Capturing slider's target1")
        ret, img1 = cam.read()
    else:
        print("Camera error")
        exit(1)
    target1 = get_target(img1, None)
    target1 = round(target1,0)
    print("First arrow distance = {:.2f} mm".format(target1))
    # then grab the slider and move it accordingly
    sleep(1)
    gripper(50)
    sendToEpson("go_approach_slider 0") # start location 0
    sleep(1)
    gripper(70)
    sleep(1)
    # #sendToEpson("go_slide 16")
    sendToEpson("go_slide " + str(target1))
    sleep(1)
    # # gripper will go back to Slider_start position
    gripper(50)
    sleep(1)
    sendToEpson("go_tool_up")
    sendToEpson("go_check_display")
    # take picture here to get slider value
    if (cam.isOpened()):
        print("Capturing slider's target2")
        ret, img2 = cam.read()
    else:
        print("Camera error")
        exit(1)
    target2 = get_target(img2, img1)
    target2 = round(target2,2)
    print("Second arrow distance = {:.2f} mm".format(target1))    
    # then grab the slider and move it accordingly
    sleep(1)
    gripper(50)
    sendToEpson("go_approach_slider " + str(target2)) # start location
    sleep(1)
    gripper(70)
    sleep(2)
    # #sendToEpson("go_slide 16")
    sendToEpson("go_slide " + str(target1))
    sleep(2)
    # # gripper will go back to Slider_start position
    gripper(50)
    sleep(1)
    sendToEpson("go_tool_up")
    

# --- open the door            
def door():
    gripper(80)
    sendToEpson("go_open_door")
    
# --- move the probe's plug
def plug():
    gripper(50)
    sleep(1.5)
    sendToEpson("go_approach_plug1")
    gripper(90)
    sleep(1.5)
    sendToEpson("go_approach_plug2")
    sleep(1.5)
    gripper(50)
    sleep(0.5)
    sendToEpson("go_approach_plug3")

# --- take probe, probe in, drop probe
def probe():
    #probing sequence here
    sendToEpson("go_probe1")
    
# --- wind cable
def cable():
    sendToEpson("go_wind_cable")
    
# --- stow
def stow():
    sendToEpson("go_stow")
    
# --- press red button
def rb():
    sendToEpson("go_press_red_button")
    
# ==== main actions

cam = ConnectCamera()           # connect to camera
sendToEpson("m Camera_Pos")     # send robot arm to Camera_pos
gripper(80)                     # close gripper
                                
x1,y1,x2,y2 = get_coord(cam)    # and get world coordinates here
print(x1,y1,x2,y2)              # verify the coordinates
sendToEpson("local " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) )
# --- run the sequence
# --- we will add the user input to enable custom sequence
m5()
bb()
slide(cam)
door()
plug()
probe()
cable()
stow()
rb()
