#include <reg52.h>
#include "stdio.h"
#include "Serial.h"
#include "StepMotor.h"
#include "mpu6050.h"
#define pi 3.14159

void main()
{
    int x,y,z;
    // while(1)
    // {
    delay(500);
	InitRs232();
    InitMPU6050();

    while(1){
    x = GetData(ACCEL_XOUT_H);
    y = GetData(ACCEL_YOUT_H);
    z = GetData(ACCEL_ZOUT_H);
    sendString(x);
	sendString(y);
	sendString(z);
    sendData(0x0d);
    sendData(0x0a);
    // tx = (atan((float)x/sqrt(fabs(y*y+z*z))));
    

    //omega = omega *4000/48;
    // sendData('A');
	// }
// 	omega /=10;
//     if(omega>0)
//     motorRun(0,omega,10);
//     else
//     motorRun(1,-omega,10);
//    // mpu();
//     delay(100);
    }
    
}
