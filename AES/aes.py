
import json
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad
from sys import getsizeof

data = {"sequence":123,"hum":11,"temp":11,"soil":23,"light":198}
 
key = b'longlonglonglong' #global

test = bytearray(b'\xAD\x5D\xE2\x07\xB7\x88\xF9\x11\xDC\x6C\xD6\xD2\x2F\x23\xF4\x7B\xBE\x69\xAD\x8E\xDE\xD4\x57\xAB\x72\x3B\x99\xD2\x8A\xE4\xA4\x11\xDB\x9D\x6A\x83\xC1\x58\x8A\xDE\x3A\x5E\xD3\x95\x3B\x98\xF7\x91\xD5\x59\x5B\xED\xB2\x3C\x61\x64\x41\xD9\x98\x1D\x83\x4D\x31\xB5')

data_str = json.dumps(data)

data_str_1 = "rV3iB7eI+RHcNbSLyP0e75prY7e1FercjuZ0orkpBHbnWqDwViK3jpe05U7mPeR1Vlb7bI8YWRB2Zgdg00xtY81F/x6X8niaMCarzGutJePNR8el/J4mjAmq8xrrSXjzUX/HpfyeJowJqvMa60l481F/x6X8niaMCarzGutJc="

def encrypt_aes(str_payload):
	bytes_payload = bytes(str_payload, 'utf-8')
	cipher = AES.new(key, AES.MODE_ECB)
	ct_bytes = cipher.encrypt(pad(bytes_payload, AES.block_size))
	print(ct_bytes, type(ct_bytes))
	return ct_bytes

def decrypt_aes(encrypted_message):
	try:
		cipher = AES.new(key, AES.MODE_ECB)
		decrypted_msg = unpad(cipher.decrypt(encrypted_message), AES.block_size)
		return decrypted_msg.decode("utf-8")
	except (ValueError, KeyError):
		print("Incorrect decryption")

test_1 = encrypt_aes(json.dumps(data))

decrypt_msg = decrypt_aes(test_1)
print("The message was: ", decrypt_msg)
print(getsizeof(decrypt_msg))



data_test = json.loads(decrypt_msg)
print(data_test)