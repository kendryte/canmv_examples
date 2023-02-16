import sensor, image, time, lcd
from maix import KPU
import gc

lcd.init()
sensor.reset()                      # Reset and initialize the sensor. It will
                                    # run automatically, call sensor.run(0) to stop
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 1000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

anchor = (0.1075, 0.126875, 0.126875, 0.175, 0.1465625, 0.2246875, 0.1953125, 0.25375, 0.2440625, 0.351875, 0.341875, 0.4721875, 0.5078125, 0.6696875, 0.8984375, 1.099687, 2.129062, 2.425937)
kpu = KPU()
kpu.load("/sd/KPU/yolo_face_detect/face_detect_320x240.kmodel")
yolo = kpu.Yolo2()
yolo.init(anchor, 0.5, 0.2)

lm68_kpu = KPU()
print("ready load model")
lm68_kpu.load("/sd/KPU/face_detect_with_68landmark/landmark68.kmodel")

RATIO = 0.08
def extend_box(x, y, w, h, scale):
    x1_t = x - scale*w
    x2_t = x + w + scale*w
    y1_t = y - scale*h
    y2_t = y + h + scale*h
    x1 = int(x1_t) if x1_t>1 else 1
    x2 = int(x2_t) if x2_t<320 else 319
    y1 = int(y1_t) if y1_t>1 else 1
    y2 = int(y2_t) if y2_t<240 else 239
    cut_img_w = x2-x1+1
    cut_img_h = y2-y1+1
    return x1, y1, cut_img_w, cut_img_h

print("Start run")
try:
    while 1:
        gc.collect()
        #print("mem free:",gc.mem_free())
        clock.tick()                    # Update the FPS clock.
        img = sensor.snapshot()
        kpu.run(img)
        dect = yolo.run()
        fps = clock.fps()
        if len(dect) > 0:
            print("dect:",dect)
            for l in dect :
                x1, y1, cut_img_w, cut_img_h = extend_box(l[0], l[1], l[2], l[3], scale=RATIO) # 扩大人脸框
                face_cut = img.cut(x1, y1, cut_img_w, cut_img_h)
                a = img.draw_rectangle(l[0],l[1],l[2],l[3], color=(0, 255, 0))
                face_cut_128 = face_cut.resize(128, 128)
                face_cut_128.pix_to_ai()
                lm68_kpu.run(face_cut_128)
                out = lm68_kpu.get_outputs()
                #print("out:",len(out))
                for j in range(68):
                    x = int(kpu.Act.sigmoid(out[2 * j])*cut_img_w + x1)
                    y = int(kpu.Act.sigmoid(out[2 * j + 1])*cut_img_h + y1)
                    #a = img.draw_cross(x, y, size=1, color=(0, 0, 255))
                    a = img.draw_circle(x, y, 2, color=(0, 0, 255), fill=True)
                del (face_cut_128)
                del (face_cut)

        a = img.draw_string(0, 0, "%2.1ffps" %(fps), color=(0, 60, 255), scale=2.0)
        lcd.display(img)
        gc.collect()
except:
    kpu.deinit()
    lm68_kpu.deinit()
    del kpu
    del lm68_kpu
    gc.collect()
