
import cv2
import numpy as np
import socket
import os 
import random

from model import NeuralNetwork
from my_rc_driver_helper import RCControl

count=0
SIGMA = 0.33
class RCDriverNNOnly(object):

    def __init__(self, host, port,_host, _port, model_path):
        #tcp host port
        #udp _host _port
        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
        self.server_socket.listen(0)

        # accept a single connection
        self.connection = self.server_socket.accept()[0].makefile('rb')

        # load trained neural network
        self.nn = NeuralNetwork(model_path)


        self.rc_car = RCControl(_h,_p)

    def drive(self):
        stream_bytes = b' '
        frame = 0
        try:
            # stream video frames one by one
            while True:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')

                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    gray = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                    # lower half of the image
                    height, width = gray.shape
                    roi = gray[int(height/2):height, :]

                    # Apply GuassianBlur (reduces noise)
                    blurred = cv2.GaussianBlur(roi, (3, 3), 0)

                    # Apply Canny filter
                    auto = self.nn.auto_canny(blurred)       
                    
                    cv2.imshow('image', image)
                    cv2.imshow('What the model sees', auto)
                    # cv2.imshow('mlp_image', roi)
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                  

                    # Neural network model makes prediciton
                    # prediction = self.model.predict(auto)

                    # reshape image
                    #image_array = roi.reshape(1, int(height/2) * width).astype(np.float32)
                    prediction_english = None
                    prediction_english_proba = None      
                    
                    
                    # neural network makes prediction
                    prediction, probas = self.nn.predict(auto)
                    proba_left, proba_right, proba_forward = probas[0]
                    if np.all(prediction   == [ 0., 0., 1.]):
                        prediction_english = 'FORWARD'
                        prediction_english_proba = proba_forward

                    elif np.all(prediction == [ 1., 0., 0.]):
                        prediction_english = 'LEFT'
                        prediction_english_proba = proba_left

                    elif np.all(prediction == [ 0., 1., 0.]):
                        prediction_english = 'RIGHT'
                        prediction_english_proba = proba_right
                    global count
                    frame += 1
                    cv2.putText(gray, "Prediction (sig={}): {}, {:>05}".format(SIGMA, 
                                                                               prediction_english, 
                                                                               prediction_english_proba), 
                                                                                (10, 30),
                                                                               cv2.FONT_HERSHEY_SIMPLEX, .45, (255, 255, 0), 1)
                    if write_temp_file:
                        cv2.imwrite('test_frames_temp/frame{:>05}.jpg'.format(frame), gray)
                    


                    if count>=10:
                        self.rc_car.steer(prediction)
                        count=0
                    else:
                        count+=1

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("car stopped")
                        self.rc_car.stop()
                        break



        finally:
            cv2.destroyAllWindows()
            self.connection.close()
            self.server_socket.close()

       
def test(file_name):
        
        jpg = file_name
        gray = cv2.imread(jpg, cv2.IMREAD_GRAYSCALE)
        image = cv2.imread(jpg, cv2.IMREAD_COLOR)
        # lower half of the image
        height, width = gray.shape
        roi = gray[int(height/2):height, :]

        # Apply GuassianBlur (reduces noise)
        blurred = cv2.GaussianBlur(roi, (3, 3), 0)

        # Apply Canny filter
        auto = nn.auto_canny(blurred)       
                    

        # cv2.imshow('mlp_image', roi)
        _image = cv2.imread(jpg, cv2.IMREAD_GRAYSCALE)
        
        # Neural network model makes prediciton
        # prediction = model.predict(auto)

        prediction_english = None
        prediction_english_proba = None      
            
        # neural network makes prediction
        prediction, probas = nn.predict(auto)
        proba_left, proba_right, proba_forward = probas[0]
        if np.all(prediction   == [ 0., 0., 1.]):
            prediction_english = 'FORWARD'
            prediction_english_proba = proba_forward

        elif np.all(prediction == [ 1., 0., 0.]):
            prediction_english = 'LEFT'
            prediction_english_proba = proba_left

        elif np.all(prediction == [ 0., 1., 0.]):
            prediction_english = 'RIGHT'
            prediction_english_proba = proba_right

        cv2.putText(gray, "Prediction (sig={}): {}, {:>05}".format(SIGMA, 
                                                                    prediction_english, 
                                                                    prediction_english_proba), 
                                                                    (10, 60),
                                                                    cv2.FONT_HERSHEY_SIMPLEX,.45, (255, 255, 255), 1)
        
        cv2.imwrite('test_frames_temp/temp.jpg', gray)
        cv2.imshow('image', image)
        cv2.imshow('What the model sees', auto)
        test = cv2.imread('test_frames_temp/temp.jpg')
        cv2.imshow('result', test)
        key = cv2.waitKey(0)
        if key==27:
            cv2.destroyAllWindows()  #wait for ESC key to exit
            exit()
        elif key==ord('r'):
            cv2.destroyAllWindows()
            refresh()

def refresh():
    x = random.randint(0, len(file_names)-1)
    print(file_names[x])
    test('./training_images/'+file_names[x])
if __name__ == '__main__':

    #test model
    test_mode = True
    write_temp_file = False
    # model path
    path = model_path
    nn = NeuralNetwork(path)
    

    if test_mode:
        file_names = []
        for parent, dirnames, filenames in os.walk('./training_images'):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            file_names = filenames
 
        refresh()
                    
    else:
        # host, port
        h, p = PC, streaming_port
        _h, _p = RasPi,cmd_port
        rc = RCDriverNNOnly(h, p, _h, _p, path)
        rc.drive()


