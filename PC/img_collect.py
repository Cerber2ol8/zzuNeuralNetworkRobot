'''
This module does the following:
  1. Collects original images of what the car sees each time a direction is inputted by the driver. Images saved to 'training_images'.
  2. Collects direction inputs as an array, each new one being vstacked below the previous. Compiles to npz file at the end.
'''

import car
import cv2
import glob
import numpy as np
import serial
import pygame
from pygame.locals import *
import socket
import time


class ImageCollect(object):

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('192.168.1.4', 8000)) # The IP address of computer . This script should run before the one on the Pi.
        print ('Listening...')
        self.server_socket.listen(0)

        # Accept a single connection ('rb' is 'read binary')
        self.connection = self.server_socket.accept()[0].makefile('rb')

        # Establish a condition that RaspPi should be sending images.
        self.send_inst = True

        # Create labels (aka the Y values; these will be the directional output to the arduino remote control)
        # Creates a 4x4 matrix, with 1's along the diagonal, upper left to bottom right:
        # array([[ 1.,  0.,  0.,  0.],
        #        [ 0.,  1.,  0.,  0.],
        #        [ 0.,  0.,  1.,  0.],
        #        [ 0.,  0.,  0.,  1.]])
        self.k = np.zeros((3, 3), 'float')
        for i in range(3):
            self.k[i, i] = 1
        self.temp_label = np.zeros((1, 3), 'float')

        pygame.init()
        self.collect_images()


    def collect_images(self):

        saved_frame = 0
        total_frame = 0

        clicks_forward       = 0
        clicks_forward_left  = 0
        clicks_forward_right = 0

        print ('Start collecting images...')

        label_array = np.zeros((1, 3), 'float')

        # Stream video frames one by one.
        try:
            stream_bytes = ' '
            frame = 0
            while self.send_inst:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find('\xff\xd8')           # ? What is this string and where did it come from?
                last = stream_bytes.find('\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]

                    # 'image' (original, in grayscale)
                    image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)

                    # Overlay click counts: cv2.putText(clicks_*)
                    clicks_total = clicks_forward + clicks_forward_left + clicks_forward_right
                    cv2.putText(image, "FW: {}, LT: {}, RT: {}, TOTAL: {}".format(clicks_forward, clicks_forward_left, clicks_forward_right, clicks_total), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, .45, (255, 255, 0), 1)

                    # Display feeds on host (laptop)
                    cv2.imshow('image', image)

                    # Get input from human driver
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:                              
                            key_input = pygame.key.get_pressed()

                            # FORWARD
                            if key_input[pygame.K_UP]:
                                # save streamed images
                                cv2.imwrite('training_images/frame{:>05}.jpg'.format(frame), image)
                                label_array = np.vstack((label_array, self.k[2]))   # self.k[2] = [ 0.,  0.,  1.]
                                car.forward(200)
                                clicks_forward += 1
                                frame += 1
                                total_frame += 1
                                saved_frame += 1

                            # FORWARD_RIGHT
                            elif key_input[pygame.K_RIGHT]:
                                # save streamed images
                                cv2.imwrite('training_images/frame{:>05}.jpg'.format(frame), image)
                                label_array = np.vstack((label_array, self.k[1]))   # self.k[1] = [ 0.,  1.,  0.]
                                car.right(300)
                                car.forward_right(300)
                                car.right(700)
                                clicks_forward_right += 1
                                frame += 1
                                total_frame += 1
                                saved_frame += 1

                            # FORWARD_LEFT
                            elif key_input[pygame.K_LEFT]:
                                # save streamed images
                                cv2.imwrite('training_images/frame{:>05}.jpg'.format(frame), image)
                                label_array = np.vstack((label_array, self.k[0]))   # self.k[0] = [ 1.,  0.,  0.]
                                car.left(300)
                                car.forward_left(300)
                                car.left(700)
                                clicks_forward_left += 1
                                frame += 1
                                total_frame += 1
                                saved_frame += 1

                            # REVERSE; not saving images for this
                            elif key_input[pygame.K_DOWN]:
                                car.reverse(200)

                            elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                                print ('EXIT')
                                self.send_inst = False
                                break

                        elif event.type == pygame.KEYUP:                            #'''Key is lifted UP?'''
                            break

            train_labels = label_array[1:, :]
            np.savez('training_images/label_array_ORIGINALS.npz', train_labels=train_labels)

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
            self.connection.close()
            self.server_socket.close
            print ('Connection closed')
            print ('Socket closed')

if __name__ == '__main__':
    ImageCollect()
