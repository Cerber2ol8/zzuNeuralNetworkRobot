#coding utf-8
__authur__="ChongyangLiu"

import serial
import pygame
from pygame.locals import *
import io
import socket
import struct
import sys
from config import *
import PyServo

BUFSIZE = 1024
_BUFSIZE = 32

class MessageHanler(object):

	def __init__(self):
		self.servo = PyServo.Servo(SerialID, Baudrate)
		print(self.servo.ser.portstr) 
		self.send_inst = True
		self.transmitor()
	def transmitor(self):
		try:
			print ('Waiting for message ....')
			while True:  
				#udp               
				data= udp_socket.recv(BUFSIZE) 
				#tcp
				#buf= connection.read(BUFSIZE)
				
				#global data
				#if buf != None and len(data)<=126:
				#data+=buf
				if data!= None:
						
					if data== left:
						self.servo.RunGroup(Move_Left,1)
                                                print('left')

					elif data == right:
						self.servo.RunGroup(Move_Right,1)
                                                print('right')
					elif data== forward:
						self.servo.RunGroup(Move_Forward,1)
                                                print('forward')
					elif data == b'\x58':
						pass
						#self.ser.write(b'\x02')
				#self.ser.write(data)
				print(data)


		except Exception as e:
			print(e)
		finally:
			#udp
			udp_socket.close()  
			
			#tcp
			#connection.close()
			#tcp_socket.close()    
			


if __name__ == "__main__":
	try:
			
		print("Creating udp server...")
		#print("Creating tcp server...")
		
		#udp
		udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		udp_socket.bind((RasPi,cmd_port)) 
		
		
		#tcp
		#tcp_socket = socket.socket()
		#tcp_socket.bind(ADDR)
		#tcp_socket.listen(0)      
		#connection = tcp_socket.accept()[0].makefile('rb')
		
		
		msghelper=MessageHanler()
		
		   
	finally:
		
		udp_socket.close() 
		#tcp_socket.close()
