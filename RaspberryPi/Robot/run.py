
import cv2
import numpy as np

import os 
import random

from model import NeuralNetwork
import time
from config import *
import PyServo


count = 0
SIGMA = 0.33
class RCDriverNNOnly(object):

    def __init__(self, model_path):



        # load trained neural network
        self.nn = NeuralNetwork(model_path)
        self.cap = cv2.VideoCapture(0)
        self.servo = PyServo.Servo(SerialID,Baudrate)

    def drive(self):

        frame = 0
        try:
            # stream video frames one by one
            while True:
                ret, img = self.cap.read()
                if ret:
                    
                    img = cv2.resize(img,(320,240),interpolation=cv2.INTER_CUBIC)
                    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    
                    
                    height, width = gray.shape
                    roi = gray[int(height/2):height, :]

                    # Apply GuassianBlur (reduces noise)
                    blurred = cv2.GaussianBlur(roi, (3, 3), 0)

                    # Apply Canny filter
                    auto = self.nn.auto_canny(blurred)       
                    global count

                    if self.servo.isLinsten():
                        if timer:
                            timer_prediction = time.time()

                        prediction_english = None
                        prediction_english_proba = None      
                        # neural network makes prediction
                        prediction, probas = self.nn.predict(auto)
                        if timer:
                            print('prediction takes:{} seconds'.format(time.time()-timer_prediction))
                            timer_action = time.time()
                        proba_left, proba_right, proba_forward = probas[0]
                        if np.all(prediction   == [ 0., 0., 1.]):
                            prediction_english = 'FORWARD'
                            self.servo.RunGroup(1,1)

                        elif np.all(prediction == [ 1., 0., 0.]):
                            prediction_english = 'LEFT'
                            self.servo.RunGroup(2,1)

                        elif np.all(prediction == [ 0., 1., 0.]):
                            prediction_english = 'RIGHT'
                            self.servo.RunGroup(3,1)

                        print(prediction_english)
                        if timer:
                            print('Action takes:{} seconds'.format(time.time()-timer_action))
                        print(count)
                        count = 0
                    else:
                        while True:
                            if self.servo.isLinsten():
                                self.servo.Group_complete = True
                                break



                            
                        count+=1


        finally:
            print('total {} frames predicted'.format(int(frame*0.1)))

       
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


    # model path
    path = model_path
    

    if test_mode:
        file_names = []
        for parent, dirnames, filenames in os.walk(training_path):    
            file_names = filenames
 
        refresh()
                    
    else:
        rc = RCDriverNNOnly(path)
        rc.drive()


