import pygame
from pygame.locals import *
import socket





if __name__ == "__main__":

    _socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    pygame.init()
    pygame.display.set_mode((250, 250))

    _socket.connect(("127.0.0.1",9870))


    while True:
            for event in pygame.event.get():
                #print(event)
                if event.type == KEYDOWN:
                    print("event.type")
                    key_input = pygame.key.get_pressed()
                    
                    # complex orders
                    if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                        print("Forward Right")
                        _socket.sendall(chr(6).encode())
                    elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                        print("Forward Left")
                        _socket.sendall(chr(7).encode())
                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                        print("Reverse Right")
                        _socket.sendall(chr(8).encode())
                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                        print("Reverse Left")
                        _socket.sendall(chr(9).encode())
                    # simple orders
                    elif key_input[pygame.K_UP]:
                        print("Forward")
                        _socket.sendall(chr(1).encode())
                    elif key_input[pygame.K_DOWN]:
                        print("Reverse")
                        _socket.sendall(chr(2).encode())
                    elif key_input[pygame.K_RIGHT]:
                        print("Right")
                        _socket.sendall(chr(3).encode())

                    elif key_input[pygame.K_LEFT]:
                        print("Left")
                        _socket.sendall(chr(4).encode())
                    # exit
                    elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                        print("Exit")
                        _socket.sendall(chr(0).encode())
                        exit()
    
