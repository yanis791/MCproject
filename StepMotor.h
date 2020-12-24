#include <reg52.h>
#include "stdio.h"

sbit key1 = P2^0;
sbit key2 = P2^1;
sbit key3 = P2^2;
sbit key4 = P2^3;

unsigned char speed=10;
unsigned char code antiClockwise[] = {0x09,0x08,0x0c,0x04,0x06,0x02,0x03,0x01};
unsigned char code clockwise[] = {0x01,0x03,0x02,0x06,0x04,0x0c,0x08,0x09};

void delay1ms(unsigned int t){
	char i;
	while(t--){
	 	for(i=0;i<10;i++);
	}
}

void motorRun(int direction, int round, int speed)
{
	int i;
	if(direction == 0)
		for(i=0;i<round;i++){
			P2 = antiClockwise[i%8];
			delay1ms(speed);	
		}
	else
		for(i=0;i<round;i++){
				P2 = clockwise[i%8];
				delay1ms(speed);	
			}
	
}
