__author__ = 'LiuChongyang'
#The python interpreter on Raspian Does support Chinese
#The annotation must be English
#Errors will happend if Chinese characters appear


#*********  Test model Config   *********#
test_mode = False
write_temp_file = False
debug = False
timer = True
exitFlag = 0

#*********  Serial Command Config    *********#
SERVO_FRAME_HEADER=           0x55
SERVO_MOVE_TIME_WRITE=        3
SERVO_ACTION_GROUP_RUN=       6
SERVO_ACTION_GROUP_STOP=      7
SERVO_ACTION_GROUP_COMPLETE=  8
SERVO_ACTION_GROUP_SPEED=     11
SERVO_GET_BATTERY_VOLTAGE=    16
SERVO_MULT_SERVO_UNLOA=       20
SERVO_MULT_SERVO_POS_READ=    21


SERVO_MOVE_TIME_READ=         2
SERVO_MOVE_STOP=              12
SERVO_ID_WRITE=               13
SERVO_ID_READ=                14
SERVO_ANGLE_OFFSET_ADJUST=    17
SERVO_ANGLE_OFFSET_WRITE=     18
SERVO_ANGLE_OFFSET_READ=      19
SERVO_VIN_LIMIT_WRITE=        22
SERVO_VIN_LIMIT_READ=         23
SERVO_TEMP_MAX_LIMIT_WRITE=   24
SERVO_TEMP_MAX_LIMIT_READ=    25
SERVO_TEMP_READ=              26
SERVO_VIN_READ=               27
SERVO_POS_READ=               28
SERVO_OR_MOTOR_MODE_WRITE=    29
SERVO_OR_MOTOR_MODE_READ=     30
SERVO_LOAD_OR_UNLOAD_WRITE=   31
SERVO_LOAD_OR_UNLOAD_READ=    32
SERVO_LED_CTRL_WRITE=         33
SERVO_LED_CTRL_READ=          34
SERVO_LED_ERROR_WRITE=        35
SERVO_LED_ERROR_READ=         36
#*********  Network Config    *********#

RasPi = '192.168.43.219' 
PC = '192.168.43.156'


localhost = '127.0.0.1'
streaming_port = 8000
cmd_port = 8001
key_port = 9870

#*********  Serial Config   *********#

#serial_mac = "/dev/tty.usbmodem1421"  # mac

SerialID = "/dev/ttyAMA0"	  # linux
Baudrate = 9600

#*********  Robot Serial command Config *********#
#Forward = b'\x01'
#Left = b'\x02'
#Right = b'\x03'


#*********  Remote command Config *********#
forward = b'\x55'
left = b'\x56'
right = b'\x57'
stop =  b'\x58'
#*********  Key Config *********#
KEY_DOWN = chr(2).encode()
KEY_UP = chr(1).encode()
KEY_LEFT = chr(4).encode()
KEY_RIGHT = chr(3).encode()


#*********  Streaming/Video Config    *********#
size = (320, 240)
framerate = 30


#*********  Path Config    *********#
training_path = "training_images"
model_path = "nn_h5/nn_20190504_182950.h5"

#*********  Action  Config    *********#
Move_Stop = 0
Move_Start = 1
Move_Forward = 2
Move_Forward1 = 3
Move_Left = 4
Move_Right = 5
Move_Reverse = 9
Move_etc = 99





