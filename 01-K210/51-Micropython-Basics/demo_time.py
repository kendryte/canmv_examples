import time
import machine

print(time.time())
t1 = time.localtime(546450051)
print('t1', t1)
t2 = time.mktime(t1)
print('t2', t2)
print(time.time())
time.set_time(t1)
print(time.time())
time.sleep(1)
print(time.localtime(time.time()))
