import sensor, image, time, utime

# 初始化摄像头
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((240, 240))  # 中心画面区域
sensor.skip_frames(time=1000)  # 跳过一些帧

# 通过LCD显示器展示检测结果
lcd = None
try:
    import lcd160cr
    lcd = lcd160cr.LCD160CR('X')
    lcd.set_orient(lcd160cr.PORTRAIT)
    lcd.erase()
except ImportError:
    print("无法导入LCD模块！")

# 初始化阈值
blue_thresh = 500   # 蓝色乒乓球像素数阈值
green_thresh = 500  # 绿色乒乓球像素数阈值
red_thresh = 500    # 红色乒乓球像素数阈值
yellow_thresh = 500 # 黄色乒乓球像素数阈值
white_thresh = 500  # 白色乒乓球像素数阈值
black_thresh = 500  # 黑色乒乓球像素数阈值

# 绘制一个小圆圈表示颜色并且输出控制信号
def draw_paint(x, y, info):
    lcd.set_pen(255, 255, 255)
    lcd.draw_circle(x, y, 10)
    lcd.set_pen(0, 0, 0)
    lcd.draw_string(x+20, y-4, info)
    lcd.update()

clock = utime.clock()
while True:
    clock.tick()  # 统计帧率

    # 获取摄像头图像
    img = sensor.snapshot()

    ## 对图像进行处理，转化为灰度图
    #img = img.to_grayscale()

    ## 对灰度图像进行二值化
    #threshold = (0, 100)
    #img = img.binary(threshold)

    # 对图像进行处理，转化为灰度图
    img = img.to_grayscale()
    # 对灰度图像进行二值化
    threshold = (50, 255)  # 设置阈值范围
    img = img.binary(threshold)

    # 使用find_blobs函数找到连通区域
    blobs = img.find_blobs(color_thresholds=[(0, 128)], pixels_threshold=10, area_threshold=10)

    # 统计各个颜色块中像素点的个数
    color_counts = {"red": 0, "green": 0, "blue": 0, "yellow": 0, "white": 0, "black": 0}
    for b in blobs:
        if b.roundness() > 0.6:
            if b.density() > 0.6:
                if b.w() >= b.h():
                    r = b.w() / b.h()
                else:
                    r = b.h() / b.w()
                if r <= 1.5:
                    x, y, w, h = b.x(), b.y(), b.w(), b.h()
                    cx, cy = x + w // 2, y + h // 2
                    color = None
                    if img.get_pixel(cx, cy) == (255, 0, 0):
                        color = "red"
                    elif img.get_pixel(cx, cy) == (0, 255, 0):
                        color = "green"
                    elif img.get_pixel(cx, cy) == (0, 0, 255):
                        color = "blue"
                    elif img.get_pixel(cx, cy) == (255, 255, 0):
                        color = "yellow"
                    elif img.get_pixel(cx, cy) == (255, 255, 255):
                        color = "white"
                    elif img.get_pixel(cx, cy) == (0, 0, 0):
                        color = "black"
                    if color:
                        color_counts[color] += 1

    # 根据颜色块的数量判断是否出现乒乓球
    blue_detected = color_counts["blue"] > blue_thresh   # 蓝
    green_detected = color_counts["green"] > green_thresh # 绿
    red_detected = color_counts["red"] > red_thresh     # 红
    yellow_detected = color_counts["yellow"] > yellow_thresh # 黄
    white_detected = color_counts["white"] > white_thresh # 白
    black_detected = color_counts["black"] > black_thresh # 黑

    # 检测结果展示
    lcd.display(img)
    x, y, r = 5, 5, 10
    draw_paint(x, y, "  颜色  控制器")
    draw_paint(x, y + 20, "蓝色：       ")
    draw_paint(x, y + 40, "绿色：       ")
    draw_paint(x, y + 60, "红色：       ")
    draw_paint(x, y + 80, "黄色：       ")
    draw_paint(x, y + 100, "白色：       ")
    draw_paint(x, y + 120, "黑色：       ")

    # 根据检测结果控制舵机
    # 这个根据您的具体硬件和代码实现进行修改
    if blue_detected:
        print("Blue ball detected!")
        # 控制舵机运动
    if green_detected:
        print("Green ball detected!")
        # 控制舵机运动
    if red_detected:
        print("Red ball detected!")
        # 控制舵机运动
