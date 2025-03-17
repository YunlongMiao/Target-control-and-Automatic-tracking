# sensor_V1.0 - By: FITQY - 周天 8 月 21 日 2022
#__________________________________________________________________
# 导入模块
import sensor, time                                         # 导入感光元件模块 sensor 跟踪运行时间模块 time

#__________________________________________________________________
# 感光元件设置
sensor.reset()                                              # 重置并初始化感光元件 默认设置为 摄像头频率 24M 不开启双缓冲模式
#sensor.reset(freq=24000000, dual_buff=True)                # 设置摄像头频率 24M 开启双缓冲模式 会提高帧率 但内存占用增加

sensor.set_pixformat(sensor.RGB565)                         # 设置图像格式为 RGB565 (彩色) 除此之外 还可设置格式为 GRAYSCALE 或者 YUV422
sensor.set_framesize(sensor.QVGA)                           # 设置图像大小为 QVGA (320 x 240) 像素个数 76800 K210最大支持格式为 VGA

sensor.set_auto_exposure(1)                                 # 设置自动曝光
#sensor.set_auto_exposure(0, exposure=120000)               # 设置手动曝光 曝光时间 120000 us

sensor.set_auto_gain(0, gain_db = 17)                       # 设置画面增益 17 dB 影响实时画面亮度
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
# 调试区
mycnt       = 0                                             # 计数变量
mycnt_max   = 30                                            # 计数上限 此值越大 计数周期越长

#__________________________________________________________________
# 主函数
while(True):

    clock.tick()                                            # 跟踪运行时间

    img = sensor.snapshot()                                 # 拍摄一张照片

    if mycnt == 0:                                          # 如果 mycnt 等于 0 此步骤的目的是控制打印周期 不要打印的太快
        mycnt = 1                                           # 将 1 赋值给 mycnt 使下一次不再满足 mycnt == 0 进入 elif
        print("Exposure:"+str(sensor.get_exposure_us()))    # 打印 曝光时间
        print("Gain:"+str(sensor.get_gain_db()))            # 打印 画面增益
        print("RGB: "+str(sensor.get_rgb_gain_db()))        # 打印 RGB 增益

    elif mycnt < mycnt_max:                                 # 计数变量 小于 计数上限 则 计数变量 自增
        mycnt = mycnt + 1

    else:                                                   # 计数变量 超出 计数上限 则 将0赋值给 mycnt 使下一次进入 if
        mycnt = 0

#__________________________________________________________________

