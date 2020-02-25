import serial
import pygame
from pygame.locals import *
from config import *
import PyServo

class ServoTest(object):

    def __init__(self):
        pygame.init()
        pygame.display.set_mode((250, 250))
        self.servo = PyServo.Servo(SerialID, Baudrate)
        print(self.servo.ser.portstr)
        self.send_inst = True
        self.speed = speed
        self.servo.RunGroup(Stand_Up,1)
        self.steer()
		
    def steer(self):


        while self.send_inst:

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    key_input = pygame.key.get_pressed()


                    if key_input[pygame.K_UP]:
                        print("Forward")
                        self.servo.RunGroup(Move_Forward,1)

                    elif key_input[pygame.K_DOWN]:
                        print("Reverse")


                    elif key_input[pygame.K_RIGHT]:
                        print("Right")
                        self.servo.RunGroup(Move_Right,1)

                    elif key_input[pygame.K_LEFT]:
                        print("Left")
                        self.servo.RunGroup(Move_Left,1)
                    elif key_input[pygame.K_KP_PLUS]:
                        self.speed += 10
                        self.servo.SetSpeed(0xFF,self.speed)
                        print("Set Speed at".format(self.speed))
                        print(self.speed)
                    elif key_input[pygame.K_KP_MINUS]:
                        self.speed -= 10
                        self.servo.SetSpeed(0xFF,self.speed)
                        print("Set Speed at".format(self.speed))
                        print(self.speed)
                    # exit
                    elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                        print("Exit")
                        self.send_inst = False
                        break

                elif event.type == pygame.KEYUP:
                    pass


if __name__ == '__main__':
    ServoTest()
