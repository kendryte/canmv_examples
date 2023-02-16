import sensor, image, time, lcd
from maix import KPU
import gc

lcd.init()
sensor.reset()                      # Reset and initialize the sensor. It will
                                    # run automatically, call sensor.run(0) to stop
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
#sensor.set_vflip(1)
sensor.skip_frames(time = 1000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

od_img = image.Image(size=(320,256))

obj_name = ("aeroplane","bicycle", "bird","boat","bottle","bus","car","cat","chair","cow","diningtable", "dog","horse", "motorbike","person","pottedplant", "sheep","sofa", "train", "tvmonitor")
anchor = (1.3221, 1.73145, 3.19275, 4.00944, 5.05587, 8.09892, 9.47112, 4.84053, 11.2364, 10.0071)
kpu = KPU()
print("ready load model")
#kpu.load(0x300000, 1536936)
kpu.load("/sd/KPU/voc20_object_detect/voc20_detect.kmodel")
yolo = kpu.Yolo2()
yolo.init(anchor, 0.5, 0.2)

i = 0
print("Start run")
try:
    while True:
        i += 1
        print("cnt :", i)
        clock.tick()                    # Update the FPS clock.
        img = sensor.snapshot()
        a = od_img.draw_image(img, 0,0)
        od_img.pix_to_ai()
        kpu.run(od_img)
        dect = yolo.run()
        fps = clock.fps()
        if len(dect) > 0:
            print("dect:",dect)
            for l in dect :
                a = img.draw_rectangle(l[0],l[1],l[2],l[3], color=(0, 255, 0))
                a = img.draw_string(l[0],l[1], obj_name[l[4]], color=(0, 255, 0), scale=1.5)

        a = img.draw_string(0, 0, "%2.1ffps" %(fps), color=(0, 60, 128), scale=1.0)
        lcd.display(img)
        gc.collect()
except:
    kpu.deinit()
    del kpu
    gc.collect()
