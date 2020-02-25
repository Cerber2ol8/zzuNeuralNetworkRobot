#include <iostream>
using namespace std;
 
typedef unsigned char uint8_t;
typedef unsigned int uint16_t;
typedef int int16_t;

#define GET_LOW_BYTE(A) ((uint8_t)(A))
//宏函数 获得A的低八位
#define GET_HIGH_BYTE(A) ((uint8_t)((A) >> 8))
//宏函数 获得A的高八位
#define BYTE_TO_HW(A, B) ((((uint16_t)(A)) << 8) | (uint8_t)(B))
//宏函数 将高地八位合成为十六位

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

uint8_t* SetID(uint8_t oldID, uint8_t newID)
{
	uint8_t *buf = new uint8_t[7];
  buf[0] = buf[1] = 85;
  buf[2] = oldID;
  buf[3] = 4;
  buf[4] = 13;
  buf[5] = newID;
  buf[6] = CheckSum(buf);
  for(int j=0;j<=6;j++){
 
  	cout<<(int)buf[j]<<endl; 
  }

  //buf[6] = CheckSum(buf);
  return buf;
}

uint8_t* Move(uint8_t id, int16_t position, uint16_t time)
{
  uint8_t *buf= new uint8_t[10];
  if(position < 0)
    position = 0;
  if(position > 1000)
	position = 1000;
  buf[0] = buf[1] = 85;
  buf[2] = id;
  buf[3] = 7;
  buf[4] = 1;
  buf[5] = GET_LOW_BYTE(position);
  buf[6] = GET_HIGH_BYTE(position);
  buf[7] = GET_LOW_BYTE(time);
  buf[8] = GET_HIGH_BYTE(time);
  buf[9] = CheckSum(buf);
  return buf;
}

int main(){
	//uint8_t *data=SetID(1,4);
	uint8_t *data=Move(1,800,1000);

	//char sum=CheckSum(buf);
  for(int i=0;i<=7;i++){
  	uint8_t temp=*(data+ i);
 
  	cout<<(uint16_t)temp<<endl; 
  	
  }
  cout<<CheckSum(data);
  delete[] data;

	return 0;
	
}
