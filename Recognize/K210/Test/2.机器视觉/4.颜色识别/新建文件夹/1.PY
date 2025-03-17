import sensor
import image
import time
import lcd
import utime
ROI = (0, 0, 320, 240)  # ROI 区域
THRESHOLD = 200  # 色块阈值

# 初始“活动物体列表”和“历史物体列表”，分别用来存储当前正在运动的物体和已经离开视野范围的物体
active_objects = []
history_objects = []

red = (55, 85, 55, 80, 20, 80)
yellow = (60,110,-30,30,40,80)
green = (40,85,-60,-20,-5,25)
blue = (50,95,-35,15,-80,-15)
black = (-10,10,-10,10,-10,10)
white = (90,110,-10,10,-10,10)

lcd.init() #初始化LCD
lcd.clear(lcd.WHITE) #清屏白色

sensor.reset() # 初始化摄像头
sensor.set_pixformat(sensor.RGB565) # 格式为 RGB565.
sensor.set_framesize(sensor.QVGA)

sensor.set_auto_whitebal(False)               # Create a clock object to track the FPS.
#sensor.set_auto_exposure(1)                                 # 设置自动曝光
#sensor.set_auto_exposure(0, exposure=120000)               # 设置手动曝光 曝光时间 120000 us

sensor.set_auto_gain(0, gain_db = 14)                       # 设置画面增益 17 dB 影响实时画面亮度
sensor.set_vflip(1)                                         # 打开垂直翻转 如果是 01Studio 的 K210 不开启会导致画面方向与运动方向相反
sensor.set_hmirror(1)

sensor.skip_frames(10) # 跳过10帧，使新设置生效

while True:
    img = sensor.snapshot()         # Take a picture and return the image.
    # 获取新的色块列表
    blobs = img.find_blobs([red, yellow], roi=ROI, pixels_threshold=THRESHOLD)

    # 更新“活动物体列表”和“历史物体列表”
    current_time = time.time()
    for blob in blobs:
        matched = False  # 标记当前色块是否已匹配到“活动物体列表”中的某个物体

        # 检查“活动物体列表”中是否有包含当前色块的物体，如果有，则更新其位置和时间戳
        for obj in active_objects:
            if blob.overlap(obj):
                obj.update(blob, current_time)
                matched = True
                break

        # 如果当前色块还没有被匹配到任何“活动物体列表”中的物体，则视为新物体添加到“活动物体列表”中
        if not matched:
            active_objects.append(Object(blob, current_time))

    # 检查“活动物体列表”中是否有已离开视野范围的物体，将其添加到“历史物体列表”中
    for obj in active_objects:
        if obj.is_out_of_roi(ROI):
            obj.depart(current_time)
            history_objects.append(obj)

    # 从“活动物体列表”中移除已离开视野范围的物体
    active_objects = [obj for obj in active_objects if not obj.is_out_of_roi(ROI)]

    # 输出物体数量
    for obj in history_objects:
        duration = obj.depart_time - obj.enter_time
        print("{} from {:.2f} to {:.2f}, duration {:.2f} seconds".format(obj.color, obj.enter_time, obj.depart_time, duration))
        history_objects.remove(obj)
    print("sgevfsfv")
