#ifndef __PID_H
#define __PID_H
#include "sys.h"

void steer_to_track(uint16_t angle_x,uint16_t angle_y);

#define PI 3.14159265
#define FILTERING_TIMES  10
#define ZERO_X 139
#define ZERO_Y 113























//typedef struct //位置式PID结构体
//{

//    float Sv;//设定值
//	float Kp;//比例
//	float Kd;//微分
//	float Ki;//积分
//	float EK;//误差
//	float EK_NEXT;//上次偏差
//	float SUM_EK;//历史偏差之和，用于积分累加
//	float OUT;//PID输出，可以是PWM占空比，可以是测距偏差，可以是输出温度（温控PID）
//}PID;
//typedef struct
//{ 
//    float Sv;//设定值
//	float Kp;//比例
//	float Kd;//微分
//	float Ki;//积分
//	float EK;//误差
//	float EK_LAST;//上次偏差    
//    float EK_LAST_LAST;//上上次偏差
//	float OUT; //PWM输出
//}PID_INC;
//typedef struct //位置式PID结构体
//{

//    float Sv;//设定值
//	float Kp;//比例
//	float Kd;//微分
//	float Ki;//积分
//	float EK;//误差
//	float EK_NEXT;//上次偏差
//	float SUM_EK;//历史偏差之和，用于积分累加
//	float OUT;//PID输出，可以是PWM占空比，可以是测距偏差，可以是输出温度（温控PID）
//}PID_POS;
//float PID_Increase(PID_INC *pid_inc,float actual_data);
//float PID_position(PID_POS *pid_pos,float actual_data);
//void set_pid_inc_param(PID_INC *pid_inc,float p,float i,float d,float sv);
//void set_pid_pos_param(PID_POS *pid_pos,float p,float i,float d,float sv);
//void openmv_to_track(uint16_t v);
//float gryo_to_turn(uint16_t v);
//void distance_to_hold(uint16_t v);
//void motor_speed_control_L(void);
//void motor_speed_control_R(void);
//void circle_to_turn(uint16_t v);
//void steer_to_track(uint16_t angle_x,uint16_t angle_y);
//float abs_s(float a);
//extern PID_POS pid_openmv;      //摄像头位置式PID结构体
//extern PID_POS pid_gyro;        //陀螺仪位置式PID结构体
//extern PID_POS pid_dis;         //距离保持位置式PID结构体
//extern PID_INC pid_speed_L;     //左轮电机速度增量式PID结构体
//extern PID_INC pid_speed_R;     //右轮电机速度增量式PID结构体
//extern PID_POS pid_encoder;     //电机编码器圈数位置环PID结构体
//extern PID_POS pid_steer;       //舵机云台追踪色块位置环PID结构体
//extern PID_POS pid_steer_y;     //舵机云台追踪色块位置环PID结构体y轴
//extern int E_flag;//循迹偏离值

#endif
