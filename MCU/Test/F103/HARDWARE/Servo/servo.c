#include "servo.h"

float Angle_Max = 1800;
float Angle_Min = 1200;

int AXIS_NUM[4][2] = { {0,0}, {0,0}, {0,0}, {0,0} };
/*
左上  X: AXIS_NUM[0][0]   Y: AXIS_NUM[0][1]
右上  X: AXIS_NUM[1][0]   Y: AXIS_NUM[1][1]
右下  X: AXIS_NUM[2][0]   Y: AXIS_NUM[2][1]
左下  X: AXIS_NUM[3][0]   Y: AXIS_NUM[3][1]
*/

//-------------------------------------------------------------------------------------------------------------------
// 函数简介     舵机引脚初始化，定时器1的通道1，2，A8 A9
// 参数说明     
// 参数说明    
// 返回参数    
// 使用示例     
// 备注信息     
//-------------------------------------------------------------------------------------------------------------------
//void ServoGpioInit(void)
//{
//	GPIO_InitTypeDef GPIO_InitStructure;
// 	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);  

//	//PWM口初始化：
//	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_8|GPIO_Pin_9;  //TIM1_CH1  TIM1_CH2
//	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;        //复用推挽输出
//	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
//	GPIO_Init(GPIOA, &GPIO_InitStructure);
//	
//	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_12;
//	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP; 
//	GPIO_Init(GPIOA, &GPIO_InitStructure);
//}


//-------------------------------------------------------------------------------------------------------------------
// 函数简介     云台舵机限幅，其实是Y方向限幅
// 参数说明     
// 参数说明    
// 返回参数    
// 使用示例     
// 备注信息     
//-------------------------------------------------------------------------------------------------------------------

int ServoXianfu(int Angle)
{
	if(Angle >= Angle_Max)
		Angle = Angle_Max;
	if(Angle <= Angle_Min)
		Angle = Angle_Min;
	
	return Angle;
}



//-------------------------------------------------------------------------------------------------------------------
// 函数简介  将限幅后的PWM填入定时器   
// 参数说明     
// 参数说明    
// 返回参数    
// 使用示例     
// 备注信息     
//-------------------------------------------------------------------------------------------------------------------

void SetServoPwm(u8 Serial,int AnglePwm ){
		AnglePwm = ServoXianfu(AnglePwm);
		if(Serial == 1)
			TIM_SetCompare2(TIM3,AnglePwm);
		else if(Serial == 2)
			TIM_SetCompare4(TIM3,AnglePwm);
}




//-------------------------------------------------------------------------------------------------------------------
// 函数简介     云台控制，传入舵机编号，转动角度  垂直0度
// 参数说明     
// 参数说明    
// 返回参数    
// 使用示例     
// 备注信息     修改后，限幅移除
//-------------------------------------------------------------------------------------------------------------------

void SetServoFin(u16 Serial,int Angle )	//范围： -83~84
{
	
//	Angle = ServoXianfu(Angle,-83,84);
	SetServo(Serial,Angle + 49 + 83);

}

//-------------------------------------------------------------------------------------------------------------------
// 函数简介     云台控制，传入舵机编号，转动角度 垂直132度
// 参数说明     
// 参数说明    
// 返回参数    
// 使用示例     
// 备注信息     修改后，限幅移除
//-------------------------------------------------------------------------------------------------------------------

void SetServo(u16 Serial,u16 Angle)		//范围：49~216    起始49  垂直：132度  结束216
{
	u32 Pwm = 0;
	if(Serial == 1){
		
//		Angle = ServoXianfu(Angle,49,216);
		Pwm = ((Angle / 270.0) * 2000) + 500;
		TIM_SetCompare1(TIM3,Pwm);
		
	}else if(Serial == 2){
		
		Pwm = ((Angle / 270.0) * 2000) + 500;
		TIM_SetCompare2(TIM3,Pwm);
		
	}
}
























///****************************************************************************
// *	@笔者	：	Q
// *	@日期	：	2023年2月8日
// *	@所属	：	杭州友辉科技
// *	@功能	：	存放舵机相关的函数
// *	@函数列表:
// *	1.	void servo_init(void) -- 舵机gpio初始化
// *	2.	void servo_pin_set(u8 index, BitAction level) -- 设置舵机引脚电平函数
// *	3.	void duoji_doing_set(u8 index, int aim, int time) -- 设置舵机控制参数函数
// ****************************************************************************/
//#include "servo.h"

//servo_t duoji_doing[DJ_NUM];

///* 舵机gpio初始化 */
//void servo_init(void)
//{
//    u8 i;
//    GPIO_InitTypeDef GPIO_InitStructure;

//    RCC_APB2PeriphClockCmd(SERVO0_GPIO_CLK | SERVO1_GPIO_CLK | SERVO2_GPIO_CLK | SERVO3_GPIO_CLK | SERVO4_GPIO_CLK | SERVO5_GPIO_CLK, ENABLE); /* 使能 舵机 端口时钟 */

//    GPIO_InitStructure.GPIO_Pin = SERVO0_PIN;         /* 配置引脚 */
//    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz; /* IO翻转50MHZ */
//    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;  /* 推挽输出 */
//    GPIO_Init(SERVO0_GPIO_PORT, &GPIO_InitStructure);

//    GPIO_InitStructure.GPIO_Pin = SERVO1_PIN;
//    GPIO_Init(SERVO1_GPIO_PORT, &GPIO_InitStructure);

//    GPIO_InitStructure.GPIO_Pin = SERVO2_PIN;
//    GPIO_Init(SERVO2_GPIO_PORT, &GPIO_InitStructure);

//    GPIO_InitStructure.GPIO_Pin = SERVO3_PIN;
//    GPIO_Init(SERVO3_GPIO_PORT, &GPIO_InitStructure);

//    GPIO_InitStructure.GPIO_Pin = SERVO4_PIN;
//    GPIO_Init(SERVO4_GPIO_PORT, &GPIO_InitStructure);

//    GPIO_InitStructure.GPIO_Pin = SERVO5_PIN;
//    GPIO_Init(SERVO5_GPIO_PORT, &GPIO_InitStructure);

//    for (i = 0; i < DJ_NUM; i++)
//    {
//        duoji_doing[i].aim = 1500;
//        duoji_doing[i].cur = 1500;
//        duoji_doing[i].inc = 0;
//        duoji_doing[i].time = 5000;
//    }
//}

///***********************************************
//    功能介绍：	设置舵机引脚电平
//    函数参数1：	index 要设置的舵机引脚索引
//    函数参数2：	level 要设置的舵机引脚电平，1为高，0为低
//    返回值：无
// ***********************************************/
//void servo_pin_set(u8 index, BitAction level)
//{
//    switch (index)
//    {
//    case 0:
//        SERVO0_PIN_SET(level);
//        break;
//    case 1:
//        SERVO1_PIN_SET(level);
//        break;
//    case 2:
//        SERVO2_PIN_SET(level);
//        break;
//    case 3:
//        SERVO3_PIN_SET(level);
//        break;
//    case 4:
//        SERVO4_PIN_SET(level);
//        break;
//    case 5:
//        SERVO5_PIN_SET(level);
//        break;
//    default:
//        break;
//    }
//}

///***********************************************
//    功能介绍：	设置舵机控制参数函数
//    函数参数：	index 舵机编号 aim 执行目标 time 执行时间(如果aim 执行目标==0，视为舵机停止)
//    返回值：		无
// ***********************************************/
//void duoji_doing_set(u8 index, int aim, int time)
//{
//    /* 限制输入值大小 */
//    if (index >= DJ_NUM)
//        return;

//    if (aim == 0)
//    {
//        duoji_doing[index].inc = 0;
//        duoji_doing[index].aim = duoji_doing[index].cur;
//        return;
//    }

//    if (aim > 2490)
//        aim = 2490;
//    else if (aim < 510)
//        aim = 510;

//    if (time > 10000)
//        time = 10000;

//    if (duoji_doing[index].cur == aim)
//    {
//        aim = aim + 0.0077;
//    }

//    if (time < 20) /* 执行时间太短，舵机直接以最快速度运动 */
//    {
//        duoji_doing[index].aim = aim;
//        duoji_doing[index].cur = aim;
//        duoji_doing[index].inc = 0;
//    }
//    else
//    {
//        duoji_doing[index].aim = aim;
//        duoji_doing[index].time = time;
//        duoji_doing[index].inc = (duoji_doing[index].aim - duoji_doing[index].cur) / (duoji_doing[index].time / 20.000);
//    }
//}

///* 设置舵机每次增加的偏移量 */
//void servo_inc_offset(u8 index)
//{
//    int aim_temp;

//    if (duoji_doing[index].inc != 0)
//    {

//        aim_temp = duoji_doing[index].aim;

//        if (aim_temp > 2490)
//        {
//            aim_temp = 2490;
//        }
//        else if (aim_temp < 500)
//        {
//            aim_temp = 500;
//        }

//        if (abs_float(aim_temp - duoji_doing[index].cur) <= abs_float(duoji_doing[index].inc + duoji_doing[index].inc))
//        {
//            duoji_doing[index].cur = aim_temp;
//            duoji_doing[index].inc = 0;
//        }
//        else
//        {
//            duoji_doing[index].cur += duoji_doing[index].inc;
//        }
//    }
//}
