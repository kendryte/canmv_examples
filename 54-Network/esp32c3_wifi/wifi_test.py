
#-------station mode-------------
import network
n = network.WLAN(network.STA_IF)
n.active(True)
#n.scan()
n.connect("mywifi", "12345678")


#-------ap mode-----------------
a = network.WLAN(network.AP_IF)
#a.config(ssid="canmv_ap", password="12345678", channel=1, txpower=56)
a.active(True) # the default ap name is "CanMV", password is "12345678"

# Get parameters values
print(a.config("ssid"))
print(a.config("mac"))
print(a.config("txpower"))

#-------socket test--------------
import socket
sockaddr = socket.getaddrinfo('www.baidu.com', 80)[0][-1]
print(sockaddr)
