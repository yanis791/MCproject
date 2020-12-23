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

void motorRun(void)
{
	unsigned char i;

	while(1){
		// if (key1==0){
			for(i=0;i<8;i++){
				P2 = clockwise[i];
				delay1ms(speed);	
		 	}
		// }
		// if (key2==0){
		// 	for(i=0;i<8;i++){
		// 		P2 = zheng [i];
		// 		delay1ms(speed);
		// 	}
		// }
		// if (key3==0){
		// 	speed = speed + 5;
		// 	if (speed>100)	speed = 100;
		// }
		// if (key4==0){
		// 	speed = speed - 5;
		// 	if (speed<40)	speed = 40;
		// }
	
}
}