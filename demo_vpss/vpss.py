#!/usr/bin/env python

#import wx files
import wx
 
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

#import the newly created GUI file
import vpss_gui

# definitions
from vpss_def import *
from vpss_func import *

import time

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
        
class pnlAuthCPABE(vpss_gui.pnlAuthorityCPABE):
    #viewfile = "/home/ema/Dropbox/ACCADEMIC/Python/wxPython/cpabe/"

    def __init__(self, parent):
        vpss_gui.pnlAuthorityCPABE.__init__(self,parent)

        for i in range(len(CURVES)):
            self.chcSecLevAndCurve.Append("SEC LEV=" + str(CURVES[i][0]) + \
                                          " -- CURVE=" + CURVES[i][1])

        # check if first login
        # (by checking if a public key exists)
        pkpath = os.path.join(PUBLIC_PARAMETERS_FOLDER, PUBLIC_KEY)
        if not os.path.isfile(pkpath):
            self.btnGenUser.Disable()
            self.btnDeleteUser.Disable()

        # add existing users
        user_names = get_users_from_authdb()
        for u in user_names:
            self.chcChooseUserToDelete.Append(u)

        # Connect Events
        self.btnSetup.Bind( wx.EVT_BUTTON, self.OnSetup )
        self.btnGenUser.Bind( wx.EVT_BUTTON, self.OnGenUser )
        self.btnDeleteUser.Bind( wx.EVT_BUTTON, self.OnDeleteUser )

        #self.chcChooseUserToDelete.Bind(wx.EVT_LEFT_CLICK, self.OnClickUsers)
        # wanted to add click event which updates the list... 
        # ...but can't find it

    # -----------------------------------------------------------
    # function definitions
    """
    def OnClickUsers(self, event):
        print "ok"
        return
    """
    def OnDeleteUser(self, event):
        # get selected user
        usertodel = self.chcChooseUserToDelete.GetStringSelection()
        usertodel_idx = self.chcChooseUserToDelete.GetSelection()

        if usertodel == "":
            wx.MessageBox("Selezionare un utente da rimuovere.",
                              "Attenzione", 
                              wx.OK | wx.ICON_ERROR)
            return
        elif usertodel == AUTHORITY_NAME:
            wx.MessageBox("Impossibile rimuovere l'utente " + \
                          AUTHORITY_NAME + "!",
                              "Attenzione", 
                              wx.OK | wx.ICON_ERROR)
            return
        else:
            # remove user from authority database
            if remove_user_from_authdb(usertodel) != 0:
                wx.MessageBox("Impossibile rimuovere utente dal database!",
                          "Attenzione", 
                          wx.OK | wx.ICON_ERROR)    

            # remove username from choice list
            self.chcChooseUserToDelete.Delete(usertodel_idx)

            # remove user folder
            # comment or uncomment if want to remove the folder...
            usertodel_folder = os.path.join(USER_FOLDER, usertodel)
            if os.path.exists(usertodel_folder):
                shutil.rmtree(usertodel_folder)
            # remove line from USERS_FOLDER
            usernames = []
            with open(USERS_FILE, "r") as f:
                usernames = f.read().splitlines()
            f.closed

            with open(USERS_FILE, "w") as f:            
                for temp in usernames:
                    if not usertodel in temp:
                        f.write(temp + "\n")
            f.closed

        wx.MessageBox("Utente " + usertodel + " rimosso con successo!")

        return


    def OnGenUser(self, event):
        # --------------------------------------------------------------------
        # checks
        username = self.txtNewUser.GetValue()
        password = self.txtNewPassword.GetValue()
        if username == "":
            wx.MessageBox("Digitare nome utente.",
                              "Attenzione", 
                              wx.OK | wx.ICON_ERROR)
            return
        elif not username.isalnum():
            wx.MessageBox("Il nome utente deve contenere " + \
                          "caratteri alfanumerici.",
                              "Attenzione", 
                              wx.OK | wx.ICON_ERROR)
            return
        else:
            # check username does not exists in authority database
            con = mdb.connect(AUTH_SERVER, AUTH_USER, AUTH_PASSWORD, AUTH_NAME)
            cursor = con.cursor()

            try:
                cursor.execute("SELECT Usr FROM users")
                usr_data = cursor.fetchall()
                existing_user_name = []
                for row in usr_data:
                    existing_user_name.append(row[0])

            except:
                wx.MessageBox("E' avvenuto un problema durante " + \
                              "il download dei nomi degli utenti!", 
                              "Errore", 
                              wx.OK | wx.ICON_ERROR)
                return
            finally:    
                if con:    
                    con.close()
            if username in existing_user_name:
                wx.MessageBox("Il nome utente digitato e' gia' in uso.",
                                  "Attenzione", 
                                  wx.OK | wx.ICON_ERROR)
                return
            else:
                # choose attributes
                attribute_universe = ATTRIBUTES
                #self.selected_attr = []
                dlg = wx.MultiChoiceDialog( self, 
                                           "Seleziona gli attributi " + \
                                           "da associare alla chiave segreta", 
                                           "Seleziona attributi",
                                           attribute_universe)
                ret = dlg.ShowModal()
                if ( ret == wx.ID_CANCEL):
                    wx.MessageBox("Generazione utente interrotta.",
                                      "Attenzione", 
                                      wx.OK | wx.ICON_ERROR)
                    return
                if (ret == wx.ID_OK):
                    idx = dlg.GetSelections()
                    selected_attributes = ":".join([attribute_universe[i] for i in idx])
                if selected_attributes == "":
                    wx.MessageBox("Al nuovo utente non verra' assegnata " + \
                                  "ne una chiave di decifratura " + \
                                  "ne una chiave di ricerca.",
                                  "Attenzione", 
                                  wx.OK | wx.ICON_ERROR)
                else:
                    print ("Generating user with attributes:\n" + \
                           selected_attributes)

        # --------------------------------------------------------------------
        # Add user data to authority database
        con = mdb.connect(AUTH_SERVER, AUTH_USER, AUTH_PASSWORD, AUTH_NAME )
        cursor = con.cursor()

        try:
            mysql_cmd = "INSERT INTO users (Usr,Pwd) " + \
                        "VALUES ('" + username + "','" + password + "')"
            ret = cursor.execute( mysql_cmd )
            con.commit()

            if selected_attributes != "":
                user_attribute = selected_attributes.split(":")
                for i in range(len(user_attribute)):
                    mysql_cmd = "INSERT INTO attributes (Id_user, attr) \
                                 VALUES ( (SELECT Id from users \
                                           WHERE Usr='" + \
                                                 username  + "'), \
                                          '" + user_attribute[i] + "')"
                    cursor.execute( mysql_cmd )
                    con.commit()

        except:
            wx.MessageBox("E' avvenuto un problema durante " + \
                          "l'inserimento del nuovo utente!", 
                          "Errore", 
                          wx.OK | wx.ICON_ERROR)
            return
        finally:    
            if con:    
                con.close()

        # --------------------------------------------------------------------
        # Add user to USERS_FILE
        userdata = username + ":" + USERS_PWD + ":" + selected_attributes.replace(":",",")
        with open(USERS_FILE,"a") as f:
          f.write(userdata + "\n")
        f.close()

        # --------------------------------------------------------------------
        # Create user folders
        user_folder = os.path.join(USER_FOLDER, username)
        if os.path.exists(user_folder):
            shutil.rmtree(user_folder)
        os.mkdir(user_folder, 0755 )
        os.mkdir(os.path.join(user_folder, USER_CIPHERTEXT), 0755 )
        os.mkdir(os.path.join(user_folder, USER_PLAINTEXT), 0755 )
        os.mkdir(os.path.join(user_folder, USER_SECRET_KEYS), 0755 )
        os.mkdir(os.path.join(user_folder, USER_ABE_KEY), 0755 )
        os.mkdir(os.path.join(user_folder, USER_AES_KEY), 0755 )
        os.mkdir(os.path.join(user_folder, USER_SEARCH_KEY), 0755 )

        # --------------------------------------------------------------------
        # generate plaintext files
        for pt in PT:
            with open(os.path.join(USER_FOLDER,username, USER_PLAINTEXT, \
                                   pt),"w") as f:
                f.write("Questo e' un file di prova scritto dall'utente "+ \
                    username + " con nome originale " + pt)
            f.close()

        # --------------------------------------------------------------------
        # put search key in folder
        if (selected_attributes) != "":
            with open(os.path.join(user_folder, USER_SEARCH_KEY, \
                      SEAK), "w") as f:
                f.write(search_iv + ":" + search_key)
            f.close

        # --------------------------------------------------------------------
        # Create abe user key and put it to its folder
        if selected_attributes != "":
            mkpath = os.path.join(AUTH_MASTER_KEY_FOLDER, MASTER_KEY)
            grpath = os.path.join(PUBLIC_PARAMETERS_FOLDER, GROUP)
            pkpath = os.path.join(PUBLIC_PARAMETERS_FOLDER, PUBLIC_KEY)
            skpath = os.path.join(user_folder, USER_ABE_KEY, 
                                  username + SECRET_KEY)
            start = time.clock()
            print ("Generating new ABE Secret Key for user " + username + "...")
            ret  = call(["python3", "abe-keygen.py",
                         grpath, mkpath, pkpath, 
                         selected_attributes, skpath
                       ])
            end = time.clock()
            #print ("DONE - CLOCK TIME: " + str(end - start) + " sec")

            if ret != 0:
                wx.MessageBox("Errore durante la generazione" + \
                              "della chiave segreta ABE!", 
                              "Errore", wx.OK | wx.ICON_ERROR)
                return

        self.chcChooseUserToDelete.Append(username)
        print "New user " + username + " correctly generated!"
        wx.MessageBox("Nuovo utente " + username + " generato correttamente!")
        return

    def OnSetup(self, event):
        """
        1 - Create new public and master key
        2 - Re-encrypt all files in the cloud with new master key.
            Decryption is performed in AUTHORITY folder 
            (locally, not in the cloud).
        """
        if self.chcSecLevAndCurve.GetStringSelection() == "":
            wx.MessageBox("Selezionare livello di sicurezza e curva.",
                              "Attenzione", 
                              wx.OK | wx.ICON_ERROR)
            return

        # set variables
        #mkname = self.txtMK.GetValue() + KEY_EXT
        mkname = MK
        mkpath = os.path.join(AUTH_MASTER_KEY_FOLDER, mkname )
        #pkname = self.txtPK.GetValue() + KEY_EXT
        pkname = PK
        pkpath = os.path.join(PUBLIC_PARAMETERS_FOLDER, pkname )

        seclev = self.chcSecLevAndCurve.GetStringSelection()\
                          .split(" -- ")[0].split("=")[1]

        # SS512
        curve  = self.chcSecLevAndCurve.GetStringSelection()\
                          .split(" -- ")[1].split("=")[1]
        # group.g
        groupname = GROUP 
        grouppath = os.path.join(PUBLIC_PARAMETERS_FOLDER, GROUP )
        #seclev = get_security_level(grouppath)

        old_mkpath = os.path.join(AUTH_TEMP_FOLDER, "old_master" + KEY_EXT)        
        old_pkpath = os.path.join(AUTH_TEMP_FOLDER, "old_public" + KEY_EXT)
        old_grouppath = os.path.join(AUTH_TEMP_FOLDER, "old_group" + GROUP_EXT)
        old_skpath = os.path.join(AUTH_TEMP_FOLDER, "old_secret" + KEY_EXT)

        ct_folder = os.path.join(AUTH_FOLDER, USER_CIPHERTEXT)
        pt_folder = os.path.join(AUTH_FOLDER, USER_PLAINTEXT)
        sk_folder = os.path.join(AUTH_FOLDER, USER_ABE_KEY)
        symk_folder = os.path.join(AUTH_FOLDER, USER_AES_KEY)
        symkenc_folder = os.path.join(AUTH_FOLDER, USER_AES_KEY)

        skpath = os.path.join(sk_folder, "AUTHORITY_secret" + KEY_EXT)

        # send alert message
        dlg = wx.MessageDialog(None, "In seguito a questa operazione\n \
                                      saranno sovrascritte:\n \
                                      - chiave di master\n \
                                      - chiave pubblica\n \
                                      - chiavi segrete utenti\n \
                                      e inoltre verrano ricifrati\n \
                                      i file sul cloud\n \
                                      con la nuova chiave pubblica.\n \
                                      Sicuri di voler continuare?", 
                                "Domanda", 
                                wx.CANCEL | wx.YES_NO | 
                                wx.NO_DEFAULT | wx.ICON_QUESTION)
        temp = dlg.ShowModal()
        if temp == wx.ID_NO:
            wx.MessageBox("Generazione interrotta.",
                          "Attenzione", 
                          wx.OK | wx.ICON_ERROR)
            return
        if temp == wx.ID_CANCEL:
            return

        # --------------------------------------------------------------------
        # CREATE NEW PUBLIC AND MASTER KEY

        # if mk,pk,gr do not exists, then only create and distribute keys
        # (it means it is the first access)
        if not(os.path.isfile(mkpath) and 
               os.path.isfile(pkpath) and 
               os.path.isfile(grouppath)  ):

            first_setup = 1
            new_time = 1
        else:
            first_setup = 0
            # get vpss_time
            old_time = get_public_time()
            new_time = old_time + 1

            # save old public key and group
            shutil.copy(mkpath, old_mkpath )
            shutil.copy(pkpath, old_pkpath )
            shutil.copy(grouppath, old_grouppath )

            # ----------------------------------------------------------------
            # CREATE OLD AUTHORITY SECRET KEYS
            attr_list = ":".join(ATTRIBUTES)
            start = time.clock()
            print ("Generating temporary Authority Decryption Key...")
            ret  = call(["python3", "abe-keygen.py",
                         old_grouppath, old_mkpath, old_pkpath, 
                         attr_list, old_skpath
                       ])
            if ret != 0:
                wx.MessageBox("Errore durante la generazione" + \
                              "della chiave segreta ABE!", 
                              "Errore", wx.OK | wx.ICON_ERROR)
            end = time.clock()
            #print ("DONE - CLOCK TIME: " + str(end - start) + " sec")

        # abe-setup, overwrites pkpath and mkpath
        start = time.clock()
        print ("Generating Master and Public Key...")
        ret = call(["python3", "abe-setup.py",
                    curve, 
                    PUBLIC_PARAMETERS_FOLDER, pkpath, mkpath
            ])
        end = time.clock()
        #print ("DONE - CLOCK TIME: " + str(end - start) + " sec")

        if ret != 0:
            wx.MessageBox("Errore durante il setup ABE!", 
                          "Errore", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox("- chiave master\n\n" + \
                          mkpath + "\n\n" + \
                          "- chiave pubblica\n\n" + \
                          pkpath + "\n\n" + \
                          "generate correttamente\n\n" + \
                          "utilizzando:\n\n" + \
                          "- curva\n\n" + \
                          curve + "\n\n"
                         )

        if not first_setup:
            # ----------------------------------------------------------------
            # CREATE NEW AUTHORITY SECRET KEY
            """
            start = time.clock()
            print ("Generating new Authority Secret Key...")
            attr_list = ":".join(ATTRIBUTES)
            ret  = call(["python3", "abe-keygen.py",
                         grouppath, mkpath, pkpath, 
                         attr_list, skpath
                       ])
            if ret != 0:
                wx.MessageBox("Errore durante la generazione" + \
                              "della chiave segreta ABE!", 
                              "Errore", wx.OK | wx.ICON_ERROR)
            end = time.clock()
            print ("DONE - CLOCK TIME: " + str(end - start) + " sec")
            """

            # ----------------------------------------------------------------
            # RE-ENCRYPT CLOUD FILES

            # remove files from authority's ciphertext folder
            #ct_folder = os.path.join(USER_FOLDER, AUTHORITY_NAME, USER_CIPHERTEXT, "temp")
            if os.path.exists(ct_folder):
                shutil.rmtree(ct_folder)
            os.mkdir( ct_folder, 0755 )

            #################################################
            # I - update search db
            try:
                # login
                con = mdb.connect(SEARCH_SERVER, SEARCH_USER, 
                                  SEARCH_PASSWORD, SEARCH_NAME)
                with con:
                    cur = con.cursor()
                    
                    mysql_cmd = ("UPDATE cloud SET " + \
                                  "PKName='" + pkname + "'," + \
                                  "Curve='" + groupname + "'," + \
                                  "SecLev='" + seclev + "'," + \
                                  "Encryptor='" + AUTHORITY_NAME + "'," + \
                                  "UploadDate=NOW()," + \
                                  "Time='" + str(new_time) + "'")
                                  #"WHERE Usr=''")
                    cur.execute( mysql_cmd )
            except mdb.Error, e:
                print "Error %d: %s" % (e.args[0],e.args[1])
                sys.exit(1)
            finally:    
                if con:    
                    con.close()

            #################################################
            # II - update cloud server
            # login
            ftp = FTP(CLOUD_SERVER)
            ftp.login(user=CLOUD_USERNAME, passwd = CLOUD_PASSWORD)

            filenames = ftp.nlst() # get filenames within the directory
            print filenames

            for filename in filenames:
                #################################################
                # 1 - download file
                local_ctpath = os.path.join(ct_folder, filename)
                file = open(local_ctpath, "wb")
                ftp.retrbinary("RETR "+ filename, file.write)
                file.close()

                #################################################
                # 2 - decrypt file
                ret = decrypt_file_with_metadata(local_ctpath, 
                                                 pt_folder, 
                                                 old_pkpath, 
                                                 old_grouppath, 
                                                 old_skpath,
                                                 symk_folder, 
                                                 symkenc_folder, 1
                                                )
                if ret == ABE_DECRYPTION_FAILED:
                    wx.MessageBox("Errore durante la decifratura ABE!", 
                                  "Errore", wx.OK | wx.ICON_ERROR)
                    return
                elif ret == AES_DECRYPTION_FAILED:
                    wx.MessageBox("Errore durante la decifratura AES!", 
                                  "Errore", wx.OK | wx.ICON_ERROR)
                    return
                elif ret == UNAUTHORIZED_DECRYPTION_KEY:
                    wx.MessageBox("Gli attributi associati " + \
                                  "alla chiave segreta selezionata " + \
                                  "non soddisfano la policy.", 
                                  "Errore", wx.OK | wx.ICON_ERROR
                                 )
                    return
                elif ret == OBSOLETE_ENCRYPTED_FILE:
                    wx.MessageBox("Impossibile eseguire la decifratura, " + \
                                  " file decifrato " + \
                                  "con chiave pubblica obsoleta.", 
                                  "Errore", wx.OK | wx.ICON_ERROR
                                 )
                    return
                elif ret == OK:
                    print("Succesful decryption of file:\n  " + local_ctpath)
                else:
                    print("Unexpected error during decryption...")
                    return

                # get policy from metadata
                meta, vpss_time, encr, sl, gr, pk, policy = get_encrypted_file_metadata(local_ctpath)

                metadata = create_metadata(str(new_time), AUTHORITY_NAME, 
                                           seclev, grouppath, pkpath, policy)

                #################################################
                # 3 - re-encrypt file 
                #     (overwrites previous ciphertext, local_ctpath)
                local_ptpath = os.path.join(pt_folder, filename.replace(CT_EXT,""))

                start = time.clock()
                print ("Re-encrypting file " + filename + "...")
                ret = encrypt_file_with_metadata(local_ptpath, 
                                                 ct_folder, 
                                                 pkpath, 
                                                 grouppath, 
                                                 policy, 
                                                 symk_folder, 
                                                 symkenc_folder, 
                                                 metadata, 1
                                                )
                end = time.clock()
                print ("DONE - CLOCK TIME: " + str(end - start) + " sec")

                if ret == RANDOM_POINT_GEN_FAILED:
                    wx.MessageBox("Errore durante la generazione " +
                                  "di un punto della curva!", 
                                  "Errore", wx.OK | wx.ICON_ERROR)
                    #some action???
                    return
                elif ret == ABE_ENCRYPTION_FAILED:
                    wx.MessageBox("Errore durante la cifratura ABE!", 
                          "Errore", wx.OK | wx.ICON_ERROR)
                    #some action???
                    return
                elif ret == AES_ENCRYPTION_FAILED:
                    wx.MessageBox("Errore durante la cifratura AES!", 
                                  "Errore", wx.OK | wx.ICON_ERROR)
                    #some action???
                    return
                elif ret == OK:
                    print("Succesful encryption of file:\n  " + local_ptpath)
                else:
                    print("Unexpected error during encryption...")
                    return
 
                #################################################
                # 4 - upload file

                # upload (overwrites previous file)
                filetouploadname = local_ctpath.split(os.sep)[-1]
                filein = local_ctpath
                fileout = filetouploadname
                ftp.storbinary("STOR " + fileout, open(filein, "rb"))

                #################################################
                #################################################

            ftp.quit() # close the connection
            # ----------------------------------------------------------------
            # END RE-ENCRYPT CLOUD FILES

      
        #################################################
        # --------------------------------------------------------------------
        # CREATE AND DISTRIBUTE USERS SECRET KEYS
        # get usernames and attributes from authority database
        con = mdb.connect(AUTH_SERVER, AUTH_USER, AUTH_PASSWORD, AUTH_NAME )
        cursor = con.cursor()

        try:
            cursor.execute("SELECT Id, Usr FROM users")
            #cursor.execute("SELECT Id, Usr FROM users where Usr!='" + AUTHORITY_NAME + "'")
            usr_data = cursor.fetchall()
            for row in usr_data:
                user_id = row[0]
                user_name = row[1]
                cursor.execute("SELECT Attr FROM attributes " + \
                                "where Id_user='" + str(user_id) + "'")

                attr_data = cursor.fetchall()
                user_attr = []
                for a in attr_data:
                    user_attr.append(a[0])
                skpath = os.path.join(USER_FOLDER, user_name, USER_ABE_KEY, 
                                      user_name + SECRET_KEY)
                attr_list = ":".join([user_attr[i] for i in range(len(user_attr))])

                start = time.clock()
                print ("Generating new ABE Secret Key for user " + user_name + "...")
                ret  = call(["python3", "abe-keygen.py",
                             grouppath, mkpath, pkpath, 
                             attr_list, skpath
                           ])
                end = time.clock()
                #print ("DONE - CLOCK TIME: " + str(end - start) + " sec")

                if ret != 0:
                    wx.MessageBox("Errore durante la generazione" + \
                                  "della chiave segreta ABE!", 
                                  "Errore", wx.OK | wx.ICON_ERROR)

        except:
            wx.MessageBox("E' avvenuto un problema durante la generazione" + \
                          "delle chiavi segrete.\n" + \
                          "Chiavi segrete non generate!", 
                          "Errore", 
                          wx.OK | wx.ICON_ERROR)
            return
        finally:    
            if con:    
                con.close()

        # udate vpss_time
        set_new_public_time(new_time)

        self.btnGenUser.Enable()
        self.btnDeleteUser.Enable()
        wx.MessageBox("Chiavi generate e distribuite correttamente")

# ----------------------------------------------------------------------------
# ------------------------ USER PANEL ----------------------------------------
# ----------------------------------------------------------------------------

class pnlUsrCPABE(vpss_gui.pnlClientCPABE):
    #viewfile = "/home/ema/Dropbox/ACCADEMIC/Python/wxPython/cpabe/"
    def __init__(self, parent):
        vpss_gui.pnlClientCPABE.__init__(self,parent)

        # variables definitions ----------------------------------------------
        # read attributes and policies from file POLICIES_FILE
        allpolicies = []
        with open(POLICIES_FILE, "r") as fpol:
            #allpolicies = fpol.readlines()
            allpolicies = fpol.read().splitlines()
        fpol.closed

        for temp in allpolicies:
            self.chcShowPolicies.Append(temp)

        # prepare tables
        self.lstEncFilesData.ClearAll()
        self.lstEncFilesData.InsertColumn(0,"File") 
        self.lstEncFilesData.InsertColumn(1,"Autorizzazione") 
        self.lstEncFilesData.InsertColumn(2,"Policy")
        self.lstEncFilesData.InsertColumn(3,"Cifrato da")
        self.lstEncFilesData.InsertColumn(4,"Chiave Pubblica")
        self.lstEncFilesData.InsertColumn(5,"Livello sicurezza")
        self.lstEncFilesData.InsertColumn(6,"Gruppo")
        self.lstEncFilesData.InsertColumn(7,"Tempo")

        self.lstCloudEncFilesData.ClearAll()
        self.lstCloudEncFilesData.InsertColumn(0,"File") 
        self.lstCloudEncFilesData.InsertColumn(1,"Autorizzazione") 
        self.lstCloudEncFilesData.InsertColumn(2,"Policy")
        self.lstCloudEncFilesData.InsertColumn(3,"Cifrato da")
        self.lstCloudEncFilesData.InsertColumn(4,"Chiave Pubblica")
        self.lstCloudEncFilesData.InsertColumn(5,"Gruppo")
        self.lstCloudEncFilesData.InsertColumn(6,"Livello sicurezza")
        self.lstCloudEncFilesData.InsertColumn(7,"Parole chiave")
        self.lstCloudEncFilesData.InsertColumn(8,"Data")
        self.lstCloudEncFilesData.InsertColumn(9,"Tempo")

        # SETTING VARIABLES
        self.seclev = "" # security level
        self.grouppath = "" # group name and path
        self.pkpath = "" # public key name and path

        self.skpath = "" # secret key name and path

        self.username = ""
        self.userfolder = "" # ciphertext folder

        # ENCRYPT VARIABLES
        self.plaintextpath = "" # file name and path
        self.plaintextname = "" # only file name
        self.ciphertextpath = "" # file name and path
        self.ciphertextname = "" # only file name
        self.policy = "" # policy
        self.encsymkpath = "" # encrypted symmetric key name and path
        self.symkpath = "" # symmetric key name and path

        # DECRYPT VARIABLES
        self.plaintextpath2 = "" # file name and path
        self.plaintextname2 = "" # only file name
        self.ciphertextpath2 = "" # file name and path
        self.ciphertextname2 = "" # only file name
        self.encsymkpath2 = "" # encrypted symmetric key name and path
        self.symkpath2 = "" # symmetric key name and path

        # UPLOAD/DOWNLOAD VARIABLES
        self.filetouploadpath = ""
        self.filetouploadname = ""

        # Connect Events -----------------------------------------------------

        # SETTING EVENTS
        #self.chcSecLev.Bind( wx.EVT_CHOICE, self.OnChooseSecLev )
        #self.btnChoosePK.Bind( wx.EVT_BUTTON, self.OnChoosePK )
        #self.btnChooseGroup.Bind( wx.EVT_BUTTON, self.OnChooseGroup )
        #self.btnChooseSK.Bind( wx.EVT_BUTTON, self.OnChooseSK )

        # ENCRYPT EVENTS
        self.btnChooseFileToEncrypt.Bind( wx.EVT_BUTTON, 
                                          self.OnChooseFileToEncrypt )
        self.btnCreatePolicy.Bind( wx.EVT_BUTTON, self.OnCreatePolicy )
        self.chcShowPolicies.Bind( wx.EVT_CHOICE, self.OnSelectPolicy )
        self.btnEncrypt.Bind( wx.EVT_BUTTON, self.OnEncrypt )

        # DECRYPT EVENTS
        self.btnChooseFileToDecrypt.Bind( wx.EVT_BUTTON, 
                                          self.OnChooseFileToDecrypt )
        self.btnDecrypt.Bind( wx.EVT_BUTTON, self.OnDecrypt )

        # OTHER EVENTS
        self.btnUpdateFileTable.Bind( wx.EVT_BUTTON, self.OnUpdateFileTable )
        self.btnUpdate.Bind( wx.EVT_BUTTON, self.OnUpdate )
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)

        # OPEN LOCAL FILES EVENTS
        self.lstFile.Bind( wx.EVT_LEFT_DCLICK, self.OnDoubleClickFile )
        self.lstEncFile.Bind( wx.EVT_LEFT_DCLICK, self.OnDoubleClickEncFile )
        self.lstSK.Bind( wx.EVT_LEFT_DCLICK, self.OnDoubleClickSK )
        self.lstPP.Bind( wx.EVT_LEFT_DCLICK, self.OnDoubleClickPP )

        # UPLOAD/DOWNLOAD EVENTS
        self.btnChooseFileToUpload.Bind( wx.EVT_BUTTON, 
                                         self.OnChooseFileToUpload )
        self.btnUpdateCloudFileTable.Bind( wx.EVT_BUTTON,
                                           self.OnUpdateCloudFileTable )
        self.btnUpload.Bind( wx.EVT_BUTTON, self.OnUpload )
        self.btnDownload.Bind( wx.EVT_BUTTON, self.OnDownload )


    # methods definitions ----------------------------------------------------

    def OnPageChanged(self, event):
        page_number =  event.GetSelection()
        if page_number == 0:
            return  
        elif page_number == 1: # update local ciphertexts table
            self.OnUpdateFileTable(event)
            return
        elif page_number == 2: # update cloud ciphertexts table
            self.OnUpdateCloudFileTable(event)
            return
        elif page_number == 3: # update local folders content
            self.OnUpdate(event)
            return
        else:
            return
        return


    ################ BEGIN OPEN LOCAL FILES METHODS ##########################

    def OnDoubleClickFile(self, parent):
         global CONNECTED_USER
         filepath = os.path.join(USER_FOLDER, CONNECTED_USER, USER_PLAINTEXT, \
                    self.lstFile.GetStringSelection())
         print "trying to open file: " + filepath
         open_file(filepath)

    def OnDoubleClickEncFile(self, parent):
         global CONNECTED_USER
         filepath = os.path.join(USER_FOLDER, CONNECTED_USER, USER_CIPHERTEXT, \
                    self.lstEncFile.GetStringSelection())
         print "trying to open file: " + filepath
         open_file(filepath)

    def OnDoubleClickSK(self, parent):
         global CONNECTED_USER
         filepath = os.path.join(USER_FOLDER, CONNECTED_USER, USER_ABE_KEY, \
                    self.lstSK.GetStringSelection())
         print "trying to open file: " + filepath
         open_file(filepath)

    def OnDoubleClickPP(self, parent):
         filepath = os.path.join(PUBLIC_PARAMETERS_FOLDER, \
                    self.lstPP.GetStringSelection())
         print "trying to open file: " + filepath
         open_file(filepath)

    ################ END OPEN LOCAL FILES METHODS ############################
    """
    ################ BEGIN SETTING METHODS ###################################

    def OnChooseSecLev(self, event):
        s = self.chcSecLev.GetStringSelection()
        if s == u"selezionare":
            self.seclev = ""
            self.groupname = ""
        else:
            s = s.split(":")
            self.seclev = s[0]
            #self.groupname = s[1] + GROUP_EXT
            self.groupname = GROUP
            self.grouppath = os.path.join(PUBLIC_PARAMETERS_FOLDER, \
                             self.groupname )

    def OnChoosePK(self, event):
        dlg = wx.FileDialog(self, "Scegli una chiave pubblica", 
                            PUBLIC_PARAMETERS_FOLDER, "", "*" + KEY_EXT, wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.pkpath = dlg.GetPath()
            self.lblPKName.SetLabel(self.pkpath)
        dlg.Destroy()

    def OnChooseGroup(self, event):
        dlg = wx.FileDialog(self, "Scegli una gruppo", 
                            PUBLIC_PARAMETERS_FOLDER, "", "*.g", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.grouppath = dlg.GetPath()
            self.lblGroupName.SetLabel(self.grouppath)
        dlg.Destroy()

    def OnChooseSK(self, event):
        dlg = wx.FileDialog(self, "Scegli una chiave segreta", 
                            os.path.join(self.userfolder, USER_ABE_KEY), 
                            "", "*" + KEY_EXT, wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.skpath = dlg.GetPath()
            self.lblSKName.SetLabel(self.skpath)
        dlg.Destroy()

    ################ END SETTING METHODS #####################################
    """

    ################ BEGIN ENCRYPT METHODS ###################################

    def OnChooseFileToEncrypt(self, event):
        dlg = wx.FileDialog(self, "Scegli un file",  
                            os.path.join(self.userfolder, USER_PLAINTEXT), 
                            "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.plaintextpath = dlg.GetPath()
            self.plaintextname = dlg.GetFilename()
            self.lblFileToEncryptName.SetLabel(self.plaintextpath)
        dlg.Destroy()

    def OnCreatePolicy(self, event):
        dlg = DialogCreatePolicy(self)
        dlg.ShowModal()

        # update policies list
        allpolicies = []
        with open(POLICIES_FILE, "r") as fpol:
            allpolicies = fpol.read().splitlines()
        fpol.closed
        self.chcShowPolicies.Clear()
        self.chcShowPolicies.Append(u"Seleziona esistente")
        for temp in allpolicies:
            self.chcShowPolicies.Append(temp)

        dlg.Destroy()

    def OnSelectPolicy(self, event):
        if self.chcShowPolicies.GetStringSelection() == u"Seleziona esistente":
            self.lblShowPolicy.SetLabel(u"Nessuna policy creata")
        else: 
            self.lblShowPolicy.SetLabel(self.chcShowPolicies.GetStringSelection())

    def OnEncrypt(self, event):

        readytoenc = 1
        # INPUT checks

        self.groupname = GROUP
        self.grouppath = os.path.join(PUBLIC_PARAMETERS_FOLDER, \
                             self.groupname )
        print("Gruppo di default selezionato:\n" + \
               self.grouppath)

        self.seclev = str(get_security_level(self.grouppath))
        print("Livello sicurezza di default selezionata:\n" + \
              self.seclev)

        self.pkpath = os.path.join(PUBLIC_PARAMETERS_FOLDER, PUBLIC_KEY)
        print("Chiave pubblica di default selezionata:\n" + \
              self.pkpath)

        # check group and public key are ok with each other ???
        # ...

        if self.plaintextpath == "":
            readytoenc = 0
            wx.MessageBox("Nessun file da cifrare selezionato.", "Errore", 
                          wx.OK | wx.ICON_ERROR)
            return

        self.policy = self.lblShowPolicy.GetLabel()
        # check policy
        # ...
        if self.policy == u"Nessuna policy creata":
            readytoenc = 0
            wx.MessageBox("Nessuna policy inserita.", "Errore", 
                          wx.OK | wx.ICON_ERROR)
            return

        # ENCRYPT
        if readytoenc == 1:
            self.userfolder = os.path.join(USER_FOLDER, CONNECTED_USER)
            ct_folder = os.path.join(self.userfolder, USER_CIPHERTEXT)

            symk_folder = os.path.join(self.userfolder, \
                            USER_AES_KEY) # symmetric key name and path 

            symkenc_folder = os.path.join(self.userfolder, \
                               USER_CIPHERTEXT )

            # 3 - add metadata to encrypted file
            vpss_time = get_public_time()
            metadata = create_metadata(str(vpss_time), self.username, 
                                       self.seclev, self.grouppath, 
                                       self.pkpath, self.policy )

            ret = encrypt_file_with_metadata(self.plaintextpath, 
                                             ct_folder, 
                                             self.pkpath, 
                                             self.grouppath, 
                                             self.policy, 
                                             symk_folder, 
                                             symkenc_folder, 
                                             metadata, 0
                                            )
            if ret == RANDOM_POINT_GEN_FAILED:
                wx.MessageBox("Errore durante la generazione " +
                              "di un punto della curva!", 
                              "Errore", wx.OK | wx.ICON_ERROR)
                #some action???
                return
            elif ret == ABE_ENCRYPTION_FAILED:
                wx.MessageBox("Errore durante la cifratura ABE!", 
                      "Errore", wx.OK | wx.ICON_ERROR)
                #some action???
                return
            elif ret == AES_ENCRYPTION_FAILED:
                wx.MessageBox("Errore durante la cifratura AES!", 
                              "Errore", wx.OK | wx.ICON_ERROR)
                #some action???
                return
            elif ret == OK:
                print("Succesful encryption of file:\n  " + self.plaintextpath)
                wx.MessageBox("Cifratura eseguita correttamente.\n\n" + 
                              "File:\n\n" + self.plaintextpath + "\n\n" +
                              "Livello di sicurezza:\n\n" +  self.seclev + "\n\n" 
                              "Gruppo:\n\n" +  self.groupname + "\n\n" 
                              "Chiave pubblica:\n\n" + self.pkpath + "\n\n" + 
                              "Policy:\n\n" + self.policy + "\n\n"
                             )
            else:
                print("Unexpected error during encryption...")
                return

            self.plaintextpath = ""
            self.plaintextname = ""
            self.ciphertextpath = ""
            self.ciphertextname = ""
            self.lblFileToEncryptName.SetLabel(u"Nessuna selezione effettuata...")

    ################ END ENCRYPT METHODS #####################################

    ################ BEGIN DECRYPT METHODS ###################################

    def OnChooseFileToDecrypt(self, event):
        dlg = wx.FileDialog(self, "Scegli un file",  
                            os.path.join(self.userfolder, USER_CIPHERTEXT), 
                            "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.ciphertextpath2 = dlg.GetPath()
            self.ciphertextname2 = dlg.GetFilename() 


            self.lblFileToDecryptName.SetLabel(self.ciphertextpath2)

        dlg.Destroy()

    def OnDecrypt(self, event):
        readytodec = 1
        # INPUT checks?

        if self.ciphertextpath2 == "":
            wx.MessageBox("Nessun file da decifrare selezionato.", 
                          "Errore", wx.OK | wx.ICON_ERROR)
            readytodec = 0
            return

        # DECRYPT
        if readytodec == 1:
            self.userfolder = os.path.join(USER_FOLDER, CONNECTED_USER) 

            pt_folder = os.path.join(self.userfolder, USER_PLAINTEXT)

            self.pkpath = os.path.join(PUBLIC_PARAMETERS_FOLDER, 
                                       PUBLIC_KEY)    
            self.grouppath = os.path.join(PUBLIC_PARAMETERS_FOLDER, 
                                          GROUP)
            self.skpath = os.path.join(self.userfolder, 
                                       USER_ABE_KEY, 
                                       CONNECTED_USER + SECRET_KEY)
            symk_folder = os.path.join(self.userfolder, \
                            USER_AES_KEY ) # symmetric key name and path 

            symkenc_folder = os.path.join(self.userfolder, \
                               USER_CIPHERTEXT, )

            # 2 - decrypt file
            ret = decrypt_file_with_metadata(self.ciphertextpath2, 
                                             pt_folder, 
                                             self.pkpath, 
                                             self.grouppath, 
                                             self.skpath,
                                             symk_folder, 
                                             symkenc_folder, 0
                                            )
            if ret == ABE_DECRYPTION_FAILED:
                wx.MessageBox("Errore durante la decifratura ABE!", 
                              "Errore", wx.OK | wx.ICON_ERROR)
                return
            elif ret == AES_DECRYPTION_FAILED:
                wx.MessageBox("Errore durante la decifratura AES!", 
                              "Errore", wx.OK | wx.ICON_ERROR)
                return
            elif ret == UNAUTHORIZED_DECRYPTION_KEY:
                wx.MessageBox("Gli attributi associati " + \
                              "alla chiave segreta selezionata " + \
                              "non soddisfano la policy.", 
                              "Errore", wx.OK | wx.ICON_ERROR
                             )
                return
            elif ret == OBSOLETE_ENCRYPTED_FILE:
                wx.MessageBox("Impossibile eseguire la decifratura, " + \
                              " file decifrato " + \
                              "con chiave pubblica obsoleta.", 
                              "Errore", wx.OK | wx.ICON_ERROR
                             )
                return
            elif ret == OK:
                print("Succesful decryption of file:\n  " + self.ciphertextpath2)
                wx.MessageBox("Decifratura eseguita correttamente.\n\n" + 
                              "File:\n\n" + self.ciphertextpath2
                             )
            else:
                print("Unexpected error during decryption...")
                return

            self.plaintextpath2 = ""
            self.plaintextname2 = ""
            self.ciphertextpath2 = ""
            self.ciphertextname2 = ""
            self.lblFileToDecryptName.SetLabel(u"Nessuna selezione effettuata...")

    ################ END DECRYPT METHODS #####################################

    # ------------------------------------------------------------------------

    def OnUpdateFileTable(self, event):

        self.lstEncFilesData.DeleteAllItems()
        index = 1
        for fname in os.listdir(os.path.join(USER_FOLDER, \
                                self.lblUserName.GetLabel(), \
                                USER_CIPHERTEXT)):

            # read encrypted file data and metadata
            filename = os.path.join(USER_FOLDER, \
                                self.lblUserName.GetLabel(), \
                                USER_CIPHERTEXT, fname.encode())

            meta, vpss_time, encr, sl, gr, pk, pol = get_encrypted_file_metadata(filename)

            if meta == NODATA:
                print("Il file \n" + filename + "\nnon contiene metadata!")
            else:
                index = self.lstEncFilesData.InsertStringItem(index, fname)

                self.lstEncFilesData.SetStringItem(index, 2, pol)
                self.lstEncFilesData.SetStringItem(index, 3, encr)
                self.lstEncFilesData.SetStringItem(index, 4, pk)
                self.lstEncFilesData.SetStringItem(index, 5, sl)
                self.lstEncFilesData.SetStringItem(index, 6, gr)
                self.lstEncFilesData.SetStringItem(index, 7, vpss_time)

                if int(vpss_time) < get_public_time():
                    self.lstEncFilesData.SetItemTextColour(index, 
                                                     wx.NamedColour("orange"))
                    self.lstEncFilesData.SetStringItem(index, 1, "Obsoleto")
                else:
                    # get user attributes
                    temp = self.lstAttributes.GetStrings()
                    usr_attr = []
                    for a in temp:
                        usr_attr.append(a.encode())

                    # get attributes in the policy
                    pol_attr = list(set(
                                 re.compile("\w+").findall(
                                   pol.replace("or","").replace("and","").replace("not","")
                                 )
                               ))

                    # transform policy in Boolean formula
                    for a in pol_attr:
                        if a in usr_attr:
                            pol = pol.replace(a,"1")
                        else:
                            pol = pol.replace(a,"0")

                    if bool(eval(pol)):
                        self.lstEncFilesData.SetStringItem(index, 1, 
                                                           "Autorizzato")
                    else:
                        self.lstEncFilesData.SetItemTextColour(index, wx.RED)
                        self.lstEncFilesData.SetStringItem(index, 1, 
                                                           "NON Autorizzato")
                index = index + 1

    # ------------------------------------------------------------------------

    def OnUpdate(self, event):
        self.lstPP.Clear()
        for fname in os.listdir(PUBLIC_PARAMETERS_FOLDER):
            #if fname.endswith(GROUP_EXT):
                self.lstPP.Append(fname)

        self.lstSK.Clear()
        for fname in os.listdir(os.path.join(USER_FOLDER, \
                                self.lblUserName.GetLabel(), \
                                USER_ABE_KEY)):
            if fname.endswith(KEY_EXT):
                self.lstSK.Append(fname)

        self.lstFile.Clear()
        for fname in os.listdir(os.path.join(USER_FOLDER, \
                                self.lblUserName.GetLabel(), \
                                USER_PLAINTEXT)):
            #if fname.endswith(KEY_EXT):
            self.lstFile.Append(fname)

        self.lstEncFile.Clear()
        for fname in os.listdir(os.path.join(USER_FOLDER, \
                                self.lblUserName.GetLabel(), \
                                USER_CIPHERTEXT)):
            #if fname.endswith(KEY_EXT):
            self.lstEncFile.Append(fname)


    ################ BEGIN UPLOAD/DOWNLOAD METHODS ###########################

    def OnChooseFileToUpload(self, parent):
        dlg = wx.FileDialog(self, "Scegli un file",  
                            os.path.join(self.userfolder, USER_CIPHERTEXT), 
                            "", "*" + CT_EXT, wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filetouploadpath = dlg.GetPath()
            self.filetouploadname = dlg.GetFilename()
            self.lblFileToUploadName.SetLabel(self.filetouploadpath)
        dlg.Destroy()

    def OnUpload(self, parent):
        global CONNECTED_USER

        #####################################################################
        # IMPORTANT NOTE:                                                   #
        # ---------------                                                   #
        # FIRST ENCRYPTED FILE IS UPLOADED TO FTP SERVER                    # 
        # SECOND METADATA ARE UPLOADED TO DB SERVER                         #
        # NO CHECK IS DONE IF ONE OF THE TWO DOES NOT SUCCEED               #
        # THIS MAY BRING TO SOME INCONGRUENCE                               #
        #####################################################################

        self.filetouploadpath = self.lblFileToUploadName.GetLabel()
        self.filetouploadname = self.filetouploadpath.split(os.sep)[-1]

        if self.filetouploadpath == "" or \
           self.filetouploadpath == u"Nessuna selezione effettuata...":
            wx.MessageBox("Selezionare un file da caricare.",
                          "Errore", wx.OK | wx.ICON_ERROR
                         )
            return

        meta, file_time, encr, sl, gr, pk, pol = get_encrypted_file_metadata(self.filetouploadpath)

        # check vpss_time (to see if the file is obsolete)
        file_time = int(file_time)
        current_time = get_public_time()
        if current_time > file_time:
            wx.MessageBox("Il file che si sta cercando di caricare " + \
                          "risulta cifrato con una chiave pubblica " + \
                          "non aggiornata, " + \
                          "quindi l'upload non verra' eseguito!",
                          "Errore", wx.OK | wx.ICON_ERROR
                         )
            return

        # get and check keywords        
        keywords = self.txtKeywords.GetValue().replace(" ","")
        # remove empty keywords
        keywords = keywords.split(",")
        while "" in keywords: keywords.remove("") 
        #keywords = ",".join(l)
        for w in keywords:
            if not w.isalnum():
                wx.MessageBox("Una delle parole chiave inserite " + \
                              "contiene caratteri NON alfanumerici.\n" + \
                              "Upload interrotto.",
                              "Errore", wx.OK | wx.ICON_ERROR
                             )
                return
        print keywords

        # encrypt keywords
        with open(os.path.join(USER_FOLDER, CONNECTED_USER, \
                  USER_SEARCH_KEY, SEAK),"r") as f:
            s = f.read()
        f.close()
        search_iv  = s.split(":")[0]
        search_key = s.split(":")[1]
        enc_keywords = []
        for w in keywords:
            obj = AES.new(search_key, AES.MODE_CBC, search_iv)
            padd_w = w + "," * (16 - (len(w) % 16))
            enc_keywords.append(obj.encrypt(padd_w).encode("hex"))
        print enc_keywords

        # UPDATE FTP SERVER (CLOUD)
        # -------------------------

        # login
        ftp = FTP(CLOUD_SERVER)
        ftp.login(user=CLOUD_USERNAME, passwd = CLOUD_PASSWORD)

        # check if file exists
        files = ftp.nlst()
        if self.filetouploadname in files:
            wx.MessageBox("Trovato un file con lo stesso nome, " + \
                          "aggiungo al nome del file " + \
                          "il primo indice progressivo non esistente " + \
                          "maggiore o uguale a 2 ."
                         )
            # if file exists, ad a new index to its name
            i = 2
            while 1:
                temp = self.filetouploadname.replace(".",str(i)+".",1)
                i = i + 1
                if not temp in files:
                    break
            self.filetouploadname = temp

        filein = self.filetouploadpath
        fileout = self.filetouploadname

        # upload        
        ftp.storbinary("STOR " + fileout, open(filein, "rb"))

        # close connection
        ftp.quit() 

        # UPDATE MYSQL DATABASE
        # ---------------------

        try:
            con = mdb.connect(SEARCH_SERVER, SEARCH_USER, 
                              SEARCH_PASSWORD, SEARCH_NAME)
            with con:
                cur = con.cursor()

                # insert entries to the table
                mysql_command = "INSERT INTO cloud( \
                               FileName, \
                               FilePath, \
                               Policy, \
                               PKName, \
                               Curve, \
                               SecLev, \
                               Encryptor, \
                               Keywords, \
                               UploadDate, \
                               Time \
                              ) VALUES ( \
                               '" + self.filetouploadname + "', \
                               '" + os.path.join(CLOUD_FOLDER,
                                                self.filetouploadname) + "', \
                               '" + pol + "', \
                               '" + pk + "', \
                               '" + gr + "', \
                               '" + sl + "', \
                               '" + encr + "', \
                               '" + ",".join(enc_keywords) + "', \
                               NOW(), \
                               '" + str(file_time) + "' \
                              )"
                cur.execute( mysql_command )
                con.commit()
                for w in enc_keywords:
                    mysql_command = "INSERT INTO keywords (kw, Id_file) \
                                     VALUES ( '" + w + "', \
                                              (SELECT id from cloud \
                                               WHERE FileName='" + \
                                                     self.filetouploadname + "'))"
                    cur.execute( mysql_command )
                    con.commit()

        except mdb.Error, e:
          
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
            
        finally:    
                
            if con:    
                con.close()

        self.filetouploadpath = ""
        self.filetouploadname = ""

        self.OnUpdateCloudFileTable(parent)
        self.lblFileToUploadName.SetLabel("")
        wx.MessageBox("File caricato correttamente")

        return

    def OnUpdateCloudFileTable(self, parent):
        self.lstCloudEncFilesData.DeleteAllItems()
        boolean_formula = self.txtSearchKeywords.GetValue()

        rows = get_cloud_data_by_keywords(boolean_formula, CONNECTED_USER)
        if type(rows) == int:
            if rows == SEARCH_DB_CONNECTION_FAILED:
                wx.MessageBox("Connessione con database di ricerca fallita.", 
                              "Errore", wx.OK | wx.ICON_ERROR)                
                return
            elif rows == BAD_SYNTAX:
                wx.MessageBox("Errore di sintassi nella formula inserita.", 
                              "Errore", wx.OK | wx.ICON_ERROR)            
                return
            elif rows == NO_SEARCH_KEY_AVAILABLE:
                wx.MessageBox("Utente non in possesso " + \
                              "di una chiave di ricerca.", 
                              "Errore", wx.OK | wx.ICON_ERROR)            
                return
        
        # make table
        index = 1
        
        for i in range(len(rows)):
            index = self.lstCloudEncFilesData.InsertStringItem(index, 
                                                           rows[i][1])

            self.lstCloudEncFilesData.SetStringItem(index, 1, 
                                                    "x") # 
            self.lstCloudEncFilesData.SetStringItem(index, 2, 
                                                    rows[i][3]) # policy
            self.lstCloudEncFilesData.SetStringItem(index, 3, 
                                                    rows[i][7]) # encryptor
            self.lstCloudEncFilesData.SetStringItem(index, 4, 
                                                    rows[i][4]) # pk
            self.lstCloudEncFilesData.SetStringItem(index, 5, 
                                                    rows[i][5]) # group
            self.lstCloudEncFilesData.SetStringItem(index, 6, 
                                                    rows[i][6]) # seclev
            self.lstCloudEncFilesData.SetStringItem(index, 7, 
                                                    rows[i][8]) # keywords
            self.lstCloudEncFilesData.SetStringItem(index, 8, 
                                                    str(rows[i][9])) # date
            self.lstCloudEncFilesData.SetStringItem(index, 9, 
                                                    str(rows[i][10])) # vpss_time

            pol = rows[i][3]
            # get user attributes
            temp = self.lstAttributes.GetStrings()
            usr_attr = []
            for a in temp:
                usr_attr.append(a.encode())

            # get attributes in the policy
            pol_attr = list(set(
                         re.compile("\w+").findall(
                           pol.replace("or","").replace("and","").replace("not","")
                         )
                       ))

            # transform policy in Boolean formula
            for a in pol_attr:
                if a in usr_attr:
                    pol = pol.replace(a,"1")
                else:
                    pol = pol.replace(a,"0")

            if bool(eval(pol)):
                self.lstCloudEncFilesData.SetStringItem(index, 1, 
                                                    "Autorizzato")
            else:
                self.lstCloudEncFilesData.SetItemTextColour(index, 
                                                            wx.RED)
                self.lstCloudEncFilesData.SetStringItem(index, 1, 
                                                    "NON Autorizzato")

            index = index + 1

    def OnDownload(self, parent):
        # login
        ftp = FTP(CLOUD_SERVER)
        ftp.login(user=CLOUD_USERNAME, passwd = CLOUD_PASSWORD)

        # download all selected files
        ind = self.lstCloudEncFilesData.GetFirstSelected()
        for i in range(self.lstCloudEncFilesData.GetSelectedItemCount()):
            # define input file path
            filein = self.lstCloudEncFilesData.GetItemText(ind)
            filename = filein
            
            # check filename does not exist
            local_files = os.listdir(os.path.join(USER_FOLDER, \
                                self.lblUserName.GetLabel(), \
                                USER_CIPHERTEXT))
            if filename in local_files:
                wx.MessageBox("Trovato un file locale con nome\n" + \
                              filein + \
                              "\nAggiungo al nome del file " + \
                              "il primo indice progressivo non esistente " + \
                              "maggiore o uguale a 2 ."
                             )
                # if file exists, add a new index to its name
                i = 2
                while 1:
                    filename = filein.replace(".",str(i)+".",1)
                    i = i + 1
                    if not filename in local_files:
                        break

            # define output file path
            fileout = os.path.join(self.userfolder, \
                                   USER_CIPHERTEXT, filename)

            print filename

            ind = self.lstCloudEncFilesData.GetNextSelected(ind)
       
            # get file from server (overwrites if not checked)
            localfile = open(fileout, "wb")
            ftp.retrbinary("RETR " + filein, localfile.write, 1024) 
            localfile.close()

        # close connection
        ftp.quit() 

        wx.MessageBox("File scaricato correttamente")
    ################ END UPLOAD/DOWNLOAD METHODS #############################

# ----------------------------------------------------------------------------

#inherit from the dlgEncrypt created in wxFowmBuilder and create DialogEncrypt
class DialogCreatePolicy(vpss_gui.dlgCreatePolicy):
    #constructor
    def __init__(self,parent):
        #initialize parent class
        vpss_gui.dlgCreatePolicy.__init__(self,parent)

        # read attributes and policies from file POLICIES_FILE
        allpolicies = []
        with open(POLICIES_FILE, "r") as fpol:
            #allpolicies = fpol.readlines()
            allpolicies = fpol.read().splitlines()
        fpol.closed

        # Connect Events
        self.btnAnd.Bind( wx.EVT_BUTTON, self.OnAnd )
        self.btnOr.Bind( wx.EVT_BUTTON, self.OnOr )
        self.btnNot.Bind( wx.EVT_BUTTON, self.OnNot )
        self.btnAddToList.Bind( wx.EVT_BUTTON, self.OnAddToList )
        self.btnFine.Bind( wx.EVT_BUTTON, self.OnEnd )

    def OnAnd(self, event):
        # read attributes and policies from file POLICIES_FILE
        allpolicies = []
        with open(POLICIES_FILE, "r") as fpol:
            allpolicies = fpol.read().splitlines()
        fpol.closed

        dlg = wx.MultiChoiceDialog( self, 
                                   "Scegli gli input",
                                   "Crea Formula con And", allpolicies)
 
        if (dlg.ShowModal() == wx.ID_OK):
            selections = dlg.GetSelections()
            if len(selections) == 1:
                wx.MessageBox("Selezionare almeno due elementi.", 
                              "Errore", wx.OK | wx.ICON_ERROR)
            else:
                atomic_policy = ""
                for i in range(len(selections)-1):
                    atomic_policy = atomic_policy + "(" + \
                                    allpolicies[selections[i]] + ")" + " and " 
                atomic_policy = atomic_policy + "(" + \
                                allpolicies[selections[len(selections)-1]] + \
                                ")" + "" 

                self.txtAtomicPolicy.SetLabel(atomic_policy)

        dlg.Destroy()
            
    def OnOr(self, event):
        # read attributes and policies from file POLICIES_FILE
        allpolicies = []
        with open(POLICIES_FILE, "r") as fpol:
            allpolicies = fpol.read().splitlines()
        fpol.closed

        dlg = wx.MultiChoiceDialog( self, 
                                   "Scegli gli input",
                                   "Crea Formula con Or", allpolicies)
 
        if (dlg.ShowModal() == wx.ID_OK):
            selections = dlg.GetSelections()
            if len(selections) == 1:
                wx.MessageBox("Selezionare almeno due elementi.", 
                              "Errore", wx.OK | wx.ICON_ERROR)
            else:
                atomic_policy = ""
                for i in range(len(selections)-1):
                    atomic_policy = atomic_policy + "(" + \
                                    allpolicies[selections[i]] + ")" + " or " 
                atomic_policy = atomic_policy + "(" + \
                                allpolicies[selections[len(selections)-1]] + \
                                ")" + "" 

                self.txtAtomicPolicy.SetLabel(atomic_policy)

        dlg.Destroy()

    def OnNot(self, event):
        # read attributes and policies from file POLICIES_FILE
        allpolicies = []
        with open(POLICIES_FILE, "r") as fpol:
            allpolicies = fpol.read().splitlines()
        fpol.closed

        dlg = wx.SingleChoiceDialog( self, 
                                   "Scegli un input",
                                   "Crea Formula con Not", allpolicies)
 
        if (dlg.ShowModal() == wx.ID_OK):
            selection = dlg.GetSelection()
            atomic_policy = "not (" + allpolicies[selection] + ")"

            self.txtAtomicPolicy.SetLabel(atomic_policy)            

        dlg.Destroy()

    def OnAddToList(self, event):
        # read attributes and policies from file POLICIES_FILE
        allpolicies = []
        with open(POLICIES_FILE, "r") as fpol:
            allpolicies = fpol.read().splitlines()
        fpol.closed
        
        # check if policy already exists
        if self.txtAtomicPolicy.GetLabel() in allpolicies:
            wx.MessageBox("La policy che si sta cercando di aggiungere " + \
                          "e' gia' presente nell'elenco.", 
                          "Errore", wx.OK | wx.ICON_ERROR)
        elif self.txtAtomicPolicy.GetLabel() == "Nessuna policy creata":
            wx.MessageBox("Nessuna policy inserita.", 
                          "Errore", wx.OK | wx.ICON_ERROR)
        else:
            with open(POLICIES_FILE, "a") as fpol:
                fpol.write(self.txtAtomicPolicy.GetLabel() + "\n")
            fpol.closed
            wx.MessageBox("Policy aggiunta correttamente") 

    def OnEnd(self, event):
        self.Destroy()

# ----------------------------------------------------------------------------

#inherit from the CpAbeFrame created in wxFowmBuilder and create CPABE
class CPABE(vpss_gui.CpAbeFrame):

    #constructor
    def __init__(self,parent):
        #initialize parent class
        vpss_gui.CpAbeFrame.__init__(self,parent)

        self.LoadPanels()

        # Connect Events
        self.Bind( wx.EVT_MENU, self.OnClose, id = self.menuFileClose.GetId() )
        self.Bind( wx.EVT_MENU, self.OnInfo, id = self.menuHelpInfo.GetId() )
        self.btnLogout.Bind( wx.EVT_BUTTON, self.OnLogout )

    # -----------------------------------------------------------
    # function definitions

    def LoadPanels(self):
        global CONNECTED_USER
        # log user or authority in
        #self.dlg = DialogLogin(self)
        #self.dlg.ShowModal()
        self.pnlusr = pnlUsrCPABE(self)
        self.pnlusr.Hide()
        self.pnlauth = pnlAuthCPABE(self)
        self.pnlauth.Hide()

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.pnlusr,  wx.ID_ANY, wx.EXPAND)
        box.Add(self.pnlauth, wx.ID_ANY, wx.EXPAND)

        if CONNECTED_USER == "":
            print "No user logged in! Closing session..."
            #self.Close()
            self.Destroy()

        elif CONNECTED_USER == AUTHORITY_NAME:
            # load authority panel
            self.pnlauth.SetBackgroundColour(wx.RED)
            #pnl.lblUserName.SetLabel(dlg.txtUsr.GetValue()) 
            self.pnlauth.Show()
            self.Show()
        else:
            # load user panel
            self.pnlusr.SetBackgroundColour(wx.GREEN)
            self.pnlusr.lblUserName.SetLabel(CONNECTED_USER) 

            self.pnlusr.username = CONNECTED_USER
            self.pnlusr.userfolder = os.path.join(USER_FOLDER, self.pnlusr.username) # ciphertext folder

            attr = get_user_attributes_from_authdb(CONNECTED_USER)
            for a in attr:
                self.pnlusr.lstAttributes.Append(a)
            # disable decryption if user has no attributes
            if attr == []:
                 self.pnlusr.btnDecrypt.Disable()

            self.pnlusr.Show()
            self.Show()

        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()

    def OnLogout(self, event):
        self.Destroy()
        print("Logged out")
        dlg = DialogLogin(None)
        dlg.ShowModal()
        dlg.Destroy()

    def OnClose(self,event):
        self.Destroy()

    def OnInfo(self, event):
        description = "CODICE: 415CL-101-N001\n" + \
                      "Client per cifratura e decifratura con tecnologia \n" + \
                      "+ Ciphertext-Policy Attribute-Based Encryption (CPABE)\n" + \
                      " + Advance Encryption Standard (AES) \n" + \
                      " + Searchable Encryption (SE)."
        #licence = "Diritti appartenenti a " + \
        #          "Telsy Elettronica e Comunicazioni S.p.A."

        info = wx.AboutDialogInfo()
        info.SetIcon(wx.Icon(TELSY_LOGO_PNG, wx.BITMAP_TYPE_PNG))
        info.SetName("Dimostratore VPSS")
        info.SetVersion("1.0")
        info.SetDescription(description)
        info.SetCopyright("(C) 2015 - 2015 Telsy S.p.A.")
        info.SetWebSite("http://www.telsy.com")
        #info.SetLicence(licence)
        info.AddDeveloper("Emanuele Bellini, Guglielmo Morgari, Marco Coppola")
        info.AddDocWriter("Emanuele Bellini, Guglielmo Morgari, Marco Coppola")
        info.AddArtist("Telsy Elettronica e Comunicazioni S.p.A.")
        #info.AddTranslator("Emanuele Bellini, Guglielmo Morgari, Marco Coppola")

        wx.AboutBox(info) # display box

# ----------------------------------------------------------------------------

class DialogLogin(vpss_gui.dlgLogin):
    #constructor
    def __init__(self, parent):
        #initialize parent class
        vpss_gui.dlgLogin.__init__(self, parent)

        self.logged_in_usr = False
        self.logged_in_auth = False

        # check if first login
        # (by checking if a public key exists)
        pkpath = os.path.join(PUBLIC_PARAMETERS_FOLDER, PUBLIC_KEY)
        if not os.path.isfile(pkpath):
            self.btnUsrLogin.Disable()

        # read usernames from file USERS_FILE
        usernames = []
        with open(USERS_FILE, "r") as f:
            usernames = f.read().splitlines()
        f.closed
        
        for temp in usernames:
            self.chcUsername.Append(temp.split(":")[0])

		    # Connect Events
        self.btnUsrLogin.Bind( wx.EVT_BUTTON, self.OnUsrLogin )
        self.btnAuthLogin.Bind( wx.EVT_BUTTON, self.OnAuthLogin )

    def OnCancel(self, event):
        self.Close()

    def OnUsrLogin(self, event):
        """
        Check credentials and login
        """
        global CONNECTED_USER

        con = mdb.connect(AUTH_SERVER, AUTH_USER, AUTH_PASSWORD, AUTH_NAME )
        cursor = con.cursor()

        #username = self.txtUsr.GetValue()
        username = self.chcUsername.GetStringSelection()
        password = self.txtUsrPwd.GetValue()

        dbpass = get_user_password_from_authdb(username)
        if dbpass == password:
            CONNECTED_USER = username

            self.logged_in_usr = True
            self.logged_in_auth = False # log out the authority
            #self.MakeModal(False)
            #e.Skip()
            self.Close()
            #wx.MessageBox("You are now logged in", "Info", 
            #              wx.OK | wx.ICON_INFORMATION)
            frame = CPABE(None)
            frame.SetIcon(wx.Icon(TELSY_LOGO_ICO, wx.BITMAP_TYPE_ICO))
            #show the frame
            frame.Show(True)

            print "Logged in as " + CONNECTED_USER
        elif dbpass == "":
            wx.MessageBox("Utente non presente nel database.", "Errore", 
                      wx.OK | wx.ICON_ERROR)
            return
        elif dbpass == None:
            wx.MessageBox("Errore durante il login.", "Errore", 
                      wx.OK | wx.ICON_ERROR)
            return
        else:
            wx.MessageBox("Password NON corretta.", "Errore", 
                      wx.OK | wx.ICON_ERROR)


    def OnAuthLogin(self, event):
        """
        Check credentials and login
        """
        global CONNECTED_USER

        con = mdb.connect( AUTH_SERVER, AUTH_USER, AUTH_PASSWORD, AUTH_NAME )
        cursor = con.cursor()
			
        username = AUTHORITY_NAME
        password = self.txtAuthPwd.GetValue()
        
        try:
            cursor.execute("SELECT * FROM users WHERE Usr='" + username  + "'")
            #cursor.execute("SELECT * FROM users WHERE Usr=%s", username)
            data = cursor.fetchall()

            for row in data:
                dbpass = row[2] # second column contains password

            if dbpass == password:
                CONNECTED_USER = AUTHORITY_NAME

                self.logged_in_auth = True
                self.logged_in_usr = False # log out any user
                #self.MakeModal(False)
                #e.Skip()
                self.Close()
                #wx.MessageBox("You are now logged in", "Info", 
                #              wx.OK | wx.ICON_INFORMATION)

                #create an object of CPABE
                frame = CPABE(None)
                frame.SetIcon(wx.Icon(TELSY_LOGO_ICO, wx.BITMAP_TYPE_ICO))
                #show the frame
                frame.Show(True)

                print "Logged in as " + CONNECTED_USER
            else:
                wx.MessageBox("Nome utente o password NON corretti.", "Errore", 
                          wx.OK | wx.ICON_ERROR)
        except:
            wx.MessageBox("E' avvenuto un problema durante il login.", "Errore", 
                          wx.OK | wx.ICON_ERROR)
        finally:    
            if con:    
                con.close()

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

# MAIN 
if __name__ == "__main__":
    # global variable
    CONNECTED_USER = ""

    #mandatory in wx, create an app, False stands for not rederiction stdin/stdout
    #refer manual for details
    app = wx.App(False)

    dlg = DialogLogin(None)
    dlg.ShowModal()
    dlg.Destroy()

    #start the applications
    app.MainLoop()


