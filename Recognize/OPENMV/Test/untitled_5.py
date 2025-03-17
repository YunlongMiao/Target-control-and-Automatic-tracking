#import sensor, image, time

#black_threshold =

#sensor.reset() # 初始化摄像头传感器
#sensor.set_pixformat(sensor.RGB565) # 使用 RGB565 彩图
#sensor.set_framesize(sensor.QQVGA) # 使用 QQVGA 分辨率
#sensor.skip_frames(10) #跳过几帧，让新的设置生效。
#sensor.set_auto_whitebal(False) # 因为是颜色识别，所以需要把白平衡关闭
#clock = time.clock() # 追踪帧率，影响不大
##__________________________________________________________________
##定义寻找最大色块的函数，因为图像中有多个色块，所以追踪最大的那个
#def find_max(blobs):
    #max_size=0
    #for blob in blobs:
        #if blob[2]*blob[3] > max_size:
            #max_blob=blob
            #max_size = blob[2]*blob[3]
    #return max_blob
##__________________________________________________________________
#while(True):
    #clock.tick() # 跟踪快照()之间经过的毫秒数。
    #img = sensor.snapshot() # 截取一张图片
    #blobs = img.find_blobs([black_threshold])  #识别黑色阈值
    #max_blob = find_max(blobs)  #调用上面自定义函数，找到最大色块
    #max_blob.x()  #返回识别区域左上角的x坐标
    #max_blob.y()  #返回识别区域左上角的y坐标
    #max_blob.w()  #返回识别区域的宽度
    #max_blob.h()  #返回识别区域的长度
















# 边缘检测例子:
#
# 这个程序示范了在图像上使用morph函数来进行边缘检测。
# 然后在进行阈值和滤波

import sensor, image, time

#设置核函数滤波，核内每个数值值域为[-128,127],核需为列表或元组
kernel_size = 1 # kernel width = (size*2)+1, kernel height = (size*2)+1
kernel = [-1, -1, -1,\
          -1, +8, -1,\
          -1, -1, -1]
# 这个一个高通滤波器。见这里有更多的kernel
# http://www.fmwconcepts.com/imagemagick/digital_image_filtering.pdf
thresholds = [(100, 255)] # grayscale thresholds设置阈值

sensor.reset() # 初始化 sensor.
#初始化摄像头

sensor.set_pixformat(sensor.GRAYSCALE) # or sensor.RGB565
#设置图像色彩格式，有RGB565色彩图和GRAYSCALE灰度图两种

sensor.set_framesize(sensor.QQVGA) # or sensor.QVGA (or others)
#设置图像像素大小
sensor.skip_frames(10) # 让新的设置生效
clock = time.clock() # 跟踪FPS帧率

# 在OV7725 sensor上, 边缘检测可以通过设置sharpness/edge寄存器来增强。
# 注意:这将在以后作为一个函数实现
if (sensor.get_id() == sensor.OV7725):
    sensor.__write_reg(0xAC, 0xDF)
    sensor.__write_reg(0x8F, 0xFF)

while(True):
    clock.tick() # 追踪两个snapshots()之间经过的毫秒数.
    img = sensor.snapshot().lens_corr(strength = 1.9) # 拍一张照片，返回图像

    img.morph(kernel_size, kernel)
    #morph(size, kernel, mul=Auto, add=0)，morph变换，mul根据图像对比度
    #进行调整，mul使图像每个像素乘mul；add根据明暗度调整，使得每个像素值加上add值。
    #如果不设置则不对morph变换后的图像进行处理。
    img.binary(thresholds)
    #利用binary函数对图像进行分割

    # Erode pixels with less than 2 neighbors using a 3x3 image kernel
    # 腐蚀像素小于2邻居使用3x3图像内核
    img.erode(1, threshold = 2)
    #侵蚀函数erode(size, threshold=Auto)，去除边缘相邻处多余的点。threshold
    #用来设置去除相邻点的个数，threshold数值越大，被侵蚀掉的边缘点越多，边缘旁边
    #白色杂点少；数值越小，被侵蚀掉的边缘点越少，边缘旁边的白色杂点越多。

    print(clock.fps()) # 注意: 当连接电脑后，OpenMV会变成一半的速度。当不连接电脑，帧率会增加。
