/***************
测试CD4094+CD4511驱动共阴数码管显示数字
一个4094带两个CD4511驱动两个数码管
然后输出级连口
********************/
#include <reg52.h>
#include <intrins.h>
#define uchar unsigned char
#define uint  unsigned int

#define nop(); _nop_();

sbit STR4094=P1^4; //锁存器移位使能端,H 使能
sbit D4094=P1^5; //串行数据输出端,H 使能
sbit CLK4094=P1^6; //串行时钟输出端,H 使能输出状态使能端,H 使能
//code uchar tab[10]={0x40,0x79,0x24,0x30,0x19,0x12,0x02,0x78,0x00,0x10,};
code uchar tab[11]={0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f,0x40};
//code uchar tab[10]={0xFB,0x68,0xDD,0xFC,0x6E,0xBE,0xBF,0xE8,0xFF,0xFE};
void delayms(unsigned short ms)
{
   unsigned short i;
   uchar j;
   for(i=0;i<ms;i++)
        {
    for(j=0;j<200;j++);
    for(j=0;j<102;j++);
    } //for(i=0;i<ms;i++)
}

void Out4094(int dat0)
{
        int a,b;

        b=tab[dat0];//读入待发送的数据
        STR4094=0;
        for(a=0;a<8;a++)
        {
                if(b&0x80)
                D4094=1;
                else D4094=0;
                CLK4094=0;
                nop();
                CLK4094=1;
                b<<=1;//向左移一位
        }
        STR4094=1;
}
 

void lcd(int omega)
{
	int flag;
    
	flag = omega;
    if(flag<0) omega = -omega;

    Out4094(omega%10);
    omega/=10;

    Out4094(omega%10);
    omega/=10;

    Out4094(omega%10);
    omega/=10;

    Out4094(omega%10);
    omega/=10;

    Out4094(omega%10);
    omega/=10;

    if(flag<0)
            Out4094(10);
    else    Out4094(0);

    delay(100);
}
