import gc

print(gc.mem_free() / 1024) # stack mem

import maix

print(maix.utils.heap_free() / 1024) # heap mem
