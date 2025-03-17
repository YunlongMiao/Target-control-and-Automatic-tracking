#ifndef __SERIAL_H
#define __SERIAL_H

#include "stm32f10x.h" 
#include <stdio.h>

#define USART_REC_LEN  			200  	//定义最大接收字节数 200


void Serial_Init(void);
void Serial_SendByte(USART_TypeDef* USARTx,uint8_t Byte);
void Serial_SendArray(u8 *Array, u16 Length);
void Serial_SendString(char *String);
void Serial_SendNumber(u32 Number, u8 Length);
void Serial_Printf(char *format, ...);

u8 Serial_GetRxFlag(void);
u8 Serial_GetRxData(void);

void get_steer_mid_err(int *x_error,int *y_error);
	
#endif
