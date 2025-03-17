import sensor, image, time,pyb
import ustruct
from pyb import UART
from pid import PID
from pyb import Servo

#(30, 69, 8, -20, -3, -109)
uart = UART(3, 115200,timeout_char=3000)


#Circle_Centle = (120,115)
#red_threshold  = (13, 49, 18, 64, 121, -98)
#red_threshold  = (89, 55, 47, 125, -66, 127)    #晚上22：31
#red_threshold  = (83, 55, 47, 95, -43, 71)     #下午16：23
red_threshold  = (85, 100, -15, 108, -106, 127)
green_threshold  = (41, 97, -101, -17, 95, 33)


X_Zero = 117
Y_Zero = 120

x_error=0.0; #X轴偏差,就是实际坐标减去中点坐标得到的误差，然后摄像头旋转去减少这个误差即可，以下变量同理
y_error=0.0; #Y轴偏差
pan_error=0.0; #X轴偏差
tilt_error=0.0; #Y轴偏差

pan_pid = PID(p=0.07, i=0.05, imax=90) #脱机运行或者禁用图像传输，使用这个PID
tilt_pid = PID(p=0.07, i=0.05, imax=90) #脱机运行或者禁用图像传输，使用这个PID

'''
全局变量
'''

# 舵机参数
servo_rotation = 1  #自转轴舵机序号,下舵机:X    舵机1的引脚编号
servo_pitch = 2     #仰俯轴舵机序号，上舵机:Y   舵机2的引脚编号

servo_pan  = pyb.Servo(1) # 初始化自转轴舵机1
servo_tilt = pyb.Servo(2) # 初始化俯轴舵机2



#RED_LED_PIN = 1
#BLUE_LED_PIN = 3
#lcd.init()
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





def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
    return max_blob




while True:
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot().lens_corr(strength = 1.7) # Take a picture and return the image.
    #img.draw_circle(119, 119, 1, color=(255, 0, 0), thickness=3) #描点函数,描绘中心点坐标
    blobs = img.find_blobs([red_threshold])

    if blobs:
        max_blob = find_max(blobs)
        pan_error = max_blob.cx()-X_Zero
        tilt_error = max_blob.cy()-Y_Zero

        pan_output=pan_pid.get_pid(pan_error,1)/2
        tilt_output=tilt_pid.get_pid(tilt_error,1)

        img.draw_cross(max_blob.cx(), max_blob.cy()) # cx, cy
        print(max_blob.cx(), max_blob.cy())
        print(pan_output, tilt_output)
        servo_pan.pulse_width(1060+int(pan_output*10))
        servo_tilt.pulse_width(1355-int(tilt_output*10))


