#include "delay.h"
#include "usart.h"
#include "usartcamer.h"
#include "LobotSerialServo.h"
#include "bool.h"
#include "led.h"

#include "sys.h"

 int N=0;
	
 int main(void)
 {
	 
	
	 //KEY_Init();
	 //EXTIX_Init();
	 LED_Init();
 	SystemInit();//系统时钟等初始化
	delay_init(72);	     //延时初始化
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);//设置NVIC中断分组2:2位抢占优先级，2位响应优先级
	usartInit(9600);//舵机串口初始化为9600
 usartcamer_init(115200);//camera串口初始化
	  while(1)
	 { 
	 
		 switch(N)
		 {
			 case 0x01:
		LobotSerialRunGroup(1,1);N=0;break;//前进
			 case 0x02:
			LobotSerialRunGroup(2,1);N=0;break; //左转
			  case 0x03:
			LobotSerialRunGroup(3,1);N=0;break; //右转
			 default:
				 delay_ms(20);
	   }
  } 
 	
 }

 
	
