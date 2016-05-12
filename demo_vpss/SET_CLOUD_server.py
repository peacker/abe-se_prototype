#!/usr/bin/python
# -*- coding: utf-8 -*-

# system modules
import sys
import os
import shutil
from subprocess import call

# ftp module
from ftplib import FTP

# global definitions
from vpss_def import *

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

# ----------------------
# SETUP FTP CLOUD SERVER
# ----------------------
print "======================================================================"
print "Setting up cloud ftp server..."
# login
ftp = FTP(CLOUD_SERVER)
ftp.login(user=CLOUD_USERNAME, passwd = CLOUD_PASSWORD)

# get list of files
files = []
try:
    files = ftp.nlst()
except ftplib.error_perm, resp:
    if str(resp) == "550 No files found":
        print "No files in this directory"
    else:
        raise

# empty cloud folder
for f in files:
    ftp.delete(f)

# close connection
ftp.quit() 

print "Done!"

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
