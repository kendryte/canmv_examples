#------http server--------------------
html = """<!DOCTYPE html>
<html>
    <head> <title>canmv web</title> </head>
    <body> <h1>canmv web</h1>
        <br />
        <a >
        hello world
        </a>
    </body>
</html>
"""

import socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)

    response = html
    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    cl.send(response)
    cl.close()
