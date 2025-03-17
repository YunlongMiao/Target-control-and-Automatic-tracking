import sensor
import image
import lcd
import time
import utime
import ustruct
from machine import UART
from fpioa_manager import fm

fm.register(10, fm.fpioa.UART1_TX, force=True)#映射串口引脚
fm.register(9, fm.fpioa.UART1_RX, force=True)#映射串口引脚

# 初始化摄像头参数
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.set_auto_gain(False)  # 脱机环境关闭自动增益控制
sensor.set_auto_whitebal(False)  # 脱机环境关闭自动白平衡控制
sensor.set_auto_exposure(False, exposure_us=3000)  # 进行固定曝光，免受光照的影响
clock = time.clock()

# 初始化LCD
lcd.init(color=(255, 255, 255))
lcd.draw_string(90, 10, "K210 Ping-pong", lcd.RED, lcd.BLACK)
lcd.draw_string(40, 150, "Press key to start", lcd.GREEN, lcd.BLACK)
lcd.draw_string(80, 180, "mode: Normal", lcd.BLUE, lcd.BLACK)
lcd.swap()

uart = UART(UART.UART1, 115200, 8, 1, 0, timeout=1000, read_buf_len=4096)
ball_colors = []  # 球的颜色码
color_counts = [0, 0, 0, 0, 0, 0]  # 颜色计数器
pingpong = ''  # 乒乓球状态
start_count_time = 0  # 记录小球停止的时间

while True:
    if uart.any():
        cmd = uart.read()
        if cmd == b"start":
            lcd.draw_string(80, 150, "Counting...", lcd.BLUE, lcd.BLACK)
            lcd.swap()
            break
        else:
            lcd.draw_string(80, 150, "Wrong command", lcd.RED, lcd.BLACK)
            lcd.swap()
            utime.sleep(2)  # 等待几秒后清除显示
            lcd.clear()
            lcd.draw_string(90, 10, "K210 Ping-pong", lcd.RED, lcd.BLACK)
            lcd.draw_string(40, 150, "Press key to start", lcd.GREEN, lcd.BLACK)
            lcd.draw_string(80, 180, "mode: Normal", lcd.BLUE, lcd.BLACK)
            lcd.swap()

    clock.tick()
    img = sensor.snapshot().rotation_corr(z_rotation=90)
    img_binary = img.to_rgb888().to_bitmap()
    uart.write("abc")
    roi = img_binary[80:160, 70:230]  # 感兴趣区域
    for i in range(6):
        if color_counts[i] > 100:  # 重置小球颜色的计数器
            color_counts[i] = 0

        color_middle
