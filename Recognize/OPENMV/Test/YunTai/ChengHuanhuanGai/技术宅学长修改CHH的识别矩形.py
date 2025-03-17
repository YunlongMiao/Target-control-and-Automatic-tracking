from machine import Pin
import sensor, image, time
import pyb
# 初始化TFT180屏幕


# 初始化摄像头
sensor.reset()
sensor.set_pixformat(sensor.RGB565) # 设置图像色彩格式为RGB565格式
sensor.set_framesize(sensor.QQVGA)  # 设置图像大小为160*120
sensor.set_auto_whitebal(True)      # 设置自动白平衡
sensor.set_brightness(3000)         # 设置亮度为3000
sensor.skip_frames(time = 20)       # 跳过帧

clock = time.clock()

'''
识别A4纸的黑线
'''


def detect_black_line():
    global pencil_points, red_threshold, taruge_rect_in_QQVGA#这几个参数自己设置一下、分别是铅笔线坐标，红色阈值（这里好像没有用），方框顶点坐标

    # 初始化摄像头
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)  # 设置图像色彩格式为RGB565格式
    sensor.set_framesize(sensor.QQVGA)  # 设置图像大小为160*120
    sensor.set_auto_whitebal(True)  # 设置自动白平衡
    sensor.set_brightness(3000)  # 设置亮度为3000
    sensor.skip_frames(time=20)  # 跳过帧

    clock = time.clock()

    for n in range(4):
            pencil_points_in_QQVGA.append([round(pencil_points[n][0]*0.5), round(pencil_points[n][1]*0.5)])
            print(pencil_points_in_QQVGA[n])
    laser_move_by_degress(90,100)    #激光点扭转到画面外，防止影响识别
    last_taruge_rect_in_QQVGA = [[0,0],[0,0],[0,0],[0,0]]  #记录上一次识别到的定点数据，用来判断数据是否稳定
    loop = False
    matching_counts = 0#记录识别稳定不变的次数，达到一定数量则判断识别成功
    while loop:
        img = sensor.snapshot() #获取画面
        img.rotation_corr(corners = (pencil_points_in_QQVGA[:4]))   #画面梯形校正   根据铅笔线坐标矫正
        img.draw_image(img,0,0,x_size=120,y_size=120)   #缩放画面至正常比例
        img.draw_rectangle(120,0,40,120,color=(0,0,0),fill=True)    #右侧空白处涂黑
        img.midpoint(1, bias=0.9, threshold=True, offset=5, invert=True)    #凸显黑线
        rr = img.find_rects()   #找矩形
        if rr:  #如果有目标
            for r in rr:    #遍历目标，当然，目标应该只有一个
                taruge_rect_in_QQVGA = r.corners()  #存储方框顶点坐标
                img.draw_rectangle(r.rect(), color = (255, 0, 0))   #在屏幕绘制标识框
                for p in r.corners():   #绘制四个定点的标识
                    img.draw_circle(p[0], p[1], 5, color = (0, 255, 0))
                for n in range(4):#对比方框定点坐标数据的变动情况，判断是否获取成功
                    for n2 in range(2):
                        #注意，此处判断阈值为3，如果画面不稳定，可能程序无法向后进行。可以修改阈值。另外还可以增加低通滤波。
                        if abs(taruge_rect_in_QQVGA[n][n2] - last_taruge_rect_in_QQVGA[n][n2]) < 3:
                            matching_counts += 1
                            print(matching_counts)
                        else:
                            matching_counts = 0
                            print('识别失败')
                last_taruge_rect_in_QQVGA = taruge_rect_in_QQVGA
                if matching_counts > 300:
                    loop = False
                    print('识别成功')
                    sensor_set_QVGA_dark()
                    laser_move_by_degress(90,90)    #激光点回证
                    sleep(0.5)  #使云台保持稳定，防止超调
    # 打印帧率
    print(clock.fps())
    return taruge_rect_in_QQVGA

while(True):

    print(detect_black_line())