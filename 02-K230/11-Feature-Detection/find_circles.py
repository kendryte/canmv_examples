# Find Circles Example
#
# This example shows off how to find circles in the image using the Hough
# Transform. https://en.wikipedia.org/wiki/Circle_Hough_Transform
#
# Note that the find_circles() method will only find circles which are completely
# inside of the image. Circles which go outside of the image/roi are ignored...

from media.camera import *
from media.display import *
from media.media import *
import time, os, gc, sys

DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080
SCALE = 4
DETECT_WIDTH = DISPLAY_WIDTH // SCALE
DETECT_HEIGHT = DISPLAY_HEIGHT // SCALE

def camera_init():
    # use hdmi for display
    display.init(LT9611_1920X1080_30FPS)
    # config vb for osd layer
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4*DISPLAY_WIDTH*DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE
    # meida buffer config
    media.buffer_config(config)
    # init default sensor
    camera.sensor_init(CAM_DEV_ID_0, CAM_DEFAULT_SENSOR)
    # set chn0 output size
    camera.set_outsize(CAM_DEV_ID_0, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    # set chn0 output format
    camera.set_outfmt(CAM_DEV_ID_0, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)
    # create meida source device
    globals()["meida_source"] = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    # create meida sink device
    globals()["meida_sink"] = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    # create meida link
    media.create_link(meida_source, meida_sink)
    # set display plane with video channel
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)
    # set chn1 output nv12
    camera.set_outsize(CAM_DEV_ID_0, CAM_CHN_ID_1, DETECT_WIDTH, DETECT_HEIGHT)
    camera.set_outfmt(CAM_DEV_ID_0, CAM_CHN_ID_1, PIXEL_FORMAT_RGB_888)
    # media buffer init
    media.buffer_init()
    # request media buffer for osd image
    globals()["buffer"] = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # start stream for camera device0
    camera.start_stream(CAM_DEV_ID_0)

def camera_deinit():
    # stop stream for camera device0
    camera.stop_stream(CAM_DEV_ID_0)
    # deinit display
    display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # release media buffer
    media.release_buffer(globals()["buffer"])
    # destroy media link
    media.destroy_link(globals()["meida_source"], globals()["meida_sink"])
    # deinit media buffer
    media.buffer_deinit()

def capture_picture():
    # create image for drawing
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # create image for osd
    buffer = globals()["buffer"]
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, alloc=image.ALLOC_VB, phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr, poolid=buffer.pool_id)
    osd_img.clear()
    display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD0)
    fps = time.clock()
    while True:
        fps.tick()
        try:
            os.exitpoint()
            rgb888_img = camera.capture_image(CAM_DEV_ID_0, CAM_CHN_ID_1)
            img = rgb888_img.to_rgb565()
            camera.release_image(CAM_DEV_ID_0, CAM_CHN_ID_1, rgb888_img)
            draw_img.clear()
            # Circle objects have four values: x, y, r (radius), and magnitude. The
            # magnitude is the strength of the detection of the circle. Higher is
            # better...

            # `threshold` controls how many circles are found. Increase its value
            # to decrease the number of circles detected...

            # `x_margin`, `y_margin`, and `r_margin` control the merging of similar
            # circles in the x, y, and r (radius) directions.

            # r_min, r_max, and r_step control what radiuses of circles are tested.
            # Shrinking the number of tested circle radiuses yields a big performance boost.

            for c in img.find_circles(threshold = 2000, x_margin = 10, y_margin = 10, r_margin = 10,
                                        r_min = 2, r_max = 100, r_step = 2):
                draw_img.draw_circle(c.x()*SCALE, c.y()*SCALE, c.r()*SCALE, color = (255, 0, 0))
                print(c)
            draw_img.copy_to(osd_img)
            del img
            gc.collect()
            print(fps.fps())
        except KeyboardInterrupt as e:
            print("user stop: ", e)
            break
        except BaseException as e:
            sys.print_exception(e)
            break

def main():
    os.exitpoint(os.EXITPOINT_ENABLE)
    camera_is_init = False
    try:
        print("camera init")
        camera_init()
        camera_is_init = True
        print("camera capture")
        capture_picture()
    except Exception as e:
        sys.print_exception(e)
    finally:
        if camera_is_init:
            print("camera deinit")
            camera_deinit()

if __name__ == "__main__":
    main()
