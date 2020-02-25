import cv2
import tensorflow
from tensorflow import keras
import numpy as np
import os
import time
from config import *

timestr = time.strftime('%Y%m%d_%H%M%S')

class NeuralNetwork(object):


    global timestr

    def __init__(self,path, receiving=False  ):
        self.receiving = receiving
        self.model = keras.models.load_model(path)





    def auto_canny(self, blurred):
        # Compute the median of the single channel pixel intensities
        global SIGMA
        v = np.median(blurred)

        # Apply automatic Canny edge detection using the computed median of the image
        lower = int(max(0,   (1.0 - SIGMA) * v))
        upper = int(min(255, (1.0 + SIGMA) * v))
        edged = cv2.Canny(blurred, lower, upper)
        return edged


    def preprocess(self, frame):
        #image_array = frame.reshape(1, 38400).astype(np.float32)
        image_array=frame.reshape(roi[1]-roi[0], 320).astype(np.float32)
        image_array = np.array([image_array])
        image_array = image_array / 255.
        return image_array


    def predict(self, image):
        image_array = self.preprocess(image)
        #print("input shape")
        #print(self.model.input_shape)
        #print(image.shape)
        #print(image_array.shape)
        #exit()
        y_hat       = self.model.predict(image_array)
        i_max       = np.argmax(y_hat)
        y_hat_final = np.zeros((1,3))
        np.put(y_hat_final, i_max, 1)
        return y_hat_final[0], y_hat

