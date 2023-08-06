import sensor, image, time,math
from pyb import UART
from pid import PID
from pyb import Servo

pan_servo=Servo(1)
tilt_servo=Servo(2)

pan_servo.calibration(500,2500,500)
tilt_servo.calibration(500,2500,500)
#设置阈值
grayscale_thres = (0, 128)
rgb565_thres = (63, 100, -62, -20, -3, 65)
def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
    return max_blob
# 初始化最左上方的黑点坐标
leftmost_black_x = None
leftmost_black_y = None

red_threshold  =    (0, 00, 0, 0, 0, 0)       # (63, 100, -62, -20, -3, 65)#绿色光跟踪(100, 100, 0, 0, 0, 0)
hong            = (73, 93, -80, 125, -128, 127)#归位红色
row_data=[-1,-1]
#pan_pid = PID(p=0.07, i=0, imax=90) #脱机运行或者禁用图像传输，使用这个PID
#tilt_pid = PID(p=0.05, i=0, imax=90) #脱机运行或者禁用图像传输，使用这个PID
pan_pid = PID(p=0.09, i=0.05, imax=90)#在线调试使用这个PID
tilt_pid = PID(p=0.09, i=0.030, imax=90)#在线调试使用这个PID
uart = UART(3, 9600)
sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # 灰度更快(160x120 max on OpenMV-M7)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(10) # Let new settings take affect.
sensor.set_auto_whitebal(False) # turn this off.
sensor.set_auto_gain(False) # 关闭增益（色块识别时必须要关）
clock = time.clock() # Tracks FPS.


threshold=[( 0, 15, -26, 7, -16, 21)]

x=0
y=0#矩形左上角
k=0
i=0
shu=0
m=0
o=0
f=1
n=0
pan_servo.angle(91.35)
tilt_servo.angle(93.031)#这个位置开始
while(True):

    clock.tick() # Track elapsed milliseconds between snapshots().
     # 下面的`threshold`应设置为足够高的值，以滤除在图像中检测到的具有
    # 低边缘幅度 的噪声矩形。最适用与背景形成鲜明对比的矩形。
    img = sensor.snapshot()
    for r in img.find_rects(threshold = 15000):
        img.draw_rectangle(r.rect(), color = (255, 0, 0))
        for p in r.corners(): img.draw_circle(p[0], p[1], 5, color = (0, 255, 0))
        #print(r)

    blobs = img.find_blobs([hong],pixels_threshold=0,area_threshold=0)
    if blobs:
            max_blob = find_max(blobs)
            img.draw_rectangle(max_blob.rect()) # rect
            img.draw_cross(max_blob.cx(), max_blob.cy()) # cx, cy
            #pan_error = max_blob.cx()  -r.x()#与矩形左上角x偏差
            #tilt_error = max_blob.cy() -r.y()
            print('偏差',pan_error,tilt_error)



    if f==1:

       m=m+0.4
       print('m',m)
       pan_servo.angle(91.35)
       tilt_servo.angle(93.031+m)#这个位置开始
       i=1
       if m>15.1:
           f=2
    if(f==2):
       k=k+0.4
       pan_servo.angle(91.35+k)
       tilt_servo.angle(93.031+m)#这个位置开始
       print('k',k)
       if k>13:
           f=3
    if(f==3):
       o=o+0.4
       pan_servo.angle(91.35+k)
       tilt_servo.angle(93.031+m-o)#这个位置开始
       print('o',o)
       if o>16:
           f=4
    if(f==4):
       n=n+0.4
       pan_servo.angle(91.35+k-n)
       tilt_servo.angle(93.031+m-o)#这个位置开始
       print('n',n)
       if n>13:
           f=5
         #openmv自带的寻找色块函数。
            #pixels_threshold是像素阈值，面积小于这个值的色块就忽略
            #roi是感兴趣区域，只在这个区域内寻找色块
            #are_threshold是面积阈值，如果色块被框起来的面积小于这个值，会被过滤掉
                #print('该形状占空比为',blob.density())


            #pan_error = max_blob.cx()-img.width()/2
            #tilt_error = max_blob.cy()-img.height()/2
            #if(pan_error>-6 and pan_error<6):
             #pan_error=0
            #if(tilt_error>-6 and tilt_error<6):
             #tilt_error=0
            #if(pan_error==0 and tilt_error==0): #识别到红色激光笔
              #uart.write('1')#发送给32，让32发出声音和光线
            #print("pan_error: ", pan_error)
            #print("tilt_error",tilt_error)
            #img.draw_rectangle(max_blob.rect()) # rect
            #img.draw_cross(max_blob.cx(), max_blob.cy()) # cx, cy

                        #max_blob = find_max(blobs)
                        #if(m==0):
                             #m=1
                             #shu=r.x()
                        #pan_error = max_blob.cx()-shu+7#与矩形左上角x偏差
                        #tilt_error = max_blob.cy() -r.y()-7


                        #if(pan_error>-4 and pan_error<4):
                         #pan_error=0
                        #if(tilt_error>4 and tilt_error<4):
                         #tilt_error=0
                        #if(pan_error==0 and tilt_error==0): #识别到红色激光笔
                          #uart.write('1')#发送给32，让32发出声音和光线
                        #print("pan_error: ", pan_error)
                        #print("tilt_error",tilt_error)
                        #img.draw_rectangle(max_blob.rect()) # rect
                        #img.draw_cross(max_blob.cx(), max_blob.cy()) # cx, cy

                        #pan_output=pan_pid.get_pid(pan_error,1)/2
                        #tilt_output=tilt_pid.get_pid(tilt_error,1)

                        #print(pan_servo.angle()+pan_output,tilt_servo.angle()-tilt_output)
                        #pan_servo.angle(pan_servo.angle()-pan_output)
                        #tilt_servo.angle(tilt_servo.angle()+tilt_output)
                        #jiange=r.w()/10
                        #shu=shu+jiange
            #pan_output=pan_pid.get_pid(pan_error,1)/2
            #tilt_output=tilt_pid.get_pid(tilt_error,1)

            ##print(pan_servo.angle()+pan_output,tilt_servo.angle()-tilt_output)
            #pan_servo.angle(pan_servo.angle()+pan_output)
            #tilt_servo.angle(tilt_servo.angle()-tilt_output)
