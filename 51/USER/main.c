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
 	SystemInit();//ϵͳʱ�ӵȳ�ʼ��
	delay_init(72);	     //��ʱ��ʼ��
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);//����NVIC�жϷ���2:2λ��ռ���ȼ���2λ��Ӧ���ȼ�
	usartInit(9600);//������ڳ�ʼ��Ϊ9600
 usartcamer_init(115200);//camera���ڳ�ʼ��
	  while(1)
	 { 
	 
		 switch(N)
		 {
			 case 0x01:
		LobotSerialRunGroup(1,1);N=0;break;//ǰ��
			 case 0x02:
			LobotSerialRunGroup(2,1);N=0;break; //��ת
			  case 0x03:
			LobotSerialRunGroup(3,1);N=0;break; //��ת
			 default:
				 delay_ms(20);
	   }
  } 
 	
 }

 
	
