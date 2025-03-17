# 导入模块
import sensor, time, image                                  # 导入感光元件模块 sensor 跟踪运行时间模块 time 机器视觉模块 image
import utime                                                # 导入延时模块 utime
from fpioa_manager import fm                                # 从 GPIO 模块中导入 引脚注册模块 fm
from Maix import GPIO                                       # 从 Maix 模块中导入 模块 GPIO
import lcd                                                  # 导入 LCD 模块

#__________________________________________________________________
# 感光元件设置
sensor.reset()                                              # 重置并初始化感光元件 默认设置为 摄像头频率 24M 不开启双缓冲模式
#sensor.reset(freq=24000000, dual_buff=True)                # 设置摄像头频率 24M 开启双缓冲模式 会提高帧率 但内存占用增加

sensor.set_pixformat(sensor.RGB565)                         # 设置图像格式为 RGB565 (彩色) 除此之外 还可设置格式为 GRAYSCALE 或者 YUV422
sensor.set_framesize(sensor.QVGA)                           # 设置图像大小为 QVGA (320 x 240) 像素个数 76800 K210最大支持格式为 VGA

sensor.set_auto_exposure(1)                                 # 设置自动曝光      80  240  60 180
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
# 黑色#(0, 50, -10, 10, -10, 10)(0, 13, -3, 10, -4, 11)
black = color_property()
black.color_threshold         = (0, 0, -47, 2, -30, 1)
black.color_roi               = (150,100,200,130)
black.color_x_stride          =  1
black.color_y_stride          =  1
black.color_pixels_threshold  =  100
black.color_area_threshold    =  100
black.color_merge             =  True
black.color_margin            =  1

# 红色#(0, 100, 20, 127, -10, 127)(0, 100, 21, 127, -9, 53)
red   = color_property()
red.color_threshold           = (12, 60, 34, 84, -19, 55)
red.color_roi                 = (150,100,200,130)
red.color_x_stride            =  1
red.color_y_stride            =  1
red.color_pixels_threshold    =  10
red.color_area_threshold      =  10
red.color_merge               =  True
red.color_margin              =  1

# 绿色 预留#(30, 100, -64, -8, -32, 32)(0, 32, -38, -4, 41, -37)
green = color_property()
green.color_threshold           = (11, 69, -57, -2, 52, -21)
green.color_roi                 = (150,100,200,130)
green.color_x_stride            =  1
green.color_y_stride            =  1
green.color_pixels_threshold    =  10
green.color_area_threshold      =  10
green.color_merge               =  True
green.color_margin              =  1


# 蓝色 预留#(0, 15, 0, 40, -80, -20)(0, 100, -128, 127, -128, -10）
blue  = color_property()
blue.color_threshold           = (0, 100, -16, 46, -83, -26)
blue.color_roi                 = (150,100,200,130)
blue.color_x_stride            =  1
blue.color_y_stride            =  1
blue.color_pixels_threshold    =  10
blue.color_area_threshold      =  10
blue.color_merge               =  True
blue.color_margin              =  1


# 黄色 预留#(79, 100, 41, -26, 15, 94)(87, 29, -1, 31, 102, 29)(100, 43, -18, 40, 94, 47)
yellow  = color_property()
yellow.color_threshold           = (100, 43, -18, 40, 94, 47)
yellow.color_roi                 = (150,100,200,130)
yellow.color_x_stride            =  1
yellow.color_y_stride            =  1
yellow.color_pixels_threshold    =  10
yellow.color_area_threshold      =  10
yellow.color_merge               =  True
yellow.color_margin              =  1


# 白色 预留#(57, 100, 63, -76, 10, -44)(100, 29, -29, 35, -39, 2)
white  = color_property()
white.color_threshold           = (100, 41, -31, 42, -60, 6)
white.color_roi                 = (150,100,200,130)
white.color_x_stride            =  1
white.color_y_stride            =  1
white.color_pixels_threshold    =  10
white.color_area_threshold      =  10
white.color_merge               =  True
white.color_margin              =  1
