#include <stm32f10x.h>
#include "delay.h"
#include "sys.h"
#include "Serial.h"
#include "oled.h"
#include "motor.h"
#include "timer.h"
#include "servo.h"
#include "TM1637.h"
#include <pid.h>
#include "key.h"
//#include "usart.h"	
extern int Angle1,Angle2;
//unsigned int KeyNum;
//float Ang1,Ang2,AngFlag;
//int Angle1,Angle2;

/*
36,23
228,13

108,79
*/
u16 lent,tt;	
extern u8  USART_RX_BUF[USART_REC_LEN]; //接收缓冲,最大USART_REC_LEN个字节.末字节为换行符 
extern u16 USART_RX_STA;         		//接收状态标记	
int main()
{
	u8 key=0;	
	
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);
	delay_init();
	Serial_Init();
	
	TIM3_PWM_init(20000-1,72-1); //TIM1的pwm模式初始化
	KEY_Init();          //初始化与按键连接的硬件接口
	OLED_Init();			//初始化OLED  
	OLED_Clear(); 
	
	while(1)
	{
			OLED_Clear(); 
			key=KEY_Scan(0);	//得到键值
			if(key)
			{						   
				switch(key)
				{				 
					case KEY0_PRES:	 
						OLED_ShowNum(0,3,Angle1,3,20);
						OLED_ShowNum(0,5,Angle2,3,20);
						delay_ms(1500);
						break;
					
					case KEY1_PRES:	
						TIM_SetCompare2(TIM3,1100);
						delay_ms(1500);
						delay_ms(1500);
						TIM_SetCompare4(TIM3,1400);
						delay_ms(1500);
						break;
					
					case KEY2_PRES:	
						OLED_ShowNum(0,0,236,3,16);
						delay_ms(1500);
						break;
					
					case WKUP_PRES:	
						OLED_ShowString(0,0,"WKUP_PRES",20);
						delay_ms(1500);
						break;
				}
			}
}

}




//extern u8  USART_RX_BUF[USART_REC_LEN]; //接收缓冲,最大USART_REC_LEN个字节.末字节为换行符 
//extern u16 USART_RX_STA;         		//接收状态标记	

// int main(void)
// {		
// 	u16 t;  
//	u16 len;	
//	u16 times=0;
//	delay_init();	    	 //延时函数初始化	  
//	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2); //设置NVIC中断分组2:2位抢占优先级，2位响应优先级
//	Serial_Init();	 //串口初始化
//	delay_init();
//	Serial_SendByte(1);
//	printf("START");
// 	while(1)
//	{
//		if(USART_RX_STA&0x8000)
//		{					   
//			len=USART_RX_STA&0x3fff;//得到此次接收到的数据长度
//			printf("\r\n您发送的消息为:\r\n\r\n");
//			for(t=0;t<len;t++)
//			{
//				USART_SendData(USART3, USART_RX_BUF[t]);//向串口1发送数据
//				while(USART_GetFlagStatus(USART3,USART_FLAG_TC)!=SET);//等待发送结束
//			}
//			printf("\r\n\r\n");//插入换行
//			USART_RX_STA=0;
//		}else
//		{
//			times++;
//			if(times%5000==0)
//			{
//				printf("\r\n战舰STM32开发板 串口实验\r\n");
//				printf("正点原子@ALIENTEK\r\n\r\n");
//			}
//			if(times%200==0)printf("请输入数据,以回车键结束\n");  
//			delay_ms(10);   
//		}
//	}	 
// }







//--,+-
//-+,++

	
//	while(1)
//	{
////		steer_to_track(1,1);
//			TIM_SetCompare1(TIM1,20000 - 1170);	//右,减小
//			TIM_SetCompare2(TIM1,20000 - 1360);		//上，减小
////			delay_ms(1500);
////			delay_ms(1500);
//			
////			TIM_SetCompare1(TIM1,20000 - 1274);	//左
////			TIM_SetCompare2(TIM1,20000 - 1540);		//下
////			delay_ms(1500);
////			delay_ms(1500);
//	}

//}


