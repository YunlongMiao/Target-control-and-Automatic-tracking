#OpenMV 摄像头有一个 RGB LED 和两个红外 LED 灯。您可以单独控制 RGB LED 的红色，绿色和蓝色区段，将两个 IR LED 控制为一个单位。

#要控制 LED，首先导入 pyb 模块。然后为要控制的特定 LED 创建一个 LED 类对象pyb.LED(number) 创建一个 LED 对象，您可以使用它来控制特定的 LED。

#通过 pyb.LED 1”控制红色 RGB LED 段， “2”控制绿色 RGB LED 段， “3”控制蓝色 RGB LED 段， “4”控制两个红外 LED

#LED引脚排列：

#LED（1）->红色RGB LED段
#LED（2）->绿色RGB LED分段
#LED（3）->蓝色RGB LED段
#LED（4）->红外LED

#当使用的 IR 镜头（这是没有红外线滤镜的镜头）更换您的 OpenMV Cam 的常规镜头时，您可以打开红外LED，以使您的 OpenMV Cam 可以在黑暗中看到。红外 LED 足够亮，可以在黑色的 OpenMV Cam 前面照亮 3 米左右

#LED.off()
#关闭LED。

#LED.on()
#打开LED，达到最大强度。

#LED.toggle()
#切换LED的开（最大强度）关。若LED在非零强度下，则会被认为已打开，随之被切换为关。


# Main Module Example
#
# 当OpenMV摄像头从电脑断开时，它会运行SD卡上的main.py脚本(如果插了内存卡)或你的OpenMV摄像头内部Flash里的main.py脚本。






#example
#import time, pyb

##将蓝灯赋值给变量led
#led = pyb.LED(3) # Red LED = 1, Green LED = 2, Blue LED = 3, IR LEDs = 4.
#usb = pyb.USB_VCP() # This is a serial port object that allows you to
## communciate with your computer. While it is not open the code below runs.


##如果openmv未连接到电脑，蓝灯亮150ms，延时100ms，亮150ms，延时600ms，循环。
#while(not usb.isconnected()):
    #led.on()            #亮灯
    #time.sleep_ms(150)     #延时150ms
    #led.off()           #暗灯
    #time.sleep_ms(100)
    #led.on()
    #time.sleep_ms(150)
    #led.off()
    #time.sleep_ms(600)

##变量led此时代表绿灯
#led = pyb.LED(2) # 切换到使用绿色led。

##如果openmv已连接到电脑
#while(usb.isconnected()):
    #led.on()
    #time.sleep_ms(150)
    #led.off()
    #time.sleep_ms(100)
    #led.on()
    #time.sleep_ms(150)
    #led.off()
    #time.sleep_ms(600)



#2
import time,pyb

led1 = pyb.LED(1)
led2 = pyb.LED(2)
led3 = pyb.LED(3)


while (True):
    led1.on()
    time.sleep_ms(500)
    led1.off()
    time.sleep_ms(500)

    led2.on()
    time.sleep_ms(500)
    led2.off()
    time.sleep_ms(500)

    led3.on()
    time.sleep_ms(500)
    led3.off()
    time.sleep_ms(500)

