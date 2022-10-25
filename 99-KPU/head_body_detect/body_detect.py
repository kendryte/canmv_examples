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

anchor_body_detect = (0.0978, 0.1758, 0.1842, 0.3834, 0.3532, 0.5982, 0.4855, 1.1146, 0.8869, 1.6407, 1.2388, 3.4157, 2.0942, 2.1114, 2.7138, 5.0008, 6.0293, 6.4540)
body_kpu = KPU()
print("ready load model")
body_kpu.load_kmodel("/sd/KPU/head_body_detect/uint8_person_detect_v1_old.kmodel")
body_kpu.init_yolo2(anchor_body_detect, anchor_num=9, img_w=320, img_h=240, net_w=320 , net_h=256 ,layer_w=10 ,layer_h=8, threshold=0.7, nms_value=0.2, classes=1)

while True:
    gc.collect()
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()
    a = od_img.draw_image(img, 0,0)
    od_img.pix_to_ai()

    body_kpu.run_with_output(od_img)
    body_boxes = body_kpu.regionlayer_yolo2()
    if len(body_boxes) > 0:
        for l in body_boxes :
            a = img.draw_rectangle(l[0],l[1],l[2],l[3], color=(255, 0, 0))

    fps = clock.fps()
    a = img.draw_string(0, 0, "%2.1ffps" %(fps), color=(0, 60, 128), scale=2.0)
    lcd.display(img)

body_kpu.deinit()
