#-------socket cleint---------
import socket, time
s = socket.socket()         # 创建 socket 对象
host = '192.168.0.102'      # server ip
port = 8080                # 设置端口号

s.connect((host, port))

while True:
    msg = '123456'
    s.send(msg)
    time.sleep(1)
