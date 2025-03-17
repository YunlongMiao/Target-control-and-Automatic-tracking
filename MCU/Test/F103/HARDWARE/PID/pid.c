#include <pid.h>
//#include "usart.h"
#include "Serial.h"
#include "oled.h"
#include "servo.h"

extern int Angle1,Angle2;

float Balance_Kp=0.20,Balance_Ki=0.00,Balance_Kd=0.3;//增量式PID 比例积分足够

//float Zero_X=1100,Zero_Y=1350,Target_X=1450,Target_Y=1000;// 激光打向原点处二维舵机占空比以及舵机幅值初始值
float Zero_X=1100,Zero_Y=1350,Target_X=1100,Target_Y=1350;// 激光打向原点处二维舵机占空比以及舵机幅值初始值
int Max_Target=1800,Min_Target=1200,count_=0;// 舵机限幅
float Last_Target_X,Last_Target_Y;

float balanceX(float Angle )//X轴PID
{  
   float  Differential,Bias;//定义差分变量和偏差,Balance_Ki=0.0
	 static float Last_Bias;  //上一次的偏差值,Integration,Balance_Integration,Flag_Target
	 float balance;//平衡的返回值
// Bias=(Angle-Zero_X);  //===求出平衡的角度中值 和机械相关  
	 Bias=(Angle*4-500);  //===求出平衡的角度中值 和机械相关  
	 Differential=Bias-Last_Bias;  //求得偏差的变化率	 


	balance=Balance_Kp*Bias/10+Balance_Kd*Differential/10;   //===计算平衡控制的舵机PWM  PD控制   kp是P系数 kd是D系数  未使用积分
	Last_Bias=Bias;  //保存上一次的偏差
	if(balance<-20)balance=-20;
	if(balance>20)balance=20;//输出限幅
	return balance;  //返回值
}

float balanceY(float Angle )//Y轴PID
{  
   float  Differential,Bias;//定义差分变量和偏差,Balance_Ki=0.0
	 static float Last_Bias;  //上一次的偏差值,Integration,Balance_Integration,Flag_Target
	 float balance;//平衡的返回值
// Bias=(Angle-Zero_Y);  //===求出平衡的角度中值 和机械相关  
	 Bias=(Angle*4-500);  //===求出平衡的角度中值 和机械相关  
	 Differential=Bias-Last_Bias;  //求得偏差的变化率	 
		
	 balance=Balance_Kp*Bias/10+Balance_Kd*Differential/10;   //===计算平衡控制的舵机PWM  PD控制   kp是P系数 kd是D系数 未使用
	 Last_Bias=Bias;  //保存上一次的偏差
	 if(balance<-20)balance=-20;
	 if(balance>20)balance=20;//输出限幅
	 return balance;  //返回值
}

void Set_Pwm(int motor_x,int motor_y)//舵机幅值
{
// TIM4->CCR1=150;
// TIM2->CCR2=150;//预留发挥
		 TIM3->CCR3=motor_x;
     TIM3->CCR4=motor_y;
}

int myabs(int a)//绝对值函数
{ 		   
	  int temp;
		if(a<0)  temp=-a;  
	  else temp=a;
	  return temp;
}



void steer_to_track(uint16_t angle_x,uint16_t angle_y)
{
    int x_er=0,y_er=0; //定义两个变量去接收MV传送过来的偏差值
    static float pid_steer_out=0; //X轴PID输出量
    static float pid_steer_out_y=0; //Y轴PID输出量
		x_er = Angle1;
		y_er = Angle2;
		if(x_er>100)
			x_er = 0-(x_er - 100);
		if(y_er>100)
			y_er = 0-(y_er - 100);
//    get_steer_mid_err(&x_er,&y_er); //调用数据接收函数，接收OPENMV发来的偏差
    pid_steer_out = angle_x + balanceX(x_er); //X轴增量位置式PID输出
		pid_steer_out_y = angle_y - balanceY(y_er); 
		
    if(pid_steer_out>=1250)    //舵机角度限幅，以防转多了卡住
		pid_steer_out=1250;
		if(pid_steer_out<900)
			pid_steer_out=900;	
    if(pid_steer_out_y>=1600)   //舵机角度限幅
		pid_steer_out_y=1600;
		if(pid_steer_out_y<1300)
			pid_steer_out_y=1300;	

	  if(Target_X<Min_Target) 
			Target_X=Min_Target;	
	  if(Target_X>Max_Target)  
			Target_X=Max_Target;	
	  if(Target_Y<Min_Target) 
			Target_Y=Min_Target;	
	  if(Target_Y>Max_Target)  
			Target_Y=Max_Target;	//舵机占空比限幅
		
	  Last_Target_X=Target_X;	//保存上一次的值				
    Last_Target_Y=Target_Y;
		
		TIM_SetCompare2(TIM3,pid_steer_out);
		TIM_SetCompare4(TIM3,-pid_steer_out_y);
      
}

















//extern signed int Angle1,Angle2;
///********** 位置环PID变量 ********/
//PID_POS pid_steer;       //舵机云台追踪色块位置环PID结构体x轴
//PID_POS pid_steer_y;     //舵机云台追踪色块位置环PID结构体y轴
///********** 位置环PID变量 ********/

///**
// *@brief 速度增量式PID函数
// *@param pid_inc:增量式PID参数结构体 actual_data:速度实际值 set_data：速度目标值
// *@retvl OUT:最终输出的PWM电压
// */
//float PID_Increase(PID_INC *pid_inc,float actual_data)
//{   
//	pid_inc->EK =pid_inc->Sv - actual_data;	// 计算当前速度误差
//	pid_inc->OUT +=  
//                pid_inc->Kp * (pid_inc->EK - pid_inc->EK_LAST) //比例P
//			  + pid_inc->Ki *  pid_inc->EK  //积分I
//			  + pid_inc->Kd * (pid_inc->EK - 2 * pid_inc->EK_LAST + pid_inc->EK_LAST_LAST);  //微分D	
//	pid_inc->EK_LAST_LAST = pid_inc->EK_LAST;	// 更新上上误差
//	pid_inc->EK_LAST = pid_inc->EK;		  	// 更新上次误差
//	return pid_inc->OUT;	// 返回增量
//}

///**
// *@brief 位置式PID函数（可用于陀螺仪 摄像头中线 红外循迹 灰度循迹）
// *@param pid_pos:位置式PID参数结构体 actual_data:位置实际值
// *@retvl OUT:最终输出的PWM电压
// */
//float PID_position(PID_POS *pid_pos,float actual_data)
//{   
//	pid_pos->EK =pid_pos->Sv - actual_data;	// 计算当前速度误差
//    pid_pos->SUM_EK+=pid_pos->EK; //误差累加
//	pid_pos->OUT = 
//                pid_pos->Kp * (pid_pos->EK) //比例P
//			  + pid_pos->Ki *  pid_pos->SUM_EK //积分I
//			  + pid_pos->Kd * (pid_pos->EK - pid_pos->EK_NEXT);  //微分D	
//	pid_pos->EK_NEXT = pid_pos->EK;		  	// 更新上次误差
//	return pid_pos->OUT;	// 返回增量
//}

///**
// *@brief 设置增量式PID的Kp,Ki,Kd数值以及目标值
// *@param pid_inc:增量式PID参数结构体 p,i,d：比例-积分-微分 sv:目标设定值
// */
//void set_pid_inc_param(PID_INC *pid_inc,float p,float i,float d,float sv)
//{
//    pid_inc->Kp=p/1000000;
//    pid_inc->Ki=i/1000000;
//    pid_inc->Kd=d/1000000;
//    pid_inc->Sv=sv;
//}

///**
// *@brief 设置位置式PID的Kp,Ki,Kd数值以及目标值
// *@param pid_pos:位置式PID参数结构体 p,i,d：比例-积分-微分 sv:目标设定值
// */
//void set_pid_pos_param(PID_POS *pid_pos,float p,float i,float d,float sv)
//{
//    pid_pos->Kp=p;
//    pid_pos->Ki=i;
//    pid_pos->Kd=d;
//    pid_pos->Sv=sv;
//}
///**
// *@brief 绝对值函数
// */
//float abs_s(float a)
//{
//    float temp;
//    if(a>=0)
//    {
//        temp=a;
//    }
//    if(a<0)
//    {
//        temp=-a;
//    }
//    return temp;
//}

///*****************************这里是云台重点代码************/
///************** 5-舵机追踪色块位置环位置式PID **************/
////angle为舵机复位角度,中心位置
//void steer_to_track(uint16_t angle_x,uint16_t angle_y)
//{
//    int x_er=0,y_er=0; //定义两个变量去接收MV传送过来的偏差值
//    static float pid_steer_out=0; //X轴PID输出量
//    static float pid_steer_out_y=0; //Y轴PID输出量
//		x_er = Angle1;
//		y_er = Angle2;
//		if(x_er>100)
//			x_er = 0-(x_er - 100);
//		if(y_er>100)
//			y_er = 0-(y_er - 100);
////    get_steer_mid_err(&x_er,&y_er); //调用数据接收函数，接收OPENMV发来的偏差
//    pid_steer_out+=PID_position(&pid_steer,x_er); //X轴增量位置式PID输出
//    if(pid_steer_out>=1250)    //舵机角度限幅，以防转多了卡住
//		pid_steer_out=1250;
//		if(pid_steer_out<900)
//			pid_steer_out=900;	
////     OLED_ShowNum(0,5,pid_steer_out,4,16);
//		
////		OLED_ShowNum(0,3,x_er,10,16);
//		
//    
//    pid_steer_out_y+=PID_position(&pid_steer_y,y_er); 
//    if(pid_steer_out_y>=1600)   //舵机角度限幅
//		pid_steer_out_y=1600;
//		if(pid_steer_out_y<1300)
//			pid_steer_out_y=1300;	
////    OLED_ShowNum(30,5,pid_steer_out_y,4,16);//Y轴增量位置式PID输出
//		
////		OLED_ShowNum(0,5,y_er,10,16);//Y轴增量位置式PID输出
//		
//		TIM_SetCompare2(TIM3,(pid_steer_out+angle_x));
//		TIM_SetCompare4(TIM3,(-pid_steer_out_y+angle_y));
//      
//}
/*---------------------
负偏差往左边拐
正偏差往右边拐
---------------------*/


