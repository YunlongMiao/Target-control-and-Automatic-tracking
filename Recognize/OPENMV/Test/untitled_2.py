import sensor, image, time
import json
from pyb import UART


blue_threshold   = (22, 67, 9, 127, -128, -54)#蓝色的阈值
red_threshold   = (41, 61, 42, 127, -128, 127)#红色的阈值
yellow_threshold   = ( 60 ,10,-15,20,30,80)#黄色的阈值


sensor.set_hmirror(True)
sensor.set_vflip(True)
sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # use RGB565.
sensor.set_framesize(sensor.QQVGA) # use QQVGA for speed.
sensor.skip_frames(10) # Let new settings take affect.
sensor.set_auto_whitebal(False) # turn this off.
clock = time.clock() # Tracks FPS.


uart = UART(3, 9600)#波特率两边要设置成一样

#定义一个函数，返回最大色块的坐标，因为在寻找同一颜色的色块时，可能存在多个同一颜色的色块，故我们只需要找到最大的色块即可
def find_max(blobs):
    max_size=0
    for blob in blobs:
       if blob.pixels() > max_size:
            max_blob=blob
            max_size = blob.pixels()
    return max_blob #寻找最大色块并返回最大色块的坐标


while(True):
    clock.tick()
    img = sensor.snapshot()
#初始化
    blobs0 = img.find_blobs([blue_threshold])#让蓝色色块为blob0
    blobs1 = img.find_blobs([red_threshold])#让蓝色色块为blob1
    blobs2 = img.find_blobs([yellow_threshold])#让蓝色色块为blob2



    #如果找到蓝色色块
    if blobs0:
     max_blob=find_max(blobs0)
     img.draw_rectangle(max_blob.rect())#框选最大色块
     img.draw_cross(max_blob.cx(), max_blob.cy())#在最大色块中心画十字
     data="0"
     data_out = json.dumps(set(data))#将data转化为json
     uart.write(data_out +'\n')#写到缓冲区，由arduino进行读取
     print('you send:',data_out)#写到串口监视端，让你能够看到数据


    elif blobs1:
     max_blob=find_max(blobs1)
     img.draw_rectangle(max_blob.rect())#框选最大色块
     img.draw_cross(max_blob.cx(), max_blob.cy())#在最大色块中心画十字
     data="1"
     data_out = json.dumps(set(data))
     uart.write(data_out +'\n')
     print('you send:',data_out)


    elif blobs2:
     max_blob=find_max(blobs2)
     img.draw_rectangle(max_blob.rect())#框选最大色块
     img.draw_cross(max_blob.cx(), max_blob.cy())#在最大色块中心画十字
     data="{'key': 'wwww', 'word': 'qqqq'}"
     data_out = json.dumps((data))
     uart.write(data_out +'\n')
     print('you send:',data_out)
    else:
        print('not found')
