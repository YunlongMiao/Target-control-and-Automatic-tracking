import sensor, image, time
from machine import UART

# 初始化串口对象
uart = UART(1, 115200)

# 初始化图像传感器
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)

while True:
    # 获取图像数据
    img = sensor.snapshot()

    # 获取图像中心像素点的RGB值
    center_pixel = img.get_pixel(img.width()//2, img.height()//2)
    r, g, b = center_pixel[0], center_pixel[1], center_pixel[2]

    # 判断颜色
    if r > g and r > b:
        color = "red"
    elif g > r and g > b:
        color = "green"
    elif b > r and b > g:
        color = "blue"
    elif r < 10 and g < 10 and b < 10:
        color = "black"
    elif r > 220 and g > 220 and b > 220:
        color = "white"
    elif r > 220 and g > 220 and b < 50:
        color = "yellow"
    else:
        color = "unknown"

    # 输出颜色信息
    uart.write(color.encode())
    time.sleep(100)
