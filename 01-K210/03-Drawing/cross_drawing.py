# Cross Drawing
#
# This example shows off drawing crosses on the CanMV Cam.

import sensor, image, time, urandom

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # or GRAYSCALE...
sensor.set_framesize(sensor.QVGA) # or QQVGA...
sensor.skip_frames(time = 2000)
clock = time.clock()

while(True):
    clock.tick()

    img = sensor.snapshot()

    for i in range(10):
        x = (urandom.getrandbits(30) % (2*img.width())) - (img.width()//2)
        y = (urandom.getrandbits(30) % (2*img.height())) - (img.height()//2)
        r = (urandom.getrandbits(30) % 127) + 128
        g = (urandom.getrandbits(30) % 127) + 128
        b = (urandom.getrandbits(30) % 127) + 128

        # If the first argument is a scaler then this method expects
        # to see x and y. Otherwise, it expects a (x,y) tuple.
        img.draw_cross(x, y, color = (r, g, b), size = 10, thickness = 2)

    print(clock.fps())
