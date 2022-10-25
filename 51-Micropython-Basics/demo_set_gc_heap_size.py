import machine
import maix

gc_mem_size = 1024*1024

print('config micropython gc stack 1M (1024KB) if not')
if maix.utils.gc_heap_size() != gc_mem_size:
    maix.utils.gc_heap_size(gc_mem_size)
    print('updates take effect when you reboot the system. ')
    machine.reset()

print('Current: ', maix.utils.gc_heap_size())

