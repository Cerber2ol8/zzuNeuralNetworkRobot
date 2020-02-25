#!/bin/bash


for ((i=1;i<=100;i++))
	do 
	sudo raspistill  -t 0.1 -w 480 -h 360 -o /home/pi/ram/mjpg/i.jpg -n -q 30
	done


