import cv2
import numpy as np
from numpy import ones,vstack
from numpy.linalg import lstsq
import glob
import random
import time
from statistics import mean
from config import *
import math

sigma = 0.33
ROIS = [(0,140,320,40,0.7),
(0,80,320,40,0.2),
(0,0,320,80,0.1)]
weight_sum = 0
for r in ROIS:
    weight_sum += r[4]
def proc_img(original_image):
    img = original_image[40:220,:]
    #img, proc  = process_img(file)
    blurred = cv2.GaussianBlur(img, (3, 3), 0)
    canny = auto_canny(blurred)
    #segment = do_segment(canny)
    segment = canny
    hough = cv2.HoughLinesP(segment, 2, np.pi/180, 15,minLineLength=20, maxLineGap=10)
    return hough
def calculate_lines(frame,lines):

	left = []
	right = []
	y1s_l = []
	y1s_r = []

	for line in lines:

		x1,y1,x2,y2 = line.reshape(4)

		parameters = np.polyfit((x1,x2), (y1,y2), 1)
		slope = parameters[0] 
		y_intercept = parameters[1] 


		if slope < 0:
			left.append((slope,y_intercept))
			y1s_l.append(y1) 
		else:
			right.append((slope,y_intercept))
			y1s_r.append(y1) 

	#print(y1s_l, y1s_r)
	if y1s_l != []:
		y1_l = max(y1s_l)
	else:
		y1_l = frame.shape[0]

	if y1s_r != []:
		y1_r = max(y1s_r)
	else:
		y1_r = frame.shape[0]

	if left != []:
		left_avg = np.average(left,axis=0)
		left_line = calculate_coordinate(frame,parameters=left_avg, y1 = y1_l)
	else:
		left_line = calculate_coordinate(frame,parameters=[0,0], y1 = y1_l)
	if right != []:
		right_avg = np.average(right,axis=0)
		right_line = calculate_coordinate(frame, parameters=right_avg, y1 = y1_r)
	else:
		right_line = calculate_coordinate(frame, parameters=[0,0], y1 = y1_r)


    
	return np.array([left_line,right_line])


def calculate_coordinate(frame,parameters, y1):

	slope, y_intercept = parameters


	y2 = 0

	if slope == 0:
		x1 = 0
		x2 = 0
	else:
	    x1 = int((y1-y_intercept)/slope)
	    x2 = int((y2-y_intercept)/slope)
	return np.array([x1,y1,x2,y2])


def visualize_lines(frame,lines):
	lines_visualize = frame

	color = [(0,0,255),(0,255,0)]
	line_list = lines.tolist()

	if lines is not None:
		for x1,y1,x2,y2 in lines:
			if x1 !=0 and x2 != 0:
 				index = line_list.index([x1,y1,x2,y2])
 				clr = color[index]
 				cv2.line(lines_visualize,(int(x1),int(y1)),(int(x2),int(y2)),clr,5)
	return lines_visualize


def auto_canny(blurred):
    # Compute the median of the single channel pixel intensities
    v = np.median(blurred)

    # Apply automatic Canny edge detection using the computed median of the image
    lower = int(max(0,   (1.0 - SIGMA) * v))
    upper = int(min(255, (1.0 + SIGMA) * v))
    edged = cv2.Canny(blurred, lower, upper)
    return edged
def predict_fn1(edged):
    print(edged.shape)
    #hough = cv2.HoughLinesP(edged, 2, np.pi/180, 20,minLineLength=20, maxLineGap=10)
    
    color = edged[160 ]
    white_count = np.sum(color == 255)
    white_index = np.where(color == 255)
    if white_count == 0:
        white_count = 1
    try:
        #lines = calculate_lines(edged, hough)
        center = (white_index[0][0] + white_index[0][white_count-1])/2

    except:
        pass

    direction = center - 160
    print("center:{} ; count:{} ; index:{} ; direction:{} ".format(center,white_count,white_index,direction))
    if direction <= -45:
        return np.array([0., 1., 0.]), None
    elif direction <= 45:
        return np.array([0., 0., 1.]), None
    else:
        return np.array([1., 0., 0.]), None
def predict(img):
    #angel = get_angel(img)
    angel = get_point(img)
    if angel == -50:
        return np.array([0., 1., 0.]), None
    elif angel == 0:
        return np.array([1., 0., 0.]), None
    else:
        return np.array([.0, 0., 1.]), None

    




def get_point(canny):
    line = canny[140]
    center_point = line[160]
    left_point = 0
    right_point = 0
    left_index = 159
    right_index = 161
    while left_index > 0:
        if line[left_index] == 255:
            left_point = left_index
            break
        else:
            left_index -= 1


    while right_index < 320:
        if line[right_index] == 255:
            right_point = right_index
            break
        else:
            right_index += 1

    width = right_point - left_point
    dl, dr =  width-left_point, right_point-width
    print("dl:{}, dr:{}".format(dl,dr))
    if dr <=5:
        return -50
    if dl - dr > 30 :
        return 50
    elif dl - dr < -20:
        return -50
    else:
        return 0
    
    

def get_angel(img):
    centroid_sum = 0
    angel = 0
    blobs = get_blobs(img)
    if blobs:
        most_pixels = 0
        largest_blobs = 0
        for i in range(len(blobs)):
            if blobs[i].pixels() > most_pixels:
                most_pixels = blobs[i]
                largest_blobs = i
        #cv2.rectangele(img, )
        #cv2.drawcross()
        centroid_sum += blobs[largest_blobs][0] *r[4]
    print(blobs)

    centroid_pos = (centroid_sum / weight_sum)

    angel = -math.atan((centroid_pos - 160)/90)
    angel = angel*108/np.pi
    return angel
    print("Need to trun angel:{}".format(angel))
def get_mask(img):
    blurred = cv2.GaussianBlur(img,(3,3),0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    prepleMin = (115,50,10)
    purpleMax(160,255,255)
    mask = cv2.inRange(hsv, purpleMin, purpleMax)
    res = cv2.bitwise_and(frame,frame,mask = mask)
    mask = cv2.erode(mask, None, iterations = 1)
    mask = cv2.dilate(mask, None, iterations = 1)
    return mask 
def get_blobs(mask):
    params = cv2.SimpleBlobDetector_Params()
    params.minThreshold = 0
    params.maxThreshold = 256
    params.filterByArea = True
    params.minArea = 30
    params.filterByConvexity = True
    params.minConvexity = 0.5
    params.filterByInertia = True
    params.minInertiaRatio = 0.5


    detector = cv2.SimpleBlobDetector_create(params)
    reversemask = 255 - mask
    blobs = detector.detect(mask)
    return blobs


def predict_fn(edged):
    hough = cv2.HoughLinesP(edged, 2, np.pi/180, 20,minLineLength=20, maxLineGap=10)
    #predict = np.array([ 0. , 0. , 1.])
    try:
        
        lines = calculate_lines(edged, hough)
        l = lines.tolist() #[[x1,y1,x2,y2], [x1,y1,x2,y2]]
        l_x1, l_y1, l_x2, l_y2, r_x1, r_y1, r_x2, r_y2 =  l[0][0], l[0][1], l[0][2], l[0][3], l[1][0], l[1][1], l[1][2], l[1][3]
        if (l_x2 - l_x1) != 0:
            slope_l = (l_y2 - l_y1)/(l_x2 - l_x1)
        else:
            slope_l = None
        
        if (r_x2 - r_x1) != 0:
            slope_r = (r_y2 - r_y1)/(r_x2 - r_x1)
        else:
            slope_r = None  
        predict = np.array([ 1. , 0. , 0.])
        predict = predict_from_slope_fn(slope_l=slope_l, slope_r=slope_r)


    except Exception as e:

        print(str(e))
    return predict, lines
def predict_from_slope_fn(slope_l = None,slope_r = None):
    limit = 80/180*np.pi
    limit_l = 75/180*np.pi
    limit_r = 75/180*np.pi
    limit_min = 15/180*np.pi
    
    if slope_r !=None:
        theta_r = abs(math.atan(slope_r))
    else: 
        theta_r = 0
    if slope_l !=None:
        theta_l = abs(math.atan(slope_l))
    else:
        theta_l = 0
    predict = np.array([ 1. , 0. , 0.])
    if theta_l*theta_r != 0:
        predict = np.array([ 0. , 0. , 1.])
    elif theta_l == 0 and theta_r < limit:
        predict = np.array([ 1. , 0. , 0.])
    elif theta_r == 0 and theta_l < limit:
        predict = np.array([ 0. , 1. , 0.])
    else:
        predict = np.array([ 0. , 0. , 1.])
        print(2)
    return predict
def predict_from_slope(slope_l = None,slope_r = None):
    limit = 75/180*np.pi
    limit_l = 75/180*np.pi
    limit_r = 75/180*np.pi
    limit_min = 15/180*np.pi
    predict = np.array([ 0. , 0. , 1.])
    if slope_r !=None:
        theta_r = math.atan(slope_r)
    else: 
        theta_r = 0
    if slope_l !=None:
        theta_l = math.atan(slope_l)
    else:
        theta_l = 0

    if slope_l == None and slope_r !=None:

        if theta_r > -limit and theta_r <= 0:
            predict = np.array([ 1. , 0. , 0.])
        elif theta_r > 0 and theta_r < limit_r:
            predict = np.array([ 1. , 0. , 0.])
        else:
            predict = np.array([ 0. , 0. , 1.])
            print('slope_l == None and slope_r !=None')
    elif slope_l != None and slope_r == None:
        if theta_l < limit and theta_l >= 0:
            predict = np.array([ 0. , 1. , 0.])
        elif theta_l < 0 and theta_l > -limit_l:
            predict = np.array([ 0. , 1. , 0.])
        #elif theta_1 
        else:
            predict = np.array([ 0. , 0. , 1.])
            print('slope_l != None and slope_r == None')
    elif slope_l != None and slope_r != None:
        if abs(theta_r) <= limit_min:
            return predict_from_slope(slope_l=slope_l,slope_r=None)
        if abs(theta_l) <= limit_min:
            return predict_from_slope(slope_l=None,slope_r=slope_r)

        if theta_r <= 0 and theta_l >= 0 :
            predict = np.array([ 0. , 0. , 1.])
            print('theta_r <= 0 and theta_l >= 0')
        elif theta_l > 0 and theta_r > 0 and theta_l < limit_l and theta_r < limit_r :
            predict = np.array([ 0. , 1. , 0.])
        elif theta_l < 0 and theta_r < 0 and theta_l > -limit_l and theta_r > -limit_r :
            predict = np.array([ 1. , 0. , 0.])   
        else:
            predict = np.array([ 0. , 0. , 1.])
            print('slope_l != None and slope_r != None')
    else:
            predict = np.array([ 0. , 0. , 1.])
            print('else')
    print('k = ',slope_l,slope_r)
    print('theta = ',theta_l,theta_r)
    return predict

def test_visiukize(img):
    hough = proc_img(img)
    try:
        lines = calculate_lines(img, hough)
        lines_visualize = visualize_lines(img, lines)
        #output = cv2.addWeighted(img,0.6,lines_visualize,1,0.1)
        cv2.imshow("img", img)
        cv2.imshow("lines_visualize", lines_visualize)
        #cv2.imshow('processed',proc)
        #print(m1,m2)
    except Exception as e:
        print(str(e))
    while True:
        if cv2.waitKey(0) & 0xff == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    files = glob.glob('./training_images/*.jpg')
    file = files[int(random.random()*len(files))]
    img = cv2.imread(file)[40:220,:]
    blurred = cv2.GaussianBlur(img, (3, 3), 0)
    canny = auto_canny(blurred)
    print(predict(canny))
    cv2.imshow("img", img)
    cv2.imshow("canny", canny)
    while True:
        if cv2.waitKey(0) & 0xff == ord('q'):
            cv2.destroyAllWindows()
            break