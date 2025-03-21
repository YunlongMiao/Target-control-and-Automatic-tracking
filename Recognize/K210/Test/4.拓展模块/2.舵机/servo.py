'''
实验名称：舵机控制
版本：v1.0
日期：2019.12
作者：01Studio 【www.01Studio.org】
说明：通过编程控制舵机旋转到不同角度
'''

from machine import Timer,PWM
import time

#PWM通过定时器配置，接到IO17引脚
tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
S1 = PWM(tim, freq=50, duty=0, pin=17)

'''
#4路舵机代码定义,利用定时器的4个通道。

tim2 = Timer(Timer.TIMER0, Timer.CHANNEL1, mode=Timer.MODE_PWM)
S2 = PWM(tim2, freq=50, duty=0, pin=35)

tim3 = Timer(Timer.TIMER0, Timer.CHANNEL2, mode=Timer.MODE_PWM)
S3 = PWM(tim3, freq=50, duty=0, pin=34)

tim4 = Timer(Timer.TIMER0, Timer.CHANNEL3, mode=Timer.MODE_PWM)
S4 = PWM(tim4, freq=50, duty=0, pin=33)
'''


'''
说明：舵机控制函数
功能：180度舵机：angle:-90至90 表示相应的角度
     360连续旋转度舵机：angle:-90至90 旋转方向和速度值。
    【duty】占空比值：0-100
'''

def Servo(servo,angle):
    servo.duty((angle+90)/180*10+2.5)


while True:
    #-90度
    Servo(S1,-90)
    time.sleep(1)

    #-45度
    Servo(S1,-45)
    time.sleep(1)

    #0度
    Servo(S1,0)
    time.sleep(1)

    #45度
    Servo(S1,45)
    time.sleep(1)

    #90度
    Servo(S1,90)
    time.sleep(1)
