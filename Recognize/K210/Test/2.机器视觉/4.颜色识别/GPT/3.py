import time
import machine
#from machine import Servo
import sensor, image, time
import lcd  , UART
# 初始化颜色阈值
red_threshold = (30, 67, 10, 42, 2, 60)
green_threshold = (34, 94, -33, -17, -49, -21)
blue_threshold = (25, 61, -44, -11, 4, 43)
yellow_threshold = (61, 95, -22, -12, -35, 15)
white_threshold = (79, 5, 7, 21, -9, 22)
black_threshold = (7, 36, -6, 16, -10, 12)

## 初始化舵机
#servo1 = Servo(1)
#servo1.calibration(6400, 1200)

# 感光元件设置
sensor.reset()                                              # 重置并初始化感光元件 默认设置为 摄像头频率 24M 不开启双缓冲模式
#sensor.reset(freq=24000000, dual_buff=True)                # 设置摄像头频率 24M 开启双缓冲模式 会提高帧率 但内存占用增加

sensor.set_pixformat(sensor.RGB565)                         # 设置图像格式为 RGB565 (彩色) 除此之外 还可设置格式为 GRAYSCALE 或者 YUV422
sensor.set_framesize(sensor.QVGA)                           # 设置图像大小为 QVGA (320 x 240) 像素个数 76800 K210最大支持格式为 VGA

sensor.set_auto_exposure(1)                                 # 设置自动曝光
#sensor.set_auto_exposure(0, exposure=120000)               # 设置手动曝光 曝光时间 120000 us

sensor.set_auto_gain(0, gain_db = 17)                       # 设置画面增益 17 dB 影响实时画面亮度
sensor.set_auto_whitebal(0, rgb_gain_db = (0,0,0))          # 设置RGB增益 0 0 0 dB 影响画面色彩呈现效果 在 K210 上无法调节增益 初步判定是感光元件 ov2640 无法支持

# 不断获取图像，并进行颜色识别
while True:
    # 获取图像
    img = sensor.snapshot()

    # 检测红色乒乓球
    blobs = img.find_blobs([red_threshold])
    if blobs:
        # 找到最大的连通区域
        max_area = 0
        max_blob = None
        for blob in blobs:
            if blob.pixels() > max_area:
                max_area = blob.pixels()
                max_blob = blob

        # 绘制包围矩形及标记
        img.draw_rectangle(max_blob.rect())
        img.draw_cross(max_blob.cx(), max_blob.cy())

        ## 控制舵机转动
        #if max_blob.cx() < 80:
            #servo1.angle(20)  # 左转20度
        #elif max_blob.cx() > 180:
            #servo1.angle(160)  # 右转20度

        time.sleep(100)

    # 检测白色乒乓球
    blobs = img.find_blobs([white_threshold])
    if blobs:
        # 找到最大的连通区域
        max_area = 0
        max_blob = None
        for blob in blobs:
            if blob.pixels() > max_area:
                max_area = blob.pixels()
                max_blob = blob

        # 绘制包围矩形及标记
        img.draw_rectangle(max_blob.rect())
        img.draw_cross(max_blob.cx(), max_blob.cy())

        ## 控制舵机转动
        #if max_blob.cx() < 80:
            #servo1.angle(20)  # 左转20度
        #elif max_blob.cx() > 180:
            #servo1.angle(160)  # 右转20度

        time.sleep(100)

    # 检测蓝色乒乓球
    blobs = img.find_blobs([blue_threshold])
    if blobs:
        # 找到最大的连通区域
        max_area = 0
        max_blob = None
        for blob in blobs:
            if blob.pixels() > max_area:
                max_area = blob.pixels()
                max_blob = blob

        # 绘制包围矩形及标记
        img.draw_rectangle(max_blob.rect())
        img.draw_cross(max_blob.cx(), max_blob.cy())

        ## 控制舵机转动
        #if max_blob.cx() < 80:
            #servo1.angle(20)  # 左转20度
        #elif max_blob.cx() > 180:
            #servo1.angle(160)  # 右转20度

        time.sleep(100)

    # 检测黄色乒乓球
    blobs = img.find_blobs([yellow_threshold])
    if blobs:
        # 找到最大的连通区域
        max_area = 0
        max_blob = None
        for blob in blobs:
            if blob.pixels() > max_area:
                max_area = blob.pixels()
                max_blob = blob

# 绘制包围矩形及标记
        img.draw_rectangle(max_blob.rect())
        img.draw_cross(max_blob.cx(), max_blob.cy())

        ## 控制舵机转动
        #if max_blob.cx() < 80:
            #servo1.angle(20)  # 左转20度
        #elif max_blob.cx() > 180:
            #servo1.angle(160)  # 右转20度

        time.sleep(100)

    ## 如果没有检测到乒乓球，则舵机归位
    #servo1.angle(90)
    #time.sleep(100)

