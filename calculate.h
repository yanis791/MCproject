#include	<reg52.h>
#include <intrins.h>
#include "math.h"

#define pi 3.14159

int calcTheta(int Ax,int Ay, int Az)
{
    float theta_x;
    int t_x;
    theta_x = (atan((float)Ax / sqrt(fabs(Ay * Ay + Az * Az)))) *180 / pi;
    t_x = theta_x;
    return 5;
}