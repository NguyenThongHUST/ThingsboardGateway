import json
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

res = 'd2v9zAT9wO8rWH5hAAswoQ=='
print(type(res))

key = b'Xinchaocacban123'

try:
    cipher = AES.new(key, AES.MODE_ECB)
    ct = b64decode(res)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    print("The message was: ", pt)
except (ValueError, KeyError):
    print("Incorrect decryption")