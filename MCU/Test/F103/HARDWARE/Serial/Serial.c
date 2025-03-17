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

u8  USART_RX_BUF[USART_REC_LEN]; //接收缓冲,最大USART_REC_LEN个字节.末字节为换行符 
u16 USART_RX_STA;         		//接收状态标记	

char source[10];   
int tractdata_x=0; 
int tractdata_y=0;   
int real_data_x=0;     
int real_data_y=0;    
int tractdata=0;   
int real_data=0;  
uint8_t t,i;         /* 变量用于循环 */
uint16_t len;        /* 变量用于串口接收数据的字节数 */

void Serial_Init(void)
{
	
	GPIO_InitTypeDef GPIO_InitStructure;
	USART_InitTypeDef USART_InitStructure;
	NVIC_InitTypeDef NVIC_InitStructure;
	
	
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_USART3, ENABLE);
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);
	
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;		//复用推挽输出
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_10;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOB, &GPIO_InitStructure);
	
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;			//上拉输入
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_11;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOB, &GPIO_InitStructure);
	
	
	USART_InitStructure.USART_BaudRate = 9600;
	USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;
	USART_InitStructure.USART_Mode = USART_Mode_Tx | USART_Mode_Rx;
	USART_InitStructure.USART_Parity = USART_Parity_No;
	USART_InitStructure.USART_StopBits = USART_StopBits_1;
	USART_InitStructure.USART_WordLength = USART_WordLength_8b;
	USART_Init(USART3, &USART_InitStructure);					//初始化串口1
	
	USART_ITConfig(USART3, USART_IT_RXNE, ENABLE);		//开启串口接受中断
	
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);
	

	NVIC_InitStructure.NVIC_IRQChannel = USART3_IRQn;
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;
	NVIC_Init(&NVIC_InitStructure);
	
	USART_Cmd(USART3, ENABLE);
}



//-------------------------------------------------------------------------------------------------------------------
// 函数简介     发送1字节数据
// 参数说明     
// 参数说明    
// 返回参数    
// 使用示例     
// 备注信息     
//-------------------------------------------------------------------------------------------------------------------

void Serial_SendByte(USART_TypeDef* USARTx,uint8_t Byte)
{
	USART_SendData(USART3, Byte);
	while (USART_GetFlagStatus(USART3, USART_FLAG_TXE) == RESET);
}


//-------------------------------------------------------------------------------------------------------------------
// 函数简介    发送数组 
// 参数说明     
// 参数说明    
// 返回参数    
// 使用示例     
// 备注信息     
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
// 函数简介     发送字符串
// 参数说明     
// 参数说明    
// 返回参数    
// 使用示例     
// 备注信息     
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
// 函数简介   获得X的Y次方？  
// 参数说明     
// 参数说明    
// 返回参数    
// 使用示例     
// 备注信息     
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
// 函数简介     发送数字
// 参数说明     数字，数字位数
// 参数说明    
// 返回参数    
// 使用示例     23，2
// 备注信息     
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
//加入以下代码,支持printf函数,而不需要选择use MicroLIB	  
#if 1
#pragma import(__use_no_semihosting)             
//标准库需要的支持函数                 
struct __FILE 
{ 
	int handle; 

}; 

FILE __stdout;       
//定义_sys_exit()以避免使用半主机模式    
void _sys_exit(int x) 
{ 
	x = x; 
} 
////重定义fputc函数 
//int fputc(int ch, FILE *f)
//{      
//	while((USART3->SR&0X40)==0);//循环发送,直到发送完毕   
//    USART1->DR = (u8) ch;      
//	return ch;
//}


/*重定向C库函数printf到串口，重定向后可以使用printf函数*/
int fputc(int ch,FILE *f)
{
	/*发送一个字节数据到串口*/
	USART_SendData(USART3,(uint8_t) ch);
	/*等待发送完毕*/
	while(USART_GetFlagStatus(USART3,USART_FLAG_TXE) == RESET);
	
	return(ch);
}
 
/*重定义C库函数scanf到串口，重定向后可以使用scanf函数*/
int fgetc(FILE *f)
{
	/*等待串口输入数据*/
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
//USART3 全局中断服务函数
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

		if( USART_GetITStatus(USART3,USART_IT_RXNE)!=RESET){  	   //接收中断  
		
//				USART_ClearITPendingBit(USART3,USART_IT_RXNE);   //清除中断标志
				com_data = USART_ReceiveData(USART3);
					
//				OLED_ShowString(0,3,"START1 ",16); 
//				OLED_ShowNum(0,0,com_data>>4,3,16);
//				OLED_ShowNum(0,3,com_data&0xf,3,16);
//			OLED_ShowNum(0,0,com_data>>4,3,16);
//			Serial_SendNumber(23,1);
			
				if((USART_RX_STA&0x8000)==0){//接收未完成
				
					if(USART_RX_STA&0x4000){//接收到了0x0d
					
							if(com_data!=0x0a)
								USART_RX_STA=0;//接收错误,重新开始
							else 
								USART_RX_STA|=0x8000;	//接收完成了 
						}
					 else{ //还没收到0X0D
						
							if(com_data==0x0d)
								USART_RX_STA|=0x4000;
							else{
								USART_RX_BUF[USART_RX_STA&0X3FFF]=com_data ;
								
								USART_RX_STA++;
								if(USART_RX_STA>(USART_REC_LEN-1))
									USART_RX_STA=0;//接收数据错误,重新开始接收	  
							}		 
					 }
					 
				}
		}
}

#endif





//USART3 全局中断服务函数
void USART3_IRQHandler(void)			 
{
		u8 com_data; 
		u8 i;
	
		static u8 RxCounter1=0;
		static u16 RxBuffer1[10]={0};
		static u8 RxState = 0;	
		static u8 RxFlag1 = 0;

		if( USART_GetITStatus(USART3,USART_IT_RXNE)!=RESET)  	   //接收中断  
		{
//				USART_ClearITPendingBit(USART3,USART_IT_RXNE);   //清除中断标志
				com_data = USART_ReceiveData(USART3);
					
//				OLED_ShowString(0,3,"START1 ",16); 
//				OLED_ShowNum(0,0,com_data,3,16);
//			printf("%c",com_data);
				if(RxState==0&&com_data==0x2C)  //0x2c帧头
				{
					RxBuffer1[RxCounter1++]=com_data;
					RxState=1;
				}
		
				else if(RxState==1&&com_data==0x12)  //0x12帧头
				{
					RxBuffer1[RxCounter1++]=com_data;
					RxState=2;
				}			
				else if(RxState==2)
				{
					RxBuffer1[RxCounter1++]=com_data;

					if(RxCounter1>=8||com_data == 0x5B)       //RxBuffer1接受满了,接收数据结束
					{					
						RxState=3;
						RxFlag1=1;
						//但是实测RxBuffer1[2] = RxBuffer1[3]
						Cx=RxBuffer1[RxCounter1-5];	//RxBuffer1[2]
						Cy=RxBuffer1[RxCounter1-3];	//RxBuffer1[4]
//						OLED_ShowNum(0,0,Cx,3,16);
					}
				}
		
				else if(RxState==3)		//检测是否接受到结束标志
				{
						if(RxBuffer1[RxCounter1-1] == 0x5B)
						{

									USART_ITConfig(USART3,USART_IT_RXNE,DISABLE);//关闭DTSABLE中断
									if(RxFlag1)
									{	
										
//										Angle1 = RxCounter1;
										Angle1 = RxBuffer1[RxCounter1-5];	//CX:舵盘
										Angle2 = RxBuffer1[RxCounter1-3];	//CY:转向
										
//										OLED_ShowNum(0,0,Angle1,10,16);
//										OLED_ShowNum(0,3,Angle2,10,16);
										RxFlag1 = 0;
										RxCounter1 = 0;
										RxState = 0;									
									}
									USART_ITConfig(USART3,USART_IT_RXNE,ENABLE);
								
									
						}
						else   //接收错误
						{
									RxState = 0;
									RxCounter1=0;
									for(i=0;i<10;i++)
									{
											RxBuffer1[i]=0x00;      //将存放数据数组清零
									}
						}
				} 
	
				else   //接收异常
				{
						RxState = 0;
						RxCounter1=0;
						for(i=0;i<10;i++)
						{
								RxBuffer1[i]=0x00;      //将存放数据数组清零
							
						}
				}
			
		}
	}

	
	
	
	
	
	
	
	
	
//void USART3_IRQHandler(void){

//		u8 Res;  
// 
//    if(USART_GetITStatus(USART3,USART_IT_RXNE)!=RESET)  //接收中断(接收到的数据必须是0x0d 0x0a结尾)
//    {
////			USART_ClearITPendingBit(USART3,USART_IT_RXNE);   //清除中断标志			
//			Res =USART_ReceiveData(USART3);	//读取接收到的数据
//			USART_SendData(USART3,Res);
//			if((USART_RX_STA&0x8000)==0)//接收未完成
//			{
//					if(USART_RX_STA&0x4000)//接收到了0x0d
//					{
//							if(Res!=0x0a)USART_RX_STA=0;//接收错误,重新开始
//							else 
//							{
//								USART_RX_STA|=0x8000;	//接收完成了 
////								USART_ITConfig(USART3,USART_IT_RXNE,DISABLE);//关闭DTSABLE中断
//							}
//					}
//					else //还没收到0X0D
//					{	
//								if(Res==0x0d)
//									USART_RX_STA|=0x4000;
//								else
//								{
//											USART_RX_BUF[USART_RX_STA&0X3FFF]=Res ;
//											USART_RX_STA++;
//											if(USART_RX_STA>(USART_REC_LEN-1))USART_RX_STA=0;//接收数据错误,重新开始接收	  
//								}		 
//					}
//			}   		 
//	}
//}

///**
// *@brief STM32从OPENMV串口x和y轴偏差
// *@retval 返回中线偏差值
// *@param x_error:接收X轴数据偏差 y_error:接收Y轴数据偏差 
// */
///*这里的接收串口数据，你可以去正点原子的串口视频了解，不多说，反正能接受数据就行*/
//void get_steer_mid_err(int *x_error,int *y_error)
//{
//    if(USART_RX_STA&0x8000) //接收到一帧数据
//    {					   
//        len=USART_RX_STA&0x3fff;/* 得到此次接收到的数据长度 */
//        for(t=0;t<len;t++) //取值，MV发了8个数字字符过来，现在解析它
//        {
//            source[t]=USART_RX_BUF[t];  /* 将BUF的串口数据转移到source数组 */
//            //千位*1000+百位*100+十位*10+个位，是这个原理
//            tractdata_x=(source[0]-'0')*1000+(source[1]-'0')*100+(source[2]-'0')*10+(source[3]-'0'); //接收色块x轴偏差
//            tractdata_y=(source[4]-'0')*1000+(source[5]-'0')*100+(source[6]-'0')*10+(source[7]-'0'); //接收色块y轴偏差            
//        }
//				
//				OLED_ShowNum(0,0,tractdata_x,10,16); 
//				OLED_ShowNum(0,4,tractdata_y,10,16); 
//        
//        /* 因为发送来的数据是+100来的，所以跟100比较可以判断发来的是不是负数，以下代码就是这个作用 */
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
//        /* 因为发送来的数据是+100来的，所以跟100比较可以判断发来的是不是负数，以下代码就是这个作用 */
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
////			printf("\r\n\r\n");/* 插入换行 */
//        *x_error=real_data_x; //返回值
//        *y_error=real_data_y;
//				
////				OLED_ShowNum(0,0,real_data_x,10,16); 
////				OLED_ShowNum(0,4,real_data_y,10,16); 
//				
//        USART_RX_STA=0; //接收完成，开启下一轮的接收
//        for(i=0;i<10;i++)  /* 数据清零 */
//        {
//            source[i]=0;
//        }
//    }
//}

