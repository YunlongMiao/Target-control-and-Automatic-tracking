#ifndef __TIMER_H
#define __TIMER_H
#include "sys.h"

void pwm_gpio_init(void);
void TIM1_PWM_Init(u16 arr,u16 psc); //TIM1的pwm模式初始化
void TIM3_PWM_init(u16 arr,u16 psc); //TIM3的编码器模式初始化
void TIM2_encoder_init(void);        //TIM2的编码器模式初始化
#endif


#if 0

			TIM_SetCompare1(TIM1,20000 - 1000);	//右
			TIM_SetCompare2(TIM1,20000 - 1280);		//上
			delay_ms(1500);
			delay_ms(1500);
			
			TIM_SetCompare1(TIM1,20000 - 1274);	//左
			TIM_SetCompare2(TIM1,20000 - 1540);		//下
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
