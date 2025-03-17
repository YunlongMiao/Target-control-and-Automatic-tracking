# Untitled - By: 30824 - 周三 8月 2 2023

import sensor, image, time
import ustruct
from pyb import UART

red_threshold  = (100, 0, 127, 29, -114, 113)
green_threshold  = (100, 62, 127, -125, -128, 127)


uart = UART(3, 9600,timeout_char=3000)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((240, 240))
sensor.set_auto_gain(False)
sensor.skip_frames(20) # Let new settings take affect.
#sensor.set_auto_exposure(False, 2700)
sensor.set_auto_whitebal(False) # turn this off.

clock = time.clock()

def sending_data(cx,cy):
    global uart;
    data = ustruct.pack("<bbhhb",      #格式为俩个字符俩个短整型(2字节)
                   0x2C,                      #帧头1
                   0x12,                      #帧头2
                   int (cx), # up sample by 4    #数据26
                   int (cy),
                   0x5B)
    uart.write(data);   #必须要传入一个字节数组


def color_blob(threshold):
    blobs = img.find_blobs([green_threshold])
    if len(blobs) == 1:
        # Draw a rect around the blob.
        b = blobs[0]
        img.draw_rectangle(b[0:4]) # rect
        cx = b[5]
        cy = b[6]
        img.draw_cross(b[5], b[6]) # cx, cy
        print(cx,cy)
        sending_data(cx,cy)
        return cx, cy
    return 160, 120



while(True):
    clock.tick()
    img = sensor.snapshot().lens_corr(strength = 1.5, zoom = 0.9)
    color_blob(green_threshold)
    #print(clock.fps())
