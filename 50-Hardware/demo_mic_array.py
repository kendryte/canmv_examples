from maix import mic_array as mic
import lcd

lcd.init()
#mic.init()  # 默认配置
mic.init(i2s_d0=12, i2s_d1=13, i2s_d2=14, i2s_d3=15, i2s_ws=24, i2s_sclk=25, sk9822_dat=11, sk9822_clk=10)# for CanMV_K210

#mic.init(i2s_d0=20, i2s_d1=21, i2s_d2=15, i2s_d3=8, i2s_ws=7, i2s_sclk=6, sk9822_dat=25, sk9822_clk=24)# for maix cube

while True:
    imga = mic.get_map()            # 获取声音源分布图像
    b = mic.get_dir(imga)           # 计算、获取声源方向
    a = mic.set_led(b,(0,0,255))    # 配置 RGB LED 颜色值
    imgb = imga.resize(160,160)
    imgc = imgb.to_rainbow(1)       # 将图像转换为彩虹图像
    a = lcd.display(imgc)
mic.deinit()
