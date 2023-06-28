import json
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
# from Crypto.Random import get_random_bytes
import sys

data = "cat".encode()
key = "0123456789abcdef".encode()
nonce = "0".encode()
cipher = AES.new(key, AES.MODE_CTR, nonce = nonce)
ct_bytes = cipher.encrypt(data)
ct = b64encode(ct_bytes).decode('utf-8')
result = json.dumps({'nonce':b64encode(nonce).decode('utf-8'), 'ciphertext':ct})
print(key)
print(ct_bytes)
print(nonce)


try:
    b64 = json.loads(result)
    nonce = b64decode(b64['nonce'])
    ct = b64decode(b64['ciphertext'])
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    pt = cipher.decrypt(ct).decode()
    print("The message was: ", pt)

    hash_object = SHA256.new(data)
    print ("The hash is: ",hash_object.hexdigest())
    print (type(hash_object))
except (ValueError, KeyError):
    print("Incorrect decryption")