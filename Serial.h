#ifndef     Serial
#define		Serial
#include	<reg52.h>
#include	<intrins.h>

#define BAUD0		0xfd


void Init_Time1(void)
{
	TR1 = 0;		//停止计数
	TMOD	= (TMOD & 0x0f) | 0x20;
	TH1	= BAUD0;		//初始化Time0数据
	TL1	= BAUD0;
	ET1	= 0;		//没有Time1中断
	TR1=1;		//开始计时
}

void InitRs232(void)
{
	REN=1;//	允许接收
	SCON= 0x50;		//串口方式1
	EA=1;
    ES= 1;		//开放串口

	Init_Time1();
}


// void Serial(void) interrupt 4
// {
//   if(RI)
//    {
//     RI=0;
//     a=SBUF;
//     ES=0;
//    }

// }

void sendData(unsigned char data2send)
{
    SBUF = data2send;
    while (TI==0);
    TI = 0;
    ES=1;
}
#endif