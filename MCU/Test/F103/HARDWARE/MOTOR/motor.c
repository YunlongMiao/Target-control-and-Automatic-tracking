#include "motor.h"
#include "delay.h"
#include "timer.h"


//PWM��   ��PA8
//        ��PA11
//����ת�� ��PB14��15
//        ��PB13��12
void motor_gpio_init()
{
	GPIO_InitTypeDef GPIO_InitStructure;
 	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);  

	//PWM�ڳ�ʼ����
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_11;  //TIM1_CH4
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;        //�����������
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOA, &GPIO_InitStructure);
	
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_12;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP; 
	GPIO_Init(GPIOA, &GPIO_InitStructure);
}


void MotorControl(int pwm_worth)
{
	
	if(pwm_worth>=0)                              //��ת
      {
       GPIO_WriteBit(GPIOA,GPIO_Pin_12,Bit_SET);
       TIM_SetCompare4(TIM1,pwm_worth);	//0
      }
    else
      {
        GPIO_WriteBit(GPIOA,GPIO_Pin_12,Bit_RESET);
        TIM_SetCompare4(TIM1,-pwm_worth);	  //��ת
      }
}


void MotorDire(unsigned int DirePwm)			//700~950,950~1200
{
	if(DirePwm<700)
		TIM_SetCompare1(TIM1,700);
	else if(DirePwm>1200)
		TIM_SetCompare1(TIM1,1200);
	else
		TIM_SetCompare1(TIM1,DirePwm);
}
