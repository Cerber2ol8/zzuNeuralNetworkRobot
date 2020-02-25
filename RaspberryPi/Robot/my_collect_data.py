
import numpy as np
import cv2
import socket
import time
import os
import threading
from config  import *


class VideoStreaming(threading.Thread):
    def __init__(self,threadID, name,input_size):
        print("串流线程初始化...")
        threading.Thread.__init__(self)
        self.server_socket = socket.socket()
        self.server_socket.bind((PC, streaming_port))
        self.server_socket.listen(0)
        self.connection, self.client_address = self.server_socket.accept()
        print(self.connection, self.client_address)
        self.connection = self.connection.makefile('rb')
        self.threadID = threadID
        self.name = name
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        self.thread_stop = False 
        self.input_size = input_size
        self.send_inst =True
        self.k = np.zeros((3, 3), 'float')

        self.frame = 0
        self.saved_frame = 0
        self.total_frame = 0
        self.clicks_forward = 0
        self.clicks_left  = 0
        self.clicks_right = 0
        self.stream_bytes = b' '
        self.clicks_total = 0
        self.img_num = 0

        self.file_name = ''
        self.jpg = b' '
        self.image = None
        #X = np.empty((0, self.input_size))     数据集先储存为图片，训练时再转换成np.arrary
        self.y = np.empty((0, 3))
        for i in range(3):
            self.k[i, i] = 1
    def run(self): #Overwrite run() method, put what you want the thread do here  
        if not self.thread_stop: 
            print("线程"+self.name+"开始运行")
            self.streaming()

    def stop(self):  
            self.thread_stop = True  
            print("线程"+self.name+"结束")

    def streaming(self):

        # collect images for training
        print("Host: ", self.host_name + ' ' + self.host_ip)
        print("Connection from: ", self.client_address)
        print("Start collecting images...")
        print("Press 'q' or 'x' to finish...")
        start = cv2.getTickCount()

        

        # stream video frames one by one
        try:
            
            self.frame = 1
            while self.send_inst:
                self.stream_bytes += self.connection.read(1024)
                first = self.stream_bytes.find(b'\xff\xd8')
                last = self.stream_bytes.find(b'\xff\xd9')

                if first != -1 and last != -1:
                    self.jpg = self.stream_bytes[first:last + 2]
                    self.stream_bytes = self.stream_bytes[last + 2:]
                    self.image = cv2.imdecode(np.frombuffer(self.jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                    self.clicks_total = self.clicks_forward + self.clicks_left + self.clicks_right
                    cv2.putText(self.image, "FW: {}, LT: {}, RT: {}, TOTAL: {}".format(self.clicks_forward, 
                                                                                  self.clicks_left, 
                                                                                  self.clicks_right, self.clicks_total
                                                                                  ), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, .45, (255, 255, 0), 1)
                    # select lower half of the image
                    #height, width = image.shape            不在collect里处理图片了，训练之前预处理再说
                    #roi = image[int(height/2):height, :]
                    cv2.imshow('image', self.image)
 

                    # reshape the roi image into a vector
                    #img_array = roi.reshape(1, int(height/2) * width).astype(np.float32)
                    self.frame += 1
                    self.total_frame += 1
                    #print(np.shape(img_array),np.shape(X))
                    #exit()
                key = cv2.waitKeyEx(1)>>16
                if key == 35:
                    break
                elif key == -1:
                    pass
                else:
                    #key_left = 37  key_up = 38    
                    #key_right = 39   key_down = 40
                    SendCmd.send(key)
                    print(key)



            

        finally:
            # save data as a numpy file
            end = cv2.getTickCount()
            # calculate streaming duration
            print("Streaming duration: , %.2fs" % ((end - start) / cv2.getTickFrequency()))
            with open('./logs/log_img_collect.txt', 'a') as f:
                f.write('Date: ' + time.strftime('%x') + '\n')
                f.write('Time: ' + time.strftime('%X') + '\n')
                f.write('Total images: {}'+ str(self.img_num) + '\n')
                f.write('Total frames: ' + str(self.total_frame) + '\n')
                f.write('Saved frames: ' + str(self.saved_frame) + '\n')
                f.write('Dropped frames: ' + str(self.total_frame - self.saved_frame) + '\n')
                f.write('Forward clicks: ' + str(self.clicks_forward) + '\n')
                f.write('Forward-left clicks: ' + str(self.clicks_left) + '\n')
                f.write('Forward-right clicks: ' + str(self.clicks_right) + '\n')
                f.write('-----------------------------\n')
            
            
            print ('Forward clicks: {}'.format( self.clicks_forward))
            print ('Forward-left clicks:{}'.format(self.clicks_left))
            print ('Forward-right clicks: {}'.format(self.clicks_right))
            print ('Total images: {}'.format(self.img_num))
            print ('Total frame:{}'.format(self.total_frame))
            print ('Saved frame:{}'.format(self.saved_frame))
            print ('Dropped frame{}'.format(self.total_frame - self.saved_frame))
            self.file_name = str(int(time.time()))
            try:
                np.savez('training_images/label_array_ORIGINALS_{}.npz'.format(self.file_name), train_labels=self.y)
            except IOError as e:
                print(e)
            print( "销毁串流线程...")
            self.connection.close()
            self.server_socket.close()
    def collect_pic(self,key):
                if key == KEY_LEFT:
                    #print('left')
                    #X = np.vstack((X, img_array))      
                    cv2.imwrite('./training_images/frame{:>05}.jpg'.format(self.frame), self.image)
                    self.y = np.vstack((self.y, self.k[0]))       # self.k[0] = [ 1.,  0.,  0.]
                    self.clicks_left += 1                              
                    self.saved_frame += 1
                elif key ==KEY_RIGHT:   
                    #print('right')
                    #X = np.vstack((X, img_array))
                    cv2.imwrite('./training_images/frame{:>05}.jpg'.format(self.frame), self.image)
                    self.y = np.vstack((self.y, self.k[1]))       # self.k[1] = [ 0.,  1.,  0.]
                    self.clicks_right += 1
                    self.saved_frame += 1
                elif key==KEY_UP:
                    #print('forward')
                    #X = np.vstack((X, img_array))
                    cv2.imwrite('./training_images/frame{:>05}.jpg'.format(self.frame), self.image)
                    self.y = np.vstack((self.y, self.k[2]))       # self.k[2] = [ 0.,  0.,  1.]
                    self.clicks_forward += 1
                    self.saved_frame += 1
                self.img_num +=1
                print(self.clicks_left,self.clicks_forward,self.clicks_right)




class SendCmd():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.socket.connect((RasPi,cmd_port))
        self.socket.sendall(b'\x52\x53')
    def send(self,key):
        #key_left = 37  key_up = 38    
        #key_right = 39   key_down = 40
        if key==38:
            print("Forward")
            self.socket.sendall(forward)
            Stream.collect_pic(KEY_UP)
        elif key==40:
            print("Stop")
            self.socket.sendall(stop)
            Stream.collect_pic(KEY_DOWN)
        elif key==39:
            print("Right")
            self.socket.sendall(right)
            Stream.collect_pic(KEY_RIGHT)
        elif key==37:
            print("Left")
            self.socket.sendall(left)
            Stream.collect_pic(KEY_LEFT)




if __name__ == '__main__':
    if not os.path.exists(training_path):
        os.makedirs(training_path)
    _size = 120*320
    Stream = VideoStreaming(1,"串流",_size)
    SendCmd = SendCmd()
    Stream.start()
    #readkey = Read()
    #Stream = Streaming(_size)
    #threads = []
    #t1 = threading.Thread(target=readkey.run)
    #threads.append(t1)
    #t2 = threading.Thread(target=Stream.streaming)
    #threads.append(t2)
    #for t in threads:
    #    t.start()
    #for t in threads:
    #    t.join()

    


 
