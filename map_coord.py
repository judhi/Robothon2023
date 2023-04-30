import cv2
import datetime
import math
from time import sleep
import numpy as np
import arduino_communication
from SendToEpson import sendToEpson # connect to EPSON Robot and send command via TCP/IP
import Settings

sendToEpson("M Camera_Pos")
sleep(1.5)
   

def increase_contrast(img, clipLimit = 2.0, tileGridSize=(120,12)):
    lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)

    # Applying CLAHE to L-channel
    clahe = cv2.createCLAHE(clipLimit, tileGridSize)
    cl = clahe.apply(l_channel)
    
    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl,a,b))
    
    # Converting image from LAB Color model to BGR color spcae
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    
    return enhanced_img

def show_image(title,file):
    cv2.imshow(title,file)
    cv2.waitKey(0)
    cv2.destroyWindow(title)
    cv2.waitKey(1)

def increase_contrast(img, clipLimit = 2.0, tileGridSize=(120,12)):
    lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)

    # Applying CLAHE to L-channel
    clahe = cv2.createCLAHE(clipLimit, tileGridSize)
    cl = clahe.apply(l_channel)
    
    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl,a,b))
    
    # Converting image from LAB Color model to BGR color spcae
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    
    return enhanced_img

def detect_door(image):
    x = y = w = h = 0
    
    # Step 1: Preprocessing
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)

    # Threshold with an optimal value
    t,thresh = cv2.threshold(blurred, 128, 255, cv2.THRESH_BINARY)

    # Step 2: Morphological operations
    kernel = np.ones((5, 5), np.uint8)
    eroded = cv2.erode(thresh, kernel, iterations=1)
    dilated = cv2.dilate(eroded, kernel, iterations=1)

    # Step 3: Contour detection
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Step 4: Bounding box and filtering based on area and aspect ratio
    # Since our door is roughly a square
    for contour in contours:
        area = cv2.contourArea(contour)
        t_x, t_y, t_w, t_h = cv2.boundingRect(contour)
        aspect_ratio = float(t_w)/t_h  
        if 140000 < area < 240000 and 0.75 < aspect_ratio < 1.5:
            cv2.drawContours(image, [contour], -1, (0, 255, 0), 3)
            x = t_x
            y = t_y
            w = t_w
            h = t_h
    #show_image('i', image)
    return x, y, w, h

def detect_knob(image, x, y, w, h):
    # Set center and radius to 0
    center = radius = 0
    
    # Create an image of the same size as the original
    # Set it to all black, and just replace the door in the
    # correct position.
    # This is done so that the coordinates match the original image
    size = image.shape[0], image.shape[1], 3
    final = np.zeros(size, np.uint8)
    final[y:y+h, x:x+w] = image[y:y+h, x:x+w]
    #final = increase_contrast(final, 1.5)
    
    # Convert to grayscale, apply a bilateral filter
    f_gray = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
    f_blur = cv2.bilateralFilter(f_gray, 9, 150, 150)
    
    # Find circles. Parameters here ensure that the circles are far apart
    # Of a certain size, and use the correct Canny thresholds
    rows = f_blur.shape[0]
    circles = cv2.HoughCircles(f_blur, cv2.HOUGH_GRADIENT, 1, rows, param1=100, param2=10,minRadius=20, maxRadius=60)
    
    # If we've found even one circle, that's our guy.
    # Just look at the first and return the center and radius.
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            radius = i[2]
            break
    return center, radius



def get_coord(vid):
    # print("Starting camera")
    # #cam_device = 3 # on Judhi's laptop
    # cam_device = 0 # on lab's desktop
    # #vid = cv2.VideoCapture(cam_device,cv2.CAP_DSHOW) # activate Windows Direct Show for faster camera setup
    # vid = cv2.VideoCapture(0) # for other systems

    # print("Setting video resolution")
    # vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # max 3840 for 4K, 1920 for FHD
    # vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # max 2160 for 4K, 1080 for FHD
    # sleep(1.5)

    n_frame = 1 # frame counter

    while(1): 
        # Capture the video frame by frame
        print("Capturing frame")
        ret, img = vid.read()
        #print("using existing image")
        #img = cv2.imread("last_detected_image.png")
        #now = datetime.datetime.now()
        #filename = now.strftime("BOARD_%Y%m%d_%H%M%S.png")
        filename = "last_detected_image.png"
        cv2.imwrite(filename, img)
        # img = cv2.imread('images/BOARD9.jpg')

        # convert to HSV for color detection
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # ----------------- daylight --------------
        #lower_blue = np.array([75, 56, 56])
        #higher_blue = np.array([115, 255, 205])
        #lower_bright = np.array([75, 72, 129])  
        #higher_b = np.array([115, 253, 245])

        # # --------------- most reliable params so far (29-05-2022) --------------
        # lower_blue = np.array([70, 108, 88])
        # higher_blue = np.array([136, 255, 255])
        # lower_bright = np.array([0, 0, 0])
        # higher_bright = np.array([180, 255, 114])
        
        # --------------- new params (25-04-2023) --------------
        lower_blue = np.array([70, 108, 88])
        higher_blue = np.array([136, 255, 255])
        lower_bright = np.array([0, 0, 100])
        higher_bright = np.array([228, 60, 200])

        # getting the range of blue color in frame
        blue_range = cv2.inRange(hsv, lower_blue, higher_blue)
        bright_range = cv2.inRange(hsv, lower_bright, higher_bright)
        res_blue = cv2.bitwise_and(img,img, mask=blue_range)
        res_bright = cv2.bitwise_and(img,img, mask=bright_range)

        # Convert to grayscale and 
        # Blur using 3 * 3 kernel.
        print("Converting to grayscale")
        gray_blue = cv2.cvtColor(res_blue, cv2.COLOR_BGR2GRAY)
        gray_blue_blurred = cv2.blur(gray_blue, (3, 3))
        gray_bright = cv2.cvtColor(res_bright, cv2.COLOR_BGR2GRAY)
        gray_bright_blurred = cv2.blur(gray_bright, (3,3))

        # Apply Hough transform on the blurred image. One for the blue button, one for the keyhole
        print("Detecting circles")
        detected_blue_circles = cv2.HoughCircles(gray_blue_blurred, 
                        cv2.HOUGH_GRADIENT, 0.5, 1000, param1 = 45, #55
                    param2 = 10, minRadius = 19, maxRadius = 55)

        # Draw circles if detected.
        print("Drawing circles")
        if detected_blue_circles is not None:
            # Convert the circle parameters a, b and r to integers.
            detected_blue_circles = np.uint16(np.around(detected_blue_circles))
            print(detected_blue_circles)
            
            for pt in detected_blue_circles[0]:
                a1, b1, r1 = pt[0], pt[1], pt[2]
                x1, y1 = Settings.calculateXY(a1, b1)
                # compensate for blue button here
                x1 = x1 + 0.5
                # Draw the circle
                cv2.circle(img, (a1, b1), r1, (0, 255, 0), 2)
                # Draw the center of the circle
                cv2.circle(img, (a1, b1), 1, (0, 0, 255), 3)
                # add text label
                a1 = round(a1, 2)
                b1 = round(b1, 2)
                x1 = round(x1, 2)
                y1 = round(y1, 2)
                cv2.putText(img, "Blue (" + str(a1) + ","+ str(b1) + ") r=" + str(r1), (a1+10,b1+r1+2), cv2.FONT_HERSHEY_SIMPLEX,1,(255,100,0),2 )
                cv2.putText(img, "World [" + str(x1) + ","+ str(y1)+ "]", (a1+10,b1+r1-50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,100,100),2 )

            #contr = increase_contrast(img)
            
            # Find the door first
            x, y, w, h = detect_door(img)

            # If a door is found, detect the knob and draw it on the original
            if x != 0:
                # knob_center and knob_readius are your pixel values for the door-knob
                # Maybe the radius isn't as important, but the center should be useful
                knob_center, knob_radius  = detect_knob(img, x, y, w, h)
                a2,b2 = knob_center
                x2, y2 = Settings.calculateXY(a2, b2)
                # compensate knob position here
                x2 = x2 + 1.5
                y2 = y2 + 0.5
                # Draw both and show the image, just for fun.
                if knob_radius != 0:
                    cv2.circle(img, knob_center, 5, (255, 0, 0), -1)
                    cv2.circle(img, knob_center, knob_radius, (0, 255, 0), 3)
                    cv2.putText(img, "Knob (" + str(a2) + ","+ str(b2) + ") r=" + str(knob_radius), (a2+knob_radius+2,b2+10), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2 )
                    cv2.putText(img, "World [" + str(x2) + ","+ str(y2)+ "]", (a2+10,b2+knob_radius+50), cv2.FONT_HERSHEY_SIMPLEX,1,(0,50,255),2 )
                # add label for human input to start the robot OR quit OR recapture image
                cv2.putText(img, "Press 'g' = start robot, 'q' = quit, other key = recapture", (50,100), cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,255),2)
                
                # check the distance between the Blue button and the Keyhole
                pixel_distance = np.sqrt((int(a2)-int(a1))**2 + (int(b2)-int(b1))**2)
                print("Pixel distance : " + str(round(pixel_distance,0)) ) 
                # resize the image to show
                img_r = cv2.resize(img,(860,540))
                cv2.imshow("Detected Circle", img_r)

                print("Blue Button:")
                print("Pixel is at x=" + str(a1) + "  y="+ str(b1) + " r=" + str(r1))
                print("World [" + str(x1) + ","+ str(y1)+ "]")
                print("go here :x(" + str(x1) + ") :y("+ str(y1) + ") :z(550)")
                print("-----")
                print("Knob:")
                print("Pixel is at x=" + str(a2) + "  y="+ str(b2) + " r=" + str(knob_radius))
                print("World [" + str(x2) + ","+ str(y2)+ "]")
                print("go here :x(" + str(x2) + ") :y("+ str(y2) + ") :z(550)")
                #sendToEpson("T "+str(x1)+" "+str(y1)+" "+str(x2)+" "+str(y2))
                print("MAKE SURE ROBOT IS READY!")
                print("Press 'g' to start robot")
                print("Press 'q' to quit")
                print("Any other key to re-capture image")
                # waiting for human's input
                k = cv2.waitKey(0)
                # if human selected to quit
                if k == ord('q'):
                    action = "quit"
                    break
                # if human selecting g
                if k == ord('g'):
                    action = "go"
                    break
            else:
                print("Door not found!")
        else:
            print("No circles detected") 
    
    if action == "quit":
        return False
    
    if action == "go":
        return x1,y1,x2,y2
    

            
