
import numpy as np
import cv2
import socket
import time
import os
import threading
import my_rc_driver_helper
import Readkey


host, port = "192.168.1.4", 8000
_host,_port = "192.168.1.12",8001
exitFlag = 0

KEY_CHANGE= False
LOCK = False
_CMD=chr(51).encode()
tick = 0





class VideoStreaming(threading.Thread):
    def __init__(self,threadID, name,input_size):
        print("串流线程初始化...")
        threading.Thread.__init__(self)
        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
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
        for i in range(3):
            self.k[i, i] = 1
        print(self.k)
    def run(self): #Overwrite run() method, put what you want the thread do here  
        if not self.thread_stop: 
            print("线程"+self.name+"开始运行")
            self.collect()

    def stop(self):  
            self.thread_stop = True  
            print("线程"+self.name+"结束")

    def collect(self):

        saved_frame = 0
        total_frame = 0
        clicks_forward       = 0
        clicks_forward_left  = 0
        clicks_forward_right = 0

        # collect images for training
        print("Host: ", self.host_name + ' ' + self.host_ip)
        print("Connection from: ", self.client_address)
        print("Start collecting images...")
        print("Press 'q' or 'x' to finish...")
        start = cv2.getTickCount()

        #X = np.empty((0, self.input_size))     数据集先储存为图片，训练时再转换成np.arrary
        y = np.empty((0, 3))
        # stream video frames one by one
        try:
            stream_bytes = b' '
            frame = 1
            while self.send_inst:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')

                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                    clicks_total = clicks_forward + clicks_forward_left + clicks_forward_right
                    cv2.putText(image, "FW: {}, LT: {}, RT: {}, TOTAL: {}".format(clicks_forward, 
                                                                                  clicks_forward_left, 
                                                                                  clicks_forward_right, clicks_total
                                                                                  ), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, .45, (255, 255, 0), 1)
                    # select lower half of the image
                    #height, width = image.shape            不在collect里处理图片了，训练之前预处理再说
                    #roi = image[int(height/2):height, :]
                    cv2.imshow('image', image)
 

                    # reshape the roi image into a vector
                    #img_array = roi.reshape(1, int(height/2) * width).astype(np.float32)
                    frame += 1
                    total_frame += 1
                    #print(np.shape(img_array),np.shape(X))
                    #exit()
                    global KEY_CHANGE
                    global _CMD
                    global LOCK
                        

                    if KEY_CHANGE:
                        
                        # print(chr(3).encode(),chr(4).encode(),chr(6).encode(),chr(7).encode())
                        # >> b'\x03' b'\x04' b'\x05' b'\x06' b'\x07'
                        #RIGHT 3,6    LEFT  4,7   FORWARD  1
                        if _CMD != chr(51).encode():

                            if _CMD == chr(4).encode() or _CMD == chr(7).encode():
                                #print('left')
                                #X = np.vstack((X, img_array))      
                                cv2.imwrite('./training_images/frame{:>05}.jpg'.format(frame), image)
                                y = np.vstack((y, self.k[0]))       # self.k[0] = [ 1.,  0.,  0.]
                                thread_Command.steer(np.array([ 1., 0., 0.]))
                                clicks_forward_left += 1                              
                                saved_frame += 1
                            elif _CMD ==chr(3).encode() or _CMD == chr(6).encode():   
                                #print('right')
                                #X = np.vstack((X, img_array))
                                cv2.imwrite('./training_images/frame{:>05}.jpg'.format(frame), image)
                                y = np.vstack((y, self.k[1]))       # self.k[1] = [ 0.,  1.,  0.]
                                thread_Command.steer(np.array([ 0., 1., 0.]))
                                clicks_forward_right += 1
                                saved_frame += 1
                            elif _CMD ==chr(1).encode():
                                #print('forward')
                                #X = np.vstack((X, img_array))
                                cv2.imwrite('./training_images/frame{:>05}.jpg'.format(frame), image)
                                y = np.vstack((y, self.k[2]))       # self.k[2] = [ 0.,  0.,  1.]
                                thread_Command.steer(np.array([ 0., 0., 1.]))
                                clicks_forward += 1
                                saved_frame += 1
                           

                        #print(KEY_CHANGE)
                        LOCK = True
                        KEY_CHANGE = False

                        
                        print(clicks_forward_left,clicks_forward_right,clicks_forward)

                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            # save data as a numpy file
            file_name = str(int(time.time()))
            directory = "training_images"
            if not os.path.exists(directory):
                os.makedirs(directory)
            try:
                np.savez('training_images/label_array_ORIGINALS_{}.npz'.format(file_name), train_labels=y)
            except IOError as e:
                print(e)

            end = cv2.getTickCount()
            # calculate streaming duration
            print("Streaming duration: , %.2fs" % ((end - start) / cv2.getTickFrequency()))



            with open('./logs/log_img_collect.txt', 'a') as f:
                f.write('Date: ' + time.strftime('%x') + '\n')
                f.write('Time: ' + time.strftime('%X') + '\n')
                f.write('Total frames: ' + str(total_frame) + '\n')
                f.write('Saved frames: ' + str(saved_frame) + '\n')
                f.write('Dropped frames: ' + str(total_frame - saved_frame) + '\n')
                f.write('Forward clicks: ' + str(clicks_forward) + '\n')
                f.write('Forward-left clicks: ' + str(clicks_forward_left) + '\n')
                f.write('Forward-right clicks: ' + str(clicks_forward_right) + '\n')
                f.write('-----------------------------\n')
            
            
            print ('Forward clicks: '), clicks_forward
            print ('Forward-left clicks: '), clicks_forward_left
            print ('Forward-right clicks: '), clicks_forward_right

            print ('Total frame:'), total_frame
            print ('Saved frame:'), saved_frame
            print ('Dropped frame'), total_frame - saved_frame

        finally:
            print( "销毁串流线程...")
            self.connection.close()
            self.server_socket.close()






class CommandTest(threading.Thread):
    def __init__(self,threadID, name):
        
        threading.Thread.__init__(self)
        #upd连接
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.threadID = threadID
        self.name = name
        self.thread_stop = False 
        self.send_inst = True
        print("通信线程初始化...")
        print("测试输出")
        self.server_socket.sendto(b"/0x52,0x53" ,(_host,_port))
        self.CMD = _CMD
        
    def run(self): #Overwrite run() method, put what you want the thread do here  
        if not self.thread_stop: 
            print("线程"+self.name+"开始运行")
            self.steer()

    def stop(self):  
            self.thread_stop = True  
            print("线程"+self.name+"结束")


    def steer(self):

        global KEY_CHANGE
        global LOCK
        while True:

            if KEY_CHANGE and LOCK:
                print("ser.send()")
                self.server_socket.sendto(_CMD ,(_host,_port))
                LOCK = False




if __name__ == '__main__':
    _size = 120*320
    Stream = VideoStreaming(1,"串流收集",_size)
    _socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    _socket.bind(("127.0.0.1",9870))
    #thread_Command = CommandTest(2, "通信")
    thread_Command = my_rc_driver_helper.RCControl(_host,_port)
    Stream.start()
    #thread_Command.start()
    while True:
        data,address = _socket.recvfrom(1)  
        CMD = data
        if CMD != None :
            _CMD = CMD
            KEY_CHANGE = True
            #print(_CMD)
        else:
            KEY_CHANGE = False

    _socket.close()



    


 
