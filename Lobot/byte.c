typedef unsigned char uint8_t;
typedef unsigned int uint16_t;

#define LobotSerialWrite  usartWriteBuf

#define GET_LOW_BYTE(A) ((uint8_t)(A))
//�꺯�� ���A�ĵͰ�λ
#define GET_HIGH_BYTE(A) ((uint8_t)((A) >> 8))
//�꺯�� ���A�ĸ߰�λ
#define BYTE_TO_HW(A, B) ((((uint16_t)(A)) << 8) | (uint8_t)(B))
//�꺯�� ���ߵذ�λ�ϳ�Ϊʮ��λ