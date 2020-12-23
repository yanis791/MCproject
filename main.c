#include <reg52.h>
#include "stdio.h"
#include "Serial.h"
#include "StepMotor.h"
#include "mpu6050.h"

void main()
{
    // while(1)
    // {
	 InitRs232();
    // sendData('A');
	// }
    //motorRun();
    mpu();
    
}
