# Timer_V1.0 - By: FITQY - 周二 8 月 23 日 2022
#__________________________________________________________________
# 导入模块
import sensor, time, image                                  # 导入感光元件模块 sensor 跟踪运行时间模块 time 机器视觉模块 image
import utime                                                # 导入延时模块 utime
from fpioa_manager import fm                                # 从 GPIO 模块中导入 引脚注册模块 fm
from Maix import GPIO                                       # 从 Maix 模块中导入 模块 GPIO
import lcd                                                  # 导入 LCD 模块
from machine import Timer, PWM                              # 从 machine 模块中导入 定时器模块 Timer 脉宽调制模块 PWM

#__________________________________________________________________
# 感光元件设置
sensor.reset()                                              # 重置并初始化感光元件 默认设置为 摄像头频率 24M 不开启双缓冲模式
#sensor.reset(freq=24000000, dual_buff=True)                # 设置摄像头频率 24M 开启双缓冲模式 会提高帧率 但内存占用增加

sensor.set_pixformat(sensor.RGB565)                         # 设置图像格式为 RGB565 (彩色) 除此之外 还可设置格式为 GRAYSCALE 或者 YUV422
sensor.set_framesize(sensor.QVGA)                           # 设置图像大小为 QVGA (320 x 240) 像素个数 76800 K210最大支持格式为 VGA

sensor.set_auto_exposure(1)                                 # 设置自动曝光
#sensor.set_auto_exposure(0, exposure=120000)               # 设置手动曝光 曝光时间 120000 us

sensor.set_auto_gain(0, gain_db = 12)                       # 设置画面增益 17 dB 影响实时画面亮度
sensor.set_auto_whitebal(0, rgb_gain_db = (0,0,0))          # 设置RGB增益 0 0 0 dB 影响画面色彩呈现效果 在 K210 上无法调节增益 初步判定是感光元件 ov2640 无法支持

#sensor.set_contrast(0)                                     # 设置对比度 0 这个参数无法读取 且调这个参数对画面似乎不会产生影响 暂时注释
#sensor.set_brightness(0)                                   # 设置亮度 0 这个参数无法读取 且调这个参数对画面似乎不会产生影响 暂时注释
#sensor.set_saturation(0)                                   # 设置饱和度 0 这个参数无法读取 且调这个参数对画面似乎不会产生影响 暂时注释

sensor.set_vflip(1)                                         # 打开垂直翻转 如果是 01Studio 的 K210 不开启会导致画面方向与运动方向相反
sensor.set_hmirror(1)                                       # 打开水平镜像 如果是 01Studio 的 K210 不开启会导致画面方向与运动方向相反

sensor.skip_frames(time = 2000)                             # 延时跳过2s 等待感光元件稳定

#__________________________________________________________________
# 创建时钟对象
clock = time.clock()                                        # 创建时钟对象 clock

#__________________________________________________________________
# 打印sensor参数
def print_sensor():
    print("Exposure: "+str(sensor.get_exposure_us()))       # 打印 曝光时间
    print("Gain: "+str(sensor.get_gain_db()))               # 打印 画面增益
    print("RGB: "+str(sensor.get_rgb_gain_db()))            # 打印 RGB 增益

#__________________________________________________________________
# 目标点输入类 举例 对标 2022 年 TI 杯送货无人机 中的目标点输入部分
class point_input():
    point1  = 0                                             # 目标点 1
    point2  = 0                                             # 目标点 2
    cross   = 0                                             # 穿圈模式标志位
    send    = 0                                             # 目标点发送标志位

point = point_input()                                       # 实例化目标点输入类 point_input() 为 point

# 按键控制下的目标点获取函数
def point_control(ckey):
    if ckey.control == 1:                                   # 按键确认及发送控制标志位为1 即 按键3 按下
        ckey.control = 0                                    # 重置标志位
        if ckey.cs == 0:                                    # 如果当前为模式 0
            point.send = 1                                  # 目标点发送标志置为 1 串口开始发送

        elif ckey.cs == 1:                                  # 如果当前为模式 1
            point.point1 = ckey.cinput                      # 将按键输入值赋值给目标点 1

        elif ckey.cs == 2:                                  # 如果当前为模式 2
            point.point2 = ckey.cinput                      # 将按键输入值赋值给目标点 2

        elif ckey.cs == 3:                                  # 如果当前为模式 3
            point.cross = ckey.cinput                       # 将按键输入值赋值给 穿圈模式标志位

    if ckey.csflag == 1:                                    # 如果检测到按键模式切换
        ckey.csflag = 0                                     # 重置按键模式切换标志位
        ckey.cinput = 0                                     # 重置按键输入值

#__________________________________________________________________
# 按键的使用
# 定义按键控制类
class key_control():                                        # 定义按键控制类
    cnt     = 0                                             # 按键计数值
    cs      = 0                                             # 按键模式选择标志位
    csmax   = 0                                             # 按键模式上限
    csflag  = 0                                             # 按键模式切换标志位
    cinput  = 0                                             # 按键输入值保存位
    control = 0                                             # 按键确认及发送控制标志位

# 实例化按键类
key = key_control()                                         # 实例化按键控制类 key_control() 为 key
key.csmax = 4                                               # 按键模式上限为 4 即最多有 4 个模式

# 注册按键引脚
fm.register(16, fm.fpioa.GPIOHS0, force = True)             # 配置 16 脚为 KEY0 使用高速 GPIO 口 强制注册
fm.register(18, fm.fpioa.GPIOHS1, force = True)             # 配置 18 脚为 KEY1 使用高速 GPIO 口 强制注册
fm.register(19, fm.fpioa.GPIOHS2, force = True)             # 配置 19 脚为 KEY2 使用高速 GPIO 口 强制注册
fm.register(20, fm.fpioa.GPIOHS3, force = True)             # 配置 20 脚为 KEY3 使用高速 GPIO 口 强制注册

# 创建按键对象
KEY0 = GPIO(GPIO.GPIOHS0, GPIO.IN, GPIO.PULL_UP)            # 创建按键对象 KEY0
KEY1 = GPIO(GPIO.GPIOHS1, GPIO.IN, GPIO.PULL_UP)            # 创建按键对象 KEY1
KEY2 = GPIO(GPIO.GPIOHS2, GPIO.IN, GPIO.PULL_UP)            # 创建按键对象 KEY2
KEY3 = GPIO(GPIO.GPIOHS3, GPIO.IN, GPIO.PULL_UP)            # 创建按键对象 KEY3

# 中断回调函数 KEY0 控制按键模式选择
def key0_switch(KEY0):
    utime.sleep_ms(10)                                      # 延时 10ms 消除按键抖动
    if KEY0.value() == 0:                                   # 确认 按键0 按下
        key.csflag = 1                                      # 标记按键模式切换
        if key.cs < key.csmax:                              # 控制按键模式选择 自增
            key.cs = key.cs + 1
        else:                                               # 若达到上限 则重新从 0 开始
            key.cs = 0

# 中断回调函数 KEY1 按键输入值自增
def key1_switch(KEY1):
    utime.sleep_ms(10)                                      # 延时 10ms 消除按键抖动
    if KEY1.value() == 0:                                   # 确认 按键1 按下
        key.cinput = key.cinput + 1                         # 按键输入值自增

# 中断回调函数 KEY2 按键输入值自减
def key2_switch(KEY2):
    utime.sleep_ms(10)                                      # 延时 10ms 消除按键抖动
    if KEY2.value() == 0:                                   # 确认 按键2 按下
        key.cinput = key.cinput - 1                         # 按键输入值自减

# 中断回调函数 KEY3 按键确认及发送控制标志位
def key3_switch(KEY3):
    utime.sleep_ms(10)                                      # 延时 10ms 消除按键抖动
    if KEY3.value() == 0:                                   # 确认按键按下
        key.control = 1                                     # 按键确认及发送控制标志位

# 开启中断 下降沿触发
KEY0.irq(key0_switch, GPIO.IRQ_FALLING)                     # 开启 按键0 外部中断 下降沿触发
KEY1.irq(key1_switch, GPIO.IRQ_FALLING)                     # 开启 按键1 外部中断 下降沿触发
KEY2.irq(key2_switch, GPIO.IRQ_FALLING)                     # 开启 按键2 外部中断 下降沿触发
KEY3.irq(key3_switch, GPIO.IRQ_FALLING)                     # 开启 按键3 外部中断 下降沿触发

#__________________________________________________________________
# LCD 的使用
# LCD 初始化
lcd.init()                                                  # lcd初始化

# LCD 按键信息及目标点信息显示函数
def lcd_key():
    lcd.draw_string(0, 0,  "key_cs: "+str(key.cs), lcd.BLUE, lcd.WHITE)
    lcd.draw_string(0, 15, "cinput: "+str(key.cinput), lcd.BLUE, lcd.WHITE)
    lcd.draw_string(0, 30, "point1: "+str(point.point1), lcd.BLUE, lcd.WHITE)
    lcd.draw_string(0, 45, "point2: "+str(point.point2), lcd.BLUE, lcd.WHITE)
    lcd.draw_string(0, 60, "cross : "+str(point.cross), lcd.BLUE, lcd.WHITE)
    lcd.draw_string(0, 75, "red_cx: "+str(red.cx), lcd.BLUE, lcd.WHITE)
    lcd.draw_string(0, 90, "motor1: "+str(motor.motor1), lcd.BLUE, lcd.WHITE)
    lcd.draw_string(0, 105,"motor2: "+str(motor.motor2), lcd.BLUE, lcd.WHITE)
    lcd.draw_string(0, 120,"FPS   : "+str(clock.fps()), lcd.BLUE, lcd.WHITE)

#__________________________________________________________________
# LED 的使用
# 注册LED引脚
fm.register(14, fm.fpioa.GPIO2, force = True)               # 配置 14 脚为 LED_R 强制注册
fm.register(13, fm.fpioa.GPIO1, force = True)               # 配置 13 脚为 LED_G 强制注册
fm.register(12, fm.fpioa.GPIO0, force = True)               # 配置 12 脚为 LED_B 强制注册

# 创建LED对象
LED_R = GPIO(GPIO.GPIO2, GPIO.OUT)                          # 创建 LED_R 对象
LED_G = GPIO(GPIO.GPIO1, GPIO.OUT)                          # 创建 LED_G 对象
LED_B = GPIO(GPIO.GPIO0, GPIO.OUT)                          # 创建 LED_B 对象

# LED控制函数
def led_control(led_flag):                                  # LED控制函数 根据传入 led_flag 点亮对应的灯
    if led_flag == 0:                                       # 传入参数为 0 所有灯打开
        LED_R.value(0)
        LED_G.value(0)
        LED_B.value(0)

    elif led_flag == 1:                                     # 传入参数为 1 所有灯关闭
        LED_R.value(1)
        LED_G.value(1)
        LED_B.value(1)

    elif led_flag == 2:                                     # 传入参数为 2 红灯常亮
        LED_R.value(0)
        LED_G.value(1)
        LED_B.value(1)

    elif led_flag == 3:                                     # 传入参数为 3 绿灯常亮
        LED_R.value(1)
        LED_G.value(0)
        LED_B.value(1)

    elif led_flag == 4:                                     # 传入参数为 4 蓝灯常亮
        LED_R.value(1)
        LED_G.value(1)
        LED_B.value(0)

    else:                                                   # 其他情况 紫灯
        LED_R.value(0)
        LED_G.value(1)
        LED_B.value(0)

#__________________________________________________________________
# 定时器的使用
# 定义定时器属性类
class timer_property():
    cnt     = 0                                             # 定时器计数值
    cnt_max = 0                                             # 定时器计数值上限
    period  = 0                                             # 定时器周期
    freq    = 0                                             # 定时器频率

# 定时器0 配置_______________________________________________________
# 定时器0 实例化类
timer0 = timer_property()                                   # 实例化定时器属性类 timer_property() 为 timer0
timer0.cnt_max = 9                                          # 设定 定时器0 的计数值上限为 9
timer0.period = 100                                         # 设定 定时器0 的周期为 100

# 定时器0 定义回调函数
def timer0_back(tim0):
    if timer0.cnt < timer0.cnt_max:                         # 若 定时器0 的计数值小于 定时器0 的计数值上限
        timer0.cnt = timer0.cnt + 1                         # 计数值自增
    else:
        timer0.cnt = 0                                      # 超出计数值上限 则计数值重置为0

# 定时器0 初始化
tim0 = Timer(Timer.TIMER0,                                  # 定时器编号 定时器0
            Timer.CHANNEL0,                                 # 定时器通道 通道0
            mode = Timer.MODE_PERIODIC,                     # 定时器模式 周期性
            unit = Timer.UNIT_MS,                           # 定时器周期单位 ms
            period = timer0.period,                         # 定时器周期 timer0.period 若 unit 为 Timer.UNIT_MS 则周期为 timer0.period ms
            callback = timer0_back)                         # 定时器触发中断后执行的回调函数 timer0_back

# 定时器1 配置_______________________________________________________
# 电机类定义
class motor_property():
    motor1      = 0                                         # 电机1 占空比
    motor2      = 0                                         # 电机2 占空比
    motor3      = 0                                         # 电机3 占空比
    motor4      = 0                                         # 电机4 占空比

    motor1_pin  = 0                                         # 电机1 引脚
    motor2_pin  = 0                                         # 电机2 引脚
    motor3_pin  = 0                                         # 电机3 引脚
    motor4_pin  = 0                                         # 电机4 引脚

    control_x   = 0                                         # 被控坐标 x
    control_y   = 0                                         # 被控坐标 y

# 实例化电机类
motor = motor_property()                                    # 实例化电机类 motor_property() 为 motor
motor.motor1 = 50                                           # 电机1的占空比 初始设置为 50%
motor.motor2 = 50                                           # 电机2的占空比 初始设置为 50%
motor.motor1_pin  = 14                                      # 电机1的引脚 14为红灯引脚 这里先用灯的亮灭观察效果
motor.motor2_pin  = 13                                      # 电机2的引脚 13为绿灯引脚 这里先用灯的亮灭观察效果

# 定时器1 实例化类
timer1 = timer_property()                                   # 实例化定时器属性类 timer_property() 为 timer1
timer1.freq = 1000                                          # 设定 定时器1 的频率为 1000

# 定时器1 通道0 初始化
tim1_ch0 = Timer(Timer.TIMER1,                              # 定时器编号 定时器1
                 Timer.CHANNEL0,                            # 定时器通道 通道0
                 mode = Timer.MODE_PWM)                     # 定时器模式 PWM

# 定时器1 通道1 初始化
tim1_ch1 = Timer(Timer.TIMER1,                              # 定时器编号 定时器1
                 Timer.CHANNEL1,                            # 定时器通道 通道1
                 mode = Timer.MODE_PWM)                     # 定时器模式 PWM

# 创建对象 电机1 通道为 定时器1的通道0 频率为 定时器1的频率 占空比为 电机1的占空比 引脚为 电机1的引脚
motor1 = PWM(tim1_ch0, freq = timer1.freq, duty = motor.motor1, pin = motor.motor1_pin)

# 创建对象 电机2 通道为 定时器1的通道1 频率为 定时器1的频率 占空比为 电机2的占空比 引脚为 电机2的引脚
motor2 = PWM(tim1_ch1, freq = timer1.freq, duty = motor.motor2, pin = motor.motor2_pin)

# 定义电机占空比控制函数
def motor_control(motor, x):
    val = 0
    if x < motor.control_x:                                 # 若 当前坐标 小于 被控坐标x 即当前状态小车在目标的 左边
        val = (motor.control_x - x) * 0.3125                # 获取坐标差值 并转换为 0~50 之间的值
        motor.motor1 = 50 - val                             # 减小 电机1 占空比 电机1为左电机 使小车右转
        motor.motor2 = 50 + val                             # 增大 电机2 占空比 电机2为右电机 使小车右转

    elif x > motor.control_x:                               # 若 当前坐标 大于 被控坐标x 即当前状态小车在目标的 右边
        val = (x - motor.control_x) * 0.3125                # 获取坐标差值 并转换为 0~50 之间的值
        motor.motor1 = 50 + val                             # 增大 电机1 占空比 电机1为左电机 使小车左转
        motor.motor2 = 50 - val                             # 减小 电机2 占空比 电机2为右电机 使小车左转

    motor.motor1 = int(motor.motor1)                        # 将 电机1占空比 转换为 整数
    motor.motor2 = int(motor.motor2)                        # 将 电机1占空比 转换为 整数

#__________________________________________________________________
# 寻找色块
# 定义类
class color_property():
    cx                      =  0                            # 色块 x轴 中心坐标
    cy                      =  0                            # 色块 y轴 中心坐标
    flag                    =  0                            # 色块标志位 1 找到 0 未找到
    color                   =  0                            # 色块颜色标志位 例如 你可以用 1 来表示 黑色
    density                 =  0                            # 色块密度比 反映色块锁定程度 值越大 锁定程度越好
    pixels_max              =  0                            # 色块像素最大值
    led_flag                =  0                            # LED标志位 方便调试用

    color_threshold         = (0, 0, 0, 0, 0, 0)            # 色块颜色阈值
    color_roi               = (0,0,320,240)                 # 色块寻找区域（感兴趣区域）
    color_x_stride          =  1                            # 色块 x轴 像素最小宽度 色块如果比较大可以调大此参数 提高寻找速度
    color_y_stride          =  1                            # 色块 y轴 像素最小宽度 色块如果比较大可以调大此参数 提高寻找速度
    color_pixels_threshold  =  100                          # 色块 像素个数阈值 例如调节此参数为100 则可以滤除色块像素小于100的色块
    color_area_threshold    =  100                          # 色块 被框面积阈值 例如调节此参数为100 则可以滤除色块被框面积小于100的色块
    color_merge             =  True                         # 是否合并寻找到的色块 True 则合并 False 则不合并
    color_margin            =  1                            # 色块合并间距 例如调节此参数为1 若上面选择True合并色块 且被找到的色块有多个 相距1像素 则会将这些色块合并

# 实例化类
# 黑色
black = color_property()
black.color_threshold         = (0, 50, -10, 10, -10, 10)
black.color_roi               = (0,0,320,240)
black.color_x_stride          =  1
black.color_y_stride          =  1
black.color_pixels_threshold  =  100
black.color_area_threshold    =  100
black.color_merge             =  True
black.color_margin            =  1

# 红色
red   = color_property()
red.color_threshold           = (0, 100, 20, 127, -10, 127)

#red.color_roi                = (0,0,320,240)
red.color_roi                 = (0,110,320,20)

red.color_x_stride            =  1
red.color_y_stride            =  1

#red.color_pixels_threshold   =  100
#red.color_area_threshold     =  100
red.color_pixels_threshold    =  10
red.color_area_threshold      =  10

red.color_merge               =  True
red.color_margin              =  1

# 绿色 预留
green = color_property()

# 蓝色 预留
blue  = color_property()

# 定义寻找色块函数
def opv_find_blobs(color,led_flag):
    color.pixels_max = 0                                    # 重置 色块 最大像素数量
    color.flag       = 0                                    # 重置 色块 标志位
    color.led_flag   = 0                                    # 重置 led 标志位

    for blobs in img.find_blobs([color.color_threshold],    # 色块颜色阈值
    roi = color.color_roi,                                  # 色块寻找区域（感兴趣区域）
    x_stride = color.color_x_stride,                        # 色块 x轴 像素最小宽度 色块如果比较大可以调大此参数 提高寻找速度
    y_stride = color.color_y_stride,                        # 色块 y轴 像素最小宽度 色块如果比较大可以调大此参数 提高寻找速度
    pixels_threshold = color.color_pixels_threshold,        # 色块 像素个数阈值 例如调节此参数为100 则可以滤除色块像素小于100的色块
    area_threshold = color.color_area_threshold,            # 色块 被框面积阈值 例如调节此参数为100 则可以滤除色块被框面积小于100的色块
    merge = color.color_merge,                              # 是否合并寻找到的色块 True 则合并 False 则不合并
    margin = color.color_margin):                           # 色块合并间距 例如调节此参数为1 若上面选择True合并色块 且被找到的色块有多个 相距1像素 则会将这些色块合并
        img.draw_rectangle(blobs[0:4])                      # 圈出找到的色块
        if color.pixels_max < blobs.pixels():               # 找到面积最大的色块
            color.pixels_max = blobs.pixels()
            color.cx = blobs.cx()                           # 将面积最大的色块的 x轴 中心坐标值 赋值给 color
            color.cy = blobs.cy()                           # 将面积最大的色块的 y轴 中心坐标值 赋值给 color
            color.flag = 1                                  # 标志画面中有找到色块
            color.density = blobs.density()                 # 将面积最大的色块的 色块密度比 赋值给 color
            color.led_flag = led_flag                       # 将控制led颜色的标志位的值 赋值给 color

    if color.flag == 1:                                     # 标记画面中被找到的最大色块的中心坐标
        img.draw_cross(color.cx,color.cy, color=127, size = 15)
        img.draw_circle(color.cx,color.cy, 15, color = 127)

# 定义打印色块参数函数
def print_blobs_property(color,name):
    print(name,"cx:",color.cx,"cy:",color.cy,"flag:",color.flag,"color:",color.color,"density:",color.density,"led_flag:",color.led_flag)

#__________________________________________________________________
# 调试区
led_control(1)                                              # 关闭一下所有灯 再进入 while 循环 使显示结果正确

#__________________________________________________________________
# 主函数
while(True):

    clock.tick()                                            # 跟踪运行时间

    img = sensor.snapshot()                                 # 拍摄一张照片

    #opv_find_blobs(black,1)                                # 找黑色色块 led标志为1 表示黑色
    opv_find_blobs(red,2)                                   # 找红色色块 led标志为2 表示红色

    point_control(key)                                      # 按键控制下的目标点获取函数

    lcd.display(img)                                        # LCD 显示图像
    lcd_key()                                               # LCD 显示按键信息及目标点信息

    #led_control(red.led_flag)                              # LED 标记色块识别情况

    motor.control_x = 160                                   # 控制目标处于 x轴中心点 160
    motor_control(motor,red.cx)                             # 电机占空比控制函数获取电机控制占空比

    motor1.duty(motor.motor1)                               # 将获取到的电机1占空比 装载
    motor2.duty(motor.motor2)                               # 将获取到的电机2占空比 装载

    if timer0.cnt == 0:                                     # 如果 timer0.cnt 等于 0 此步骤的目的是控制打印周期 不要打印的太快
        print_sensor()                                      # 打印sensor参数
        print_blobs_property(black,"Black-")                # 打印黑色色块参数
        print_blobs_property(red,  "Red-  ")                # 打印红色色块参数

#__________________________________________________________________



#
