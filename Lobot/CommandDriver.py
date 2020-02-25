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
BUFSIZE = 1
_BUFSIZE = 32
ADDR = (HOST,PORT)
data= b''
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
				#data= udp_socket.recv(BUFSIZE) 
				buf= connection.read(BUFSIZE)
				global data
				if buf != None and len(data)<=126:
					data+=buf
					
				if data[0]== b'\x56':
					self.ser.write(data)
					print('left')
				elif data[0] == b'\x57':
					self.ser.write(data)
					print('right')
				elif data[0]== b'\x55':
					self.ser.write(data)
					print('forward')
				

					self.ser.flush()
					data = b''

		except Exception as e:
			print(e)
		finally:
			#udp_socket.close()  
			connection.close()
			tcp_socket.close()    
			self.ser.close()
    


if __name__ == "__main__":
	try:
			
		#print("Creating udp server...")
		print("Creating tcp server...")
		#udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		tcp_socket = socket.socket()
		
		#udp_socket.bind(ADDR) 
		tcp_socket.bind(ADDR)
		tcp_socket.listen(0)      
		connection = tcp_socket.accept()[0].makefile('rb')
		msghelper=MessageHanler()
		
		   
	finally:
		
		#udp_socket.close() 
		tcp_socket.close()
