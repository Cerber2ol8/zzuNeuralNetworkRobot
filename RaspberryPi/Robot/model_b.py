import cv2
import numpy as np
from numpy import ones,vstack
from numpy.linalg import lstsq
import glob
import random
import time
from statistics import mean
sigma = 0.33
def proc_img(file):
    img = cv2.imread(file)[40:220,:]
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    v = np.median(blurred)
    lower = int(max(0,   (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edges = cv2.Canny(blurred, lower, upper, apertureSize = 3)
    #return edges
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 10,minLineLength=20,maxLineGap=15)
    try:
        l1, l2 = draw_lanes(img,lines)
        cv2.line(img, (l1[0], l1[1]), (l1[2], l1[3]), [0,255,0], 30)
        cv2.line(img, (l2[0], l2[1]), (l2[2], l2[3]), [0,255,0], 30)
    except Exception as e:
        print(str(e))
        pass
    try:
        for coords in lines:
            coords = coords[0]
            try:
                cv2.line(edges, (coords[0], coords[1]), (coords[2], coords[3]), [255,0,0], 3)
                
                
            except Exception as e:
                print(str(e))
    except Exception as e:
        pass
    return edges
def calculate_lines(frame,lines):
	# 建立两个空列表，用于存储左右车道边界坐标
	left = []
	right = []

	# 循环遍历lines
	for line in lines:
		# 将线段信息从二维转化能到一维
		x1,y1,x2,y2 = line.reshape(4)

		# 将一个线性多项式拟合到x和y坐标上，并返回一个描述斜率和y轴截距的系数向量
		parameters = np.polyfit((x1,x2), (y1,y2), 1)
		slope = parameters[0] #斜率 
		y_intercept = parameters[1] #截距

		# 通过斜率大小，可以判断是左边界还是右边界
		# 很明显左边界slope<0(注意cv坐标系不同的)
		# 右边界slope>0
		if slope < 0:
			left.append((slope,y_intercept))
		else:
			right.append((slope,y_intercept))
	print(left,right)
	# 将所有左边界和右边界做平均，得到一条直线的斜率和截距
	if left != []:
		left_avg = np.average(left,axis=0)
		left_line = calculate_coordinate(frame,parameters=left_avg)
	else:
		left_line = calculate_coordinate(frame,parameters=[0,0])
	if right != []:
		right_avg = np.average(right,axis=0)
		right_line = calculate_coordinate(frame, parameters=right_avg)
	else:
		right_line = calculate_coordinate(frame, parameters=[0,0])

	#print(left_avg,right_avg)
	# 将这个截距和斜率值转换为x1,y1,x2,y2


	return np.array([left_line,right_line])

# 将截距与斜率转换为cv空间坐标
def calculate_coordinate(frame,parameters):
	# 获取斜率与截距
	slope, y_intercept = parameters

	# 设置初始y坐标为自顶向下(框架底部)的高度
	# 将最终的y坐标设置为框架底部上方150
	y1 = frame.shape[0]
	y2 = 0
	# 根据y1=kx1+b,y2=kx2+b求取x1,x2
	if slope == 0:
		x1 = 0
		x2 = 0
	else:
	    x1 = int((y1-y_intercept)/slope)
	    x2 = int((y2-y_intercept)/slope)
	return np.array([x1,y1,x2,y2])

# 可视化车道线
def visualize_lines(frame,lines):
	lines_visualize = np.zeros_like(frame)
	# 检测lines是否为空
	if lines is not None:
		for x1,y1,x2,y2 in lines:
			if x1 !=0 and x2 != 0:
				# 画线
				cv2.line(lines_visualize,(int(x1),int(y1)),(int(x2),int(y2)),(0,0,255),5)
	return lines_visualize

# Tools 
# Canny检测
def do_canny(frame):
	# 将每一帧转化为灰度图像，去除多余信息
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	# 高斯滤波器，去除噪声，平滑图像
	blur = cv2.GaussianBlur(gray,(5,5),0)
	# 边缘检测
	# minVal = 50
	# maxVal = 150
	canny = cv2.Canny(blur,50,150)

	return canny

# 图像分割，去除多余线条信息
def do_segment(frame):
	# 获取图像高度(注意CV的坐标系,正方形左上为0点，→和↓分别为x,y正方向)
	height = frame.shape[0]

	# 创建一个三角形的区域,指定三点
	polygons = np.array([
		[(0,height), 
		 (320,height),
		 (240,0)]
		])

	# 创建一个mask,形状与frame相同，全为0值
	mask = np.zeros_like(frame)

	# 对该mask进行填充，做一个掩码
	# 三角形区域为1
	# 其余为0
	cv2.fillPoly(mask,polygons,255) 

	# 将frame与mask做与，抠取需要区域
	segment = cv2.bitwise_and(frame,mask) 

	return segment

# 车道左右边界标定
def process_img(image):
    image = image[40:220,:]
    original_image = image
    # edge detection
    processed_img =  cv2.Canny(image, threshold1 = 200, threshold2=300)
    
    processed_img = cv2.GaussianBlur(processed_img,(5,5),0)
   

    # more info: http://docs.opencv2.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
    #                                     rho   theta   thresh  min length, max gap:        
    lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180,      20,       15)
    m1 = 0
    m2 = 0
    try:
        l1, l2, m1,m2 = draw_lanes(original_image,lines)
        cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [0,255,0], 30)
        cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [0,255,0], 30)
    except Exception as e:
        print(str(e))
        pass
    try:
        for coords in lines:
            coords = coords[0]
            try:
                cv2.line(processed_img, (coords[0], coords[1]), (coords[2], coords[3]), [255,0,0], 3)
                
                
            except Exception as e:
                print(str(e))
    except Exception as e:
        pass

    return processed_img,original_image, m1, m2

def draw_lanes(img, lines, color=[0, 255, 255], thickness=3):

    # if this fails, go with some default line
    #try:

    # finds the maximum y value for a lane marker 
    # (since we cannot assume the horizon will always be at the same point.)

    ys = []  
    for i in lines:
        for ii in i:
            ys += [ii[1],ii[3]]
    min_y = min(ys)
    max_y = 600
    new_lines = []
    line_dict = {}

    for idx,i in enumerate(lines):
        for xyxy in i:
            # These four lines:
            # modified from http://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points
            # Used to calculate the definition of a line, given two sets of coords.
            x_coords = (xyxy[0],xyxy[2])
            y_coords = (xyxy[1],xyxy[3])
            A = vstack([x_coords,ones(len(x_coords))]).T
            m, b = lstsq(A, y_coords)[0]

            # Calculating our new, and improved, xs
            x1 = (min_y-b) / m
            x2 = (max_y-b) / m

            line_dict[idx] = [m,b,[int(x1), min_y, int(x2), max_y]]
            new_lines.append([int(x1), min_y, int(x2), max_y])

    final_lanes = {}

    for idx in line_dict:
        final_lanes_copy = final_lanes.copy()
        m = line_dict[idx][0]
        b = line_dict[idx][1]
        line = line_dict[idx][2]
            
        if len(final_lanes) == 0:
            final_lanes[m] = [ [m,b,line] ]
                
        else:
            found_copy = False

            for other_ms in final_lanes_copy:

                if not found_copy:
                    if abs(other_ms*1.2) > abs(m) > abs(other_ms*0.8):
                        if abs(final_lanes_copy[other_ms][0][1]*1.2) > abs(b) > abs(final_lanes_copy[other_ms][0][1]*0.8):
                            final_lanes[other_ms].append([m,b,line])
                            found_copy = True
                            break
                    else:
                        final_lanes[m] = [ [m,b,line] ]

    line_counter = {}

    for lanes in final_lanes:
        line_counter[lanes] = len(final_lanes[lanes])

    top_lanes = sorted(line_counter.items(), key=lambda item: item[1])[::-1][:2]

    lane1_id = top_lanes[0][0]
    lane2_id = top_lanes[1][0]

    def average_lane(lane_data):
        x1s = []
        y1s = []
        x2s = []
        y2s = []
        for data in lane_data:
            x1s.append(data[2][0])
            y1s.append(data[2][1])
            x2s.append(data[2][2])
            y2s.append(data[2][3])
        return int(mean(x1s)), int(mean(y1s)), int(mean(x2s)), int(mean(y2s)) 

    l1_x1, l1_y1, l1_x2, l1_y2 = average_lane(final_lanes[lane1_id])
    l2_x1, l2_y1, l2_x2, l2_y2 = average_lane(final_lanes[lane2_id])

    return [l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2], lane1_id, lane2_id



if __name__ == '__main__':
    files = glob.glob('./images/imgs_20190819_190820/*.jpg')
    file = files[int(random.random()*len(files))]
    img = cv2.imread(file)[40:220,:]
    #img, proc  = process_img(file)
    canny = do_canny(img)
    #segment = do_segment(canny)
    segment = canny
    #cv2.imshow('img',img)
    hough = cv2.HoughLinesP(segment, 2, np.pi/180, 100,minLineLength=20, maxLineGap=10)
    try:
        lines = calculate_lines(img, hough)
        print(lines)
        lines_visualize = visualize_lines(img, lines)
        output = cv2.addWeighted(img,0.6,lines_visualize,1,0.1)
        cv2.imshow("output", output)
        #cv2.imshow('processed',proc)
        #print(m1,m2)
    except Exception as e:
        print(str(e))
        cv2.imshow("img", img)
    while True:
        if cv2.waitKey(0) & 0xff == ord('q'):
            cv2.destroyAllWindows()
            break

    pass
