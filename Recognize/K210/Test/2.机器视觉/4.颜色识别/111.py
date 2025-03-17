#可以使用
import sensor, image,time,lcd,utime
yellow_threshold   = (70, 100, -8, 31, -23, 12)#括号里面是颜色阈值
red_threshold     =(25, 89, 30, 87, -41, 52)
green_threshold     =(30, 100, -64, -8, -32, 32)
blue_threshold     =(0, 15, 0, 40, -80, -20)
black_threshold     =(66, 0, -51, -8, 6, 127)
white_threshold     =(57, 100, 63, -76, 10, -44)

#摄像头初始化
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)   #后置拍摄模式
sensor.skip_frames(10) # Let new settings take affect.
sensor.set_auto_whitebal(False) # 白平衡关闭
#sensor.snapshot(1.8)#去鱼眼化
#LCD初始化
lcd.init()
clock = time.clock() # Tracks FPS.
img = sensor.snapshot()
K=5000#the value should be measured K=length*Lm # 实际的大小=K2*直径的像素
K2=10.5/101#QQVGA模式下K2=10.5/139  #QVGA模式下K2=10.5/279
#blobs = img.find_blobs([yellow_threshold], x_stride=5, y_stride=5, invert=False, area_threshold=10, pixels_threshold=25, merge=False, margin=0, threshold_cb=None, merge_cb=None)#调用颜色阈值
while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # Take a picture and return the image.
    #lcd.display(img)#lcd屏幕显示
    blobs = img.find_blobs([yellow_threshold,red_threshold,green_threshold,blue_threshold,black_threshold,white_threshold],pixels_threshold = 400,area_threshold = 200,margin=5,merge = False)

    if blobs:
    #如果找到了目标颜色
        for b in blobs: #循环效果不好，会有很多误识别，采用单个矩形采样方便返回坐标
            if b[8]:            #blob.code() 返回一个16bit数字，每一个bit会对应每一个阈值。
        #迭代找到的目标颜色区域
            x = b[0]
            y = b[1]
            width = b[2]
            height = b[3]
                # Draw a rect around the blob.
            img.draw_rectangle([x,y,width,height]) # rect
                #用矩形标记出目标颜色区域
            img.draw_cross(b[5], b[6]) # cx, cy00000000000000000,
                #在目标颜色区域的中心画十字形标记
            Lm = (b[2]+b[3])/2 #b[2]色块的外框的宽 ，b[3]色块的外框的高
            pixels=b[4]#色块的像素数量
            length = K/Lm
        #print(length)#长度27
        #print(Lm)#像素点
            size=K2*Lm
            print(size)#色块的外框的平均直径
            K3=13/140
            b2=K3*b[2]
            b3=K3*b[3]
            K4=17.74*12.9/24846
            area=pixels*K4#物体的面积
            ratio=pixels/76241*100#76241为摄像头检测出来的像素点个数
            img.draw_string(x,y, "area=")#写面积
            img.draw_string(x+40, y, str(area))#写面积
            img.draw_string(x,y+10, "pixels=")#像素点
            img.draw_string(x+40, y+10, str(pixels))#写像素点。
            img.draw_string(x,y+20, "pixel ratio=")#像素占比
            img.draw_string(x+60, y+20, str(ratio))#像素占比
            #utime.sleep(2) #延时2秒

            lcd.display(img)#lcd屏幕显示
