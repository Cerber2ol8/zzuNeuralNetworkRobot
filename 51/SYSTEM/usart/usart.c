#include "stm32f10x.h"
#include "string.h"
#include "usart.h"
#include "bool.h"
#include "LobotSerialServo.h"

u8 USART_RX_BUF[64];
bool isUsartRxCompleted = false;

int fputcl(int ch, FILE *f)
{
        if(ch =='\n')  
        {  
            USART_SendData(USART2, 0x0D);  
            while (!(USART2->SR & USART_FLAG_TXE)); 
            USART_SendData(USART2, 0x0A);  
            while (!(USART2->SR & USART_FLAG_TXE));  
        }  
        else  
        {  
            USART_SendData(USART2, (unsigned char)ch);  
            while (!(USART2->SR & USART_FLAG_TXE));   
        }  
	return ch;
}

void usartNVICInit(void) {
		//Usart2 NVIC
	NVIC_InitTypeDef NVIC_InitStructure;
	
	NVIC_InitStructure.NVIC_IRQChannel = USART2_IRQn;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 3;
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 3; 

	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE; 
	NVIC_Init(&NVIC_InitStructure);
}

void usartInit(u32 boundl)
{
	GPIO_InitTypeDef GPIO_InitStructure;
	USART_InitTypeDef USART_InitStructure;

	RCC_APB1PeriphClockCmd(RCC_APB1Periph_USART2 | RCC_APB2Periph_GPIOA | RCC_APB2Periph_AFIO, ENABLE);
	
	//USART2_TX   PA2
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_2;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
	GPIO_Init(GPIOA, &GPIO_InitStructure);
	
	//USART1_RX	  PA3
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_3;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING;
	GPIO_Init(GPIOA, &GPIO_InitStructure);

	//USART 配置
	USART_InitStructure.USART_BaudRate = boundl;//波特率
	USART_InitStructure.USART_WordLength = USART_WordLength_8b; //数据位
	USART_InitStructure.USART_StopBits = USART_StopBits_1; //停止位
	USART_InitStructure.USART_Parity = USART_Parity_No; //校验位
	USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None; //流控制
	USART_InitStructure.USART_Mode = USART_Mode_Rx | USART_Mode_Tx; //发送接收

	USART_Init(USART2, &USART_InitStructure);
	usartNVICInit();
	USART_ITConfig(USART2, USART_IT_RXNE, ENABLE);
	USART_Cmd(USART2, ENABLE);
}

void usartWriteBuf(uint8_t *buf, uint8_t len)
{
	while (len--) {
		while ((USART2->SR & 0x40) == 0);
		USART_SendData(USART2,*buf++);
	}
}



void USART2_IRQHandler(void)
{
	uint8_t Resl;
	
	static bool isGotFrameHeader = false;
	static uint8_t frameHeaderCount = 0;
	static uint8_t dataLength = 2;
	static uint8_t dataCount = 0;
	if (USART_GetITStatus(USART2, USART_IT_RXNE) != RESET) { //判断接收中断
		Resl = USART_ReceiveData(USART2);//(USART2->DR);	//取出接收寄存器数据
		if (!isGotFrameHeader) {  //判断帧头
			if (Resl == 0x55) {
				frameHeaderCount++;
				if (frameHeaderCount == 2) {
					frameHeaderCount = 0;
					isGotFrameHeader = true;
					dataCount = 1;
				}
			} else {
				isGotFrameHeader = false;
				dataCount = 0;
				frameHeaderCount = 0;
			}
		}
		if (isGotFrameHeader) { //接收接收数据部分
			USART_RX_BUF[dataCount] = Resl;
			if (dataCount == 3) {
				dataLength = USART_RX_BUF[dataCount];
				if (dataLength < 3 || dataLength > 7) {
					dataLength = 3;
					isGotFrameHeader = false;
				}
			}
			dataCount++;
			if (dataCount == dataLength + 3) {
				if (isUsartRxCompleted == false) {
					isUsartRxCompleted = true;
					memcpy(LobotRxBuf, USART_RX_BUF, dataCount+2);	
				}
				isGotFrameHeader = false;
			}
		}
	}
	
}

bool isRxCompleted(void)
{
	if(isUsartRxCompleted == true){
		isUsartRxCompleted = false;
		return true;
	}else{
		return false;
	}
}

