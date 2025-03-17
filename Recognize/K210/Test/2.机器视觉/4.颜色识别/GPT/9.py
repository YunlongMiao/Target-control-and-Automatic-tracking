import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_whitebal(False) # must be turned off for color tracking
sensor.set_auto_exposure(1)                                 # 设置自动曝光
#sensor.set_auto_exposure(0, exposure=120000)               # 设置手动曝光 曝光时间 120000 us
sensor.set_auto_gain(0, gain_db = 17)

clock = time.clock()

# 定义两个数组
keys = [1, 2, 4, 8, 16, 32]
values = [0, 1, 2, 3, 4, 5]
# 合并成一个字典
key_value_dict = dict(zip(keys, values))

while(True):
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8)
    # 获取字典中的值
    value = key_value_dict[32] # key_value_dict[8]返回3
    print(value)
    print(key_value_dict)
    print("FPS %f" % clock.fps())
