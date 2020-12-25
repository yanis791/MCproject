#include <reg52.h>
#include "stdio.h"
#include "Serial.h"
#include "StepMotor.h"
#include "mpu6050.h"
#define Round 4096

void main()
{
    int omega;
    // while(1)
    // {
    delay(500);
	InitRs232();
    InitMPU6050();

    while(1){
    omega = GetData(GYRO_ZOUT_H);
    //omega = omega *4000/48;
    // sendData('A');
	// }
	omega /=10;
    if(omega>0)
    motorRun(0,omega,10);
    else
    motorRun(1,-omega,10);
   // mpu();
    delay(100);
    }
    
}
