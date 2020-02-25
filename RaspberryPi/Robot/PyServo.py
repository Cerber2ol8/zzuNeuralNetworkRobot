#Coding-utf-8
#Serial Servo realization for Python
#author:LiuChongyang
#如果因为存在中文注释，导致树莓派报错，删去中文注释即可

#必要库
import serial
import time
import struct
#项目的设置文件，存储各种变量常量。根据需要自行替换
from config import *
#用到的config中的常量：以SERVO_ 开头的常量  main()中的 SerialID, Baudrate


#----------------位运算及校验和函数(校验和可能需要根据协议改写)--------------
def GET_LOW_BYTE(u16):
    #get low byte
    return u16&0xff

def GET_HIGH_BYTE(u16):
    #get height byte
    return 0xff&(u16>>8)

def BYTE_TO_HW(u8_A, u8_B):
    #combine low and height to uint16
    return (u8_A>>8)|(u8_B<<8)

def CheckSum(buf):
    #check sum
    temp = 0
    for byte in buf[2:buf[3]+2]:
        temp += byte
    #print('%#x'%temp)
    temp=~temp
    #print('%#x'%temp)
    #print('%#x'%GET_LOW_BYTE(temp))
    return GET_LOW_BYTE(temp)

class Servo(object):
    #用法： Servo(string:"串口设备号", int:波特率) 实例化一个舵机控制器
    #function:  SetID(self,oldID, newID) 设置舵机ID
    #           Move(self, time, id=None, position=None)  控制单个舵机运动
    #           RunGroup(self, numOfAction, times)  运行动作组，需要事先将
    #           动作组储存到舵机控制板，当然也可以通过多次调用Move()来自行
    #           实现
    #           ReadPosition(self,id = None)    读出舵机角度，需要协议支持
    #           MsgHandle(self)    消息处理函数，用于处理舵机返回的消息。可
    #           依据协议自行扩充相关功能 
    #           isLinsten(self)     检测是否在监听端口
    #           ServoLoad(self)     加载舵机动作(还没写)
    #           SetSpeed(self, numOfAction, speed)      舵机调速
    #           SendData(self, data)        串口消息发送函数

    def __init__(self, SerialID, Baudrate):
        self.ser = serial.Serial(SerialID, Baudrate, timeout=1)
        self.Group_complete = True
        self.LastAction = Move_Stop


    def SetID(self,oldID, newID):
        buf=[]
        #0~1 data frame header
        #SERVO_FRAME_HEADER需要自己定义
        #注：以SERVO_开头的常量都是舵机协议里规定的，需要查询协议
        buf.append(SERVO_FRAME_HEADER)
        buf.append(SERVO_FRAME_HEADER)

        buf.append(oldID)
        buf.append(4)
        buf.append(SERVO_ID_WRITE)
        buf.append(newID)
        buf.append(CheckSum(buf))
        self.SendData(buf)
        
    def Move(self, time, id=None, position=None):
        if type(id) == int:
            temp = id
            id = []
            id.append(temp)
        if type(position) == int:
            temp = position
            position = []
            position.append(temp)
        if len(id) != len(position):
            return
        for n in range(len(position)):
            if position[n]<0:
                position[n] = 0
            if position[n]>1000:
                position[n] = 1000


        #0x55 0x55   Length     Cmd
        buf=bytearray(b'\x55\x55')
        buf.append(len(id)*3+5)
        buf.append(SERVO_MOVE_TIME_WRITE)

        # Prm 1~Prm N
        buf.append(len(id)) 
        buf.append(GET_LOW_BYTE(time))
        buf.append(GET_HIGH_BYTE(time))

        for i in range(len(id)):
            buf.append(id[i])
            buf.append(GET_LOW_BYTE(position[i]))
            buf.append(GET_HIGH_BYTE(position[i]))
 
 
        #buf.append(CheckSum(buf))
        
        print(buf)
        self.SendData(buf)

    def RunGroup(self, numOfAction, times):
        if self.Group_complete:
            #0x55 0x55   Length     Cmd
            buf=bytearray(b'\x55\x55')
            buf.append(5)
            buf.append(SERVO_ACTION_GROUP_RUN)

            if numOfAction == Move_forward and self.LastAction == Move_forward:
                numOfAction == Move_forward1

            buf.append(numOfAction)
            buf.append(GET_LOW_BYTE(times))
            buf.append(GET_HIGH_BYTE(times))
            #buf.append(CheckSum(buf))
            if debug == False:
                self.SendData(buf)
            self.Group_complete = False
            self.MsgHandle()

    def ReadPosition(self,id = None):
        n = len(id)
        if n>0:
            buf=bytearray(b'\x55\x55')
            buf.append(n+3)
            buf.append(SERVO_MULT_SERVO_POS_READ)

            buf.append(n)
            for i in id:
               buf.append(i)

            if debug == False:
                self.SendData(buf)
            self.MsgHandle()
            return id
        else:
            return None
    def MsgHandle(self):
        count = 50000
        if debug:
            time.sleep(1.5)
            self.Group_complete = True
        data = ''
        while 1:
            while self.ser.inWaiting() > 0:
                data += self.ser.read(1)
            count-=1


            if data != '':
                #print(data)
                len = struct.unpack('B',data[2])[0]
                cmd = struct.unpack('B',data[3])[0]
                print(len)
                print(cmd)
                if cmd == SERVO_ACTION_GROUP_COMPLETE:  #8
                    numOfAction = struct.unpack('B',data[4])[0]
                    self.LastAction = numOfAction
                    print('Action group {} completed!'.format(numOfAction))
                    data = ''
                    self.Group_complete = True
                    break
                elif cmd == SERVO_ACTION_GROUP_STOP:
                    self.Group_complete = True
                    print('Action group stop!')
                    data = ''
                    break
                elif cmd == SERVO_ACTION_GROUP_STOP:
                    self.Group_complete = True
                    print('Action group stop!')
                    data = ''
                    break
                elif cmd == SERVO_MULT_SERVO_POS_READ:  #21
                    self.Group_complete = True
                    print('Get position:')
                    #return data[4:n]
                    data = ''
                    break
                else:
                    data = ''
                    self.MsgHandle()
            elif self.Group_complete == True:
                break

            if count < 0 :
                #break
                pass

        pass
    def isLinsten(self):
        #指令内容要看协议规定
        self.SendData(b'\x55\x55\x04\x15\x01\x01')
        count=0
        while 1:
            data = ''
            while self.ser.inWaiting() > 0:
              data += self.ser.read(1)
            if data != '':
                cmd = struct.unpack('B',data[3])[0]
                if cmd == SERVO_MULT_SERVO_POS_READ:
                    return True
            count+=1
            if count >50000:
                return False




    def ServoLoad(self):
        pass
    def SetSpeed(self, numOfAction, speed):
        #0x55 0x55   Length     Cmd
        buf=bytearray(b'\x55\x55')
        buf.append(5)
        buf.append(SERVO_ACTION_GROUP_SPEED)

        buf.append(numOfAction)
        buf.append(GET_LOW_BYTE(speed))
        buf.append(GET_HIGH_BYTE(speed))
        pass
    def SendData(self, data):
        if debug: 
            for d in data:
               print(d)
        else:
            self.ser.write(data)


if __name__ == '__main__':
    servo = Servo(SerialID, Baudrate)
    #servo.RunGroup(1,1)
    #servo.SetSpeed(0xff,200)
    print(servo.isLinsten())
    #servo.Move(1000,[1,2,3,4,5],[123,123,123,123,100])

    #servo.ser.write(b'\x55\x55\x05\x0b\xff\xc8\x00') 
    #time.sleep(0.5)
