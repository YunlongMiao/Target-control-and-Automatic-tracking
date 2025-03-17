import sensor, image, time, pyb
from pyb import UART
import ustruct

x_max = 320
x_min = 0
x_1 = 135 #中心区域左边界
x_2 = 175 #中心区域右边界

y_max = 240
y_min = 0
y_1 = 110 #中心区域上边界
y_2 = 130 #中心区域下边界
flag = 0#位置信息标志


red_threshold   = (14, 68, 11, 70, 9, 56) #红色阈值设定

uart = UART(3, 115200)  #串口3初始化，波特率115200

sensor.reset() # 初始化摄像头传感器.
sensor.set_pixformat(sensor.RGB565) # 使用RGB565.
sensor.set_framesize(sensor.QVGA) # 使用QVGA.
sensor.skip_frames(10) # 让新设置生效.
sensor.set_auto_whitebal(False) # 关闭自动白平衡.
clock = time.clock() # Tracks FPS.




#**************************传输数据的函数************************************
def sending_data(cx,cy):
    global uart;
    #frame=[0x2C,18,cx%0xff,int(cx/0xff),cy%0xff,int(cy/0xff),0x5B];
    #data = bytearray(frame)
    data = ustruct.pack("<bbhhb",               #格式为俩个字符俩个短整型(2字节)
                   0x2C,                        #帧头1
                   0x12,                        #帧头2
                   int(cx), # up sample by 4    #数据1
                   int(cy), # up sample by 4    #数据2
                   0x5B)
    uart.write(data);   #必须要传入一字节的数组，这个函数似乎不能发送单个字节，必须得一次发送多个字节
    print(data[2])
#**************************************************************************



def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob.pixels() > max_size:
            max_blob=blob
            max_size = blob.pixels()
    return max_blob


while(True):
    img = sensor.snapshot() # 拍照并返回图像.
    blobs = img.find_blobs([red_threshold])
    if blobs:
        max_blob=find_max(blobs)
        img.draw_rectangle(max_blob.rect())
        img.draw_cross(max_blob.cx(), max_blob.cy())
        print(max_blob.cx(), max_blob.cy())

    if max_blob.cx()>= x_min  and max_blob.cx() <= 160 and max_blob.cy() >= 120 and max_blob.cy() <= y_max :
            flag = 1
    if max_blob.cx()>=160 and max_blob.cx() <= x_max and max_blob.cy() >=120 and max_blob.cy() <= y_max :
            flag = 2
    if max_blob.cx()>= x_min and max_blob.cx() <= 160 and max_blob.cy() >= y_min and max_blob.cy() <= 120 :
            flag = 3
    if max_blob.cx()>= 160 and max_blob.cx() <= x_max and max_blob.cy() >= y_min and max_blob.cy() <= 120 :
            flag = 4
    if max_blob.cx()>= x_1 and max_blob.cx() <= x_2   and max_blob.cy() >= y_1 and max_blob.cy() <= y_2 :
            flag = 5

    sending_data(flag)







