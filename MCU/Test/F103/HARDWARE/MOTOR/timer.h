#ifndef __TIMER_H
#define __TIMER_H
#include "sys.h"

void pwm_gpio_init(void);
void TIM1_PWM_Init(u16 arr,u16 psc); //TIM1��pwmģʽ��ʼ��
void TIM3_PWM_init(u16 arr,u16 psc); //TIM3�ı�����ģʽ��ʼ��
void TIM2_encoder_init(void);        //TIM2�ı�����ģʽ��ʼ��
#endif


#if 0

			TIM_SetCompare1(TIM1,20000 - 1000);	//��
			TIM_SetCompare2(TIM1,20000 - 1280);		//��
			delay_ms(1500);
			delay_ms(1500);
			
			TIM_SetCompare1(TIM1,20000 - 1274);	//��
			TIM_SetCompare2(TIM1,20000 - 1540);		//��
			delay_ms(1500);
			delay_ms(1500);


			TIM_SetCompare1(TIM1,20000 - 1274);
			TIM_SetCompare2(TIM1,20000 - 1280);
			delay_ms(1500);
			delay_ms(1500);
			
			TIM_SetCompare1(TIM1,20000 - 1000);
			TIM_SetCompare2(TIM1,20000 - 1540);//2120
			delay_ms(1500);
			delay_ms(1500);
			
#endif
