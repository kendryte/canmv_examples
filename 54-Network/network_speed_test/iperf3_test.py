# Start the server on Windows first: iperf3.exe -s -p 5201

import iperf3
# tcp test
iperf3.client('192.168.137.1', reverse=True, bandwidth=30 * 1024 * 1024)

# udp test
iperf3.client('192.168.137.1', udp=True, bandwidth=30 * 1024 * 1024)

