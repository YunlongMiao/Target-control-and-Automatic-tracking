import sensor, image, time,pyb,lcd
import ustruct
from pyb import UART
#from pid import PID
#from pyb import Servo

#(30, 69, 8, -20, -3, -109)
uart = UART(3, 115200,timeout_char=3000)


#Circle_Centle = (120,115)
#red_threshold  = (13, 49, 18, 64, 121, -98)
red_threshold  = (89, 55, 47, 125, -66, 127)    #晚上22：31
#red_threshold  = (83, 55, 47, 95, -43, 71)     #下午16：23
green_threshold  = (41, 97, -101, -17, 95, 33)


X_Zero = 117
Y_Zero = 110

x_error=0.0; #X轴偏差,就是实际坐标减去中点坐标得到的误差，然后摄像头旋转去减少这个误差即可，以下变量同理
y_error=0.0; #Y轴偏差
pan_error=0.0; #X轴偏差
tilt_error=0.0; #Y轴偏差

RED_LED_PIN = 1
BLUE_LED_PIN = 3
lcd.init()
sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # 使用 RGB565.
sensor.set_framesize(sensor.QVGA) # 使用QVGA，320*240
clock = time.clock() # Tracks FPS.

sensor.skip_frames(time = 2000) #等待2秒感光器校准亮度/白平衡
sensor.set_auto_gain(False) #锁定自动亮度
sensor.set_auto_whitebal(False) #锁定自动白平衡
#sensor.set_windowing((240, 240))
sensor.set_windowing(28,0,240,240)  #剪裁画面
midpoint=160    #设置画面x轴向中值
sensor.set_auto_exposure(False,exposure_us=4000)    #设置固定帧速
sensor.set_contrast(3)  #设置对比度，范围-3~3
sensor.set_saturation(3)    #设置饱和度，范围-3~3


def sending_data(cx,cy):
    global uart;
    data = ustruct.pack("<bbhhb",      #格式为俩个字符俩个短整型(2字节)
                   0x2C,                      #帧头1
                   0x12,                      #帧头2
                   int (cx), # up sample by 4    #数据26
                   int (cy),
                   0x5B)
    uart.write(data);   #必须要传入一个字节数组


def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
    return max_blob


while(True):
    pyb.LED(BLUE_LED_PIN).on()
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot().lens_corr(strength = 1.7) # Take a picture and return the image.
    img.draw_circle(119, 119, 1, color=(255, 0, 0), thickness=3) #描点函数,描绘中心点坐标
    blobs = img.find_blobs([red_threshold])
    if blobs:
        max_blob = find_max(blobs)
        pan_error = max_blob.cx()-X_Zero
        tilt_error = max_blob.cy()-Y_Zero

        if(pan_error>0 or pan_error==0): #这里因为偏差值有负数，但是呢负数直接通过串口发送给单片机是不行的，所以当为负数时我就+100，也就是+50发的就是50，-50发的就是150
            x_error=pan_error
        if(pan_error<0):
            x_error=abs(pan_error)+100
        if(tilt_error>0 or tilt_error==0):
            y_error=tilt_error
        if(tilt_error<0):
            y_error=abs(tilt_error)+100
        #这里是画出色块的框
        #img.draw_rectangle(max_blob.rect()) # rect
        img.draw_cross(max_blob.cx(), max_blob.cy()) # cx, cy
        #sending_data(x_error, y_error)
        #print(x_error, y_error)
        #print(max_blob.cx(), max_blob.cy())
        x = max_blob.cx()
        y = max_blob.cy()
        #sending_data(x, y)
        output_bytes = bytearray([0xff, 0xfe,int((x-120+500)/4), int((y-120+500)/4),int(0),int(0),int(0),int(0),int(0),int(0)]) #x-140+500)/4控制值范围在0~255，为了stm32更好接收
        uart.write(output_bytes)           #串口把x，y传出去
        print(output_bytes)
        print(x,y)

        ##下边是串口发送数据代码，参考正点原子STM32的以\r\n结尾的协议
        #thousands=int(x_error/1000%10) #取千位
        #hundreds =int(x_error/100%10) #取百位
        #tens =int(x_error/10%10) #取十位
        #ones =int(x_error%10) #取个位
        ##将数字转化成ASCLL码发出去
        #thousands_str=str(thousands)
        #hundreds_str=str(hundreds)
        #tens_str=str(tens)
        #ones_str=str(ones)
       ## 同上
        #thousands_y=int(y_error/1000%10)
        #hundreds_y =int(y_error/100%10)
        #tens_y =int(y_error/10%10)
        #ones_y =int(y_error%10)
        #thousands_str_y=str(thousands_y)
        #hundreds_str_y=str(hundreds_y)
        #tens_str_y=str(tens_y)
        #ones_str_y=str(ones_y)
       ##这里整和数据x轴和y轴偏差发送过去
        #combined_str=thousands_str+hundreds_str+ tens_str+ ones_str+thousands_str_y+hundreds_str_y+ tens_str_y+ ones_str_y
        #uart.write(combined_str.encode())
        #uart.write('\r\n') #发送结尾必须以这个结尾,待会儿STM32端会说明
        #print("x_error: ", x_error)
        #print("y_error: ", y_error)

        ##sending_data(max_blob.cx(), max_blob.cy())
        #print(max_blob.cx(), max_blob.cy())
        #print(pan_error, tilt_error)
        #print(x_error, y_error)
