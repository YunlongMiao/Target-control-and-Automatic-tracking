#ifndef   __TM1637_H
#define   __TM1637_H

#include "stm32f10x.h"
#include "sys.h"

//与库函数操作取一个
#define    SDA_IN()  {GPIOB->CRL&=0X0FFFFFFF;GPIOB->CRL|=(u32)8<<28;}      //通过寄存器更改为输入
#define    SDA_OUT() {GPIOB->CRL&=0X0FFFFFFF;GPIOB->CRL|=(u32)3<<28;}      //通过寄存器更改为输出

#define    TM_SCL_PORT        GPIOB
#define    TM_SCL_CLK         RCC_APB2Periph_GPIOB
#define    TM_SCL_PIN         GPIO_Pin_5

#define    TM_DIO_PORT        GPIOB
#define    TM_DIO_CLK         RCC_APB2Periph_GPIOB
#define    TM_DIO_PIN         GPIO_Pin_7

#define TM_SCL PBout(5)
#define TM_SDA PBout(7)
#define READ_SDA PBin(7)


/*函数声明，这里省略，使用时请自加*/
void TM_Init(void);
void TM_Display(uint8_t *discode);
void TM_AdDisplay(uint8_t addr,uint8_t data);
#endif

#if 0

uint8_t time[4]={0x3f,0x3f|0x80,0x3f,0x3f};   //一个四位数组,这里代表00:00


int main()
{
	u8 flag_s = 0;
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);
	delay_init();
	Serial_Init();
	TM_Init();
	
	while(1)
	{
		 while ( 1 )
    {
			TM_AdDisplay(0,tab[14]);
			TM_AdDisplay(1,tab[13]|0x80);
			TM_AdDisplay(2,tab[12]);
			TM_AdDisplay(3,tab[14]&tab[0]);
    }


	}

}


#endif
