import sys

for i in range(0, 2):
    print("hello canmv")
    print("hello ", end="canmv\n")

print("implementation:", sys.implementation)
print("platform:", sys.platform)
print("path:", sys.path)
print("Python version:", sys.version)

print("please input string, end with Enter")
r = sys.stdin.readline()
w_len = sys.stdout.write(r)


