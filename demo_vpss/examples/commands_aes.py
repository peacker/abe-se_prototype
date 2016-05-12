from Crypto.Cipher import AES

message = "ciao"

# encrypt
# padd message with commas ","
obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
padded_message = message + "," * (16 - (len(message) % 16))
ciphertext = obj.encrypt(padded_message)
ciphertext

# decrypt
obj2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
plaintext = obj2.decrypt(ciphertext).replace(",","")
plaintext

"""
from Crypto.Cipher import AES

keywords = [u'missione4', u'roma', u'giugno']
search_key = "0123456789abcdef"
search_iv = "0000000000000000"
enc_keywords = []
for w in keywords:
    obj = AES.new(search_key, AES.MODE_CBC, search_iv)
    padd_w = w + "," * (16 - (len(w) % 16))
    print(obj.encrypt(padd_w))
    enc_keywords.append(obj.encrypt(padd_w).encode("hex"))

enc_keywords
"""
