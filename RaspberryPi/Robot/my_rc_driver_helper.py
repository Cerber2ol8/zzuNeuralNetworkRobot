import cv2
import math
import socket
import numpy as np
class RCControl(object):

    def __init__(self,_host,_port):
        #udp
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        #tcp
        #self.socket = socket.socket()
        

        print(b"/0x52,0x53")
        self.host = _host
        self.port = _port

        #self.socket.connect((_host,_port))
        #self.connection = self.socket.makefile('wb') 
        #self.connection.write(b"\x52,\x53")
        #self.connection.close()


        self.socket.sendto(b"\x52,\x53",(_host,_port))

    def steer(self, prediction):
        if (prediction == [ 0., 0., 1.]).all() :


            #self.socket.sendto(chr(1).encode(),(self.host,self.port))
            self.socket.sendto(b'\x55',(self.host,self.port))


            #self.connection = self.socket.makefile('wb')
            #self.connection.write(b'\x55')
            #self.connection.close()
            print("Forward")
        elif (prediction  == [ 1., 0., 0.]).all():

            #self.socket.sendto(chr(7).encode(),(self.host,self.port))
            self.socket.sendto(b'\x56',(self.host,self.port))
            

            #self.connection = self.socket.makefile('wb')
            #self.connection.write(b"\x56")
            #self.connection.close()

            print("Left")
        elif (prediction == [ 0., 1., 0.]).all():

            #self.socket.sendto(chr(6).encode(),(self.host,self.port))
            self.socket.sendto(b'\x57',(self.host,self.port))
            

            #self.connection = self.socket.makefile('wb')
            #self.connection.write(b"\x57")
            #self.connection.close()
            
            print("Right")
        else:
            self.stop()

    def stop(self):
        #udp
        self.socket.sendto(chr(0).encode(),(self.host,self.port))
        #tcp
        #self.connection.close()
        self.socket.close()
class RCControl_test(object):

    def __init__(self,_host,_port):
        #udp
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        #tcp
        #self.socket = socket.socket()

        print(b"/0x52,0x53")
        self.host = _host
        self.port = _port

        #self.socket.connect((_host,_port))
        #self.connection = self.socket.makefile('wb') 
        #self.connection.write(b"\x52,\x53")
        #self.connection.close()


        self.socket.sendto(b"\x52,\x53",(_host,_port))

    def steer(self, prediction):
        if (prediction == chr(1).encode()):
            self.socket.sendto(b'\x55',(self.host,self.port))
            print("Forward")
        elif (prediction  == chr(4).encode()):

            #self.socket.sendto(chr(7).encode(),(self.host,self.port))
            self.socket.sendto(b'\x56',(self.host,self.port))

            #self.connection = self.socket.makefile('wb')
            #self.connection.write(b"\x56")
            #self.connection.close()

            print("Left")
        elif (prediction == chr(3).encode()):

            #self.socket.sendto(chr(6).encode(),(self.host,self.port))
            self.socket.sendto(b'\x57',(self.host,self.port))
            

            #self.connection = self.socket.makefile('wb')
            #self.connection.write(b"\x57")
            #self.connection.close()
            
            print("Right")
        elif (prediction == chr(2).encode()):

            self.socket.sendto(b'\x58',(self.host,self.port))
            

        else:
            self.stop()

    def stop(self):
        #udp
        self.socket.sendto(chr(0).encode(),(self.host,self.port))
        #tcp
        #self.connection.close()
        self.socket.close()
class DistanceToCamera(object):

    def __init__(self):
        # camera params
        self.alpha = 8.0 * math.pi / 180    # degree measured manually
        self.v0 = 119.865631204             # from camera matrix
        self.ay = 332.262498472             # from camera matrix

    def calculate(self, v, h, x_shift, image):
        # compute and return the distance from the target point to the camera
        d = h / math.tan(self.alpha + math.atan((v - self.v0) / self.ay))
        if d > 0:
            cv2.putText(image, "%.1fcm" % d,
                        (image.shape[1] - x_shift, image.shape[0] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        return d


class ObjectDetection(object):

    def __init__(self):
        self.red_light = False
        self.green_light = False
        self.yellow_light = False

    def detect(self, cascade_classifier, gray_image, image):

        # y camera coordinate of the target point 'P'
        v = 0

        # minimum value to proceed traffic light state validation
        threshold = 150

        # detection
        cascade_obj = cascade_classifier.detectMultiScale(
            gray_image,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30))

        # draw a rectangle around the objects
        for (x_pos, y_pos, width, height) in cascade_obj:
            cv2.rectangle(image, (x_pos + 5, y_pos + 5), (x_pos + width - 5, y_pos + height - 5), (255, 255, 255), 2)
            v = y_pos + height - 5
            # print(x_pos+5, y_pos+5, x_pos+width-5, y_pos+height-5, width, height)

            # stop sign
            if width / height == 1:
                cv2.putText(image, 'STOP', (x_pos, y_pos - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # traffic lights
            else:
                roi = gray_image[y_pos + 10:y_pos + height - 10, x_pos + 10:x_pos + width - 10]
                mask = cv2.GaussianBlur(roi, (25, 25), 0)
                (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask)

                # check if light is on
                if maxVal - minVal > threshold:
                    cv2.circle(roi, maxLoc, 5, (255, 0, 0), 2)

                    # Red light
                    if 1.0 / 8 * (height - 30) < maxLoc[1] < 4.0 / 8 * (height - 30):
                        cv2.putText(image, 'Red', (x_pos + 5, y_pos - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                        self.red_light = True

                    # Green light
                    elif 5.5 / 8 * (height - 30) < maxLoc[1] < height - 30:
                        cv2.putText(image, 'Green', (x_pos + 5, y_pos - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),2)
                        self.green_light = True

                    # yellow light
                    # elif 4.0/8*(height-30) < maxLoc[1] < 5.5/8*(height-30):
                    #    cv2.putText(image, 'Yellow', (x_pos+5, y_pos - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                    #    self.yellow_light = True
        return v
