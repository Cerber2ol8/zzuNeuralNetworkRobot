/*******************************************************************************
* 文件名： SerialServo.c
* 作者： lcy
* 日期：20190724
* LX串口舵机C语言API接口
*******************************************************************************/

typedef unsigned char uint8_t;
typedef unsigned int uint16_t;
typedef	int int16_t;
#define LOBOT_SERVO_FRAME_HEADER         0x55
#define LOBOT_SERVO_MOVE_TIME_WRITE      1
#define LOBOT_SERVO_MOVE_TIME_READ       2
#define LOBOT_SERVO_MOVE_TIME_WAIT_WRITE 7
#define LOBOT_SERVO_MOVE_TIME_WAIT_READ  8
#define LOBOT_SERVO_MOVE_START           11
#define LOBOT_SERVO_MOVE_STOP            12
#define LOBOT_SERVO_ID_WRITE             13
#define LOBOT_SERVO_ID_READ              14
#define LOBOT_SERVO_ANGLE_OFFSET_ADJUST  17
#define LOBOT_SERVO_ANGLE_OFFSET_WRITE   18
#define LOBOT_SERVO_ANGLE_OFFSET_READ    19
#define LOBOT_SERVO_ANGLE_LIMIT_WRITE    20
#define LOBOT_SERVO_ANGLE_LIMIT_READ     21
#define LOBOT_SERVO_VIN_LIMIT_WRITE      22
#define LOBOT_SERVO_VIN_LIMIT_READ       23
#define LOBOT_SERVO_TEMP_MAX_LIMIT_WRITE 24
#define LOBOT_SERVO_TEMP_MAX_LIMIT_READ  25
#define LOBOT_SERVO_TEMP_READ            26
#define LOBOT_SERVO_VIN_READ             27
#define LOBOT_SERVO_POS_READ             28
#define LOBOT_SERVO_OR_MOTOR_MODE_WRITE  29
#define LOBOT_SERVO_OR_MOTOR_MODE_READ   30
#define LOBOT_SERVO_LOAD_OR_UNLOAD_WRITE 31
#define LOBOT_SERVO_LOAD_OR_UNLOAD_READ  32
#define LOBOT_SERVO_LED_CTRL_WRITE       33
#define LOBOT_SERVO_LED_CTRL_READ        34
#define LOBOT_SERVO_LED_ERROR_WRITE      35
#define LOBOT_SERVO_LED_ERROR_READ       36
#define RunGroup  6


//#define GET_LOW_BYTE(A) ((uint8_t)(A))
////宏函数 获得A的低八位
//#define GET_HIGH_BYTE(A) ((uint8_t)((A) >> 8))
////宏函数 获得A的高八位
//#define BYTE_TO_HW(A, B) ((((uint16_t)(A)) << 8) | (uint8_t)(B))
////宏函数 将高地八位合成为十六位

uint8_t GET_LOW_BYTE(uint16_t A)
{
	return (uint8_t)(A);
}
uint8_t GET_HIGH_BYTE(uint16_t B)
{
	return (uint8_t)((A) >> 8);
}
uint16_t BYTE_TO_HW(uint8_t A, uint8_t B) 
{
	return (((uint16_t)(A)) << 8) | (uint8_t)(B);
}
uint8_t CheckSum(uint8_t buf[])
{
  uint8_t i;
  uint16_t temp = 0;
  for (i = 2; i < buf[3] + 2; i++) {
    temp += buf[i];
  }
  temp = ~temp;
  i = (uint8_t)temp;
  return i;
}

uint8_t SerialServoSetID(uint8_t oldID, uint8_t newID)
{
	uint8_t buf[7];
  buf[0] = buf[1] = LOBOT_SERVO_FRAME_HEADER;
  buf[2] = oldID;
  buf[3] = 4;
  buf[4] = LOBOT_SERVO_ID_WRITE;
  buf[5] = newID;
  buf[6] = CheckSum(buf);
  return buf;
}

uint8_t SerialServoMove(uint8_t id, int16_t position, uint16_t time)
{
  uint8_t buf[10];
  if(position < 0)
    position = 0;
  if(position > 1000)
	position = 1000;
  buf[0] = buf[1] = LOBOT_SERVO_FRAME_HEADER;
  buf[2] = id;
  buf[3] = 7;
  buf[4] = LOBOT_SERVO_MOVE_TIME_WRITE;
  buf[5] = GET_LOW_BYTE(position);
  buf[6] = GET_HIGH_BYTE(position);
  buf[7] = GET_LOW_BYTE(time);
  buf[8] = GET_HIGH_BYTE(time);
  buf[9] = CheckSum(buf);
  return buf;
}

uint8_t SerialServoUnload(uint8_t id)
{
  uint8_t buf[7];
  buf[0] = buf[1] = LOBOT_SERVO_FRAME_HEADER;
  buf[2] = id;
  buf[3] = 4;
  buf[4] = LOBOT_SERVO_LOAD_OR_UNLOAD_WRITE;
  buf[5] = 0;
  buf[6] = CheckSum(buf);
  return buf;
}

uint8_t SerialRunGroup(uint8_t numOfAction, uint16_t Times)
{
  uint8_t buf[8];
  buf[0] = buf[1] = LOBOT_SERVO_FRAME_HEADER;
  buf[2] = 5;
	buf[3]=RunGroup;
  buf[4] =numOfAction;
  buf[5] = GET_LOW_BYTE(Times);
  buf[6] = GET_HIGH_BYTE(Times);
	buf[7] = CheckSum(buf);
	return buf;
}


uint8_t SerialServoLoad(uint8_t id)
{
  uint8_t buf[7];
  buf[0] = buf[1] = LOBOT_SERVO_FRAME_HEADER;
  buf[2] = id;
  buf[3] = 4;
  buf[4] = LOBOT_SERVO_LOAD_OR_UNLOAD_WRITE;
  buf[5] = 1;
  buf[6] = CheckSum(buf);
  return buf;
}

uint8_t SerialServoReadPosition(uint8_t id)
{
  int ret;
  uint8_t buf[6];

  buf[0] = buf[1] = LOBOT_SERVO_FRAME_HEADER;
  buf[2] = id;
  buf[3] = 3;
  buf[4] = LOBOT_SERVO_POS_READ;
  buf[5] = CheckSum(buf);

  return buf;
}


int test(int a) 
{
	return GET_LOW_BYTE(a);

}