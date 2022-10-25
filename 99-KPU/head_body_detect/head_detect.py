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
head_kpu.load_kmodel("/sd/KPU/head_body_detect/uint8_head_detect_v1_old.kmodel")
head_kpu.init_yolo2(anchor_head_detect, anchor_num=9, img_w=320, img_h=240, net_w=320 , net_h=256 ,layer_w=10 ,layer_h=8, threshold=0.7, nms_value=0.2, classes=1)


while True:
    gc.collect()
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()
    a = od_img.draw_image(img, 0,0)
    od_img.pix_to_ai()
    head_kpu.run_with_output(od_img)
    head_boxes = head_kpu.regionlayer_yolo2()
    if len(head_boxes) > 0:
        for l in head_boxes :
            a = img.draw_rectangle(l[0],l[1],l[2],l[3], color=(0, 255, 0))

    fps = clock.fps()
    a = img.draw_string(0, 0, "%2.1ffps" %(fps), color=(0, 60, 128), scale=2.0)
    lcd.display(img)

head_kpu.deinit()

