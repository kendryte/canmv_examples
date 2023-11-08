# LCD Example
#
# Note: To run this example you will need a LCD Shield for your CanMV Cam.
#
# The LCD Shield allows you to view your CanMV Cam's frame buffer on the go.

import sensor, image, lcd

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QVGA) # Special QVGA(320x240) framesize for LCD Shield.
lcd.init() # Initialize the lcd screen.

while(True):
    lcd.display(sensor.snapshot()) # Take a picture and display the image.
