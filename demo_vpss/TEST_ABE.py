#!/usr/bin/python
# -*- coding: utf-8 -*-

# system modules
import sys
import os
import shutil
from subprocess import call

# mysql module
#import MySQLdb as mdb

# ftp module
#from ftplib import FTP

# global definitions
#from cpabe_def import *

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

GROUP_NAME = "SS512"
TEST_FOLDER = os.path.join(os.getcwd(), "test_abe")
PK = "public.k"
MK = "master.k"

PT = "prova.txt"
CT = "prova.txt.enc"

# -------------------
# TEST ABE SCHEME
# -------------------

if os.path.exists(TEST_FOLDER):
    shutil.rmtree(TEST_FOLDER)
os.mkdir( TEST_FOLDER, 0755 )

with open(os.path.join(TEST_FOLDER, PT), "w") as f:
    f.write("ciao come va???")
f.close()

# ---------------------------------------------------------------------------

print "======================================================================"
print "Checking abe setup..."
# ABE setup
ret = call([
            "python3", "abe-setup.py",
             GROUP_NAME,
             TEST_FOLDER,
             os.path.join(TEST_FOLDER, PK),
             os.path.join(TEST_FOLDER, MK)
          ])
if ret != 0:
    print("ABE-setup failed!*****************")
else:
    print("ABE-setup OK!")

# ---------------------------------------------------------------------------

print "======================================================================"
print "Checking abe keygen..."

# ABE keygen: create one user key
SK1 = "user_secret1.k" 
SK2 = "user_secret2.k" 
ATTR_LIST1 = "ATTR1"
ATTR_LIST2 = "ATTR1,ATTR2"
ret = call([
            "python3", "abe-keygen.py",
            os.path.join(TEST_FOLDER, GROUP_NAME + ".g"),
            os.path.join(TEST_FOLDER, MK),
            os.path.join(TEST_FOLDER, PK),
            ATTR_LIST1,
            os.path.join(TEST_FOLDER, SK1)
          ])
if ret != 0:
    print("ABE-keygen failed!*****************")
else:
    print("ABE-keygen OK!")
    
ret = call([
            "python3", "abe-keygen.py",
            os.path.join(TEST_FOLDER, GROUP_NAME + ".g"),
            os.path.join(TEST_FOLDER, MK),
            os.path.join(TEST_FOLDER, PK),
            ATTR_LIST2,
            os.path.join(TEST_FOLDER, SK2)
          ])
if ret != 0:
    print("ABE-keygen failed!*****************")
else:
    print("ABE-keygen OK!")
# ---------------------------------------------------------------------------

print "======================================================================"
print "Generating random elliptic curve point..."

SYMK = "symmetric.k"
# ABE generate random point on elliptic curve
ret = call([
            "python3", "abe-random-ec-point.py",
            os.path.join(TEST_FOLDER, GROUP_NAME + ".g"),
            os.path.join(TEST_FOLDER, SYMK)
          ])
if ret != 0:
    print("ABE-random_ec_point failed!*****************")
else:
    print("ABE-random_ec_point OK!")

# ---------------------------------------------------------------------------

print "======================================================================"
print "Checking abe encryption..."

# ABE encryption
SYMK_ENC = "prova.txt.k.enc"
ret = call([
            "python3", "abe-encrypt.py",
            os.path.join(TEST_FOLDER, GROUP_NAME + ".g"),
            os.path.join(TEST_FOLDER, PK),
            "(ATTR1 and ATTR2)",
            os.path.join(TEST_FOLDER, SYMK),
            os.path.join(TEST_FOLDER, SYMK_ENC)
          ])
if ret != 0:
    print("ABE-encrypt failed!*****************")
else:
    print("ABE-encrypt OK!")

# AES encryption
ret = call([
      "python3", "aescrypt.py", "-f",
      os.path.join(TEST_FOLDER, PT),
      os.path.join(TEST_FOLDER, CT),
      os.path.join(TEST_FOLDER, SYMK)
    ])
if ret != 0:
    print("AES-encrypt failed!*****************")
else:
    print("AES-encrypt OK!")
    
# remove original files
print ("Removing:\n" + SYMK + "\n" + PT)
os.remove(os.path.join(TEST_FOLDER, SYMK))
os.remove(os.path.join(TEST_FOLDER, PT))
print ("Done!")

# ---------------------------------------------------------------------------

print "======================================================================"
print "Checking abe decryption does not work when policy not satisfied..."
# FAILED ABE decryption
RET = call([
            "python3", "abe-decrypt.py",
            os.path.join(TEST_FOLDER, GROUP_NAME + ".g"),
            os.path.join(TEST_FOLDER, PK),
            os.path.join(TEST_FOLDER, SK1),
            os.path.join(TEST_FOLDER, SYMK_ENC),
            os.path.join(TEST_FOLDER, SYMK)
          ])
if ret != 0:
    print("ABE-decrypt failed!*****************")
else:
    print("ABE-decrypt OK!")
    
# FAILED AES decryption
ret = call([
            "python3", "aescrypt.py", "-d", "-f",
            os.path.join(TEST_FOLDER, CT),
            os.path.join(TEST_FOLDER, PT),
            os.path.join(TEST_FOLDER, SYMK)
          ])
if ret != 0:
    print("AES-decrypt failed!*****************")
else:
    print("AES-decrypt OK!")
    
print "Done!"

# ---------------------------------------------------------------------------

print "======================================================================"
print "Checking abe decryption works when policy satisfied..."
# ABE decryption
ret = call([
            "python3", "abe-decrypt.py",
            os.path.join(TEST_FOLDER, GROUP_NAME + ".g"),
            os.path.join(TEST_FOLDER, PK),
            os.path.join(TEST_FOLDER, SK2),
            os.path.join(TEST_FOLDER, SYMK_ENC),
            os.path.join(TEST_FOLDER, SYMK)
          ])
if ret != 0:
    print("ABE-decrypt failed!*****************")
else:
    print("ABE-decrypt OK!")
# AES decryption
ret = call([
        "python3", "aescrypt.py", "-d", "-f",
        os.path.join(TEST_FOLDER, CT),
        os.path.join(TEST_FOLDER, PT),
        os.path.join(TEST_FOLDER, SYMK)
      ])
if ret != 0:
    print("AES-decrypt failed!*****************")
else:
    print("AES-decrypt OK!")
# ---------------------------------------------------------------------------

# remove encrypted files
#os.remove(os.path.join(TEST_FOLDER, SYMK))
#os.remove(os.path.join(TEST_FOLDER, CT))
#os.remove(os.path.join(TEST_FOLDER, SYMK_ENC))
print "Done!"

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

print "======================================================================"
print "Ready to start!"

