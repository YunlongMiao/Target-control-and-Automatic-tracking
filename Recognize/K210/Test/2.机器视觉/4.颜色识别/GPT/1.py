import sensor, image, time, utime

# 初始化摄像头
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((240, 240)) # 中心画面区域
sensor.skip_frames(time=2000)

# 通过 LCD 显示器展示检测结果
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
    clock.tick()

    # 通过摄像头获取图像
    img = sensor.snapshot()

    # 计算每个颜色块像素点的个数
    b_pixel_count = g_pixel_count = r_pixel_count = y_pixel_count = w_pixel_count = bl_pixel_count = 0
    for x in range(img.width()):
        for y in range(img.height()):
            # 获取像素值
            pixel = img.get_pixel(x, y)
            # 分别计算乒乓球各颜色块的像素点个数
            if pixel[0] > 120 and pixel[1] < 50 and pixel[2] < 50: # 红
                r_pixel_count += 1
            elif pixel[0] < 50 and pixel[1] > 120 and pixel[2] < 50: # 绿
                g_pixel_count += 1
            elif pixel[0] < 50 and pixel[1] < 50 and pixel[2] > 120: # 蓝
                b_pixel_count += 1
            elif pixel[0] > 200 and pixel[1] > 200 and pixel[2] < 50: # 黄
                y_pixel_count += 1
            elif pixel[0] > 200 and pixel[1] > 200 and pixel[2] > 200: # 白
                w_pixel_count += 1
            elif pixel[0] < 50 and pixel[1] < 50 and pixel[2] < 50: # 黑
                bl_pixel_count += 1

    # 检测颜色块是否存在
    blue_detected = b_pixel_count > blue_thresh   # 蓝
    green_detected = g_pixel_count > green_thresh # 绿
    red_detected = r_pixel_count > red_thresh     # 红
    yellow_detected = y_pixel_count > yellow_thresh # 黄
    white_detected = w_pixel_count > white_thresh # 白
    black_detected = bl_pixel_count > black_thresh # 黑

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

if blue_detected:
    draw_paint(x+80, y + 20, "检测通过！")
    # 在此处添加控制代码以操作蓝色乒乓球。
if green_detected:
    draw_paint(x+80, y + 40, "检测通过！")
    # 在此处添加控制代码以操作绿色乒乓球。
if red_detected:
    draw_paint(x+80, y + 60, "检测通过！")
    # 在此处添加控制代码以操作红色乒乓球。
if yellow_detected:
    draw_paint(x+80, y + 80, "检测通过！")
    # 在此处添加控制代码以操作黄色乒乓球。
if white_detected:
    draw_paint(x+80, y + 100, "检测通过！")
    # 在此处添加控制代码以操作白色乒乓球。
if black_detected:
    draw_paint(x+80, y + 120, "检测通过！")
    # 在此处添加控制代码以操作黑色乒乓球。
