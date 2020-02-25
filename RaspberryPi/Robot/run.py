
import cv2
import numpy as np
import os 
import random
import time
from config import *
from config import model as model_num
import PyServo
 

count = 0
map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM,  cv2.CV_16SC2)
class RCDriverNNOnly(object):

    def __init__(self, model_path):
        print('initing...')


        # load trained neural network
        if model_num == 1:
            import model_b as model
            self.model = model
        elif model_num == 0:
            load_model_start = time.time()
            from model import NeuralNetwork
            self.model = NeuralNetwork(model_path)
            load_model_end = time.time()
            print('loading model costs {:02f} second(s)'.format(load_model_end - load_model_start))
        self.cap = cv2.VideoCapture(0)
        self.servo = PyServo.Servo(SerialID,Baudrate)

    def drive(self):

        step = 0
        try:
            while True:
                ret, img = self.cap.read()
                if ret:
                    #print(img.shape)
                    img = cv2.resize(img,(320,240),interpolation=cv2.INTER_CUBIC)
                    #img = cv2.remap(img,map1,map2, interpolation= cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
                    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    
                    
                    height, width = gray.shape
                    roi_img = gray[roi[0]:roi[1], :]

                    # Apply GuassianBlur (reduces noise)
                    blurred = cv2.GaussianBlur(roi_img, (3, 3), 0)

                    # Apply Canny filter
                    auto = self.model.auto_canny(blurred)       
                    #print(auto.shape)
                    global count

                    if self.servo.isLinsten():
                        if timer:
                            timer_prediction = time.time()

                        prediction_english = None
                        prediction_english_proba = None      
                        # neural network makes prediction
                        print("predicting...")
                        prediction, lines = self.model.predict(auto)
                        if timer:
                            print('prediction takes:{} seconds'.format(time.time()-timer_prediction))
                            timer_action = time.time()
                        #proba_left, proba_right, proba_forward = probas[0]
                        if np.all(prediction   == [ 0., 0., 1.]):
                            prediction_english = 'FORWARD'
                            self.servo.RunGroup(Move_Forward,1)

                        elif np.all(prediction == [ 1., 0., 0.]):
                            prediction_english = 'LEFT'
                            self.servo.RunGroup(Move_Left,1)

                        elif np.all(prediction == [ 0., 1., 0.]):
                            prediction_english = 'RIGHT'
                            self.servo.RunGroup(Move_Right,1)

                        print(prediction_english)
                        if write_temp_file:
                            if model_num ==1:
                                #auto = self.model.visualize_lines(cv2.cvtColor(roi_img,cv2.COLOR_GRAY2BGR),lines)
                                pass
                            cv2.putText(auto, "Prediction: {}".format(prediction_english,
                                                                                ), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, .45, (255, 255, 0), 1)

                                
                            step += 1
                            cv2.imwrite('./test_images/step{}.jpg'.format(step), auto)
                            print('writing images of step{}'.format(step))
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

        except Exception as e:
            print(e)
        finally:
            print('total {} frames predicted'.format(step))

       
def test(file_name):
        
        jpg = file_name
        gray = cv2.imread(jpg, cv2.IMREAD_GRAYSCALE)
        image = cv2.imread(jpg, cv2.IMREAD_COLOR)
        # lower half of the image
        height, width = gray.shape
        roi_img = gray[roi[0]:roi[1], :]

        # Apply GuassianBlur (reduces noise)
        blurred = cv2.GaussianBlur(roi_img, (3, 3), 0)

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
        cv2.putText(auto, "Prediction (sig={}): {}, {:>05}".format(SIGMA, 
                                                                    prediction_english, 
                                                                    prediction_english_proba), 
                                                                    (10, 60),
                                                                    cv2.FONT_HERSHEY_SIMPLEX,.45, (255, 255, 255), 1)
        
        cv2.imshow('What the model sees', auto)
        cv2.imshow('result', gray)
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
    test('./test_images/'+file_names[x])
if __name__ == '__main__':


    # model path
    path = model_path
    

    if test_mode:
        import win_unicode_console
        win_unicode_console.enable()
        nn = NeuralNetwork(model_path)
        file_names = []
        for parent, dirnames, filenames in os.walk(training_path):    
                file_names = filenames
        refresh()
                    
    else:
        rc = RCDriverNNOnly(path)
        rc.drive()


