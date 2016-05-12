#importing wx files
import wx
 
#import the newly created GUI file
import cpabe_gui
 
# import other libraries
import os
import glob

from subprocess import call

from cpabe_def import *

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
                            os.getcwd(), "", "*.k", wx.OPEN)
        dlg.SetDirectory(os.getcwd() + LOCAL_AUTH_MASTER_KEY_FOLDER)
        if dlg.ShowModal() == wx.ID_OK:
            self.mkpath = dlg.GetPath()
            self.lblMKName.SetLabel(self.mkpath)
        dlg.Destroy()

    def OnChoosePK(self, event):
        dlg = wx.FileDialog(self, "Scegli una chiave pubblica", 
                            os.getcwd(), "", "*.k", wx.OPEN)
        dlg.SetDirectory(os.getcwd() + LOCAL_PUBLIC_KEY_FOLDER)
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

        self.grouppath = "." + LOCAL_PUBLIC_KEY_FOLDER + "/" + self.curve + ".g"
        self.skpath = "." + LOCAL_AUTH_SECRET_KEY_FOLDER + "/" + \
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
        self.group_folder = "." + LOCAL_PUBLIC_KEY_FOLDER
        self.mkname = self.txtMK.GetValue()
        self.mkpath = "." + LOCAL_AUTH_MASTER_KEY_FOLDER + "/" + self.mkname + ".k"
        self.pkname = self.txtPK.GetValue()
        self.pkpath = "." + LOCAL_PUBLIC_KEY_FOLDER + "/" + self.pkname + ".k"

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

class pnlUsrCPABE(cpabe_gui.pnlClientCPABE):
    #viewfile = "/home/ema/Dropbox/ACCADEMIC/Python/wxPython/cpabe/"

    def __init__(self, parent):
        cpabe_gui.pnlClientCPABE.__init__(self,parent)

        # Connect Events
        self.btnEnc.Bind( wx.EVT_BUTTON, self.OnEncrypt )
        self.btnDec.Bind( wx.EVT_BUTTON, self.OnDecrypt )
        self.btnViewFile.Bind( wx.EVT_BUTTON, self.OnViewFile )
        self.btnUpdate.Bind( wx.EVT_BUTTON, self.OnUpdate )

    # -----------------------------------------------------------
    # function definitions

    def OnEncrypt(self, event):
        dlg = DialogEncrypt(self)
        dlg.ShowModal()
        dlg.Destroy()

    def OnDecrypt(self, event):
        dlg = DialogDecrypt(self)
        dlg.ShowModal()
        dlg.Destroy()

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
        for fname in os.listdir(os.getcwd() + LOCAL_USER_FOLDER + "/" + \
                                self.lblUserName.GetLabel() + \
                                LOCAL_USER_ABE_KEY):
            if fname.endswith(".k"):
                self.lstSK.Append(fname)

        self.lstFile.Clear()
        for fname in os.listdir(os.getcwd() + LOCAL_USER_FOLDER + "/" + \
                                self.lblUserName.GetLabel() + \
                                LOCAL_USER_PLAINTEXT):
            #if fname.endswith(".k"):
            self.lstFile.Append(fname)

        self.lstEncFile.Clear()
        for fname in os.listdir(os.getcwd() + LOCAL_USER_FOLDER + "/" + \
                                self.lblUserName.GetLabel() + \
                                LOCAL_USER_CIPHERTEXT):
            #if fname.endswith(".k"):
            self.lstEncFile.Append(fname)

    def OnViewFile(self, event):
        openFileDialog = wx.FileDialog(self, "Open file", os.getcwd(), "",
                                       "*.*", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed idea...

        # proceed loading the file chosen by the user
        # this can be done with e.g. wxPython input streams:
        #input_stream = wx.FileInputStream(openFileDialog.GetPath())
        input_stream = os.startfile(openFileDialog.GetPath())
        if not input_stream.IsOk():

            wx.LogError("Cannot open file '%s'."%openFileDialog.GetPath())
            return
        """
        dlg = wx.FileDialog(self, "Scegli un file",  os.getcwd(), "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filepath = dlg.GetPath()
            self.filename = dlg.GetFilename()
            self.encfile = self.encfile + self.filename + ".enc"

            self.lblFileName.SetLabel(self.filepath)
        dlg.Destroy()
        """

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
            self.pnlusr.Show()
            self.Show()

        elif self.dlg.logged_in_auth:
            # load user panel
            self.pnlauth.SetBackgroundColour(wx.GREEN)
            #pnl.lblUserName.SetLabel(dlg.txtUsr.GetValue()) 
            self.pnlauth.Show()
            self.Show()

        else:
            self.Close()

    def OnLogInOut(self, event):
        self.Login()
        if self.dlg.logged_in_usr:
            self.pnlusr.Show()
            self.pnlauth.Hide()
        elif self.dlg.logged_in_auth:
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

#inherit from the dlgEncrypt created in wxFowmBuilder and create DialogEncrypt
class DialogEncrypt(cpabe_gui.dlgEncrypt):
    #constructor
    def __init__(self,parent):
        #initialize parent class
        cpabe_gui.dlgEncrypt.__init__(self,parent)

        # -----------------------------------------------------------
        # dialog variables definitions
        self.seclev = "" # security level
        self.filepath = "" # file name and path
        self.filename = "" # only file name
        self.encfilepath = "" # encryopted file name and path
        self.grouppath = "" # group name and path
        self.pkpath = "" # public key name and path
        self.username = self.GetParent().lblUserName.GetLabel()
        self.userfolder = LOCAL_USER_FOLDER + "/" + self.username # ciphertext folder
        self.policy = "" # policy
        self.encsymkpath = "" # encrypted symmetric key name and path
        self.symkpath = os.getcwd() + self.userfolder + \
                        LOCAL_USER_AES_KEY + "/symmetric.k" # symmetric key name and path
        self.metapath = "" # metadata file name and path

        # read attributes and policies from file POLICY_FILE
        allpolicies = []
        with open(POLICY_FILE, 'r') as fpol:
            #allpolicies = fpol.readlines()
            allpolicies = fpol.read().splitlines()
        fpol.closed
        
        for temp in allpolicies:
            self.chcShowPolicies.Append(temp)

        # Connect Events
        self.chcSecLev.Bind( wx.EVT_CHOICE, self.OnChooseSecLev )
        self.btnChooseFile.Bind( wx.EVT_BUTTON, self.OnChooseFile )
        #self.btnChooseGroup.Bind( wx.EVT_BUTTON, self.OnChooseGroup )
        self.btnChoosePK.Bind( wx.EVT_BUTTON, self.OnChoosePK )
        self.btnCreatePolicy.Bind( wx.EVT_BUTTON, self.OnCreatePolicy )
        self.chcShowPolicies.Bind( wx.EVT_CHOICE, self.OnSelectPolicy )
        self.btnEncrypt.Bind( wx.EVT_BUTTON, self.OnEncrypt )

    # -----------------------------------------------------------
    # methods definitions

    def OnChooseFile(self, event):
        dlg = wx.FileDialog(self, "Scegli un file",  
                            os.getcwd(), "", "*.*", wx.OPEN)
        dlg.SetDirectory(os.getcwd() + self.userfolder + LOCAL_USER_PLAINTEXT)
        if dlg.ShowModal() == wx.ID_OK:
            self.filepath = dlg.GetPath()
            self.filename = dlg.GetFilename()
            self.lblFileName.SetLabel(self.filepath)
        dlg.Destroy()

    def OnChooseSecLev(self, event):
        s = self.chcSecLev.GetStringSelection()
        if s == u"selezionare":
            self.seclev = ""
            self.groupname = ""
        else:
            s = s.split(":")
            self.seclev = s[0]
            self.groupname = s[1]
            self.grouppath = os.getcwd() + LOCAL_PUBLIC_KEY_FOLDER + "/" + \
                             self.groupname + ".g"

    def OnChoosePK(self, event):
        dlg = wx.FileDialog(self, "Scegli una chiave pubblica", 
                            os.getcwd(), "", "*.k", wx.OPEN)
        dlg.SetDirectory(os.getcwd() + LOCAL_PUBLIC_KEY_FOLDER)
        if dlg.ShowModal() == wx.ID_OK:
            self.pkpath = dlg.GetPath()
            self.lblPKName.SetLabel(self.pkpath)
        dlg.Destroy()

    """
    def OnChooseGroup(self, event):
        dlg = wx.FileDialog(self, "Scegli una gruppo", 
                            os.getcwd(), "", "*.g", wx.OPEN)
        dlg.SetDirectory(os.getcwd() + LOCAL_PUBLIC_KEY_FOLDER)
        if dlg.ShowModal() == wx.ID_OK:
            self.grouppath = dlg.GetPath()
            self.lblGroupName.SetLabel(self.grouppath)
        dlg.Destroy()
    """

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
        #self.seclev = self.chcSecLev.GetStringSelection()
        self.policy = self.lblShowPolicy.GetLabel()
 
        # check policy
        # ...

        # INPUT checks
        if self.seclev == u"selezionare" or self.seclev == "":
            wx.MessageBox("Livello di sicurezza NON selezionato.", "Errore", 
                          wx.OK | wx.ICON_ERROR)
        elif self.filepath == "":
            wx.MessageBox("Nessun file da cifrare selezionato.", "Errore", 
                          wx.OK | wx.ICON_ERROR)
        elif self.pkpath == "":
            wx.MessageBox("Nessuna chiave pubblica selezionata.", "Errore", 
                          wx.OK | wx.ICON_ERROR)
        elif self.policy == u"Nessuna policy creata":
            wx.MessageBox("Nessuna policy inserita.", "Errore", 
                          wx.OK | wx.ICON_ERROR)
        # ENCRYPT
        else:
            # 0 - generate random symmetric key

            call(["python3", "abe-random-ec-point.py", 
                  self.grouppath, self.symkpath
                ])

            # 1 - encrypt symmetric key with policy
            # python3 abe-encrypt.py '((ATTR1 or ATTR2) and (ATTR3 or ATTR4))'
            self.encsymkpath = os.getcwd() + self.userfolder + \
                               LOCAL_USER_CIPHERTEXT + "/" + self.filename + ".k.enc"
            self.encfilepath = os.getcwd() + self.userfolder + \
                               LOCAL_USER_CIPHERTEXT + "/" + self.filename + ".enc"
            self.metapath = os.getcwd() + self.userfolder + \
                               LOCAL_USER_CIPHERTEXT + "/" + self.filename + ".meta"

            call(["python3", "abe-encrypt.py", self.grouppath, self.pkpath, self.policy, 
                  self.symkpath, self.encsymkpath])
            
            # remove the symmetric key
            # call(["rm", self.userfolder + "secret_keys/" + "symmetric.k"])

            # 2 - encrypt file with symmetric key
            # python3 aescrypt.py -f prova.txt
            call(["python3", "aescrypt.py", "-f", 
                  self.filepath, self.encfilepath, self.symkpath])

            # 3 - add metadata to encrypted file
            with open(self.metapath, "w") as f:
                f.write("UTENTE:" + self.username + "\n" + \
                        "SECLEV:" + self.seclev + "\n" + \
                        "GROUPPATH:" + self.grouppath + "\n" + \
                        "PKPATH:" + self.pkpath + "\n" + \
                        "POLICY:" + self.policy
                       )


            wx.MessageBox("Cifratura eseguita correttamente.\n\n" + 
                          "File:\n\n" + self.filepath + "\n\n" +
                          "Livello di sicurezza:\n\n" +  self.seclev + "\n\n" 
                          "Gruppo:\n\n" +  self.groupname + "\n\n" 
                          "Chiave pubblica:\n\n" + self.pkpath + "\n\n" + 
                          "Policy:\n\n" + self.policy + "\n\n"
                         )

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

#inherit from the dlgEncrypt created in wxFowmBuilder and create DialogEncrypt
class DialogDecrypt(cpabe_gui.dlgDecrypt):
    #constructor
    def __init__(self, parent):
        #initialize parent class
        cpabe_gui.dlgDecrypt.__init__(self, parent)

        # -----------------------------------------------------------
        # dialog variables definitions
        # dialog variables definitions
        self.filepath = "" # file name and path
        self.filename = "" # only file name
        self.decfilepath = "" # decrypted file name and path
        self.grouppath = "" # group name and path
        self.pkpath = "" # public key name and path
        self.skpath = "" # secret key name and path
        self.username = self.GetParent().lblUserName.GetLabel()
        self.userfolder = LOCAL_USER_FOLDER + "/" + self.username # ciphertext folder
        self.encsymkpath = "" # encrypted symmetric key and path
        self.metapath = "" # metadata name and path
        self.symkpath = os.getcwd() + self.userfolder + \
                        LOCAL_USER_AES_KEY + "/symmetric.k" # symmetric key name and path

        # Connect Events
        self.btnChooseFile.Bind( wx.EVT_BUTTON, self.OnChooseFile )
        self.btnChoosePK.Bind( wx.EVT_BUTTON, self.OnChoosePK )
        self.btnChooseSK.Bind( wx.EVT_BUTTON, self.OnChooseSK )
        self.btnDecrypt.Bind( wx.EVT_BUTTON, self.OnDecrypt )

    # -----------------------------------------------------------
    # methods definitions

    def OnChooseFile(self, event):
        dlg = wx.FileDialog(self, "Scegli un file",  os.getcwd(), "", "*.*", wx.OPEN)
        dlg.SetDirectory(os.getcwd() + self.userfolder + LOCAL_USER_CIPHERTEXT)
        if dlg.ShowModal() == wx.ID_OK:
            self.filepath = dlg.GetPath()
            self.filename = dlg.GetFilename() 
            # remove .enc extension
            self.filename = self.filename[0:len(self.filename)-4]

            self.metapath = os.getcwd() + self.userfolder + \
                               LOCAL_USER_CIPHERTEXT + "/" + self.filename + ".meta"

            self.encsymkpath = os.getcwd() + self.userfolder + \
                               LOCAL_USER_CIPHERTEXT + "/" + self.filename + ".k.enc"
            self.decfilepath = os.getcwd() + self.userfolder + \
                               LOCAL_USER_PLAINTEXT + "/" + self.filename

            if not os.path.exists(self.metapath):   
                self.filepath = ""
                self.lblFileName.SetLabel("Nessuna selezione effettuata...")
                wx.MessageBox("Il file contenente i metadati non esiste!\n" + \
                              "NON e' possibile decifrare questo file",
                              "Attenzione", wx.OK | wx.ICON_EXCLAMATION)
            if not os.path.exists(self.encsymkpath):   
                self.filepath = ""
                self.lblFileName.SetLabel("Nessuna selezione effettuata...")
                wx.MessageBox("Il file contenente " +\
                              "la password AES cifrata non esiste!\n" + \
                              "NON e' possibile decifrare questo file",
                              "Attenzione", wx.OK | wx.ICON_EXCLAMATION)
            if os.path.exists(self.metapath) and \
               os.path.exists(self.encsymkpath):
                self.lblFileName.SetLabel(self.filepath)

        dlg.Destroy()

    def OnChoosePK(self, event):
        dlg = wx.FileDialog(self, "Scegli una chiave pubblica", 
                            os.getcwd(), "", "*.k", wx.OPEN)
        dlg.SetDirectory(os.getcwd() + LOCAL_PUBLIC_KEY_FOLDER)
        if dlg.ShowModal() == wx.ID_OK:
            self.pkpath = dlg.GetPath()
            self.lblPKName.SetLabel(self.pkpath)
        dlg.Destroy()

    def OnChooseGroup(self, event):
        dlg = wx.FileDialog(self, "Scegli una gruppo", 
                            os.getcwd(), "", "*.g", wx.OPEN)
        dlg.SetDirectory(os.getcwd() + LOCAL_PUBLIC_KEY_FOLDER)
        if dlg.ShowModal() == wx.ID_OK:
            self.grouppath = dlg.GetPath()
            self.lblGroupName.SetLabel(self.grouppath)
        dlg.Destroy()

    def OnChooseSK(self, event):
        dlg = wx.FileDialog(self, "Scegli una chiave segreta", 
                            os.getcwd(), "", "*.k", wx.OPEN)
        dlg.SetDirectory(os.getcwd() + self.userfolder + LOCAL_USER_ABE_KEY)
        if dlg.ShowModal() == wx.ID_OK:
            self.skpath = dlg.GetPath()
            self.lblSKName.SetLabel(self.skpath)
        dlg.Destroy()

    def OnDecrypt(self, event):

        # INPUT checks
        if self.filepath == "":
            wx.MessageBox("Nessun file da decifrare selezionato.", 
                          "Errore", wx.OK | wx.ICON_ERROR)
        elif self.pkpath == "":
            wx.MessageBox("Nessuna chiave pubblica selezionata.", 
                          "Errore", wx.OK | wx.ICON_ERROR)
        elif self.skpath == "":
            wx.MessageBox("Nessuna chiave segreta selezionata.", 
                          "Errore", wx.OK | wx.ICON_ERROR)
        # DECRYPT
        else:
            # 0 - extract METADATA
            with open(self.metapath, "r") as f:
                s = f.read()
            usr = s.split("\n")[0].split(":")[1]
            seclev = s.split("\n")[1].split(":")[1]
            self.grouppath = s.split("\n")[2].split(":")[1]
            self.pkpath = s.split("\n")[3].split(":")[1]
            policy = s.split("\n")[4].split(":")[1]

            # 1 - ABE decrypt

            call(["python3", "abe-decrypt.py", self.grouppath, self.pkpath,
                  self.skpath, self.encsymkpath, self.symkpath
                ])
            
            with open(self.symkpath, "rb") as f:
                s = f.read()
            
            if s == b"USER_KEY_DOES_NOT_SATISFY_POLICY":
                wx.MessageBox("Gli attributi associati " + \
                              "alla chiave segreta selezionata" + \
                              "non soddisfano la policy", 
                              "Errore", wx.OK | wx.ICON_ERROR
                             )
            else:
                # 2 - AES decrypt
                call(["python3", "aescrypt.py", "-d", "-f", self.filepath,
                      self.decfilepath, self.symkpath
                    ])

                wx.MessageBox("Decifratura eseguita correttamente.\n\n" + 
                              "File decifrato:\n\n" + self.filepath + "\n\n"
                             )


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


