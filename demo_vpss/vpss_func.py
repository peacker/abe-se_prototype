# import other libraries
import os   # operating system functions
import sys
import glob
import re   # regular expression
import shutil

from subprocess import call

# for server connection
from ftplib import FTP

# for mysql connection
import MySQLdb as mdb

# to encrypt keywords
from Crypto.Cipher import AES

# definitions
from vpss_def import *

# for operating system primitives
import os


import time

# ----------------------------------------------------------------------------

"""
verbose = True
if verbose:
    def verboseprint(*args):
        # Print each argument separately so caller doesn't need
        # to stuff everything to be printed into a single string
        for arg in args:
            print arg
        print
else:
    verboseprint = lambda *a: None

# for python 3
# verboseprint = print if verbose else lambda *a, **k: None
"""

# ----------------------------------------------------------------------------

def create_metadata(vpss_time, encr, sl, gr, pk, pol):
    meta = "TIME=" + vpss_time + "&&" + \
           "UTENTE=" + encr + "&&" + \
           "SECLEV=" + sl + "&&" + \
           "GROUPPATH=" + gr + "&&" + \
           "PKPATH=" + pk + "&&" + \
           "POLICY=" + pol
    return meta

# ----------------------------------------------------------------------------

def get_encrypted_file_metadata(filename):
    with open(filename, "rb") as f: 
        s = f.read()
    f.close()

    # extract METADATA
    metadata = s.split(FILESEPARATOR.encode())[0].decode()

    if metadata.split("&&")[0].split("=")[0] == b"TIME":
        vpss_time = metadata.split("&&")[0].split("=")[1]
        encryptor = metadata.split("&&")[1].split("=")[1]
        seclev = metadata.split("&&")[2].split("=")[1]
        group = metadata.split("&&")[3].split("=")[1].split(os.sep)[-1]
        pk = metadata.split("&&")[4].split("=")[1].split(os.sep)[-1]
        pol = metadata.split("&&")[5].split("=")[1]

        return metadata, vpss_time, encryptor, seclev, group, pk, pol
    else:
        return NODATA, NODATA, NODATA, NODATA, NODATA, NODATA, NODATA

# ----------------------------------------------------------------------------

def get_public_time():
    """
    Return the integer contained in the file time.t
    """
    timepath = os.path.join(PUBLIC_PARAMETERS_FOLDER, TIME_COUNTER )
    with open(timepath, "r") as f:
        t = int(f.read())
    f.close()

    return t

# ----------------------------------------------------------------------------

def set_new_public_time(t):
    """
    Sets the string contained in the file time.t to the integer t
    """
    timepath = os.path.join(PUBLIC_PARAMETERS_FOLDER, TIME_COUNTER )
    with open(timepath, "w") as f:
        f.write(str(t))
    f.close()

    return

# ----------------------------------------------------------------------------

def open_file(filename):
    """
    Opens a file in different platforms (Windows, iOS, Ubuntu)
    """
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        call([opener, filename])

# ----------------------------------------------------------------------------

def decrypt_file_with_metadata(ct_path, pt_folder, pk_path, gr_path, sk_path, symk_folder, symkenc_folder, overwrite):
    """
    The file ct_path contains:
    - metadata
    - encrypted ABE key
    - encrypted file
    The function decrypts a file encrypted with an AES symmetric key,
    temporarily stored in symkenc_folder (if empty same path as ct_path).
    The symmetric key is encrypted with an ABE public key, 
    and can be decrypted with an ABE secret key, which is in sk_path.
    The decrypted AES key is temporarily stored in symk_folder 
    (if empty same folder as pt_folder).
    The decrypted file is saved in pt_folder
    (if empty same as ct_path folder without .enc extention).
    If overwrite != 0 then
    if plaintext file name already exists it is overwritten
    If overwrite = 0 then
    if plaintext file name already exists a new name is used
    INPUT:
    - ct_path 
      must be the complete file path of the encrypted file, 
      ending with .enc extension
      (EX: "path/filename.enc")
    - pt_folder
    - sk_path
    - symk_folder
    - symkenc_folder
    RETURNED VALUES:
    0 if no error occurred
    WRONG_CIPHERTEXT_EXTENSION,  if file does not end with .enc extension
    ABE_DECRYPTION_FAILED,       if ABE decryption failed
    AES_DECRYPTION_FAILED,       if AES decryption failed
    UNAUTHORIZED_DECRYPTION_KEY, if user secret key does not satisfy policy
    OBSOLETE_ENCRYPTED_FILE,     if file was encrypted with old public key
    """
    # check .enc extentsion is present
    if ct_path[-4:len(ct_path)] != CT_EXT:
        print("Error! The file you are trying to decrypt" + \
              "does not end with a " + CT_EXT + " extension!")
        return WRONG_CIPHERTEXT_EXTENSION
    ct_name = ct_path.split(os.sep)[-1]

    # SET PATHS 
    pt_name = ct_path.split(os.sep)[-1][0:-4]
    # set plaintext path
    if pt_folder == "":
        # remove .enc extension and copy ct_path folder
        pt_path = ct_path[0:len(local_ct)-4]
    else:
        # add ct file name without .enc extension to pt_folder
        pt_path = os.path.join(pt_folder, pt_name)

    # set symmetric key path
    if symk_folder == "":
       # set symmetric key path to plaintext_folder/symmetric.k
       symk_path = os.path.join(pt_path.split(os.sep)[0:-1], SYMMETRIC_KEY)
    else:
       # set symmetric key path to symk_folder/symmetric.k
       symk_path = os.path.join(symk_folder, SYMMETRIC_KEY)

    # set encrypted symmetric key path
    if symkenc_folder == "":
       # set symmetric key path to ciphertext_folder/enc_symmetric.k
       symkenc_path = os.path.join(ct_path.split(os.sep)[0:-1], SYMMETRIC_ENC_KEY)
    else:
       # set symmetric key path to symkenc_folder/enc_symmetric.k
       symkenc_path = os.path.join(symkenc_folder, SYMMETRIC_ENC_KEY)


    # READ CIPHERTEXT
    # read encrypted file data and metadata
    with open(ct_path, "rb") as f: 
        s = f.read()
    f.close()

    # extract METADATA
    metadata, vpss_time, usr, seclev, gr, pk, policy = get_encrypted_file_metadata(ct_path)

    if int(vpss_time) != get_public_time():
        print "Error! The encrypted file has been encrypted " +\
              "with an obsolete public key! Decryption interrupted..."
        return OBSOLETE_ENCRYPTED_FILE

    # write file with encrypted abe key
    with open(symkenc_path, "w") as f: 
        f.write(s.split(FILESEPARATOR.encode())[1].decode())
    f.close()

    # 1 - ABE decrypt
    start = time.clock()
    print ("Decrypting file session key with ABE...")
    ret = call(["python3", "abe-decrypt.py", gr_path, pk_path,
                             sk_path, symkenc_path, symk_path
                          ])
    end = time.clock()
    print ("DONE - CLOCK TIME: " + str(end - start) + " sec")

    if ret != 0:
        print("Error! ABE decryption failed!")
        return ABE_DECRYPTION_FAILED
    else:
        with open(symk_path, "rb") as f:
            symk = f.read()
        f.close()
        
        if symk == b"USER_KEY_DOES_NOT_SATISFY_POLICY":
            print("Error! Secret key attributes " + \
                  "do not satisfy ciphertext policy!")
            # REMOVE encrypted and unencrypted abe key file
            os.remove(symk_path)         # aes symmetric key
            os.remove(symkenc_path)      # aes encrypted symmetric key
            return UNAUTHORIZED_DECRYPTION_KEY
        else:
            # check plaintext file name does not exist
            if overwrite == 0:
                local_files = os.listdir(pt_folder)
                if pt_name in local_files:
                    print( "Found a plaintext file named\n" + \
                          pt_name + \
                          "\nAdding first free progressive index >=2."
                         )
                    # if file exists, add a new index to its name
                    i = 2
                    while 1:
                        pt_name = pt_name.replace(".",str(i)+".",1)
                        i = i + 1
                        if not pt_name in local_files:
                            break
                # set plaintext path
                pt_path = os.path.join(pt_folder, pt_name)


            # write on file only its content (no metadata and no enc-abe key)
            temp = "ciphertext.temp"
            with open(temp, "wb") as f: 
                f.write(s.split(FILESEPARATOR.encode())[2])
            f.close()

            # 2 - AES decrypt
            start = time.clock()
            print ("Decrypting file " + ct_name + " with AES...")
            ret = call(["python3", "aescrypt.py", "-d", "-f", temp,
                                    pt_path, symk_path
                                  ])
            end = time.clock()
            print ("DONE - CLOCK TIME: " + str(end - start) + " sec")

            os.remove(temp)   # encrypted file
            if ret != 0:
                return AES_DECRYPTION_FAILED
            else:
                # REMOVE encrypted file and encrypted and unencrypted abe key file
                #os.remove(ct_path)   # encrypted file
                os.remove(symk_path)         # aes symmetric key
                os.remove(symkenc_path)      # aes encrypted symmetric key

                return OK

# ----------------------------------------------------------------------------

def encrypt_file_with_metadata(pt_path, ct_folder, pk_path, group_path, policy, symk_folder, symkenc_folder, metadata, overwrite):
    """
    The final ciphertext will contain:
    - metadata
    - encrypted ABE key
    - encrypted file
    joined by FILE_SEPARATOR.
    The function encrypts a file with a randomply generated AES symmetric key,
    temporarily stored in symk_folder (if empty same path as pt_path).
    The symmetric key is encrypted with an ABE public key and group, 
    which are in pk_path and group_path.
    The encrypted AES key is temporarily stored in symkenc_folder 
    (if empty same folder as ct_folder).
    The encrypted file is saved in ct_folder
    (if empty same as pt_path folder with .enc extention).
    If overwrite != 0 then
    if ciphertext file name already exists it is overwritten
    If overwrite = 0 then
    if ciphertext file name already exists a new name is used
    INPUT:
    - pt_path 
    - ct_folder
    - pk_path
    - group_path
    - symk_folder
    - symkenc_folder
    - metadata (a list of metadata)
    RETURNED VALUES:
    0 if no error occurred
    ABE_ENCRYPTION_FAILED,       if ABE encryption failed
    AES_ENCRYPTION_FAILED,       if AES encryption failed
    RANDOM_POINT_GEN_FAILED, if random point generation failed
    """
    # SET PATHS 
    pt_name = pt_path.split(os.sep)[-1]
    ct_name = pt_name + CT_EXT
    # set plaintext path
    if ct_folder == "":
        # remove .enc extension and copy ct_path folder
        ct_path = pt_path + CT_EXT
    else:
        # add ct file name without .enc extension to pt_folder
        ct_path = os.path.join(ct_folder, pt_name + CT_EXT)

    if overwrite == 0:
        # check ciphertext file name does not exist
        local_files = os.listdir(os.path.join(ct_folder))
        if ct_name in local_files:
            print( "Found a ciphertext file named\n" + \
                   ct_name + \
                   "\nAdding first free progressive index >=2."
                 )
            # if file exists, add a new index to its name
            i = 2
            while 1:
                ct_name = ct_name.replace(".",str(i)+".",1)
                i = i + 1
                if not ct_name in local_files:
                    break
        ct_path = os.path.join(ct_folder, ct_name)


    # set symmetric key path
    if symk_folder == "":
       # set symmetric key path to plaintext_folder/symmetric.k
       symk_path = os.path.join(pt_path.split(os.sep)[0:-1], SYMMETRIC_KEY)
    else:
       # set symmetric key path to symk_folder/symmetric.k
       symk_path = os.path.join(symk_folder, SYMMETRIC_KEY)

    # set encrypted symmetric key path
    if symkenc_folder == "":
       # set symmetric key path to ciphertext_folder/enc_symmetric.k
       symkenc_path = os.path.join(ct_path.split(os.sep)[0:-1], SYMMETRIC_ENC_KEY)
    else:
       # set symmetric key path to symkenc_folder/enc_symmetric.k
       symkenc_path = os.path.join(symkenc_folder, SYMMETRIC_ENC_KEY)


    # 0 - generate random symmetric key
    start = time.clock()
    print ("Generating random elliptic curve point...")
    ret = call(["python3", "abe-random-ec-point.py", 
                            group_path, symk_path
                          ])
    end = time.clock()
    print ("DONE - CLOCK TIME: " + str(end - start) + " sec")

    if ret != 0:
        print("Error! Random generation of curve point failed!")
        return RANDOM_POINT_GEN_FAILED
    else:
        # 1 - encrypt symmetric key with policy
        # python3 abe-encrypt.py '((ATTR1 or ATTR2) and (ATTR3 or ATTR4))'

        start = time.clock()
        print ("Encrypting file session key with ABE...")
        ret = call(["python3", "abe-encrypt.py", group_path, pk_path, 
              policy, symk_path, symkenc_path])
        end = time.clock()
        print ("DONE - CLOCK TIME: " + str(end - start) + " sec")

        if ret != 0:
            return ABE_ENCRYPTION_FAILED
        else:
            # 2 - encrypt file with symmetric key
            # python3 aescrypt.py -f prova.txt
            start = time.clock()
            print ("Encrypting file " + pt_name + " with AES...")

            ret = call(["python3", "aescrypt.py", "-f", 
                                    pt_path, ct_path, symk_path ])
            end = time.clock()
            print ("DONE - CLOCK TIME: " + str(end - start) + " sec")

            if ret != 0:
                return AES_ENCRYPTION_FAILED
            else:
                # 3 - add metadata to encrypted file
                s = metadata
                s = s + FILESEPARATOR

                # read encrypted abe key
                with open(symkenc_path,"r") as f:
                  s = s + f.read()
                f.close()
                
                s = s + FILESEPARATOR

                # read encrypted file
                with open(ct_path,"rb") as f:
                  temp = f.read()
                  s = bytes(s) + temp
                f.close()

                # write in one file: metadata - encrypted abe key - encrypted file
                with open(ct_path, "w") as f:
                    f.write(s)
                f.close()

                # REMOVE encrypted abe key file
                os.remove(symk_path)      # aes symmetric key file
                os.remove(symkenc_path)   # encrypted aes symmetric key file
                #os.remove(pt_path) # aes
                
                return OK
             
# ----------------------------------------------------------------------------

def get_security_level(group_path):
    with open(group_path,"r") as f:
        curve = f.read()
    f.close()

    for c in CURVES:
        if curve == c[1]:
            return c[0]

    return 0
    
# ----------------------------------------------------------------------------

def get_user_attributes_from_authdb(username):
    attr_list = []
    con = mdb.connect(AUTH_SERVER, AUTH_USER, AUTH_PASSWORD, AUTH_NAME )
    cursor = con.cursor()

    try:
        mysql_command = "SELECT DISTINCT Attr " + \
                        "FROM users LEFT JOIN attributes " + \
                        "ON users.Id=attributes.Id_user " + \
                        "WHERE users.Usr='" + username + "'"
        cursor.execute( mysql_command )
        data = cursor.fetchall()
        if cursor.rowcount == long(0) or data[0][0] == None:
            return []
        else:
            for row in data:
                attr_list.append(row[0])
    except:
        print("Error! Could not download attributes!")
    finally:    
        if con:    
            con.close()

    return attr_list

# ----------------------------------------------------------------------------

def get_users_from_authdb():
    usr_list = []
    con = mdb.connect(AUTH_SERVER, AUTH_USER, AUTH_PASSWORD, AUTH_NAME )
    cursor = con.cursor()

    try:
        mysql_command = "SELECT Usr FROM users"
        cursor.execute( mysql_command )
        data = cursor.fetchall()
        for row in data:
            usr_list.append(row[0])
    except:
        print("Error! Could not download usernames!")
    finally:    
        if con:    
            con.close()

    return usr_list

# ----------------------------------------------------------------------------

def remove_user_from_authdb(username):
    usr_list = []
    con = mdb.connect(AUTH_SERVER, AUTH_USER, AUTH_PASSWORD, AUTH_NAME )
    cursor = con.cursor()

    try:
        mysql_command = "DELETE FROM users WHERE Usr='" + username + "'"
        cursor.execute( mysql_command )
        con.commit()
        data = cursor.fetchall()
        for row in data:
            usr_list.append(row[0])
    except:
        print("Error! Could not delete user!")
        return 1
    finally:    
        if con:    
            con.close()

    return 0

# ----------------------------------------------------------------------------

def get_user_password_from_authdb(username):
    con = mdb.connect(AUTH_SERVER, AUTH_USER, AUTH_PASSWORD, AUTH_NAME )
    cursor = con.cursor()

    try:
        mysql_command = "SELECT Pwd FROM users WHERE Usr='" + username + "'"
        cursor.execute( mysql_command )
        data = cursor.fetchall()
        if cursor.rowcount == 0:
            return ""
        for row in data:
            return row[0]
    except:
        print("Error! Could not find user's password!")
        return None
    finally:    
        if con:    
            con.close()

# ----------------------------------------------------------------------------

def check_dnf_format(f):
    """
    check formula is in disjunctive normal form
    (X and Y and Z) or (Y) or (not V and W)
    TO BE REFINED...!!!!!!!!!!!!!!!!!!!!!!!!
    NOT DOESNT WORK
    """
    # check parenthesis
    par_open = 0
    for c in f:
        # check only formula is of type (...) OR (...) AND (...)
        if c == "(":
            par_open = par_open + 1
        if c == ")":
            par_open = par_open - 1
        if par_open != 0 and par_open != 1:
            print "Error! Bad formula symtax\n" + bf
            return BAD_SYNTAX
    
# ----------------------------------------------------------------------------

def get_cloud_data_by_keywords(bf, username):
    """
    bf MUST be a boolean formula in Disjunctive Normal Form.
    AND operator is evauated before OR operator.
    NOT operator DOESNT WORK YET!!!!!!!!!!!!
    EXAMPLE of bf:
      p1 & p3 | p1 & p2
      p1 | p2
      p1 & p2
      p1 & p2 | p3
    """

    if check_dnf_format(bf) == BAD_SYNTAX:
        return BAD_SYNTAX

    if bf == "":
        mysql_cmd = "SELECT * FROM cloud"
    else:
        # (kw='ciao' OR kw!='bello) OR (kw!='ciao' OR kw='brutto')
        AND = "&"
        OR = "|"
        NOT = "!"
        SEP = "-"

        kw_list = bf.replace(AND,SEP).replace(OR,SEP).replace("(",SEP).replace(")",SEP).replace(" ","").split(SEP)
        while "" in kw_list: 
            kw_list.remove("") 

        kw_set = list(set(kw_list))

        # check if user has a search key
        searchk_path = os.path.join(USER_FOLDER, username, USER_SEARCH_KEY, SEAK)
        if not os.path.exists(searchk_path):
            return NO_SEARCH_KEY_AVAILABLE

        # encrypt keywords
        with open(searchk_path,"r") as f:
            s = f.read()
        f.close()

        search_iv  = s.split(":")[0]
        search_key = s.split(":")[1]
        kwe_set = []
        bfe = bf
        for w in kw_set:
            obj = AES.new(search_key, AES.MODE_CBC, search_iv)
            padd_w = w + "," * (16 - (len(w) % 16))
            we = obj.encrypt(padd_w).encode("hex")
            kwe_set.append(we)
            bfe = bfe.replace(w, we)
            #bfe = bfe.replace(w,"Kw='" + we + "'")

        #####################################################################
        bfe_formatted = bfe.replace(" ","").replace("(","").replace(")","")
        and_atoms = bfe_formatted.split(OR)
        atom_query = []
        for a in and_atoms:
            kw_per_atom = a.split(AND)
            for i in range(len(kw_per_atom)):
                if NOT in kw_per_atom[i]:
                    kw_per_atom[i] = "Kw!='" + kw_per_atom[i] + "'"
                else:
                    kw_per_atom[i] = "Kw='" + kw_per_atom[i] + "'"
            atom_query.append("SELECT DISTINCT \
                                       cloud.Id, FileName, FilePath, \
                                       Policy, PKName, Curve, SecLev, \
                                       Encryptor, Keywords, UploadDate, Time \
                                FROM cloud LEFT JOIN keywords \
                                ON cloud.Id=keywords.Id_file \
                                WHERE ( " + " OR ".join(kw_per_atom) + " ) \
                                GROUP BY Id_file \
                                HAVING COUNT(Id_file) = " + str(len(kw_per_atom))
                             )


        mysql_cmd = " UNION ".join(atom_query)
        #####################################################################

    try:
        con = mdb.connect(SEARCH_SERVER, SEARCH_USER, 
                          SEARCH_PASSWORD, SEARCH_NAME)
        with con:
            cur = con.cursor()
            cur.execute(mysql_cmd)
            rows = cur.fetchall()
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        return SEARCH_DB_CONNECTION_FAILED
    finally:            
        if con:    
            con.close()

    return rows
"""
SELECT DISTINCT FileName, Kw
FROM cloud LEFT JOIN keywords 
ON cloud.Id=keywords.Id_file
WHERE 
kw='794ba7c430c3c345ca6cdb6c026f2589'
OR
kw='db42f7bab5d2268cf5c364f92595ff1f'
GROUP BY Id_file
HAVING COUNT(Id_file) = 2

UNION

SELECT DISTINCT FileName, Kw
FROM cloud LEFT JOIN keywords 
ON cloud.Id=keywords.Id_file
WHERE 
kw='81e9590db042408c3e7131dbdb650268'
OR
kw='db42f7bab5d2268cf5c364f92595ff1f'
GROUP BY Id_file
HAVING COUNT(Id_file) = 2
;

SELECT id
FROM t
WHERE id IN (SELECT id
	     FROM t
             WHERE w = "w1")
      AND id IN (SELECT id
	         FROM t
                 WHERE w = "w2")
      AND id IN (SELECT id
                 FROM t
                 WHERE w = "w3")

p1 
'794ba7c430c3c345ca6cdb6c026f2589'
p2 
'db42f7bab5d2268cf5c364f92595ff1f'
p3
'81e9590db042408c3e7131dbdb650268'
p4 
'a732b418f1c2dc7da57b4441d6ac9dde'
"""

# ----------------------------------------------------------------------------

