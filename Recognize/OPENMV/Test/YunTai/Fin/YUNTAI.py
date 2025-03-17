import sensor, image, time,pyb
from pyb import Servo
from pyb import Pin

'''
设置摄像头QVGA、降低亮度
'''
def sensor_set_QVGA_dark():
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    #sensor.set_vflip(True)  #针对我的硬件，颠倒画面
    #sensor.set_hmirror(True)
    sensor.set_brightness(0)   #设置亮度
    sensor.set_contrast(10) #对比度
    #sensor.set_gainceiling(2)   #增益上限
    #sensor.set_auto_gain(False,gain_db=-1) #增益
    sensor.set_auto_exposure(False,500)  #曝光速度
sensor_set_QVGA_dark()#运行一次，对摄像头初始化

clock = time.clock()

red_threshold = (60, 97, -81, -18, 23, 73)
track_color = (255, 0, 0)
roi = (10,10, sensor.width(), sensor.height())

s1 = Servo(1) # P7 左右 + -
s2 = Servo(2) # P8 上下 - +
yd=[-42,-12]#原点
bk=[-52,-1,-32,-1,-32,-19,-51,-19,-52,0]#边框 右下 左下 左上 右上
hx=[-32,-19,-43,-19,-43,-12,-32,-13,-33,-19]#黑框
xk=[-32,-9,-39,-15,-46,-7,-40,-1,-32,-10]#黑框
def YD( x,y ):#舵机中心
        s1.angle(x)#左右 -右 +左
        s2.angle(y)#上下 —上 +下
pin0 = Pin('P0', Pin.IN, Pin.PULL_UP)
pin1 = Pin('P1', Pin.IN, Pin.PULL_UP)
pin2 = Pin('P2', Pin.IN, Pin.PULL_UP)
pin3 = Pin("P3", Pin.IN, Pin.PULL_UP)
flag_key1=0
flag_key2=0
flag_key3=0
flag_key4=0
i=500
y=0
def callback_PIN0(line):
    global flag_key1
    flag_key1=1
    pyb.delay(10)
def callback_PIN1(line):
    global flag_key2
    flag_key2=1
    pyb.delay(10)
def callback_PIN2(line):
    global flag_key3
    flag_key3=1
    pyb.delay(10)
def callback_PIN3(line):
    global flag_key4
    flag_key4=1
    pyb.delay(10)
extint = pyb.ExtInt(pin0, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, callback_PIN0)
extint = pyb.ExtInt(pin1, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, callback_PIN1)
extint = pyb.ExtInt(pin2, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, callback_PIN2)
extint = pyb.ExtInt(pin3, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, callback_PIN3)
#红点识别

while(True):
    clock.tick()
    img = sensor.snapshot()
    if flag_key1==1 and pin0.value()==0:
       YD(yd[0],yd[1])
       flag_key1=0
       pin3.high()
    if flag_key2==1 and pin1.value()==0:
       YD(bk[0],bk[1])
       time.sleep_ms(i)
       YD(bk[2],bk[3])
       time.sleep_ms(i)
       YD(bk[4],bk[5])
       time.sleep_ms(i)
       YD(bk[6],bk[7])
       time.sleep_ms(i)
       YD(bk[8],bk[9])
       flag_key2=0
    if flag_key3==1 and pin2.value()==0:
       YD(hx[0],hx[1])
       time.sleep_ms(i)
       YD(hx[2],hx[3])
       time.sleep_ms(i)
       YD(hx[4],hx[5])
       time.sleep_ms(i)
       YD(hx[6],hx[7])
       time.sleep_ms(i)
       YD(hx[8],hx[9])
       flag_key3=0
    if flag_key4==1 and pin3.value()==0:
       YD(xk[0],xk[1])
       time.sleep_ms(i)
       YD(xk[2],xk[3])
       time.sleep_ms(i)
       YD(xk[4],xk[5])
       time.sleep_ms(i)
       YD(xk[6],xk[7])
       time.sleep_ms(i)
       YD(xk[8],xk[9])
       flag_key4=0
