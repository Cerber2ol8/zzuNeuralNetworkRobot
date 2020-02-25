import pygame
from pygame.locals import *
import socket
from config import *


class ReadKey():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        pygame.init()
        pygame.display.set_mode((250, 250))
        self.socket.connect((RasPi,cmd_port))
        self.start()

    def start(self):
            while True:
                for event in pygame.event.get():
                    #print(event)
                    if event.type == KEYDOWN:
                        print("event.type")
                        key_input = pygame.key.get_pressed()
                        if key_input[pygame.K_UP]:
                            print("Forward")
                            self.socket.sendall(forward)
                        elif key_input[pygame.K_DOWN]:
                            print("Reverse")
                            self.socket.sendall(stop)
                        elif key_input[pygame.K_RIGHT]:
                            print("Right")
                            self.socket.sendall(right)
                        elif key_input[pygame.K_LEFT]:
                            print("Left")
                            self.socket.sendall(left)
                          # exit
                        elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                            print("Exit")
                            self.socket.sendall(stop)
                            exit()


if __name__ == '__main__':
    ReadKey()
