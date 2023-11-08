# 开启一个socket server 等待客户端连接
#--------socket server test-----------
import socket
ip = "192.168.0.102"
port = 8080
#ip = n.ifconfig()[0]                     #获取本地IP
print ('ip:',ip)
listenSocket = socket.socket()   #创建套接字
listenSocket.bind((ip, port))   #绑定地址和端口号
listenSocket.listen(1)   #监听套接字
listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   #设置套接字
print ('tcp waiting...')

while True:
    print("accepting.....")
    conn, addr = listenSocket.accept()   #接收连接请求，返回收发数据的套接字对象和客户端地址
    print(addr, "connected")

    while True:
        data = conn.recv(1024)   #接收数据（1024字节大小）
        if(len(data) == 0):   #判断客户端是否断开连接
            print("close socket")
            conn.close()   #关闭套接字
            break
        print(data)
        ret = conn.send(data)   #发送数据
