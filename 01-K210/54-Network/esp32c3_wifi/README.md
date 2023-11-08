# esp32c3 wifi

- 该功能仅适用于canmv_k1板子，板上自带esp32c3 wifi芯片，与sd卡共用spi1总线，分时复用。
- 默认固件没有将该功能编译进来，打开需要配置编译选项" Components configuration → Enbale micropython component → Micropython configurations → Modules configurations"下 "Enable esp32xx hosted driver"，并关闭"Enable WIZNET5K"
