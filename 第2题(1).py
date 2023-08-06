import sensor, image, time
from pyb import UART
from pid import PID
from pyb import Servo

pan_servo=Servo(1)
tilt_servo=Servo(2)

pan_servo.calibration(500,2500,500)
tilt_servo.calibration(500,2500,500)
#设置阈
grayscale_thres = (0, 128)
rgb565_thres = (63, 100, -62, -20, -3, 65)



red_threshold  =    (0, 00, 0, 0, 0, 0)       # 这个一班不用管
hong            = (47, 91, 13, 42, 23, -31)#归位红色激光笔(47, 91, 13, 42, 23, -31)
row_data=[-1,-1]
#pan_pid = PID(p=0.07, i=0, imax=90) #脱机运行或者禁用图像传输，使用这个PID
#tilt_pid = PID(p=0.05, i=0, imax=90) #脱机运行或者禁用图像传输，使用这个PID
pan_pid = PID(p=0.045, i=0.01, imax=90)#在线调试使用这个PID
tilt_pid = PID(p=0.02, i=0.005, imax=90)#在线调试使用这个PID
uart = UART(3, 9600)
sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # use RGB565.
sensor.set_framesize(sensor.SVGA) # use QQVGA for speed.
sensor.skip_frames(10) # Let new settings take affect.
sensor.set_auto_whitebal(False) # turn this off.
sensor.set_auto_gain(False) # 关闭增益（色块识别时必须要关）
clock = time.clock() # Tracks FPS.

def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
    return max_blob

threshold=[( 0, 15, -26, 7, -16, 21)]
i=0
xx=0
yy=0
xxx=0#x坐标5次计数
yyy=0#
k=0
shu=0#计数5次中心点跳出中心点采集
guiwei=0
ii=0

xbu=0
ybu=0

x1=0
x2=0
x3=0
x4=0

zuo1=0
zuoshang=0
you=0
youxia=0
zuo=0
zuoshang1=0

zhongjianmaichongx=0
zhongjianmaichongu=0
jinruyici=0
pan_servo.angle(80)
tilt_servo.angle(80.205)
while(True):

    clock.tick() # Track elapsed milliseconds between snapshots().
    if(k==0): #中心点采集5次
       while(True):
         k=1#防止进入第二次
         img = sensor.snapshot()
         img = img.binary([grayscale_thres])
         img= img.dilate(4)
         img = img.negate()

         # 下面的`threshold`应设置为足够高的值，以滤除在图像中检测到的具有
    # 低边缘幅度的噪声矩形。最适用与背景形成鲜明对比的矩形。


         blobs = img.find_blobs([red_threshold],roi=(264,127,213,194))
         #openmv自带的寻找色块函数。
            #pixels_threshold是像素阈值，面积小于这个值的色块就忽略
            #roi是感兴趣区域，只在这个区域内寻找色块
            #are_threshold是面积阈值，如果色块被框起来的面积小于这个值，会被过滤掉
            #print('该形状占空比为',blob.density())


         if blobs:

            max_blob = find_max(blobs)
            if max_blob:


            #print('该形状的面积为',area)
             #density函数居然可以自动返回色块面积/外接矩形面积这个值，太神奇了，官方文档还是要多读！
                if max_blob.density()>0.78:#理论上矩形和他的外接矩形应该是完全重合
            #但是测试时候发现总会有偏差，多次试验取的这个值。下面圆形和三角形亦然
                    shu=shu+1
                    #img.draw_rectangle(max_blob.rect(),color=(255,255,255))
                    #print(max_blob.cx(), max_blob.cy())#这个是停止点坐标，就是第一题坐标
                    print('长方形长',max_blob.density())
                    xx=max_blob.cx()
                    yy= max_blob.cy()
                    xxx=xxx+xx
                    yyy=yyy+yy
                    #print("xx和yy",xx,yy)
                    if(shu>=5):
                     xxx=xxx/5#我们要的坐标
                     yyy=yyy/5
                     print("xxx和yyy总和",xxx,yyy)
                     guiwei=1#表示开始归为
                     break
    if(guiwei==1):
         pan_servo.angle(96)
         tilt_servo.angle(100.205)
         sensor.reset() # Initialize the camera sensor.
         sensor.set_pixformat(sensor.RGB565) # use RGB565.
         sensor.set_framesize(sensor.SVGA) # use QQVGA for speed.
         sensor.skip_frames(10) # Let new settings take affect.
         sensor.set_auto_whitebal(False) # turn this off.
         sensor.set_auto_gain(False) # 关闭增益（色块识别时必须要关）
         clock = time.clock() # Tracks FPS.


         while(True):
                    #clock.tick() # Track elapsed milliseconds between snapshots().
                    img = sensor.snapshot()
                    blobs = img.find_blobs([hong])
             #openmv自带的寻找色块函数。
                #pixels_threshold是像素阈值，面积小于这个值的色块就忽略
                #roi是感兴趣区域，只在这个区域内寻找色块
                #are_threshold是面积阈值，如果色块被框起来的面积小于这个值，会被过滤掉
                    #print('该形状占空比为',blob.density())



                    if blobs:
                        max_blob = find_max(blobs)

                        pan_error = xxx-max_blob.cx()
                        tilt_error = yyy -max_blob.cy()
                        #if(pan_error>-7 and pan_error<7):
                         #pan_error=0
                        #if(tilt_error>7 and tilt_error<7):
                         #tilt_error=0
                        #if(pan_error==0 and tilt_error==0): #识别到红色激光笔
                          #uart.write('1')#发送给32，让32发出声音和光线
                        print("pan_error: ", pan_error)
                        print("tilt_error",tilt_error)
                        img.draw_rectangle(max_blob.rect()) # rect
                        img.draw_cross(max_blob.cx(), max_blob.cy()) # cx, cy
                        #if(pan_error>0 ):#需要往右走  x变小是往右

                            #pan_servo.angle(96+xbu)
                            #xbu=xbu+0.1#步长2
                            #print('xbu',xbu)
                        #if(pan_error<0):#需要往左走  x变大是往左

                            #pan_servo.angle(96-xbu)
                            #xbu=xbu+0.1#步长2
                            #print('xbu',xbu)
                        #if(tilt_error>0):#需要往下走

                            #tilt_servo.angle(100.205-ybu)
                            #ybu=ybu+0.1#步长2
                            #print('ybu',ybu)
                        #if(tilt_error<0):#需要往上走
                            #print('ybu',ybu)
                            #tilt_servo.angle(100.205+ybu)
                            #print
                            #ybu=ybu+0.1#步长2
                        if(jinruyici==0):
                               jinruyici=jinruyici+1
                               if(pan_error==0 or pan_error<0) and (tilt_error>0 or tilt_error==0):
                                 fangzhi2ci=1
                               if (pan_error==0 or pan_error>0) and (tilt_error<0 or tilt_error==0 ):
                                 fangzhi2ci=2
                               if(pan_error==0 or pan_error<0 )and(tilt_error<0 or tilt_error==0 ):
                                 fangzhi2ci=3
                               if(pan_error>0 or pan_error==0) and( tilt_error>0 or tilt_error==0):
                                 fangzhi2ci=4
                        buchang=0.06#步长度，调大了就变快了，精度可能好可能坏，多试试根据你电机调



                        #######重点调上面那个
                        if(fangzhi2ci==1) :
                          if x1==1 and (tilt_error<2 or tilt_error==0):
                             guiwei=2
                             zhongjianmaichongx=96-xbu
                             zhongjianmaichongy=100.205-ybu
                             break
                             print('任务1已经归为')

                          if pan_error<0 or pan_error==0:
                             x1=1
                          if pan_error<0 and x1==0:
                             pan_servo.angle(96-xbu)
                             xbu=xbu+buchang#步长2
                             #print('xbu',96+xbu)

                          if x1==1 and tilt_error>0:
                             tilt_servo.angle(100.205-ybu)
                             ybu=ybu+buchang#步长2


                             #print('ybu',100.205-ybu)
                          if x1==1 and (tilt_error<2 or tilt_error==0):
                             zhongjianmaichongx=96-xbu
                             zhongjianmaichongy=100.205-ybu
                             print('任务1已经归为')
                             guiwei=2
                             break




                        if (fangzhi2ci==2):
                          if x2==1 and (tilt_error>-2 or tilt_error==0):
                             guiwei=2
                             zhongjianmaichongx=96+xbu
                             zhongjianmaichongy=100.205+ybu
                             break
                             print('任务2已经归为')
                          if pan_error<0 or pan_error==0:
                             x2=1
                          if pan_error>0 and x2==0:
                             pan_servo.angle(96+xbu)
                             xbu=xbu+buchang#步长2
                             #print('xbu',96+xbu)

                          if x2==1 and tilt_error<0:
                             tilt_servo.angle(100.205+ybu)
                             ybu=ybu+buchang#步长2
                             #print('ybu',96+xbu)
                          if x2==1 and (tilt_error>-2 or tilt_error==0):
                             guiwei=2
                             zhongjianmaichongx=96+xbu
                             zhongjianmaichongy=100.205+ybu
                             print('任务2已经归为')
                             break



                        if(fangzhi2ci==3 ):
                          if x3==1 and (tilt_error>-2 or tilt_error==0):
                             guiwei=2
                             zhongjianmaichongx=96-xbu
                             zhongjianmaichongy=100.205+ybu
                             break
                             print('任务3已经归为')
                          if pan_error>0 or pan_error==0:
                             x3=1
                          if pan_error<0 and x3==0:
                             pan_servo.angle(96-xbu)
                             xbu=xbu+buchang#步长2
                             #print('xbu',96-xbu)

                          if x3==1 and tilt_error<0:
                             tilt_servo.angle(100.205+ybu)
                             ybu=ybu+buchang#步长2
                             #print('ybu',96+xbu)
                          if x3==1 and (tilt_error>-2 or tilt_error==0):
                             guiwei=2
                             zhongjianmaichongx=96-xbu
                             zhongjianmaichongy=100.205+ybu
                             print('任务3已经归为')
                             break

                        if(fangzhi2ci==4):
                          if x4==1 and (tilt_error<5 or tilt_error==0):
                             guiwei=2
                             zhongjianmaichongx=96+xbu
                             zhongjianmaichongy=100.205-ybu
                             break
                             print('任务4已经归为')
                          if pan_error<0 or pan_error==0:
                             x4=1
                          if pan_error>0 and x4==0:
                             pan_servo.angle(96+xbu)
                             xbu=xbu+buchang#步长2
                             #print('xbu',96+xbu)

                          if x4==1 and tilt_error>0:
                             tilt_servo.angle(100.205-ybu)
                             ybu=ybu+buchang#步长2
                             #print('ybu',100.205+ybu)
                          if x4==1 and (tilt_error<8 or tilt_error==0):
                             guiwei=2
                             zhongjianmaichongx=96+xbu
                             zhongjianmaichongy=100.205-ybu
                             print('任务4已经归为')
                             break


                        #else:
                          #pan_servo.angle(96+xbu)
                          #tilt_servo.angle(100.205+ybu)
                        #pan_output=pan_pid.get_pid(pan_error,1)/2
                        #tilt_output=tilt_pid.get_pid(tilt_error,1)

                        #print(pan_servo.angle()+pan_output,tilt_servo.angle()-tilt_output)
                        #pan_servo.angle(pan_servo.angle()+pan_output)
                        #tilt_servo.angle(tilt_servo.angle()-tilt_output)

                        #pan_servo.angle(96)
                        #tilt_servo.angle(100.205)
    if (guiwei==2):
        biaozhi=1
        xunxian=0
        m=0
        mm=0
        mmm=0
        mmmm=0
        mmmmm=0
        mmmmmm=0
        print(zhongjianmaichongx,zhongjianmaichongy)
        while(True)  :
               img = sensor.snapshot()
    #for r in img.find_rects(threshold = 15000):
        #img.draw_rectangle(r.rect(), color = (255, 0, 0))
        #for p in r.corners(): img.draw_circle(p[0], p[1], 5, color = (0, 255, 0))
        #print(r)

               blobs = img.find_blobs([hong],pixels_threshold=0,area_threshold=0)
               if blobs:
                    max_blob = find_max(blobs)
                    img.draw_rectangle(max_blob.rect()) # rect
                    img.draw_cross(max_blob.cx(), max_blob.cy()) # cx, cy
               if (biaozhi==1):

                   m=m+0.4
                   print('m',m)
                   pan_servo.angle(zhongjianmaichongx+m)
                   tilt_servo.angle(zhongjianmaichongy)#这个位置开始

                   print(m)
                   if m>14.5:
                       biaozhi=2
               if (biaozhi==2):

                   mm=mm+0.4
                   print('mm',mm)
                   pan_servo.angle(zhongjianmaichongx+m)
                   tilt_servo.angle(zhongjianmaichongy-mm)#这个位置开始

                   print("mm",mm)
                   if mm>11.7:
                       biaozhi=3
                       #while(True):
                        #i=1
               if (biaozhi==3):

                   mmm=mmm+0.4
                   print('mmm',mmm)
                   pan_servo.angle(zhongjianmaichongx+m-mmm)
                   tilt_servo.angle(zhongjianmaichongy-mm)#这个位置开始

                   print("mmm",mmm)
                   if mmm>30.1:
                       biaozhi=4
                       #while(True):
                        #i=1
               if (biaozhi==4):

                   mmmm=mmmm+0.4
                   print('mmmm',mmmm)
                   pan_servo.angle(zhongjianmaichongx+m-mmm)
                   tilt_servo.angle(zhongjianmaichongy-mm+mmmm)#这个位置开始

                   print("mmmm",mmmm)
                   if mmmm>27.1:
                       biaozhi=5
                       #while(True):
                        #i=1
               if (biaozhi==5):

                   mmmmm=mmmmm+0.4
                   print('mmmmm',mmmmm)
                   pan_servo.angle(zhongjianmaichongx+m-mmm+mmmmm)
                   tilt_servo.angle(zhongjianmaichongy-mm+mmmm)#这个位置开始

                   print("mmmmm",mmmmm)
                   if mmmmm>29.1:
                       biaozhi=6
                       #while(True):
                        #i=1
               if (biaozhi==6):

                   mmmmmm=mmmmmm+0.4
                   print('mmmmmm',mmmmmm)
                   pan_servo.angle(zhongjianmaichongx+m-mmm+mmmmm)
                   tilt_servo.angle(zhongjianmaichongy-mm+mmmm-mmmmmm)#这个位置开始

                   print("mmmmmm",mmmmmm)
                   if mmmmmm>14.7:
                       biaozhi=7
                       while(True):
                        i=1
