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


anchor_head_detect = (0.1074, 0.1458, 0.1367, 0.2137, 0.1758, 0.2824, 0.2441, 0.3333, 0.2188, 0.4167, 0.2969, 0.5000, 0.4102, 0.6667, 0.6094, 0.9722, 1.2364, 1.6915)
head_kpu = KPU()
print("ready load model")
# head_kpu.load("/sd/KPU/head_body_detect/uint8_head_detect_v1_old.kmodel")
head_kpu.load(0x300000)
yolo = head_kpu.Yolo2()
yolo.init(anchor_head_detect, 0.7, 0.2)


print("Start run")
try:
    while True:
        gc.collect()
        clock.tick()                    # Update the FPS clock.
        img = sensor.snapshot()
        a = od_img.draw_image(img, 0,0)
        od_img.pix_to_ai()
        head_kpu.run(od_img)
        head_boxes = yolo.run()
        if len(head_boxes) > 0:
            for l in head_boxes :
                a = img.draw_rectangle(l[0],l[1],l[2],l[3], color=(0, 255, 0))

        fps = clock.fps()
        a = img.draw_string(0, 0, "%2.1ffps" %(fps), color=(0, 60, 128), scale=2.0)
        lcd.display(img)
except:
    head_kpu.deinit()
    del head_kpu
    gc.collect()

