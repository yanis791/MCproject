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
void sendString(int temp_data)
{
	unsigned char str[6],i;
	unsigned char *s;
	s=str;
	if(temp_data<0)
	{
		temp_data=-temp_data;
		*s='-';
	}
	else *s=' ';
 
	*++s =temp_data/10000+0x30;
	temp_data=temp_data%10000;     //取余运算
 
	*++s =temp_data/1000+0x30;
	temp_data=temp_data%1000;     //取余运算
 
	*++s =temp_data/100+0x30;
	temp_data=temp_data%100;     //取余运算
	*++s =temp_data/10+0x30;
	temp_data=temp_data%10;      //取余运算
	*++s =temp_data+0x30; 

	for(i=0;i<6;i++)
	{
    sendData(str[i]);
    }
}
void send2Host(int x,int y,int z)
{
	unsigned char send;
	sendData('#');
	send = x >> 8;
	sendData(send);
	x = x ;
	send = x;
	sendData(send);
	send = y >> 8;
	sendData(send);
	y = y ;
	send = y;
	sendData(send);
	send = z >> 8;
	sendData(send);
	z = z ;
	send = z;
	sendData(send);
	sendData('$');
}
#endif