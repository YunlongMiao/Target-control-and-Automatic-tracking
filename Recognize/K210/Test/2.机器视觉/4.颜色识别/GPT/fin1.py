import sensor, image, time,lcd,utime
from machine import UART
from Maix import GPIO
from fpioa_manager import fm


lcd.init() #初始化LCD
lcd.clear(lcd.WHITE) #清屏白色


#注册IO，蓝灯-->IO12,KEY-->IO16
fm.register(12, fm.fpioa.GPIO0)
fm.register(16, fm.fpioa.GPIO1)

#初始化IO
LED_B = GPIO(GPIO.GPIO0, GPIO.OUT)
KEY = GPIO(GPIO.GPIO1, GPIO.IN)

#映射UART2的两个引脚
fm.register(GPIO.GPIOHS11,fm.fpioa.UART2_TX)
fm.register(GPIO.GPIOHS10,fm.fpioa.UART2_RX)
#初始化串口，返回调用句柄
uart_A = UART(UART.UART2, 115200, 8, None)

sensor.reset() # 初始化摄像头
sensor.set_pixformat(sensor.RGB565) # 格式为 RGB565.
sensor.set_framesize(sensor.QVGA)

sensor.set_auto_whitebal(False)               # Create a clock object to track the FPS.
#sensor.set_auto_exposure(1)                                 # 设置自动曝光
#sensor.set_auto_exposure(0, exposure=120000)               # 设置手动曝光 曝光时间 120000 us

sensor.set_auto_gain(0, gain_db = 17)                       # 设置画面增益 17 dB 影响实时画面亮度
sensor.set_vflip(1)                                         # 打开垂直翻转 如果是 01Studio 的 K210 不开启会导致画面方向与运动方向相反
sensor.set_hmirror(1)

sensor.skip_frames(10) # 跳过10帧，使新设置生效

red = (5, 55, 20, 80, 10, 80)
yellow = (60,130,-40,30,40,100)
green = (0,60,-75,-10,-10,50)
blue = (30,95,-35,35,-80,-15)
black = (-10,10,-10,10,-10,10)
white = (70,110,-10,10,-10,10)
#1225
#ROI=(145,45,35,35)
#ROI=(145,45,60,60)
ROI=(115,78,48,48)
ROI_Cir=(120,30,110,90)

#         0,1,2,3,4, 5
#Color_judge  = [1,2,4,8,16,32]

# 定义两个数组
keys = [1, 2, 4, 8, 16, 32]
values = [0, 1, 2, 3, 4, 5]
# 合并成一个字典
key_value_dict = dict(zip(keys, values))

Color = ["红色","黄色","绿色","蓝色","黑色","白色"]
Color_1 = (1,2,3,4,5,6)
Color_2 = ["1:red","2:yellow","3:green","4:blue","5:black","6:white"]

def Judge_Color():
    if 1:
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
            value = key_value_dict[max_blob.code()] # key_value_dict[8]返回3
            #uart_A.write(Color_1[value])
            #uart_A.write(value)
            #print("Max blob code:", max_blob.code())
            #print("Color:", Color_1[value])

            #lcd.draw_string(110, 120, Color_2[value],lcd.BLACK, lcd.WHITE) #显示字符
            #utime.sleep(0.5) #延时2秒
            #lcd.draw_string(110, 135, Color_1[value],lcd.BLACK, lcd.WHITE) #显示字符
            #return Color_1[value]max_blob.code()
            return Color_1[value]
            #print("Max blob code:", max_blob.code())

#if KEY.value()==0: #按键被按下接地
    #LED_B.value(0) #点亮LED_B,蓝灯
#else:
    #LED_B.value(1) #熄灭LED
while(True):
    img = sensor.snapshot()         # Take a picture and return the image.
    #statistics=img.get_statistics(roi=ROI)
    #color_l=statistics.l_mode()
    #color_a=statistics.a_mode()
    #color_b=statistics.b_mode()
    #print(color_l,color_a,color_b)
    #Judge_Color();
    #byte_data = uart_A.read(8)
    #if byte_data != None:
        #Color = Judge_Color()
        #if Color != None:
            #uart_A.write(Color)
    if KEY.value()==0: #按键被按下接地
        Color = Judge_Color()
        if Color != None:
            print(Color)
            #uart_A.write(Color)
    img.draw_rectangle(ROI)
    #img.draw_rectangle(ROI_Cir)
    lcd.display(img)     #LCD显示图片



#while(True):
    #img = sensor.snapshot()         # Take a picture and return the image.
    ##Judge_Color();
    #byte_data = uart_A.read(8)
    #if byte_data != None:
        #print("recv = ", byte_data) # 输出收到的数据
        #utime.sleep(1) #延时2秒
        #data_str = byte_data.decode('utf-8')
        #print(data_str)
        #if(data_str == '6')
            #print(data_str)
        #uart_A.write(byte_data)
    #img.draw_rectangle(ROI)
    #img.draw_rectangle(ROI_Cir)
    #lcd.display(img)     #LCD显示图片


#while(True):
    #img = sensor.snapshot()         # Take a picture and return the image.
    #read_str = uart_A.read(10)
    ##if read_str == 4:
    #if read_str != None:
        #uart_A.write('ok\r\n')
        #utime.sleep(1) #延时2秒
        #Color_Temp = Judge_Color()
        #print(Color_Temp)
        #uart_A.write(Color_Temp)
    #img.draw_rectangle(ROI)
    #img.draw_rectangle(ROI_Cir)
    #lcd.display(img)     #LCD显示图片






#count = 0     # 初始化计数器
#i = 0
#flag = 0

#while(True):
    #img = sensor.snapshot()         # Take a picture and return the image.

    #read_str = uart_A.read(10)
    #if read_str == 4:
        #flag = 1
    #if flag:
        #t_end = utime.ticks_ms() + 1000      # t_end表示计时结束的时间
        #while utime.ticks_ms() < t_end:
            #Color_Temp = Judge_Color()
            #i++
        #count = 0
        #flag = 0
    #img.draw_rectangle(ROI)
    #img.draw_rectangle(ROI_Cir)
    #lcd.display(img)     #LCD显示图片
    #uart_A.write(Color_Temp)

#count = 0     # 初始化计数器
#total_color = 0    # 初始化颜色计数器

#while(True):
    #img = sensor.snapshot()         # 获取图像
    #img.draw_rectangle(ROI)
    #img.draw_rectangle(ROI_Cir)
    #lcd.display(img)     #LCD显示图片
    ## 检查 uart_A 上是否有数据
    #read_str = uart_A.read(10)
    ##if read_str == 4:
    #if 1:
        ## 如果 uart_A 上有数据，则在 1 秒钟内运行函数 Judge_Color() 多次
        #t_end = utime.ticks_ms() + 1000      # t_end表示计时结束的时间
        #total_color = 0
        #while utime.ticks_ms() < t_end:
            #Color_Temp = Judge_Color()   # 传递参数
            #if Color_Temp == None:
                #continue
            #total_color += Color_Temp    # 记录颜色数
            #count += 1                  # 记录成功次数
            #lcd.draw_string(110, 120, str(Color_Temp),lcd.BLACK, lcd.WHITE) #显示字符
            #lcd.draw_string(110, 130, str(total_color),lcd.BLACK, lcd.WHITE) #显示字符
            #lcd.draw_string(110, 140, str(count),lcd.BLACK, lcd.WHITE) #显示字符
        ## 计算并输出平均颜色
        #if count > 0:
            #avg_color = total_color / count
            #print(avg_color)

        ## 重置计数器
        #count = 0
        #total_color = 0



#while(True):
    #img = sensor.snapshot()         # Take a picture and return the image.
    #read_str = uart_A.read(10)
    #if read_str == 4:
        #Color_Temp = Judge_Color()
        #print(Color_Temp)
    #img.draw_rectangle(ROI)
    #img.draw_rectangle(ROI_Cir)
    #lcd.display(img)     #LCD显示图片
    #uart_A.write(Color_Temp)
