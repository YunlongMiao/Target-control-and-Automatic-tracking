# Untitled - By: 30824 - 周三 8月 2 2023

import sensor, image, time
from pyb import UART
import json


red_threshold  = [(13, 49, 18, 64, 121, -98) ]
green_threshold  = [(41, 97, -101, -17, 95, 33)]


sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((240, 240))
sensor.skip_frames(time = 2000)
sensor.set_auto_whitebal(False)

clock = time.clock()

uart = UART(3, 115200)

uart.init(115200, bits=8, parity=None, stop=1)  #8位数据位，无校验位，1位停止位、


while(True):
    clock.tick()
    img = sensor.snapshot()
    blob = img.find_blobs(green_threshold, area_threshold=300)
    if blob: #如果找到了目标颜色
        FH = bytearray([0xb3,0xb4])
        uart.write(FH)
        for b in blob:
        #迭代找到的目标颜色区域
            img.draw_cross(b[5], b[6]) # cx, cy
            img.draw_edges(b.min_corners(), color=(0,255,0))
            x = b.cx()
            y = b.cy()
            print(x,y)
