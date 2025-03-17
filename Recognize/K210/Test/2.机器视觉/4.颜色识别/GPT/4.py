import time
import machine
from machine import UART
import sensor, image

# 初始化颜色阈值和数字代号
red_threshold = (30, 67, 10, 42, 2, 60)
red_id = 1
green_threshold = (34, 94, -33, -17, -49, -21)
green_id = 2
blue_threshold = (25, 61, -44, -11, 4, 43)
blue_id = 3
yellow_threshold = (61, 95, -22, -12, -35, 15)
yellow_id = 4
white_threshold = (79, 5, 7, 21, -9, 22)
white_id = 5
black_threshold = (7, 36, -6, 16, -10, 12)
black_id = 6

# 初始化相机
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_auto_exposure(1)                                 # 设置自动曝光
#sensor.set_auto_exposure(0, exposure=120000)               # 设置手动曝光 曝光时间 120000 us

sensor.set_auto_gain(0, gain_db = 17)                       # 设置画面增益 17 dB 影响实时画面亮度
sensor.set_auto_whitebal(0, rgb_gain_db = (0,0,0))          # 设置RGB增益 0 0 0 dB 影响画面色彩呈现效果 在 K210 上无法调节增益 初步判定是感光元件 ov2640 无法支持

#sensor.set_contrast(0)                                     # 设置对比度 0 这个参数无法读取 且调这个参数对画面似乎不会产生影响 暂时注释
#sensor.set_brightness(0)                                   # 设置亮度 0 这个参数无法读取 且调这个参数对画面似乎不会产生影响 暂时注释
#sensor.set_saturation(0)                                   # 设置饱和度 0 这个参数无法读取 且调这个参数对画面似乎不会产生影响 暂时注释

sensor.set_vflip(1)                                         # 打开垂直翻转 如果是 01Studio 的 K210 不开启会导致画面方向与运动方向相反
sensor.set_hmirror(1)                                       # 打开水平镜像 如果是 01Studio 的 K210 不开启会导致画面方向与运动方向相反

sensor.skip_frames(time = 2000)                             # 延时跳过2s 等待感光元件稳定
## 初始化串口
#uart = UART(2, 9600)

## 检测到乒乓球后输出串口数字代号
#def output_serial(id):
    #uart.write(str(id))

## 循环读取图像，并进行颜色识别
#while True:
    ## 获取图像
    #img = sensor.snapshot()

    ## 检测红色乒乓球
    #blobs = img.find_blobs([red_threshold])
    #if blobs:
        ## 找到最大的连通区域
        #max_area = 0
        #max_blob = None
        #for blob in blobs:
            #if blob.pixels() > max_area:
                #max_area = blob.pixels()
                #max_blob = blob

        ## 绘制包围矩形及标记
        #img.draw_rectangle(max_blob.rect())
        #img.draw_cross(max_blob.cx(), max_blob.cy())

        ## 输出数字代号
        #output_serial(red_id)

        #time.sleep(100)

    ## 检测绿色乒乓球
    #blobs = img.find_blobs([green_threshold])
    #if blobs:
        ## 找到最大的连通区域
        #max_area = 0
        #max_blob = None
        #for blob in blobs:
            #if blob.pixels() > max_area:
                #max_area = blob.pixels()
                #max_blob = blob

        ## 绘制包围矩形及标记
        #img.draw_rectangle(max_blob.rect())
        #img.draw_cross(max_blob.cx(), max_blob.cy())

        ## 输出数字代号
        #output_serial(green_id)

        #time.sleep(100)

    ## 检测蓝色乒乓球
    #blobs = img.find_blobs([blue_threshold])
    #if blobs:
        ## 找到最大的连通区域
        #max_area = 0
        #max_blob = None
        #for blob in blobs:
            #if blob.pixels() > max_area:
                #max_area = blob.pixels()
                #max_blob = blob

        ## 绘制包围矩形及标记
        #img.draw_rectangle(max_blob.rect())
        #img.draw_cross(max_blob.cx(), max_blob.cy())

        ## 输出数字代号
        #output_serial(blue_id)

        #time.sleep(100)

    ## 检测黄色乒乓球
    #blobs = img.find_blobs([yellow_threshold])
    #if blobs:
        ## 找到最大的连通区域
        #max_area = 0
        #max_blob = None
        #for blob in blobs:
            #if blob.pixels() > max_area:
                #max_area = blob.pixels()
                #max_blob = blob

        ## 绘制包围矩形及标记
        #img.draw_rectangle(max_blob.rect())
        #img.draw_cross(max_blob.cx(), max_blob.cy())

        ## 输出数字代号
        #output_serial(yellow_id)

        #time.sleep(100)

    ## 检测白色乒乓球
    #blobs = img.find_blobs([white_threshold])
    #if blobs:
        ## 找到最大的连通区域
        #max_area = 0
        #max_blob = None
        #for blob in blobs:
            #if blob.pixels() > max_area:
                #max_area = blob.pixels()
                #max_blob = blob

        ## 绘制包围矩形及标记
        #img.draw_rectangle(max_blob.rect())
        #img.draw_cross(max_blob.cx(), max_blob.cy())

        ## 输出数字代
        #output_serial(white_id)

        #time.sleep(100)

    ## 检测黑色乒乓球
    #blobs = img.find_blobs([black_threshold])
    #if blobs:
        ## 找到最大的连通区域
        #max_area = 0
        #max_blob = None
        #for blob in blobs:
            #if blob.pixels() > max_area:
                #max_area = blob.pixels()
                #max_blob = blob

        ## 绘制包围矩形及标记
        #img.draw_rectangle(max_blob.rect())
        #img.draw_cross(max_blob.cx(), max_blob.cy())

        ## 输出数字代号
        #output_serial(black_id)

        #time.sleep(100)
