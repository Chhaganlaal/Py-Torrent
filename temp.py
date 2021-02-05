import base64
import os

buffer = bytes.fromhex('0000041727101980')
print(buffer.hex())
buffer = buffer + bytes.fromhex('00000000')
buffer += os.urandom(4)

print(buffer[:4])