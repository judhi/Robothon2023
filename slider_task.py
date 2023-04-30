import cv2
import numpy as np

########################################
########################################
########### HELPER FUNCTIONS ###########
########################################
########################################

def __show_image__(title, file):
    cv2.imshow(title, file)
    cv2.waitKey(0)
    cv2.destroyWindow(title)
    cv2.waitKey(1)

def __order_points__(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")
	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	# return the ordered coordinates
	return rect

def __four_point_transform__(image, pts):
	# obtain a consistent order of the points and unpack them
	# individually
	rect = __order_points__(pts)
	(tl, tr, br, bl) = rect
	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
	# compute the height of the new image, which will be the
	# maximum distance between the top-right and bottom-right
	# y-coordinates or the top-left and bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
	# compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
	# return the warped image
	return warped

def __hsv_object_detector__(image, low_hsv, high_hsv, kSize = 3, opening = True, canny = True, return_max_contour = True, find_contours = True):
    kernel_size = (kSize, kSize)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv_image, low_hsv, high_hsv)
    opening_img = thresh
    if opening is True:
        opening_img = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    canny_img = opening_img
    if canny is True:
        canny_img = cv2.Canny(opening_img, 100, 200)
    #__show_image__('c',canny_img)
    if find_contours is True:
        contours, _ = cv2.findContours(canny_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        c = contours
        if len(c) > 0:
            if return_max_contour is True:
                c = max(contours, key=cv2.contourArea)
            return c
        else:
            return None
    else:
        return canny_img

def __detect_red_box__(image, showImage = False):
    # Crop to the relevant bottom-right corner to focus on the red-box
    #image = image[470:900, 900:1200]
    low_hsv = (0, 82, 142)
    high_hsv = (180, 255, 255)
    c = __hsv_object_detector__(image, low_hsv, high_hsv, 3, True, False, True)
    if c is not None:
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        warped = __four_point_transform__(image, box)
        if showImage is True:
            cv2.imshow('RedBox', warped)
            cv2.waitKey(0)
            cv2.destroyWindow('RedBox')
            cv2.waitKey(1)
        return warped
    else:
        return None

def __detect_screen__(image, showImage = False):
# Step 2: Detect the screen within the red-box
### Relative dimensions of the screen w.r.t. the red box are fixed
    low_hsv = (53, 0, 102)
    high_hsv = (154, 255, 255)
    thresh = __hsv_object_detector__(image, low_hsv, high_hsv, 3, opening=True, canny=False, return_max_contour=False,find_contours=False)
    kernel_size = (15, 15)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    dilate_img = cv2.dilate(thresh, kernel, iterations=2)
    eroded_img = cv2.erode(dilate_img, kernel, iterations=2)
    contours,_ = cv2.findContours(eroded_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        warped = __four_point_transform__(image, box)
        if showImage is True:
            cv2.imshow('Screen', warped)
            cv2.waitKey(0)
            cv2.destroyWindow('Screen')
            cv2.waitKey(1)
        return warped
    else:
        return None

def __calculate_distance__(target_y, screen_length, margin = 15, slider_length = 31):
    # There's a margin of 15px since the targets always appear to have some gap from the edges
    # Remove 2 x margin from the total length
    effective_slider_length = screen_length - (margin * 2)
    
    # Remove the trailing margin from the target arrow
    effective_target_y = target_y - margin
    
    # Target position is now somewhere between 0.0 and 1.0
    normalised_position = effective_target_y/effective_slider_length

    # This is done because the y-axis is reversed in OpenCV
    normalised_position = 1 - normalised_position

    distance = normalised_position * slider_length
    # print(effective_target_y)
    # print(effective_slider_length)
    # print(normalised_position)
    return distance

def __calculate_first_arrow_position__(image):
    # Step 3: Detect the arrows and calculate the relative movement: ArrowPosition (0.0 - 1.0)
    ### Within the screen, use the HSV colour space to detect the arrows
    ### The length of the slider is the same as the screen length (Convenient)

    # Step 4: Go to the slider and move accordingly
    ### Dimensions of the slider are known
    ### Starting position of the slider is known
    ### Move the slider according to ArrowPosition * TotalSliderLength
    ### E.g.: If TotalSliderLength = 31mm and ArrowPosition = 0.5 -> Move slider 15.5mm
    ### Remember new slider position
    # 31MM IS THE LENGTH OF THE SLIDER
    first_target_arrow_y = -1
    low_hsv = (0, 0, 221)
    high_hsv = (180, 100, 255)
    image = image[0:image.shape[0],int(image.shape[1]/1.5):image.shape[1]]
    final = __hsv_object_detector__(image, low_hsv, high_hsv, 3, True, False, False, False)
    contours, _ = cv2.findContours(final, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        arrow1 = contours[0]
        M1 = cv2.moments(arrow1)
        cy1 = int(M1['m01']/M1['m00'])
        first_target_arrow_y = cy1
        absolute_distance_in_mm = __calculate_distance__(first_target_arrow_y, image.shape[0])
        return abs(absolute_distance_in_mm)
    else:
        return -1

def __calculate_second_arrow_position__(previous,current):
    # Step 5: Detect the second arrow and calculate the relative movement: ArrowPosition (0.0 - 1.0)
    ### Within the screen, use the HSV colour space to detect the arrows
    ### The length of the slider is the same as the screen length (Convenient)
    second_target_arrow_y = -1
    low_hsv = (0, 0, 221)
    high_hsv = (180, 100, 255)
    previous = previous[0:previous.shape[0],int(previous.shape[1]/1.5):previous.shape[1]]
    current = current[0:current.shape[0],int(current.shape[1]/1.5):current.shape[1]] 
    previous = __hsv_object_detector__(previous, low_hsv, high_hsv, 3, True, False, False, False)
    current = __hsv_object_detector__(current, low_hsv, high_hsv, 3, True, False, False, False)
    previous_height, previous_width = previous.shape[0],previous.shape[1]
    current_height, current_width = current.shape[0],current.shape[1]
    min_height = min(previous_height, current_height)
    min_width = min(previous_width, current_width)
    cropped_previous = previous[0:min_height, 0:min_width]
    cropped_current = current[0:min_height, 0:min_width]
    final = cv2.subtract(cropped_current, cropped_previous)
    #__show_image__('Subtracted', final)
    contours, _ = cv2.findContours(final, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        cy = int(M['m01']/M['m00'])
        second_target_arrow_y = cy
        absolute_distance_in_mm = __calculate_distance__(second_target_arrow_y, current.shape[0])
        return abs(absolute_distance_in_mm)
    else:
        return -1

def __check_if_task_completed__(image, showImage = False):
    low_hsv = (32,67,46)
    high_hsv = (160,255,168)
    current = image[0:image.shape[0],int(image.shape[1]/2):image.shape[1]]
    current = __hsv_object_detector__(current, low_hsv, high_hsv, 3, True, False, False, False)
    white_pixels = cv2.countNonZero(current)
    if showImage is True:
        __show_image__('StripDetector', current)
        print(white_pixels)
    if white_pixels < 300:
        return False
    else:
        return True


########################################
########################################
########### PUBLIC FUNCTION ############
########################################
########################################
def get_target(current_image, previous_image = None, DEBUG_MODE = False):
    absolute_distance_in_mm = -1
    current_red_box = __detect_red_box__(current_image, DEBUG_MODE)
    if current_red_box is None:
        return -1
    current_screen = __detect_screen__(current_red_box, DEBUG_MODE)
    if current_screen is None:
        return -1
    if previous_image is not None:
        is_second_step_needed = __check_if_task_completed__(current_screen, DEBUG_MODE)
        if is_second_step_needed is False:
            absolute_distance_in_mm = -1
        else:
            previous_red_box = __detect_red_box__(previous_image, DEBUG_MODE)
            if previous_red_box is None:
                return -1
            previous_screen = __detect_screen__(previous_red_box, DEBUG_MODE)
            if previous_screen is None:
                return -1
            absolute_distance_in_mm = __calculate_second_arrow_position__(previous_screen, current_screen)
            if absolute_distance_in_mm > 30 or absolute_distance_in_mm < 1:
                return -1
    else:
        absolute_distance_in_mm = __calculate_first_arrow_position__(current_screen)
        if absolute_distance_in_mm > 30 or absolute_distance_in_mm < 1:
                return -1
    return absolute_distance_in_mm
