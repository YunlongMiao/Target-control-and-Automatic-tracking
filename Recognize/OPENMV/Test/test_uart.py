# Untitled - By: 30824 - 周日 7月 30 2023

#import json,ujson

#obj = [[12,0],[10,12],[22,10],[99,11]]
#print(json.dumps(obj))

#obj = {
    #"number":10,
    #"color" :[255,0,0],
    #"rate" :0.65,
    #"sfss":[6,64,420.02]
#}

#str1 = json.dumps(obj)
#print(str1)


#str2 = ujson.loads(str1)
#print(str2)




import time,pyb
from pyb import UART
import ujson,json


led = pyb.LED(3)
uart = UART(3,115200)

while True:
    #print("START")
    if (uart.any()):     #如果串口有数据
        time.sleep_ms(200)
        led.off()
        da = uart.readline().decode() #.strip() #.split(',') #读取串口数据, bytes转 str

        print(type(da))
        db = json.dumps(da)
        print(type(dd))
        #dd = eval(da)      #str 转 dict
        jsObj = ujson.loads(dd) #解析JSON
        print(type(jsObj))      #输出json格式
        print(jsObj)

        for key in jsObj.keys():
            print('key:%s    values: %s' % (key,jsObj.get()) )

        if(jsObj.get("d") == 20180901):
            print("OK")
    else:
       led.on()
    time.sleep_ms(1000)














#import sensor, image, time, math, pyb
#from pyb import UART
#import json
#import ustruct

#uart = UART(3, 115200)
#uart.init(115200, bits=8, parity=None, stop=1) # OpenMV端初始化与STM端配置一样即可。


##**************************传输数据的函数************************************
#def sending_data(cx,cy):
    #global uart;
    ##frame=[0x2C,18,cx%0xff,int(cx/0xff),cy%0xff,int(cy/0xff),0x5B];
    ##data = bytearray(frame)
    #data = ustruct.pack("<bbhhb",               #格式为俩个字符俩个短整型(2字节)
                   #0x2C,                        #帧头1
                   #0x12,                        #帧头2
                   #int(cx), # up sample by 4    #数据1
                   #int(cy), # up sample by 4    #数据2
                   #0x5B)
    #uart.write(data);   #必须要传入一字节的数组，这个函数似乎不能发送单个字节，必须得一次发送多个字节
##**************************************************************************
#while True:
    #sending_data(95,625)
    #time.sleep_ms(500)
