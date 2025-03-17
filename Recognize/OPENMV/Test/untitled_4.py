import sensor, image, time

# 初始化摄像头
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)  # 让摄像头稳定一下
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

# 阈值
threshold_value = (39, 40, 46, -34, -3, -29)  # 根据实际情况调整阈值

while True:
    img = sensor.snapshot()

    # 对比度增强 - 直方图均衡化
    img.histeq()

    # 二值化
    img.binary([threshold_value])

    # 腐蚀和膨胀，去除噪声
    img.erode(1)
    img.dilate(1)

    # 查找轮廓
    blobs = img.find_blobs([threshold_value], pixels_threshold=2000, area_threshold=10, merge=True)

    # 绘制痕迹边框
    for blob in blobs:
        img.draw_rectangle(blob.rect(), color=127)

    # 显示处理后的图像
    img.show()
