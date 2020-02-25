
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


        # load trained neural network
        self.nn = NeuralNetwork(model_path)
        self.cap = cv2.VideoCapture(0)
        
        self.rc_car = RCControl(_h,_p)

    def drive(self):
        stream_bytes = b' '
        frame = 0
        try:
            # stream video frames one by one
            while True:
                ret, frame = self.cap.read()
                if ret:
                    
                    frame = cv2.resize(frame,(320,240),interpolation=cv2.INTER_CUBIC)
                    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                    image = frame
                    
                    height, width = gray.shape
                    roi = gray[int(height/2):height, :]

                    # Apply GuassianBlur (reduces noise)
                    blurred = cv2.GaussianBlur(roi, (3, 3), 0)

                    # Apply Canny filter
                    auto = self.nn.auto_canny(blurred)       
                    
                    cv2.imshow('image', image)
                    cv2.imshow('What the model sees', auto)
                    # cv2.imshow('mlp_image', roi)
                    
                  

                    # Neural network model makes prediciton
                    # prediction = self.model.predict(auto)

                    # reshape image
                    #image_array = roi.reshape(1, int(height/2) * width).astype(np.float32)

                    global count
                    frame += 1

       

                    if count>=5:
                        
                        
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
                            count=0
                            
                        self.rc_car.steer(prediction)
                    else:
                        count+=1

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("car stopped")
                        self.rc_car.stop()
                        break



        finally:
            cv2.destroyAllWindows()


       
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
    test_mode = False
    write_temp_file = False
    # model path
    path = "nn_h5/nn_20190504_182950.h5"
    nn = NeuralNetwork(path)
    

    if test_mode:
        file_names = []
        for parent, dirnames, filenames in os.walk('./training_images'):    
            file_names = filenames
 
        refresh()
                    
    else:
        # host, port
        h, p = "192.168.1.4", 8000
        _h, _p = "192.168.1.12",8001
        rc = RCDriverNNOnly(h, p, _h, _p, path)
        rc.drive()


