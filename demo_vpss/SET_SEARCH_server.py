#!/usr/bin/python
# -*- coding: utf-8 -*-

# system modules
import sys
import os
import shutil
from subprocess import call

# mysql module
import MySQLdb as mdb

# global definitions
from vpss_def import *

# ---------------------------------------------------------------------------

# ----------------------------
# SETUP MYSQL SEARCH SERVER DB
# ----------------------------
print "======================================================================"
print "Setting up search database..."
try:
    #con = mdb.connect(SEARCH_SERVER, SEARCH_USER, SEARCH_PASSWORD, SEARCH_NAME)
    con = mdb.connect(SEARCH_SERVER, SEARCH_ROOT, SEARCH_ROOTPWD)
    with con:
        cur = con.cursor()
        # remove db
        cur.execute("DROP DATABASE IF EXISTS " + SEARCH_NAME)

        # remove table
        #cur.execute("SET FOREIGN_KEY_CHECKS = 0")
        #cur.execute("DROP TABLE IF EXISTS users")
        #cur.execute("DROP TABLE IF EXISTS cloud")
        #cur.execute("DROP TABLE IF EXISTS keywords")
        #cur.execute("SET FOREIGN_KEY_CHECKS = 1")

        # create db
        cur.execute("CREATE DATABASE " + SEARCH_NAME)
        cur.execute("USE " + SEARCH_NAME)

        # remove user
        # next command creates user if does not exists
        cur.execute("GRANT USAGE ON *.* TO '" + SEARCH_USER + "'@'" + SEARCH_SERVER + "' IDENTIFIED BY '"  + SEARCH_PASSWORD + "';")
        cur.execute("GRANT USAGE ON *.* TO '" + SEARCH_USER + "'@'%' IDENTIFIED BY '"  + SEARCH_PASSWORD + "';")

        cur.execute("DROP USER '" + SEARCH_USER + "'@'" + SEARCH_SERVER + "';")
        cur.execute("DROP USER '" + SEARCH_USER + "'@'%';")
        cur.execute("FLUSH PRIVILEGES")

        # create user
        cur.execute("CREATE USER '" + SEARCH_USER + "'@'" + SEARCH_SERVER + "' IDENTIFIED BY '" + SEARCH_PASSWORD + "';")
        #cur.execute("CREATE USER '" + SEARCH_USER + "'@'localhost' IDENTIFIED BY '" + SEARCH_PASSWORD + "';")
        cur.execute("CREATE USER '" + SEARCH_USER + "'@'%' IDENTIFIED BY '" + SEARCH_PASSWORD + "';")

        cur.execute("GRANT ALL ON *.* TO '" + SEARCH_USER + "'@'" + SEARCH_SERVER + "' ;")
        #cur.execute("GRANT ALL ON *.* TO '" + SEARCH_USER + "'@'localhost' ;")
        cur.execute("GRANT ALL ON *.* TO '" + SEARCH_USER + "'@'%' ;")

        # create encrypted file  table
        cur.execute("CREATE TABLE cloud( \
                     Id INT PRIMARY KEY AUTO_INCREMENT, \
                     FileName VARCHAR(64), \
                     FilePath VARCHAR(1024), \
                     Policy VARCHAR(1024), \
                     PKName VARCHAR(64), \
                     Curve VARCHAR(64), \
                     SecLev VARCHAR(64), \
                     Encryptor VARCHAR(64), \
                     Keywords VARCHAR(1024), \
                     UploadDate DATETIME, \
                     Time VARCHAR(64)\
                    ) ENGINE=InnoDB")
        # create keywords table
        cur.execute("CREATE TABLE keywords( \
                     Id INT PRIMARY KEY AUTO_INCREMENT, \
                     Id_file INT NOT NULL, \
                     Kw VARCHAR(64), \
                     FOREIGN KEY Id_file(Id_file) \
                     REFERENCES cloud(Id) \
                     ON UPDATE NO ACTION \
                     ON DELETE CASCADE \
                    ) ENGINE=InnoDB")

except mdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
finally:    
    if con:    
        con.close()
print "Done!"

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
