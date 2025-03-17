#include <stdio.h>
#include <stdarg.h>
#include "OLED.h"
#include "Serial.h"
#include "delay.h"

uint8_t Serial_RxData;
uint8_t Serial_RxFlag;
static int16_t Cx=0,Cy=0; 
extern float Ang1,Ang2,AngFlag;
int Angle1,Angle2;

u8  USART_RX_BUF[USART_REC_LEN]; //���ջ���,���USART_REC_LEN���ֽ�.ĩ�ֽ�Ϊ���з� 
u16 USART_RX_STA;         		//����״̬���	

char source[10];   
int tractdata_x=0; 
int tractdata_y=0;   
int real_data_x=0;     
int real_data_y=0;    
int tractdata=0;   
int real_data=0;  
uint8_t t,i;         /* ��������ѭ�� */
uint16_t len;        /* �������ڴ��ڽ������ݵ��ֽ��� */

void Serial_Init(void)
{
	
	GPIO_InitTypeDef GPIO_InitStructure;
	USART_InitTypeDef USART_InitStructure;
	NVIC_InitTypeDef NVIC_InitStructure;
	
	
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_USART3, ENABLE);
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);
	
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;		//�����������
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_10;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOB, &GPIO_InitStructure);
	
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;			//��������
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_11;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOB, &GPIO_InitStructure);
	
	
	USART_InitStructure.USART_BaudRate = 9600;
	USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;
	USART_InitStructure.USART_Mode = USART_Mode_Tx | USART_Mode_Rx;
	USART_InitStructure.USART_Parity = USART_Parity_No;
	USART_InitStructure.USART_StopBits = USART_StopBits_1;
	USART_InitStructure.USART_WordLength = USART_WordLength_8b;
	USART_Init(USART3, &USART_InitStructure);					//��ʼ������1
	
	USART_ITConfig(USART3, USART_IT_RXNE, ENABLE);		//�������ڽ����ж�
	
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);
	

	NVIC_InitStructure.NVIC_IRQChannel = USART3_IRQn;
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;
	NVIC_Init(&NVIC_InitStructure);
	
	USART_Cmd(USART3, ENABLE);
}



//-------------------------------------------------------------------------------------------------------------------
// �������     ����1�ֽ�����
// ����˵��     
// ����˵��    
// ���ز���    
// ʹ��ʾ��     
// ��ע��Ϣ     
//-------------------------------------------------------------------------------------------------------------------

void Serial_SendByte(USART_TypeDef* USARTx,uint8_t Byte)
{
	USART_SendData(USART3, Byte);
	while (USART_GetFlagStatus(USART3, USART_FLAG_TXE) == RESET);
}


//-------------------------------------------------------------------------------------------------------------------
// �������    �������� 
// ����˵��     
// ����˵��    
// ���ز���    
// ʹ��ʾ��     
// ��ע��Ϣ     
//-------------------------------------------------------------------------------------------------------------------
void Serial_SendArray(uint8_t *Array, uint16_t Length)
{
	uint16_t i;
	for (i = 0; i < Length; i ++)
	{
		Serial_SendByte(USART3,Array[i]);
	}
}



//-------------------------------------------------------------------------------------------------------------------
// �������     �����ַ���
// ����˵��     
// ����˵��    
// ���ز���    
// ʹ��ʾ��     
// ��ע��Ϣ     
//-------------------------------------------------------------------------------------------------------------------

void Serial_SendString(char *String)
{
	uint8_t i;
	for (i = 0; String[i] != '\0'; i ++)
	{
		Serial_SendByte(USART3,String[i]);
	}
}



//-------------------------------------------------------------------------------------------------------------------
// �������   ���X��Y�η���  
// ����˵��     
// ����˵��    
// ���ز���    
// ʹ��ʾ��     
// ��ע��Ϣ     
//-------------------------------------------------------------------------------------------------------------------

uint32_t Serial_Pow(uint32_t X, uint32_t Y)
{
	uint32_t Result = 1;
	while (Y --)
	{
		Result *= X;
	}
	return Result;
}


//-------------------------------------------------------------------------------------------------------------------
// �������     ��������
// ����˵��     ���֣�����λ��
// ����˵��    
// ���ز���    
// ʹ��ʾ��     23��2
// ��ע��Ϣ     
//-------------------------------------------------------------------------------------------------------------------

void Serial_SendNumber(uint32_t Number, uint8_t Length)
{
	uint8_t i;
	for (i = 0; i < Length; i ++)
	{
		Serial_SendByte(USART3,Number / Serial_Pow(10, Length - i - 1) % 10 + '0');
	}
}



//int fputc(int ch, FILE *f)
//{
//	Serial_SendByte(ch);
//	return ch;
//}

//void Serial_Printf(char *format, ...)
//{
//	char String[100];
//	va_list arg;
//	va_start(arg, format);
//	vsprintf(String, format, arg);
//	va_end(arg);
//	Serial_SendString(String);
//}

//////////////////////////////////////////////////////////////////
//�������´���,֧��printf����,������Ҫѡ��use MicroLIB	  
#if 1
#pragma import(__use_no_semihosting)             
//��׼����Ҫ��֧�ֺ���                 
struct __FILE 
{ 
	int handle; 

}; 

FILE __stdout;       
//����_sys_exit()�Ա���ʹ�ð�����ģʽ    
void _sys_exit(int x) 
{ 
	x = x; 
} 
////�ض���fputc���� 
//int fputc(int ch, FILE *f)
//{      
//	while((USART3->SR&0X40)==0);//ѭ������,ֱ���������   
//    USART1->DR = (u8) ch;      
//	return ch;
//}


/*�ض���C�⺯��printf�����ڣ��ض�������ʹ��printf����*/
int fputc(int ch,FILE *f)
{
	/*����һ���ֽ����ݵ�����*/
	USART_SendData(USART3,(uint8_t) ch);
	/*�ȴ��������*/
	while(USART_GetFlagStatus(USART3,USART_FLAG_TXE) == RESET);
	
	return(ch);
}
 
/*�ض���C�⺯��scanf�����ڣ��ض�������ʹ��scanf����*/
int fgetc(FILE *f)
{
	/*�ȴ�������������*/
	while(USART_GetFlagStatus(USART3,USART_FLAG_RXNE) == RESET);
	
	return (int)USART_ReceiveData(USART3);
}
#endif 


#if 0

void USART3_IRQHandler(void)
{
	uint8_t temp;
	if( (USART_GetITStatus(USART3, USART_IT_TXE) != RESET) )
	{
		OLED_ShowString(0,3,"START2 ",16);
		delay_ms(1000);
		USART_ITConfig(USART3,USART_IT_TXE,DISABLE);
	}
	if( (USART_GetITStatus(USART3, USART_IT_RXNE) != RESET) )
	{
		temp	=	USART_ReceiveData(USART3);
		OLED_ShowString(0,3,"SEND ",16);
		USART_SendData(USART3, temp);
		
	}
 
}

#endif


#if 0
//USART3 ȫ���жϷ�����
//void USART3_IRQHandler(void)
void USART3_IRQHandler(void)			 
{
		u8 com_data; 
		u8 i;
		u8 num[4]  = {2,3,5,7};
	
		static u8 RxCounter1=0;
		static u16 RxBuffer1[10]={0};
		static u8 RxState = 0;	
		static u8 RxFlag1 = 0;

		if( USART_GetITStatus(USART3,USART_IT_RXNE)!=RESET){  	   //�����ж�  
		
//				USART_ClearITPendingBit(USART3,USART_IT_RXNE);   //����жϱ�־
				com_data = USART_ReceiveData(USART3);
					
//				OLED_ShowString(0,3,"START1 ",16); 
//				OLED_ShowNum(0,0,com_data>>4,3,16);
//				OLED_ShowNum(0,3,com_data&0xf,3,16);
//			OLED_ShowNum(0,0,com_data>>4,3,16);
//			Serial_SendNumber(23,1);
			
				if((USART_RX_STA&0x8000)==0){//����δ���
				
					if(USART_RX_STA&0x4000){//���յ���0x0d
					
							if(com_data!=0x0a)
								USART_RX_STA=0;//���մ���,���¿�ʼ
							else 
								USART_RX_STA|=0x8000;	//��������� 
						}
					 else{ //��û�յ�0X0D
						
							if(com_data==0x0d)
								USART_RX_STA|=0x4000;
							else{
								USART_RX_BUF[USART_RX_STA&0X3FFF]=com_data ;
								
								USART_RX_STA++;
								if(USART_RX_STA>(USART_REC_LEN-1))
									USART_RX_STA=0;//�������ݴ���,���¿�ʼ����	  
							}		 
					 }
					 
				}
		}
}

#endif





//USART3 ȫ���жϷ�����
void USART3_IRQHandler(void)			 
{
		u8 com_data; 
		u8 i;
	
		static u8 RxCounter1=0;
		static u16 RxBuffer1[10]={0};
		static u8 RxState = 0;	
		static u8 RxFlag1 = 0;

		if( USART_GetITStatus(USART3,USART_IT_RXNE)!=RESET)  	   //�����ж�  
		{
//				USART_ClearITPendingBit(USART3,USART_IT_RXNE);   //����жϱ�־
				com_data = USART_ReceiveData(USART3);
					
//				OLED_ShowString(0,3,"START1 ",16); 
//				OLED_ShowNum(0,0,com_data,3,16);
//			printf("%c",com_data);
				if(RxState==0&&com_data==0x2C)  //0x2c֡ͷ
				{
					RxBuffer1[RxCounter1++]=com_data;
					RxState=1;
				}
		
				else if(RxState==1&&com_data==0x12)  //0x12֡ͷ
				{
					RxBuffer1[RxCounter1++]=com_data;
					RxState=2;
				}			
				else if(RxState==2)
				{
					RxBuffer1[RxCounter1++]=com_data;

					if(RxCounter1>=8||com_data == 0x5B)       //RxBuffer1��������,�������ݽ���
					{					
						RxState=3;
						RxFlag1=1;
						//����ʵ��RxBuffer1[2] = RxBuffer1[3]
						Cx=RxBuffer1[RxCounter1-5];	//RxBuffer1[2]
						Cy=RxBuffer1[RxCounter1-3];	//RxBuffer1[4]
//						OLED_ShowNum(0,0,Cx,3,16);
					}
				}
		
				else if(RxState==3)		//����Ƿ���ܵ�������־
				{
						if(RxBuffer1[RxCounter1-1] == 0x5B)
						{

									USART_ITConfig(USART3,USART_IT_RXNE,DISABLE);//�ر�DTSABLE�ж�
									if(RxFlag1)
									{	
										
//										Angle1 = RxCounter1;
										Angle1 = RxBuffer1[RxCounter1-5];	//CX:����
										Angle2 = RxBuffer1[RxCounter1-3];	//CY:ת��
										
//										OLED_ShowNum(0,0,Angle1,10,16);
//										OLED_ShowNum(0,3,Angle2,10,16);
										RxFlag1 = 0;
										RxCounter1 = 0;
										RxState = 0;									
									}
									USART_ITConfig(USART3,USART_IT_RXNE,ENABLE);
								
									
						}
						else   //���մ���
						{
									RxState = 0;
									RxCounter1=0;
									for(i=0;i<10;i++)
									{
											RxBuffer1[i]=0x00;      //�����������������
									}
						}
				} 
	
				else   //�����쳣
				{
						RxState = 0;
						RxCounter1=0;
						for(i=0;i<10;i++)
						{
								RxBuffer1[i]=0x00;      //�����������������
							
						}
				}
			
		}
	}

	
	
	
	
	
	
	
	
	
//void USART3_IRQHandler(void){

//		u8 Res;  
// 
//    if(USART_GetITStatus(USART3,USART_IT_RXNE)!=RESET)  //�����ж�(���յ������ݱ�����0x0d 0x0a��β)
//    {
////			USART_ClearITPendingBit(USART3,USART_IT_RXNE);   //����жϱ�־			
//			Res =USART_ReceiveData(USART3);	//��ȡ���յ�������
//			USART_SendData(USART3,Res);
//			if((USART_RX_STA&0x8000)==0)//����δ���
//			{
//					if(USART_RX_STA&0x4000)//���յ���0x0d
//					{
//							if(Res!=0x0a)USART_RX_STA=0;//���մ���,���¿�ʼ
//							else 
//							{
//								USART_RX_STA|=0x8000;	//��������� 
////								USART_ITConfig(USART3,USART_IT_RXNE,DISABLE);//�ر�DTSABLE�ж�
//							}
//					}
//					else //��û�յ�0X0D
//					{	
//								if(Res==0x0d)
//									USART_RX_STA|=0x4000;
//								else
//								{
//											USART_RX_BUF[USART_RX_STA&0X3FFF]=Res ;
//											USART_RX_STA++;
//											if(USART_RX_STA>(USART_REC_LEN-1))USART_RX_STA=0;//�������ݴ���,���¿�ʼ����	  
//								}		 
//					}
//			}   		 
//	}
//}

///**
// *@brief STM32��OPENMV����x��y��ƫ��
// *@retval ��������ƫ��ֵ
// *@param x_error:����X������ƫ�� y_error:����Y������ƫ�� 
// */
///*����Ľ��մ������ݣ������ȥ����ԭ�ӵĴ�����Ƶ�˽⣬����˵�������ܽ������ݾ���*/
//void get_steer_mid_err(int *x_error,int *y_error)
//{
//    if(USART_RX_STA&0x8000) //���յ�һ֡����
//    {					   
//        len=USART_RX_STA&0x3fff;/* �õ��˴ν��յ������ݳ��� */
//        for(t=0;t<len;t++) //ȡֵ��MV����8�������ַ����������ڽ�����
//        {
//            source[t]=USART_RX_BUF[t];  /* ��BUF�Ĵ�������ת�Ƶ�source���� */
//            //ǧλ*1000+��λ*100+ʮλ*10+��λ�������ԭ��
//            tractdata_x=(source[0]-'0')*1000+(source[1]-'0')*100+(source[2]-'0')*10+(source[3]-'0'); //����ɫ��x��ƫ��
//            tractdata_y=(source[4]-'0')*1000+(source[5]-'0')*100+(source[6]-'0')*10+(source[7]-'0'); //����ɫ��y��ƫ��            
//        }
//				
//				OLED_ShowNum(0,0,tractdata_x,10,16); 
//				OLED_ShowNum(0,4,tractdata_y,10,16); 
//        
//        /* ��Ϊ��������������+100���ģ����Ը�100�ȽϿ����жϷ������ǲ��Ǹ��������´������������� */
//         if(tractdata_x>100)
//        {
//            real_data_x=-(tractdata_x-100);
//        }
//        if(real_data_x==100)
//        {
//            real_data_x=0;
//        }
//        else if(tractdata_x<100)
//        {
//            real_data_x=tractdata_x;
//        }
//        if(real_data_x>=0)
//        {
////        OLED_ShowString(0,0,"+",16);
////        OLED_ShowNum(6,0,real_data_x,3,16); 
//        }
//        else if(real_data_x<0)
//        {
////        OLED_ShowString(0,0,"-",16);
////        OLED_ShowNum(6,0,-real_data_x,3,16); 
//        }
//      
//        
//        /* ��Ϊ��������������+100���ģ����Ը�100�ȽϿ����жϷ������ǲ��Ǹ��������´������������� */
//         if(tractdata_y>100)
//        {
//            real_data_y=-(tractdata_y-100);
//        }
//        if(real_data_y==100)
//        {
//            real_data_y=0;
//        }
//        else if(tractdata_y<100)
//        {
//            real_data_y=tractdata_y;
//        }
//        if(real_data_y>=0)
//        {
////				OLED_ShowString(40,0,"+",16);
////        OLED_ShowNum(46,0,real_data_y,3,16); 
//        }
//        else if(real_data_y<0)
//        {
////				OLED_ShowString(40,0,"-",16);
////        OLED_ShowNum(46,0,-real_data_y,3,16); 
//        }
//				
////          printf("real=%d len=%d\r\n",real_data_x,len);
////			printf("\r\n\r\n");/* ���뻻�� */
//        *x_error=real_data_x; //����ֵ
//        *y_error=real_data_y;
//				
////				OLED_ShowNum(0,0,real_data_x,10,16); 
////				OLED_ShowNum(0,4,real_data_y,10,16); 
//				
//        USART_RX_STA=0; //������ɣ�������һ�ֵĽ���
//        for(i=0;i<10;i++)  /* �������� */
//        {
//            source[i]=0;
//        }
//    }
//}

