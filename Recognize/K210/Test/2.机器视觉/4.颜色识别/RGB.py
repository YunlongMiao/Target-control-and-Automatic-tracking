import sensor

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)

while True:
    img = sensor.snapshot()

    # 将图像在指定的区域内转换为 RGB 像素
    pixels = img.crop((20, 20, 40, 40)).to_rgb565().to_rbg()

    # 遍历像素并输出RGB值
    for pixel in pixels:
        r, g, b = pixel
        print("R: %d, G: %d, B: %d" % (r, g, b))

    # 延迟 1 秒再循环
    time.sleep(1)
