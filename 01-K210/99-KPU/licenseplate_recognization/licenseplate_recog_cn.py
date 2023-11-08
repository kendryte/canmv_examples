import sensor, image, time, lcd
from maix import KPU, utils
import gc

lcd.init()
sensor.reset()                      # Reset and initialize the sensor. It will
                                    # run automatically, call sensor.run(0) to stop
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 1000)     # Wait for settings take effect.
#sensor.set_hmirror(1)
#sensor.set_vflip(1)
clock = time.clock()                # Create a clock object to track the FPS.
#image.font_load(image.UTF8, 16, 16, '/sd/font/0xA00000_font_uincode_16_16_tblr.Dzk') # load chinese font file
image.font_load(image.UTF8, 16, 16, 0xA00000)

province_cn = ("皖沪津渝冀晋蒙辽吉黑苏浙京闽赣鲁豫鄂湘粤桂琼川贵云藏陕甘青宁新")
ads = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

anchor = (8.30891522166988, 2.75630994889035, 5.18609903718768, 1.7863757404970702, 6.91480529053198, 3.825771881004435, 10.218567655549439, 3.69476690620971, 6.4088204258368195, 2.38813526350986)
kpu = KPU()
kpu.load_kmodel("/sd/KPU/licenseplate_recognization/lp_detect.kmodel")
kpu.init_yolo2(anchor, anchor_num=5, img_w=320, img_h=240, net_w=320 , net_h=240 ,layer_w=20 ,layer_h=15, threshold=0.7, nms_value=0.3, classes=0)

lp_recog_kpu = KPU()
lp_recog_kpu.load_kmodel("/sd/KPU/licenseplate_recognization/lp_recog.kmodel")
#lp_recog_kpu.lp_recog_load_weight_data(0x600000, 1498500) # load after-process data
lp_recog_kpu.lp_recog_load_weight_data("/sd/KPU/licenseplate_recognization/lp_weight.bin") # load after-process data

RATIO = 0.16
def extend_box(x, y, w, h, scale):
    x1_t = x - scale*w
    x2_t = x + w + scale*w
    y1_t = y - scale*h
    y2_t = y + h + scale*h
    x1 = int(x1_t) if x1_t>1 else 1
    x2 = int(x2_t) if x2_t<320 else 319
    y1 = int(y1_t) if y1_t>1 else 1
    y2 = int(y2_t) if y2_t<256 else 255
    cut_img_w = x2-x1+1
    cut_img_h = y2-y1+1
    return x1, y1, cut_img_w, cut_img_h

lp_index_list = []

while 1:
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()
    kpu.run_with_output(img)
    dect = kpu.regionlayer_yolo2()
    fps = clock.fps()
    if len(dect) > 0:
        #print("dect:",dect)
        for l in dect :
            x1, y1, cut_img_w, cut_img_h= extend_box(l[0], l[1], l[2], l[3], scale=RATIO)
            lp_cut = img.cut(x1, y1, cut_img_w, cut_img_h)
            a=img.draw_rectangle(l[0],l[1],l[2],l[3], color=(255, 0, 0))
            lp_resize = lp_cut.resize(208,64)
            a=lp_resize.replace(vflip=0, hmirror=1)
            lp_resize.pix_to_ai()
            lp_recog_kpu.run_with_output(lp_resize)
            out = lp_recog_kpu.lp_recog()
            #print("out:",len(out))
            lp_index_list.clear()
            for n in out:
                max_score = max(n)
                index = n.index(max_score)
                lp_index_list.append(index)
            del (lp_cut)
            del (lp_resize)
            show_lp_str = "%s   %s-%s%s%s%s%s" %(province_cn[lp_index_list[0]], ads[lp_index_list[1]], ads[lp_index_list[2]],
                ads[lp_index_list[3]], ads[lp_index_list[4]], ads[lp_index_list[5]], ads[lp_index_list[6]])
            print(show_lp_str)
            a=img.draw_string(l[0], l[1]-18, show_lp_str, color=(255, 128, 0), scale=1)
    #img.replace(vflip=0, hmirror=1)
    a=img.draw_string(10, 0, "%2.1ffps" %(fps), color=(255, 255, 0), scale=1)
    lcd.display(img)
    # print("mem free:",gc.mem_free())
    # print("heap free:",utils.heap_free())
    gc.collect()

image.font_free()
kpu.deinit()
lp_recog_kpu.deinit()
