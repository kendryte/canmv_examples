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

od_img = image.Image(size=(320,256))

anchor = (0.8125, 0.4556, 1.1328, 1.2667, 1.8594, 1.4889, 1.4844, 2.2000, 2.6484, 2.9333)
kpu = KPU()
print("ready load model")
kpu.load("/sd/KPU/yolo_hand_detect/hand_detect.kmodel")
yolo = kpu.Yolo2()
yolo.init(anchor, 0.7, 0.3)

print("Start run")
try:
    while True:
        gc.collect()
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

        a = img.draw_string(0, 0, "%2.1ffps" %(fps), color=(0, 60, 128), scale=2.0)
        lcd.display(img)
except Exception as e:
    print(e)
    kpu.deinit()
    del kpu
    gc.collect()
