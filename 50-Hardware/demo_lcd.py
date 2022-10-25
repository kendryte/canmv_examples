
import lcd, time

lcd.init()
#lcd.direction(lcd.XY_RLDU)

#lcd.init(type=2, invert=True) # cube ips
#lcd.init(width=320, height=240, invert=True, freq=20000000)

lcd.clear(lcd.RED)

lcd.rotation(0)
lcd.draw_string(30, 30, "hello canmv", lcd.WHITE, lcd.RED)
time.sleep(1)
lcd.rotation(1)
lcd.draw_string(60, 60, "hello canmv", lcd.WHITE, lcd.RED)
time.sleep(1)
lcd.rotation(2)
lcd.draw_string(120, 60, "hello canmv", lcd.WHITE, lcd.RED)
time.sleep(1)
lcd.rotation(3)
lcd.draw_string(120, 120, "hello canmv", lcd.WHITE, lcd.RED)
time.sleep(1)
