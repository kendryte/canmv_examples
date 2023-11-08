import sensor, image, time, lcd

from maix import KPU
import gc

lcd.init()
# sensor.reset(freq=48000000, dual_buff=True) # improve fps
sensor.reset()                      # Reset and initialize the sensor. It will
                                    # run automatically, call sensor.run(0) to stop
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 1000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

#anchor =(3.44/32, 4.06/32, 4.06/32, 5.60/32, 4.69/32, 7.19/32, 6.25/32, 8.12/32, 7.81/32, 11.26/32, 10.94/32, 15.11/32, 16.25/32, 21.43/32, 28.75/32, 35.19/32, 68.13/32, 77.63/32)
anchor = (0.1075, 0.126875, 0.126875, 0.175, 0.1465625, 0.2246875, 0.1953125, 0.25375, 0.2440625, 0.351875, 0.341875, 0.4721875, 0.5078125, 0.6696875, 0.8984375, 1.099687, 2.129062, 2.425937)
kpu = KPU()
kpu.load("/sd/KPU/yolo_face_detect/face_detect_320x240.kmodel")
yolo = kpu.Yolo2()
yolo.init(anchor, 0.5, 0.2)

print("Start run")
try:
    while True:
        #print("mem free:",gc.mem_free())
        clock.tick()                    # Update the FPS clock.
        img = sensor.snapshot()
        kpu.run(img)
        dect = yolo.run()
        fps = clock.fps()
        if len(dect) > 0:
            print("dect:",dect)
            for l in dect :
                a = img.draw_rectangle(l[0],l[1],l[2],l[3], color=(0, 255, 0))

        a = img.draw_string(0, 0, "%2.1ffps" %(fps), color=(0, 60, 128), scale=2.0)
        lcd.display(img)
        gc.collect()
except Exception as e:
    print(e)
    kpu.deinit()
    del kpu
    gc.collect()
