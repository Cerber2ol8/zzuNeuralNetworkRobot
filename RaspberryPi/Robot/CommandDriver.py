#coding utf-8
__authur__="ChongyangLiu"

import serial
import pygame
from pygame.locals import *
import io
import socket
import struct
import sys
HOST = '192.168.1.12' 
PORT = 8001
BUFSIZE = 1024
ADDR = (HOST,PORT)
class MessageHanler(object):

	def __init__(self):

		#self.ser = serial.Serial("/dev/tty.usbmodem1421", 115200, timeout=1)    # mac
		self.ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)           # linux
		print(self.ser.portstr) 
		self.send_inst = True
		self.transmitor()
	def transmitor(self):
		try:
			print ('Waiting for message ....')
			while True:                 
				data= udp_socket.recv(BUFSIZE) 
				if data != None :
					print(str(data))
					self.ser.write(data)
					self.ser.flush()

		
		finally:
			udp_socket.close()        
			udp_socket.close()       


if __name__ == "__main__":
	print("Creating udp server...")
	udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	udp_socket.bind(ADDR)       
	MessageHanler()
	
 
