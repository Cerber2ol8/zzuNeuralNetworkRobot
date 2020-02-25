#原作者 ：zhengwang
#在原作基础，改成使用多线程socket，同时使用串流和通信
import numpy as np
import cv2
import socket
import threading
import time


host, port = "192.168.1.4", 8000
_host,_port = "192.168.1.12",8001
exitFlag = 0

global KEY_CHANGE
KEY_CHANGE= False
global _CMD
_CMD=chr(51).encode()








class VideoStreamingTest(threading.Thread):
    def __init__(self,threadID, name):
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

        
    def run(self): #Overwrite run() method, put what you want the thread do here  
        if not self.thread_stop: 
            print("线程"+self.name+"开始运行")
            self.streaming()

    def stop(self):  
            self.thread_stop = True  
            print("线程"+self.name+"结束")
    def streaming(self):

        try:
            print("Host: ", self.host_name + ' ' + self.host_ip)
            print("Connection from: ", self.client_address)
            print("Streaming...")
            print("Press 'q' to exit")

            # need bytes here
            stream_bytes = b' '
            while True:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    cv2.imshow('image', image)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
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
            

    def stop(self):  
            self.thread_stop = True  
            print("线程"+self.name+"结束")


    def steer(self,CMD):

        global KEY_CHANGE
        if KEY_CHANGE:
            self.server_socket.sendto(CMD ,(_host,_port))
            KEY_CHANGE = False






if __name__ == '__main__':

 
    # 创建多个线程
    print("正在创建线程...")
    thread_Streaming = VideoStreamingTest(1, "串流") 

    #thread_readkey = Readkey(3,"按键")

    thread_Streaming.start()

    #thread_readkey.start()

    _socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    _socket.bind(("127.0.0.1",9870))
    thread_Command = CommandTest(2, "通信")
    thread_Command.start()
    
    print("按键检测初始化完毕")
    while True:
        data,address = _socket.recvfrom(1)  
        CMD = data
        if CMD != None :
            KEY_CHANGE = True
            thread_Command.steer(CMD)
            print(CMD)
        else:
            KEY_CHANGE = False
    

    _socket.close()



    


 
