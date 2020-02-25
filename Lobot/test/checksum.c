//#include <iostream>
//using namespace std;
 
typedef unsigned char uint8_t;
typedef unsigned int uint16_t;

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
  //for(int j=0;j<=6;j++){
 
  //	cout<<(int)buf[j]<<endl; 
  //}

  //buf[6] = CheckSum(buf);
  return buf;
}
//int main(){
//	uint8_t *data=SetID(1,4);
//
//	//char sum=CheckSum(buf);
//  for(int i=0;i<=7;i++){
//  	uint8_t temp=*(data+ i);
// 
//  	cout<<(uint16_t)temp<<endl; 
//  	
//  }
//  cout<<CheckSum(data);
//  delete[] data;
//
//	return 0;
//	
//}
