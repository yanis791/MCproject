#include <reg52.h>
#include "stdio.h"
#include "Serial.h"
#include "StepMotor.h"
#include "mpu6050.h"
#include "tubes.h"
#define pi 3.14159

void main()
{
    int x,y,z,omega,k;
 
    delay(500);
	InitRs232();
    InitMPU6050();

    while(1){
    x = GetData(ACCEL_XOUT_H);
    y = GetData(ACCEL_YOUT_H);
    z = GetData(ACCEL_ZOUT_H);
    omega = GetData(GYRO_ZOUT_H);

    send2Host(x,y,z);
    lcd(omega);
    controlMotor(omega);
    
    delay(10);
    }
    
}


