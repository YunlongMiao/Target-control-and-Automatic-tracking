import sensor, image, time,lcd,utime

lcd.init() #初始化LCD
lcd.clear(lcd.WHITE) #清屏白色

sensor.reset() # 初始化摄像头
sensor.set_pixformat(sensor.RGB565) # 格式为 RGB565.
sensor.set_framesize(sensor.QVGA)

sensor.set_auto_whitebal(False)               # Create a clock object to track the FPS.
sensor.set_auto_exposure(1)                                 # 设置自动曝光
#sensor.set_auto_exposure(0, exposure=120000)               # 设置手动曝光 曝光时间 120000 us

#sensor.set_auto_gain(0, gain_db = 17)                       # 设置画面增益 17 dB 影响实时画面亮度
sensor.set_vflip(1)                                         # 打开垂直翻转 如果是 01Studio 的 K210 不开启会导致画面方向与运动方向相反
sensor.set_hmirror(1)

sensor.skip_frames(10) # 跳过10帧，使新设置生效

#keys = [1, 2, 4, 8, 16, 32]
#values = [0, 1, 2, 3, 4, 5]
## 合并成一个字典
#key_value_dict = dict(zip(keys, values))

#Color = ["红色","黄色","绿色","蓝色","黑色","白色"]
#Color_1 = [1,2,3,4,5,6]
#Color_2 = ["1:red","2:yellow","3:green","4:blue","5:black","6:white"]
red = (55, 85, 55, 80, 20, 80)
yellow = (60,110,-30,30,40,80)
green = (40,85,-60,-20,-5,25)
blue = (50,95,-35,15,-80,-15)
black = (-10,10,-10,10,-10,10)
white = (90,110,-10,10,-10,10)

ROI=(120,30,110,90)
ROI_Cir=(145,45,45,45)


def Judge_Color():
# 寻找圆形
    for c in img.find_circles(roi = ROI,threshold=1000, x_margin=10, y_margin=10, r_margin=10, r_min=2, r_max=100):
        img.draw_circle(c.x(), c.y(), c.r(), color = (255, 0, 0))
        #红色阈值，范围35*35，面积阈值200
        blobs = img.find_blobs([red,yellow,green,blue,black,white], roi = ROI, pixels_threshold = 200)
        # 找到面积最大的色块
        max_area = 0
        max_blob = None
        for blob in blobs:
            if blob.area() > max_area:
                max_area = blob.area()
                max_blob = blob

        # 检查是否找到了最大的色块
        if max_blob is not None:
            value = max_blob.code()
            print("Max blob code:", value)
        else:
            print("No blobs found")


while(True):
    img = sensor.snapshot()         # Take a picture and return the image.
    Judge_Color()
    #statistics=img.get_statistics(roi=ROI)
    #color_l=statistics.l_mode()
    #color_a=statistics.a_mode()
    #color_b=statistics.b_mode()
    #print(color_l,color_a,color_b)
    img.draw_rectangle(ROI)
    img.draw_rectangle(ROI_Cir)
    lcd.display(img)     #LCD显示图片

