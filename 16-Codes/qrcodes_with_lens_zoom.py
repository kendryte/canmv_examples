# QRCode Example
#
# This example shows the power of the CanMV Cam to detect QR Codes
# without needing lens correction.

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
# sensor.set_windowing((240, 240)) # look at center 240x240 pixels of the VGA resolution.
# sensor.set_hmirror(True)
# sensor.set_vflip(True)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must turn this off to prevent image washout...
clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    for code in img.find_qrcodes():
        img.draw_rectangle(code.rect(), color = 127)
        print(code)
    print(clock.fps())
