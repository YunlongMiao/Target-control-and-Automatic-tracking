# Untitled - By: 30824 - 周日 7月 30 2023

from Maix import GPIO
from fpioa_manager import fm

#注册IO，蓝灯-->IO12,KEY-->IO16
fm.register(12, fm.fpioa.GPIO0)
fm.register(16, fm.fpioa.GPIO1)

#初始化IO
LED_B = GPIO(GPIO.GPIO0, GPIO.OUT)
KEY = GPIO(GPIO.GPIO1, GPIO.IN)

while True:

    if KEY.value()==0: #按键被按下接地
        LED_B.value(0) #点亮LED_B,蓝灯
    else:
        LED_B.value(1) #熄灭LED
