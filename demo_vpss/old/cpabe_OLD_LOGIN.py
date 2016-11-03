#importing wx files
import wx
 
#import the newly created GUI file
import cpabe_gui
 
# import other libraries
import os   # operating system functions
import sys
import glob
import re   # regular expression

from subprocess import call

# for server connection
from ftplib import FTP

# for mysql connection
import MySQLdb as mdb


from cpabe_def import *
from cpabe_func import *

# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------

class DialogLogin(cpabe_gui.dlgLogin):
    #constructor
    
    def __init__(self, parent):
        #initialize parent class
        cpabe_gui.dlgLogin.__init__(self, parent)

        self.logged_in_usr = False
        self.logged_in_auth = False
        self.usr = ""
        self.usrpwd = ""
        self.authpwd = ""

		    # Connect Events
        self.btnUsrLogin.Bind( wx.EVT_BUTTON, self.OnUsrLogin )
        self.btnAuthLogin.Bind( wx.EVT_BUTTON, self.OnAuthLogin )

    def OnCancel(self, event):
        self.usr = "NO_USER_SELECTED"
        self.Destroy()

    def OnUsrLogin(self, event):
        """
        Check credentials and login
        """
        self.usr = self.txtUsr.GetValue()
        self.usrpwd = self.txtUsrPwd.GetValue()

        stupid_password = "123"
        if self.usrpwd == stupid_password:
            print "Logged in as " + self.usr
            self.logged_in_usr = True
            self.logged_in_auth = False # log out the authority
            self.Close()
        else:
            self.txtUsr.SetValue("")
            self.txtUsrPwd.SetValue("")
            self.txtAuthPwd.SetValue("")
            wx.MessageBox("Nome utente o password NON corretti.", "Errore", 
                          wx.OK | wx.ICON_ERROR)


    def OnAuthLogin(self, event):
        """
        Check credentials and login
        """
        self.authpwd = self.txtAuthPwd.GetValue()
        
        stupid_password = "123"
        if self.authpwd == stupid_password:
            print "Logged in as authority"
            self.logged_in_auth = True
            self.logged_in_usr = False # log out any user
            self.Close()
        else:
            self.txtUsr.SetValue("")
            self.txtUsrPwd.SetValue("")
            self.txtAuthPwd.SetValue("")
            wx.MessageBox("Nome utente o password NON corretti.", "Errore", 
                          wx.OK | wx.ICON_ERROR)

# ----------------------------------------------------------------------------

class DialogKeygen(cpabe_gui.dlgKeygen):

    def __init__(self, parent):
        cpabe_gui.dlgKeygen.__init__(self,parent)

        for i in range(len(CURVES)):
            self.chcSecLevAndCurve.Append("SEC LEV=" + str(CURVES[i][0]) + \
                                          " -- CURVE=" + CURVES[i][1])

        self.grouppath = ""
        self.mkpath = ""
        self.pkpath = ""
        self.skpath = ""
        self.attr = ATTRIBUTES
        self.selected_attr = []

        # Connect Events
        self.btnKeygen.Bind( wx.EVT_BUTTON, self.OnKeygen )
        self.btnChooseMK.Bind( wx.EVT_BUTTON, self.OnChooseMK )
        self.btnChoosePK.Bind( wx.EVT_BUTTON, self.OnChoosePK )
        self.btnAttributes.Bind( wx.EVT_BUTTON, self.OnAttributes )

    # -----------------------------------------------------------
    # function definitions

    def OnAttributes(self, event):
        dlg = wx.MultiChoiceDialog( self, 
                                   "Seleziona attributi",
                                   "Seleziona gli attributi " + \
                                   "da associare alla chiave segreta", 
                                   self.attr)

        if (dlg.ShowModal() == wx.ID_OK):
            idx = dlg.GetSelections()
            self.selected_attr = ":".join([self.attr[i] for i in idx])

    def OnChooseMK(self, event):
        dlg = wx.FileDialog(self, "Scegli una chiave master", 
                            AUTH_MASTER_KEY_FOLDER, "", "*.k", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.mkpath = dlg.GetPath()
            self.lblMKName.SetLabel(self.mkpath)
        dlg.Destroy()

    def OnChoosePK(self, event):
        dlg = wx.FileDialog(self, "Scegli una chiave pubblica", 
                            PUBLIC_PARAMETERS_FOLDER, "", "*.k", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.pkpath = dlg.GetPath()
            self.lblPKName.SetLabel(self.pkpath)
        dlg.Destroy()

    def OnKeygen(self, event):

        if self.chcSecLevAndCurve.GetStringSelection() == "":
            wx.MessageBox("Selezionare livello di sicurezza e curva.",
                              "Attenzione", 
                              wx.OK | wx.ICON_ERROR)
            return
        else:
            self.seclev = self.chcSecLevAndCurve.GetStringSelection()\
                              .split(" -- ")[0].split("=")[1]
            self.curve = self.chcSecLevAndCurve.GetStringSelection()\
                             .split(" -- ")[1].split("=")[1]

        if self.mkpath == "":
            wx.MessageBox("Selezionare una chiave master.",
                              "Attenzione", 
                              wx.OK | wx.ICON_ERROR)
            return

        if self.pkpath == "":
            wx.MessageBox("Selezionare una chiave pubblica.",
                              "Attenzione", 
                              wx.OK | wx.ICON_ERROR)
            return

        self.grouppath = PUBLIC_PARAMETERS_FOLDER + "/" + self.curve + ".g"
        self.skpath = AUTH_SECRET_KEY_FOLDER + "/" + \
                      self.txtUsrKeyName.GetValue() + ".k"

        if os.path.exists(self.skpath):
            dlg = wx.MessageDialog(None, "Il file " + self.skpath + \
                                          ".k esiste. Sovrascriverlo?", 
                                    "Domanda", 
                                    wx.CANCEL | wx.YES_NO | 
                                    wx.NO_DEFAULT | wx.ICON_QUESTION)
            temp = dlg.ShowModal()
            if temp == wx.ID_NO:
                wx.MessageBox("Generazione interrotta. Per riprovare " + \
                              "cambiare il nome della chiave segreta " + \
                              "con uno NON esistente " + \
                              "o accettare di sovrascrivere il file.", 
                              "Attenzione", 
                              wx.OK | wx.ICON_ERROR)
                return
            if temp == wx.ID_CANCEL:
                return

        call(["python3", "abe-keygen.py",
              self.grouppath, self.mkpath, self.pkpath, 
              self.selected_attr, self.skpath
            ])

        wx.MessageBox("La seguente chiave segreta " + 
                      "e' stata generata correttamente:\n\n" + \
                      self.skpath + "\n\n" + \
                      "Utilizzando:\n\n" + \
                      "- curva\n\n" + \
                      self.grouppath + "\n\n" + \
                      "- chiave master\n\n" + \
                      self.mkpath + "\n\n" + \
                      "- chiave pubblica\n\n" + \
                      self.pkpath + "\n\n" + \
                      "- attributi\n\n" + \
                      self.selected_attr + "\n\n"
                     )

# ----------------------------------------------------------------------------
        
class pnlAuthCPABE(cpabe_gui.pnlAuthorityCPABE):
    #viewfile = "/home/ema/Dropbox/ACCADEMIC/Python/wxPython/cpabe/"

    def __init__(self, parent):
        cpabe_gui.pnlAuthorityCPABE.__init__(self,parent)


        for i in range(len(CURVES)):
            self.chcSecLevAndCurve.Append("SEC LEV=" + str(CURVES[i][0]) + \
                                          " -- CURVE=" + CURVES[i][1])

        # Connect Events
        self.btnSetup.Bind( wx.EVT_BUTTON, self.OnSetup )
        self.btnGenUsrKey.Bind( wx.EVT_BUTTON, self.OnGenUsrKey )

    # -----------------------------------------------------------
    # function definitions

    def OnGenUsrKey(self, event):
        dlg = DialogKeygen(self)
        dlg.ShowModal()
        dlg.Destroy()

    def OnSetup(self, event):
        self.group_folder = PUBLIC_PARAMETERS_FOLDER
        self.mkname = self.txtMK.GetValue()
        self.mkpath = AUTH_MASTER_KEY_FOLDER + "/" + self.mkname + ".k"
        self.pkname = self.txtPK.GetValue()
        self.pkpath = PUBLIC_PARAMETERS_FOLDER + "/" + self.pkname + ".k"

        if self.chcSecLevAndCurve.GetStringSelection() == "":
            wx.MessageBox("Selezionare livello di sicurezza e curva.",
                              "Attenzione", 
                              wx.OK | wx.ICON_ERROR)
            return
        else:
            self.group_name = CURVES[self.chcSecLevAndCurve.GetSelection()][1]

        if os.path.exists(self.mkpath):
            dlg = wx.MessageDialog(None, "Il file " + self.mkname + \
                                          ".k esiste. Sovrascriverlo?", 
                                    "Domanda", 
                                    wx.CANCEL | wx.YES_NO | 
                                    wx.NO_DEFAULT | wx.ICON_QUESTION)
            temp = dlg.ShowModal()
            if temp == wx.ID_NO:
                wx.MessageBox("Generazione interrotta. Per riprovare " + \
                              "cambiare il nome della chiave master " + \
                              "con uno NON esistente " + \
                              "o accettare di sovrascrivere il file.", 
                              "Attenzione", 
                              wx.OK | wx.ICON_ERROR)
                return
            if temp == wx.ID_CANCEL:
                return

        if os.path.exists(self.pkpath):
            dlg = wx.MessageDialog(None, "Il file " + self.pkname + \
                                          ".k esiste. Sovrascriverlo?", 
                                    "Domanda", 
                                    wx.CANCEL | wx.YES_NO | 
                                    wx.NO_DEFAULT | wx.ICON_QUESTION)
            temp = dlg.ShowModal()
            if temp == wx.ID_NO:
                wx.MessageBox("Generazione interrotta. Per riprovare " + \
                              "cambiare il nome della chiave pubblica " + \
                              "con uno NON esistente " + \
                              "o accettare di sovrascrivere il file.",
                              "Attenzione", 
                              wx.OK | wx.ICON_ERROR)
                return
            if temp == wx.ID_CANCEL:
                return


        call(["python3", "abe-setup.py",
              self.group_name, self.group_folder, self.pkpath, self.mkpath
            ])

        wx.MessageBox("- chiave master\n\n" + \
                      self.mkpath + "\n\n" + \
                      "- chiave pubblica\n\n" + \
                      self.pkpath + "\n\n" + \
                      "generate correttamente\n\n" + \
                      "utilizzando:\n\n" + \
                      "- curva\n\n" + \
                      self.group_name + "\n\n"
                     )

# ----------------------------------------------------------------------------
# ------------------------ USER PANEL ----------------------------------------
# ----------------------------------------------------------------------------

class pnlUsrCPABE(cpabe_gui.pnlClientCPABE):
    #viewfile = "/home/ema/Dropbox/ACCADEMIC/Python/wxPython/cpabe/"

    def __init__(self, parent):
        cpabe_gui.pnlClientCPABE.__init__(self,parent)

        # variables definitions ----------------------------------------------

        # read attributes and policies from file POLICY_FILE
        allpolicies = []
        with open(POLICY_FILE, 'r') as fpol:
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

        self.lstCloudEncFilesData.ClearAll()
        self.lstCloudEncFilesData.InsertColumn(0,"File") 
        self.lstCloudEncFilesData.InsertColumn(1,"Autorizzazione") 
        self.lstCloudEncFilesData.InsertColumn(2,"Policy")
        self.lstCloudEncFilesData.InsertColumn(3,"Cifrato da")
        self.lstCloudEncFilesData.InsertColumn(4,"Chiave Pubblica")
        self.lstCloudEncFilesData.InsertColumn(5,"Livello sicurezza")
        self.lstCloudEncFilesData.InsertColumn(6,"Gruppo")

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
        self.chcSecLev.Bind( wx.EVT_CHOICE, self.OnChooseSecLev )
        self.btnChoosePK.Bind( wx.EVT_BUTTON, self.OnChoosePK )
        #self.btnChooseGroup.Bind( wx.EVT_BUTTON, self.OnChooseGroup )
        self.btnChooseSK.Bind( wx.EVT_BUTTON, self.OnChooseSK )

        # ENCRYPT EVENTS
        self.btnChooseFileToEncrypt.Bind( wx.EVT_BUTTON, self.OnChooseFileToEncrypt )
        self.btnCreatePolicy.Bind( wx.EVT_BUTTON, self.OnCreatePolicy )
        self.chcShowPolicies.Bind( wx.EVT_CHOICE, self.OnSelectPolicy )
        self.btnEncrypt.Bind( wx.EVT_BUTTON, self.OnEncrypt )

        # DECRYPT EVENTS
        self.btnChooseFileToDecrypt.Bind( wx.EVT_BUTTON, self.OnChooseFileToDecrypt )
        self.btnDecrypt.Bind( wx.EVT_BUTTON, self.OnDecrypt )

        # OTHER EVENTS
        self.btnUpdateFileTable.Bind( wx.EVT_BUTTON, self.OnUpdateFileTable )
        self.btnUpdate.Bind( wx.EVT_BUTTON, self.OnUpdate )

        # UPLOAD/DOWNLOAD EVENTS
        self.btnChooseFileToUpload.Bind( wx.EVT_BUTTON, self.OnChooseFileToUpload )
        self.btnUpdateCloudFileTable.Bind( wx.EVT_BUTTON, self.OnUpdateCloudFileTable )
        self.btnUpload.Bind( wx.EVT_BUTTON, self.OnUpload )
        self.btnDownload.Bind( wx.EVT_BUTTON, self.OnDownload )


    # methods definitions ----------------------------------------------------

    ################ BEGIN SETTING METHODS ###################################

    def OnChooseSecLev(self, event):
        s = self.chcSecLev.GetStringSelection()
        if s == u"selezionare":
            self.seclev = ""
            self.groupname = ""
        else:
            s = s.split(":")
            self.seclev = s[0]
            self.groupname = s[1]
            self.grouppath = PUBLIC_PARAMETERS_FOLDER + "/" + \
                             self.groupname + ".g"

    def OnChoosePK(self, event):
        dlg = wx.FileDialog(self, "Scegli una chiave pubblica", 
                            PUBLIC_PARAMETERS_FOLDER, "", "*.k", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.pkpath = dlg.GetPath()
            self.lblPKName.SetLabel(self.pkpath)
        dlg.Destroy()

    """
    def OnChooseGroup(self, event):
        dlg = wx.FileDialog(self, "Scegli una gruppo", 
                            PUBLIC_PARAMETERS_FOLDER, "", "*.g", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.grouppath = dlg.GetPath()
            self.lblGroupName.SetLabel(self.grouppath)
        dlg.Destroy()
    """

    def OnChooseSK(self, event):
        dlg = wx.FileDialog(self, "Scegli una chiave segreta", 
                            self.userfolder + USER_ABE_KEY, 
                            "", "*.k", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.skpath = dlg.GetPath()
            self.lblSKName.SetLabel(self.skpath)
        dlg.Destroy()

    ################ END SETTING METHODS #####################################

    ################ BEGIN ENCRYPT METHODS ###################################

    def OnChooseFileToEncrypt(self, event):
        dlg = wx.FileDialog(self, "Scegli un file",  
                            self.userfolder + USER_PLAINTEXT, 
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
        with open(POLICY_FILE, 'r') as fpol:
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
        if self.seclev == u"selezionare" or self.seclev == "":
            s = self.chcSecLev.GetString(1)
            s = s.split(":")
            self.seclev = s[0]
            self.groupname = s[1]
            self.grouppath = PUBLIC_PARAMETERS_FOLDER + "/" + \
                                 self.groupname + ".g"
            print("Livello sicurezza di default selezionata:\n" + \
                         self.seclev)
            print("Gruppo di default selezionato:\n" + \
                         self.grouppath)
            #readytoenc = 0
            #wx.MessageBox("Livello di sicurezza NON selezionato " + \
            #              "nel Tab 'Impostazioni Crittografiche'.", 
            #              "Errore", 
            #              wx.OK | wx.ICON_ERROR)
            # return

        if self.pkpath == "":
            self.pkpath = PUBLIC_PARAMETERS_FOLDER + "/public.k"
            print("Chiave pubblica di default selezionata:\n" + \
                         self.pkpath)
            #readytoenc = 0
            #wx.MessageBox("Nessuna chiave pubblica selezionata " + \
            #              "nel Tab 'Impostazioni Crittografiche'.", 
            #              "Errore", 
            #              wx.OK | wx.ICON_ERROR)
            # return

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
            self.username = self.lblUserName.GetLabel()
            self.userfolder = USER_FOLDER + "/" + self.username # ciphertext folder
            self.symkpath = self.userfolder + \
                            USER_AES_KEY + "/symmetric.k" # symmetric key name and path 

            self.encsymkpath = self.userfolder + \
                               USER_CIPHERTEXT + "/" + \
                               self.plaintextname + ".k.enc"
            self.ciphertextpath = self.userfolder + \
                               USER_CIPHERTEXT + "/" + \
                               self.plaintextname + ".enc"

            # 0 - generate random symmetric key
            call(["python3", "abe-random-ec-point.py", 
                  self.grouppath, self.symkpath
                ])

            # 1 - encrypt symmetric key with policy
            # python3 abe-encrypt.py '((ATTR1 or ATTR2) and (ATTR3 or ATTR4))'

            call(["python3", "abe-encrypt.py", self.grouppath, self.pkpath, 
                  self.policy, self.symkpath, self.encsymkpath])
            
            # 2 - encrypt file with symmetric key
            # python3 aescrypt.py -f prova.txt
            call(["python3", "aescrypt.py", "-f", 
                  self.plaintextpath, self.ciphertextpath, self.symkpath])

            # 3 - add metadata to encrypted file
            metadata = "UTENTE:" + self.username + "\n" + \
                       "SECLEV:" + self.seclev + "\n" + \
                       "GROUPPATH:" + self.grouppath + "\n" + \
                       "PKPATH:" + self.pkpath + "\n" + \
                       "POLICY:" + self.policy

            # join files
            s = metadata

            s = s + FILESEPARATOR

            # read encrypted abe key
            with open(self.encsymkpath,"r") as f:
              s = s + f.read()
            f.close()
            
            s = s + FILESEPARATOR

            # read encrypted file
            with open(self.ciphertextpath,"rb") as f:
              temp = f.read()
              s = bytes(s) + temp
            f.close()

            # write in one file: metadata - encrypted abe key - encrypted file
            with open(self.ciphertextpath, "w") as f:
                f.write(s)
            f.close()

            # REMOVE encrypted abe key file
            os.remove(self.symkpath)      # aes symmetric key file
            os.remove(self.encsymkpath)   # encrypted aes symmetric key file
            os.remove(self.plaintextpath) # aes

            wx.MessageBox("Cifratura eseguita correttamente.\n\n" + 
                          "File:\n\n" + self.plaintextpath + "\n\n" +
                          "Livello di sicurezza:\n\n" +  self.seclev + "\n\n" 
                          "Gruppo:\n\n" +  self.groupname + "\n\n" 
                          "Chiave pubblica:\n\n" + self.pkpath + "\n\n" + 
                          "Policy:\n\n" + self.policy + "\n\n"
                         )

            self.plaintextpath = ""
            self.plaintextname = ""
            self.ciphertextpath = ""
            self.ciphertextname = ""
            self.lblFileToEncryptName.SetLabel(u"Nessuna selezione effettuata...")

    ################ END ENCRYPT METHODS #####################################

    ################ BEGIN DECRYPT METHODS ###################################

    def OnChooseFileToDecrypt(self, event):
        dlg = wx.FileDialog(self, "Scegli un file",  
                            self.userfolder + USER_CIPHERTEXT, 
                            "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.ciphertextpath2 = dlg.GetPath()
            self.ciphertextname2 = dlg.GetFilename() 
            # remove .enc extension
            #self.ciphertextname2 = self.ciphertextname2[0:len(self.ciphertextname2)-4]

            #self.encsymkpath2 = self.userfolder + \
            #                   USER_CIPHERTEXT + "/" + \
            #                   self.ciphertextname2 + ".k.enc"
            #self.plaintextpath2 = self.userfolder + \
            #                   USER_PLAINTEXT + "/" + \
            #                   self.ciphertextname2

            self.lblFileToDecryptName.SetLabel(self.ciphertextpath2)

        dlg.Destroy()

    def OnDecrypt(self, event):
        readytodec = 1
        # INPUT checks
        #if self.seclev == u"selezionare" or self.seclev == "":
            #s = self.chcSecLev.GetString(1)
            #s = s.split(":")
            #self.seclev = s[0]
            #self.groupname = s[1]
            #self.grouppath = PUBLIC_PARAMETERS_FOLDER + "/" + \
            #                     self.groupname + ".g"
            #print("Livello sicurezza di default selezionata:\n" + \
            #             self.seclev)
            #print("Gruppo di default selezionato:\n" + \
            #             self.grouppath)
            #readytoenc = 0
            #wx.MessageBox("Livello di sicurezza NON selezionato " + \
            #              "nel Tab 'Impostazioni Crittografiche'.", 
            #              "Errore", 
            #              wx.OK | wx.ICON_ERROR)
            # return

        if self.pkpath == "":
            self.pkpath = PUBLIC_PARAMETERS_FOLDER + "/public.k"
            print("Chiave pubblica di default selezionata:\n" + \
                         self.pkpath)
            #readytoenc = 0
            #wx.MessageBox("Nessuna chiave pubblica selezionata " + \
            #              "nel Tab 'Impostazioni Crittografiche'.", 
            #              "Errore", 
            #              wx.OK | wx.ICON_ERROR)
            # return

        # check group and public key are ok with each other ???
        # ...

        if self.skpath == "":
            wx.MessageBox("Nessuna chiave segreta selezionata " + \
                          "nel Tab 'Impostazioni Crittografiche'.", 
                          "Errore", wx.OK | wx.ICON_ERROR)
            readytodec = 0
            return

        if self.ciphertextpath2 == "":
            wx.MessageBox("Nessun file da decifrare selezionato.", 
                          "Errore", wx.OK | wx.ICON_ERROR)
            readytodec = 0
            return

        # DECRYPT
        if readytodec == 1:

            self.username = self.lblUserName.GetLabel()
            self.userfolder = USER_FOLDER + "/" + self.username # ciphertext folder

            # remove .enc extension
            self.plaintextname2 = self.ciphertextname2[0:len(self.ciphertextname2)-4]
            self.plaintextpath2 = self.userfolder + \
                               USER_PLAINTEXT + "/" + \
                               self.plaintextname2

            self.symkpath2 = self.userfolder + \
                            USER_AES_KEY + "/symmetric.k" # symmetric key name and path 

            self.encsymkpath2 = self.userfolder + \
                               USER_CIPHERTEXT + "/" + \
                               self.plaintextname2 + ".k.enc"

            # read encrypted file data and metadata
            with open(self.ciphertextpath2, "rb") as f: 
                s = f.read()
            f.close()

            print("FILE == " + self.encsymkpath2)

            # write file with encrypted abe key
            with open(self.encsymkpath2, "w") as f: 
                f.write(s.split(FILESEPARATOR.encode())[1].decode())
            f.close()

            # extract METADATA
            metadata = s.split(FILESEPARATOR.encode())[0].decode()

            usr = metadata.split("\n")[0].split(":")[1]
            seclev = metadata.split("\n")[1].split(":")[1]
            self.grouppath = metadata.split("\n")[2].split(":")[1]
            self.pkpath = metadata.split("\n")[3].split(":")[1]
            policy = metadata.split("\n")[4].split(":")[1]


            # 1 - ABE decrypt
            call(["python3", "abe-decrypt.py", self.grouppath, self.pkpath,
                  self.skpath, self.encsymkpath2, self.symkpath2
                ])

            with open(self.symkpath2, "rb") as f:
                symk = f.read()
            f.close()

            if symk == b"USER_KEY_DOES_NOT_SATISFY_POLICY":
                wx.MessageBox("Gli attributi associati " + \
                              "alla chiave segreta selezionata " + \
                              "non soddisfano la policy.", 
                              "Errore", wx.OK | wx.ICON_ERROR
                             )
                # REMOVE encrypted and unencrypted abe key file
                os.remove(self.symkpath2)         # aes symmetric key
                os.remove(self.encsymkpath2)      # aes encrypted symmetric key

            else:
                # write on file only its content (no metadata and no enc-abe key)
                with open(self.ciphertextpath2, "wb") as f: 
                    f.write(s.split(FILESEPARATOR.encode())[2])
                f.close()

                # 2 - AES decrypt
                call(["python3", "aescrypt.py", "-d", "-f", self.ciphertextpath2,
                      self.plaintextpath2, self.symkpath2
                    ])

                # REMOVE encrypted file and encrypted and unencrypted abe key file
                os.remove(self.ciphertextpath2)   # encrypted file
                os.remove(self.symkpath2)         # aes symmetric key
                os.remove(self.encsymkpath2)      # aes encrypted symmetric key

                wx.MessageBox("Decifratura eseguita correttamente.\n\n" + 
                              "File decifrato:\n\n" + self.ciphertextpath2 + "\n\n"
                             )

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
        for fname in os.listdir(USER_FOLDER + "/" + \
                                self.lblUserName.GetLabel() + \
                                USER_CIPHERTEXT):

            # read encrypted file data and metadata
            filename = USER_FOLDER + "/" + \
                                self.lblUserName.GetLabel() + \
                                USER_CIPHERTEXT + "/" + fname.encode()

            meta, encr, sl, gr, pk, pol = get_encrypted_file_data(filename)
            if meta == NODATA:
                print("Il file \n" + filename + "\nnon contiene metadata!")
            else:
                index = self.lstEncFilesData.InsertStringItem(index, fname)

                self.lstEncFilesData.SetStringItem(index, 2, pol)
                self.lstEncFilesData.SetStringItem(index, 3, encr)
                self.lstEncFilesData.SetStringItem(index, 4, pk)
                self.lstEncFilesData.SetStringItem(index, 5, sl)
                self.lstEncFilesData.SetStringItem(index, 6, gr)

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
                    self.lstEncFilesData.SetStringItem(index, 1, "Autorizzato")
                else:
                    self.lstEncFilesData.SetItemTextColour(index, wx.RED)
                    self.lstEncFilesData.SetStringItem(index, 1, "NON Autorizzato")

                index = index + 1

    # ------------------------------------------------------------------------

    def OnUpdate(self, event):
        self.lstGroups.Clear()
        for fname in os.listdir(os.getcwd() + "/public_parameters"):
            if fname.endswith(".g"):
                self.lstGroups.Append(fname)

        self.lstPK.Clear()
        for fname in os.listdir(os.getcwd() + "/public_parameters"):
            if fname.endswith(".k"):
                self.lstPK.Append(fname)

        self.lstSK.Clear()
        for fname in os.listdir(USER_FOLDER + "/" + \
                                self.lblUserName.GetLabel() + \
                                USER_ABE_KEY):
            if fname.endswith(".k"):
                self.lstSK.Append(fname)

        self.lstFile.Clear()
        for fname in os.listdir(USER_FOLDER + "/" + \
                                self.lblUserName.GetLabel() + \
                                USER_PLAINTEXT):
            #if fname.endswith(".k"):
            self.lstFile.Append(fname)

        self.lstEncFile.Clear()
        for fname in os.listdir(USER_FOLDER + "/" + \
                                self.lblUserName.GetLabel() + \
                                USER_CIPHERTEXT):
            #if fname.endswith(".k"):
            self.lstEncFile.Append(fname)


    ################ BEGIN UPLOAD/DOWNLOAD METHODS ###########################

    def OnChooseFileToUpload(self, parent):
        dlg = wx.FileDialog(self, "Scegli un file",  
                            self.userfolder + USER_CIPHERTEXT, 
                            "", "*.enc", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filetouploadpath = dlg.GetPath()
            self.filetouploadname = dlg.GetFilename()
            self.lblFileToUploadName.SetLabel(self.filetouploadpath)
        dlg.Destroy()

    def OnUpload(self, parent):

        #####################################################################
        # IMPORTANT NOTE:                                                   #
        # ---------------                                                   #
        # FIRST ENCRYPTED FILE IS UPLOADED TO FTP SERVER                    # 
        # SECOND METADATA ARE UPLOADED TO DB SERVER                         #
        # NO CHECK IS DONE IF ONE OF THE TWO DOES NOT SUCCEED               #
        # THIS MAY BRING TO SOME INCOGRUENCE                                #
        #####################################################################
        
        # UPDATE FTP SERVER (CLOUD)
        # -------------------------

        # login
        ftp = FTP(CLOUD_SERVER)
        ftp.login(user=CLOUD_USERNAME, passwd = CLOUD_PASSWORD)

        # upload
        self.filetouploadpath = self.lblFileToUploadName.GetLabel()
        self.filetouploadname = self.filetouploadpath.split("/")[-1]
        if self.filetouploadpath == "":
            wx.MessageBox("Selezionare un file da caricare.",
                          "Errore", wx.OK | wx.ICON_ERROR
                         )
        else:
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
            ftp.storbinary("STOR " + fileout, open(filein, "rb"))

        # close connection
        ftp.quit() 

        # UPDATE MYSQL DATABASE
        # ---------------------

        meta, encr, sl, gr, pk, pol = get_encrypted_file_data(self.filetouploadpath)

        try:

            con = mdb.connect(DB_SERVER, DB_USER, DB_PASSWORD, DB_NAME)

            with con:
                cur = con.cursor()

                keywords = self.txtKeywords.GetValue().replace(" ","")
                print keywords
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
                               UploadDate \
                              ) VALUES ( \
                               '" + self.filetouploadname + "', \
                               '/home/cloud/" + self.filetouploadname + "', \
                               '" + pol + "', \
                               '" + pk + "', \
                               '" + gr + "', \
                               '" + sl + "', \
                               '" + encr + "', \
                               '" + keywords + "', \
                               CURDATE() \
                              )"
                cur.execute( mysql_command )

        except mdb.Error, e:
          
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
            
        finally:    
                
            if con:    
                con.close()

        self.filetouploadpath = ""
        self.filetouploadname = ""

        return

    def OnUpdateCloudFileTable(self, parent):
        self.lstCloudEncFilesData.DeleteAllItems()
        #index = self.lstEncFilesData.GetItemCount() + 1
        ######################################################################
        try:
            con = mdb.connect(DB_SERVER, DB_USER, DB_PASSWORD, DB_NAME)

            with con:
                cur = con.cursor()

                # retrieve data (get list of files)
                cur.execute("SELECT * FROM cloud")
                rows = cur.fetchall()

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
                                                            rows[i][5]) # seclev
                    self.lstCloudEncFilesData.SetStringItem(index, 6, 
                                                            rows[i][5]) # group

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

        except mdb.Error, e:
          
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
            
        finally:    
                
            if con:    
                con.close()

        ######################################################################
        """ 
        # to get the list from ftp server

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

        # close connection
        ftp.quit() 
        """

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
            local_files = os.listdir(USER_FOLDER + "/" + \
                                self.lblUserName.GetLabel() + \
                                USER_CIPHERTEXT)
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
            fileout = self.userfolder + \
                      USER_CIPHERTEXT + "/" + filename

            print filename

            ind = self.lstCloudEncFilesData.GetNextSelected(ind)
       
            # get file from server (overwrites if not checked)
            localfile = open(fileout, "wb")
            ftp.retrbinary("RETR " + filein, localfile.write, 1024) 
            localfile.close()

        # close connection
        ftp.quit() 

    ################ END UPLOAD/DOWNLOAD METHODS #############################

# ----------------------------------------------------------------------------

#inherit from the CpAbeFrame created in wxFowmBuilder and create CPABE
class CPABE(cpabe_gui.CpAbeFrame):

    #constructor
    def __init__(self,parent):
        #initialize parent class
        cpabe_gui.CpAbeFrame.__init__(self,parent)

        self.pnlusr = pnlUsrCPABE(self)
        self.pnlusr.Hide()
        self.pnlauth = pnlAuthCPABE(self)
        self.pnlauth.Hide()

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.pnlusr,  wx.ID_ANY, wx.EXPAND)
        box.Add(self.pnlauth, wx.ID_ANY, wx.EXPAND)
  
        self.Login()

        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()

        # Connect Events
        self.Bind( wx.EVT_MENU, self.OnClose, id = self.menuFileClose.GetId() )
        self.Bind( wx.EVT_MENU, self.OnInfo, id = self.menuHelpInfo.GetId() )
        self.btnLogInOut.Bind( wx.EVT_BUTTON, self.OnLogInOut )

    # -----------------------------------------------------------
    # function definitions

    def Login(self):
        # log user or authority in
        self.dlg = DialogLogin(self)
        self.dlg.ShowModal()

        if self.dlg.logged_in_usr:
            # load user panel
            self.pnlusr.SetBackgroundColour(wx.BLACK)
            self.pnlusr.lblUserName.SetLabel(self.dlg.txtUsr.GetValue()) 

            self.pnlusr.username = self.dlg.txtUsr.GetValue()
            self.pnlusr.userfolder = USER_FOLDER + "/" + self.pnlusr.username # ciphertext folder

            for i in range(len(USERS)):
                if self.pnlusr.username in USERS[i].values():
                    self.pnlusr.lstAttributes.Clear()
                    for a in USERS[i]["attr"]:
                        self.pnlusr.lstAttributes.Append(a)
                    break
            # clear all panel content
            self.pnlusr.lstEncFilesData.DeleteAllItems()
            self.pnlusr.lstCloudEncFilesData.DeleteAllItems()
            self.pnlusr.lstGroups.Clear()
            self.pnlusr.lstPK.Clear()
            self.pnlusr.lstSK.Clear()
            self.pnlusr.lstFile.Clear()
            self.pnlusr.lstEncFile.Clear()
            self.pnlusr.txtKeywords.SetValue("parola1, parola2, parola3")
            self.pnlusr.chcSecLev.SetSelection(0)

        elif self.dlg.logged_in_auth:
            # load authority panel
            self.pnlauth.SetBackgroundColour(wx.GREEN)
            #pnl.lblUserName.SetLabel(dlg.txtUsr.GetValue()) 
            self.pnlauth.Show()
            self.Show()

        else:
            self.Close()

    def OnLogInOut(self, event):
        self.Login()
        if self.dlg.logged_in_usr:
            # switch panels
            self.pnlusr.Show()
            self.pnlauth.Hide()
        elif self.dlg.logged_in_auth:
            # switch panels
            self.pnlusr.Hide()
            self.pnlauth.Show()
        else:
            self.Close()
        self.Layout()


    def OnClose(self,event):
        self.Destroy()

    def OnInfo(self, event):
        description = "Client per cifratura e decifratura con tecnologia " + \
                      "Ciphertext-policy Attribute-Based Encryption (CPABE)" + \
                      " + Advance Encryption Standard (AES) Encryption."
        licence = "Diritti appartenenti a " + \
                  "Telsy Elettronica e Comunicazioni S.p.A."

        info = wx.AboutDialogInfo()
        info.SetIcon(wx.Icon(TELSY_LOGO_PNG, wx.BITMAP_TYPE_PNG))
        info.SetName('Dimostratore CPABE')
        info.SetVersion('0.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2015 - 2015 Emanuele Bellini')
        info.SetWebSite('http://www.telsy.com')
        info.SetLicence(licence)
        info.AddDeveloper('Emanuele Bellini')
        info.AddDocWriter('Emanuele Bellini')
        info.AddArtist('Telsy Elettronica e Comunicazioni S.p.A., Crypto Group')
        info.AddTranslator('Emanuele Bellini')

        wx.AboutBox(info) # display box

# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------

#inherit from the dlgEncrypt created in wxFowmBuilder and create DialogEncrypt
class DialogCreatePolicy(cpabe_gui.dlgCreatePolicy):
    #constructor
    def __init__(self,parent):
        #initialize parent class
        cpabe_gui.dlgCreatePolicy.__init__(self,parent)

        # read attributes and policies from file POLICY_FILE
        allpolicies = []
        with open(POLICY_FILE, 'r') as fpol:
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
        # read attributes and policies from file POLICY_FILE
        allpolicies = []
        with open(POLICY_FILE, 'r') as fpol:
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
        # read attributes and policies from file POLICY_FILE
        allpolicies = []
        with open(POLICY_FILE, 'r') as fpol:
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
        # read attributes and policies from file POLICY_FILE
        allpolicies = []
        with open(POLICY_FILE, 'r') as fpol:
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
        # read attributes and policies from file POLICY_FILE
        allpolicies = []
        with open(POLICY_FILE, 'r') as fpol:
            allpolicies = fpol.read().splitlines()
        fpol.closed
        
        # check if policy already exists
        if self.txtAtomicPolicy.GetLabel() in allpolicies:
            wx.MessageBox("La policy che si sta cercando di aggiungere " + \
                          "e' gia' presente nell'elenco.", 
                          "Errore", wx.OK | wx.ICON_ERROR)
        else:
            with open(POLICY_FILE, 'a') as fpol:
                fpol.write(self.txtAtomicPolicy.GetLabel() + "\n")
            fpol.closed
            wx.MessageBox("Policy aggiunta correttamente") 

    def OnEnd(self, event):
        self.Destroy()

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

# MAIN 
#mandatory in wx, create an app, False stands for not rederiction stdin/stdout
#refer manual for details
app = wx.App(False)


#create an object of CPABE
frame = CPABE(None)

frame.SetIcon(wx.Icon(TELSY_LOGO_ICO, wx.BITMAP_TYPE_ICO))


#show the frame
frame.Show(True)

#start the applications
app.MainLoop()


