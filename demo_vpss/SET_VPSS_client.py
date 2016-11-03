#!/usr/bin/python
# -*- coding: utf-8 -*-

# system modules
import sys
import os
import shutil
from subprocess import call

# mysql module
import MySQLdb as mdb

# ftp module
from ftplib import FTP

# global definitions
from vpss_def import *

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

print "======================================================================"
print "Setting up client folders..."

# -------------------
# SETUP ABE FOLDERS
# -------------------

# ---------------------------------------------------------------------------

# remove old folders
#if os.path.exists(AUTH_FOLDER):
#    shutil.rmtree(AUTH_FOLDER)
if os.path.exists(USER_FOLDER):
    shutil.rmtree(USER_FOLDER)
if os.path.exists(PUBLIC_PARAMETERS_FOLDER):
    shutil.rmtree(PUBLIC_PARAMETERS_FOLDER)

# set new cleaned folders
#os.mkdir( AUTH_FOLDER, 0755 )
#os.mkdir( AUTH_MASTER_KEY_FOLDER, 0755 )
#os.mkdir( AUTH_SECRET_KEY_FOLDER, 0755 )
#os.mkdir( AUTH_TEzaq12wsxMP_FOLDER, 0755 )

os.mkdir(PUBLIC_PARAMETERS_FOLDER, 0755 )
os.mkdir(USER_FOLDER, 0755 )

for i in range(len(USERS)):
    os.mkdir(os.path.join(USER_FOLDER,USERS[i]["name"]), 0755 )
    # prepare USERNAME folder
    os.mkdir(os.path.join(USER_FOLDER,USERS[i]["name"], USER_CIPHERTEXT), 0755 )
    os.mkdir(os.path.join(USER_FOLDER,USERS[i]["name"], USER_PLAINTEXT), 0755 )
    os.mkdir(os.path.join(USER_FOLDER,USERS[i]["name"], USER_SECRET_KEYS), 0755 )
    os.mkdir(os.path.join(USER_FOLDER,USERS[i]["name"], USER_ABE_KEY), 0755 )
    os.mkdir(os.path.join(USER_FOLDER,USERS[i]["name"], USER_AES_KEY), 0755 )
    os.mkdir(os.path.join(USER_FOLDER,USERS[i]["name"], USER_SEARCH_KEY), 0755 )
    # generate plaintext file
    for pt in PT:
        with open(os.path.join(USER_FOLDER,USERS[i]["name"], USER_PLAINTEXT, \
                               pt),"w") as f:
            f.write("Questo e' un file di prova scritto dall'utente "+ \
                    USERS[i]["name"] + " con nome originale " + pt)
        f.close()
    # put search key in folder
    with open(os.path.join(USER_FOLDER,USERS[i]["name"], USER_SEARCH_KEY, \
              SEAK), "w") as f:
        f.write(search_iv + ":" + search_key)
    f.close

# ---------------------------------------------------------------------------

print "Done!"

