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
extern u8  USART_RX_BUF[USART_REC_LEN]; //���ջ���,���USART_REC_LEN���ֽ�.ĩ�ֽ�Ϊ���з� 
extern u16 USART_RX_STA;         		//����״̬���	
int main()
{
	u8 key=0;	
	
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);
	delay_init();
	Serial_Init();
	
	TIM3_PWM_init(20000-1,72-1); //TIM1��pwmģʽ��ʼ��
	KEY_Init();          //��ʼ���밴�����ӵ�Ӳ���ӿ�
	OLED_Init();			//��ʼ��OLED  
	OLED_Clear(); 
	
	while(1)
	{
			OLED_Clear(); 
			key=KEY_Scan(0);	//�õ���ֵ
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




//extern u8  USART_RX_BUF[USART_REC_LEN]; //���ջ���,���USART_REC_LEN���ֽ�.ĩ�ֽ�Ϊ���з� 
//extern u16 USART_RX_STA;         		//����״̬���	

// int main(void)
// {		
// 	u16 t;  
//	u16 len;	
//	u16 times=0;
//	delay_init();	    	 //��ʱ������ʼ��	  
//	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2); //����NVIC�жϷ���2:2λ��ռ���ȼ���2λ��Ӧ���ȼ�
//	Serial_Init();	 //���ڳ�ʼ��
//	delay_init();
//	Serial_SendByte(1);
//	printf("START");
// 	while(1)
//	{
//		if(USART_RX_STA&0x8000)
//		{					   
//			len=USART_RX_STA&0x3fff;//�õ��˴ν��յ������ݳ���
//			printf("\r\n�����͵���ϢΪ:\r\n\r\n");
//			for(t=0;t<len;t++)
//			{
//				USART_SendData(USART3, USART_RX_BUF[t]);//�򴮿�1��������
//				while(USART_GetFlagStatus(USART3,USART_FLAG_TC)!=SET);//�ȴ����ͽ���
//			}
//			printf("\r\n\r\n");//���뻻��
//			USART_RX_STA=0;
//		}else
//		{
//			times++;
//			if(times%5000==0)
//			{
//				printf("\r\nս��STM32������ ����ʵ��\r\n");
//				printf("����ԭ��@ALIENTEK\r\n\r\n");
//			}
//			if(times%200==0)printf("����������,�Իس�������\n");  
//			delay_ms(10);   
//		}
//	}	 
// }







//--,+-
//-+,++

	
//	while(1)
//	{
////		steer_to_track(1,1);
//			TIM_SetCompare1(TIM1,20000 - 1170);	//��,��С
//			TIM_SetCompare2(TIM1,20000 - 1360);		//�ϣ���С
////			delay_ms(1500);
////			delay_ms(1500);
//			
////			TIM_SetCompare1(TIM1,20000 - 1274);	//��
////			TIM_SetCompare2(TIM1,20000 - 1540);		//��
////			delay_ms(1500);
////			delay_ms(1500);
//	}

//}


