#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys

try:

##############################################################################

con = mdb.connect('localhost', 'cpabeuser', 'cpabe123', 'cpabedb');

"""
cur = con.cursor()
cur.execute("SELECT VERSION()")

ver = cur.fetchone()

print "Database version : %s " % ver
"""    


with con:
    cur = con.cursor()
    
    # remove table
    cur.execute("DROP TABLE IF EXISTS cloud")

    # create table
    cur.execute("CREATE TABLE cloud( \
                 Id INT PRIMARY KEY AUTO_INCREMENT, \
                 FileName VARCHAR(64), \
                 FilePath VARCHAR(1024), \
                 Policy VARCHAR(1024), \
                 Encryptor VARCHAR(64), \
                 Keywords VARCHAR(1024), \
                 UploadDate DATE\
                )")
    # insert entries to the table
    cur.execute("INSERT INTO cloud( \
                   FileName, \
                   FilePath, \
                   Policy, \
                   PKName, \
                   Encryptor, \
                   Keywords, \
                   UploadDate \
                  ) VALUES ( \
                   'prova.txt.enc', \
                   '/home/cloud/prova.txt.enc', \
                   '(ATTR1 and ATTR2)', \
                   'public1.k', \
                   'utente1', \
                   'parola1,parola2,parola3', \
                   CURDATE() \
                  )"
                 )

    # retrieve data
    cur.execute("SELECT * FROM cloud")
    rows = cur.fetchall()
    for row in rows:
        print row
##############################################################################

except mdb.Error, e:
  
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    
finally:    
        
    if con:    
        con.close()
