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

print "======================================================================"
print "Setting up authority folders..."

# -----------------------
# SETUP AUTHORITY FOLDERS
# -----------------------

# NB: this part of the python script
#     must be run on authority server.

# remove old folders
if os.path.exists(AUTH_FOLDER):
    shutil.rmtree(AUTH_FOLDER)

# set new cleaned folders
os.mkdir( AUTH_FOLDER, 0755 )
os.mkdir( AUTH_MASTER_KEY_FOLDER, 0755 )
os.mkdir( AUTH_SECRET_KEY_FOLDER, 0755 )
os.mkdir( AUTH_TEMP_FOLDER, 0755 )

# prepare USERNAME folder
os.mkdir( os.path.join(AUTH_FOLDER, USER_CIPHERTEXT), 0755 )
os.mkdir(os.path.join(AUTH_FOLDER, USER_PLAINTEXT), 0755 )

os.mkdir(os.path.join(AUTH_FOLDER, USER_SECRET_KEYS), 0755 )
os.mkdir(os.path.join(AUTH_FOLDER, USER_ABE_KEY), 0755 )
os.mkdir(os.path.join(AUTH_FOLDER, USER_AES_KEY), 0755 )
os.mkdir(os.path.join(AUTH_FOLDER, USER_SEARCH_KEY), 0755 )

# this folder should be public... maybe in the cloud (ftp)!!!
if not os.path.exists(AUTH_FOLDER):
    os.mkdir(PUBLIC_PARAMETERS_FOLDER, 0755 )

# ---------------------------------------------------------------------------

# -------------------------------
# SETUP MYSQL AUTHORITY SERVER DB
# -------------------------------

print "Setting up authority database..."
try:
    #con = mdb.connect(AUTH_SERVER, AUTH_USER, AUTH_PASSWORD, AUTH_NAME)
    con = mdb.connect(AUTH_SERVER, AUTH_ROOT, AUTH_ROOTPWD)
    with con:
        cur = con.cursor()
        # remove db
        cur.execute("DROP DATABASE IF EXISTS " + AUTH_NAME)

        # remove table
        #cur.execute("SET FOREIGN_KEY_CHECKS = 0")
        #cur.execute("DROP TABLE IF EXISTS users")
        #cur.execute("DROP TABLE IF EXISTS cloud")
        #cur.execute("DROP TABLE IF EXISTS keywords")
        #cur.execute("SET FOREIGN_KEY_CHECKS = 1")

        # create db
        cur.execute("CREATE DATABASE " + AUTH_NAME)
        cur.execute("USE " + AUTH_NAME)

        # remove user
        # next command creates user if does not exists
        cur.execute("GRANT USAGE ON *.* TO '" + AUTH_USER + "'@'" + AUTH_SERVER + "' IDENTIFIED BY '"  + AUTH_PASSWORD + "';")
        cur.execute("GRANT USAGE ON *.* TO '" + AUTH_USER + "'@'%' IDENTIFIED BY '"  + AUTH_PASSWORD + "';")
        cur.execute("DROP USER '" + AUTH_USER + "'@'" + AUTH_SERVER + "';")
        cur.execute("DROP USER '" + AUTH_USER + "'@'%';")
        cur.execute("FLUSH PRIVILEGES")

        # create user
        cur.execute("CREATE USER '" + AUTH_USER + "'@'" + AUTH_SERVER + "' IDENTIFIED BY '" + AUTH_PASSWORD + "';")
        #cur.execute("CREATE USER '" + AUTH_USER + "'@'localhost' IDENTIFIED BY '" + AUTH_PASSWORD + "';")
        cur.execute("CREATE USER '" + AUTH_USER + "'@'%' IDENTIFIED BY '" + AUTH_PASSWORD + "';")

        cur.execute("GRANT ALL ON *.* TO '" + AUTH_USER + "'@'" + AUTH_SERVER + "' ;")
        #cur.execute("GRANT ALL ON *.* TO '" + AUTH_USER + "'@'localhost' ;")
        cur.execute("GRANT ALL ON *.* TO '" + AUTH_USER + "'@'%' ;")

        # create userstable
        cur.execute("CREATE TABLE users( \
                     Id INT PRIMARY KEY AUTO_INCREMENT, \
                     Usr VARCHAR(64), \
                     Pwd VARCHAR(64) \
                    )")
        # fill users table
        for i in range(len(USERS)):
            # insert entries to the table
            cur.execute("INSERT INTO users( \
                       Usr, \
                       Pwd \
                      ) VALUES ( \
                       '" + USERS[i]['name'] + "', \
                       '" + USERS[i]['pwd'] + "' \
                      )"
                     )
            con.commit()
        """
        cur.execute("INSERT INTO users( \
                   Usr, \
                   Pwd \
                  ) VALUES ( \
                   'AUTHORITY', \
                   '123' \
                  )"
                 )
            con.commit()
        """
                  
        # create attributes table
        cur.execute("CREATE TABLE attributes( \
                     Id INT PRIMARY KEY AUTO_INCREMENT, \
                     Id_user INT NOT NULL, \
                     Attr VARCHAR(64), \
                     FOREIGN KEY Id_user(Id_user) \
                     REFERENCES users(Id) \
                     ON UPDATE NO ACTION \
                     ON DELETE CASCADE \
                    ) ENGINE=InnoDB")
        # fill attributes table
        for i in range(len(USERS)):
            for j in range(len(USERS[i]["attr"])):
                mysql_command = "INSERT INTO attributes (Id_user, attr) \
                                 VALUES ( (SELECT Id from users \
                                           WHERE Usr='" + \
                                                 USERS[i]["name"]  + "'), \
                                          '" + USERS[i]["attr"][j] + "')"
                cur.execute( mysql_command )
                con.commit()
        """
        for i in range(len(ATTRIBUTES)):
            mysql_command = "INSERT INTO attributes (Id_user, attr) \
                             VALUES ( (SELECT Id from users \
                                       WHERE Usr='AUTHORITY'), \
                                      '" + ATTRIBUTES[i] + "')"
            cur.execute( mysql_command )
            con.commit()
        """
except mdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
finally:    
    if con:    
        con.close()
print "Done!"

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
