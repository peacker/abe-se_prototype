from abenc_waters09 import *

from charm.toolbox.pairinggroup import PairingGroup,GT

from charm.core.engine.util import objectToBytes,bytesToObject



# ----------------------------------------------------------------------------

# abe steps
group = PairingGroup('SS512')
cpabe = CPabe(group)
msg = group.random(GT)
(master_secret_key, master_public_key) = cpabe.setup()
policy = '((ONE or THREE) and (TWO or FOUR))'
attr_list = ['THREE', 'ONE', 'TWO']
secret_key = cpabe.keygen(master_public_key, master_secret_key, attr_list)
cipher_text = cpabe.encrypt(master_public_key, msg, policy)
decrypted_msg = cpabe.decrypt(master_public_key, secret_key, cipher_text)
decrypted_msg == msg

# ----------------------------------------------------------------------------

# serialization
objectToBytes(cipher_text,group)

# ----------------------------------------------------------------------------
from aescrypt import *

import argparse
import os
import struct
import sys
 
from getpass import getpass
from os.path import exists, splitext
 
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from pbkdf2 import PBKDF2

# aes steps
password = "ciao"

# parameters
SALT_MARKER = b'$'
ITERATIONS = 1000

key_size=32
salt_marker=SALT_MARKER
kdf_iterations=ITERATIONS
hashmod=SHA256

bs = AES.block_size
header = salt_marker + struct.pack('>H', kdf_iterations) + salt_marker
salt = os.urandom(bs - len(header))
kdf = PBKDF2(password, salt, min(kdf_iterations, 65535), hashmod)
key = kdf.read(key_size)
iv = os.urandom(bs)
cipher = AES.new(key, AES.MODE_CBC, iv)

with open("/home/ema/Dropbox/LAVORO/demo_cpabe/users/utente1/plaintexts/ciao.txt", "rb") as infile:
    #outfile.write(header + salt)
    c = header + salt
    #outfile.write(iv)
    c = c + iv
    finished = False
    while not finished:
        chunk = infile.read(1024 * bs)
        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = (bs - len(chunk) % bs) or bs
            chunk += (padding_length * chr(padding_length)).encode()
            finished = True
        #outfile.write(cipher.encrypt(chunk))
        c = c + cipher.encrypt(chunk)

infile.close()

