from fpioa_manager import fm

# need your connect hardware IO 10/11 to loopback
fm.register(35, fm.fpioa.UART1_TX, force=True)
fm.register(34, fm.fpioa.UART1_RX, force=True)

from machine import UART

uart_A = UART(UART.UART1, 115200, 8, 1, 0, timeout=1000, read_buf_len=4096)

import time

time.sleep_ms(100) # wait uart ready
uart_A.write(b'hello world')

while True:
  if uart_A.any():
    while uart_A.any():
      read_data = uart_A.read()
      print("recv = ", read_data) # recv =  b'hello world'
    break
  time.sleep_ms(10) # ohter event

uart_A.deinit()
del uart_A
