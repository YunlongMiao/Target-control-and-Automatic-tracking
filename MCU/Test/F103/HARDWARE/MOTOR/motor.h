#ifndef __MOTOR_H
#define __MOTOR_H


void motor_gpio_init(void);

void MotorControl(int pwm_worth);
void MotorDire(unsigned int DirePwm);
#endif
