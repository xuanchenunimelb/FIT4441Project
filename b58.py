import base58

text = "['val0', 'val1']"
base58Str = base58.b58encode(text.encode('utf-8')).decode('utf-8')
print(base58Str)

text = base58.b58decode(base58Str).decode('utf-8')
print(text)