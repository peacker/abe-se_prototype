#importing wx files
import wx
 
#import the newly created GUI file
import cpabe_gui
 
# import other libraries
import os
from subprocess import call

class pnlCPABE(cpabe_gui.pnlClientCPABE):
    viewfile = "/home/ema/Dropbox/ACCADEMIC/Python/wxPython/cpabe/"

    def __init__(self, parent):
        cpabe_gui.pnlClientCPABE.__init__(self,parent)

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

# -----------------------------------------------------------

#inherit from the CpAbeFrame created in wxFowmBuilder and create CPABE
class CPABE(cpabe_gui.CpAbeFrame):

    #constructor
    def __init__(self,parent):
        #initialize parent class
        cpabe_gui.CpAbeFrame.__init__(self,parent)
        pnl = pnlCPABE(self)
        pnl.SetBackgroundColour(wx.BLACK)

    # -----------------------------------------------------------
    # function definitions

    def OnClose(self,event):
        self.Destroy()

    def OnInfo(self, event):
        description = "Client per cifratura e decifratura con tecnologia " + \
                      "Ciphertext-policy Attribute-Based Encryption (CPABE)" + \
                      " + Advance Encryption Standard (AES) Encryption."
        licence = "Diritti appartenenti a " + \
                  "Telsy Elettronica e Comunicazioni S.p.A."

        info = wx.AboutDialogInfo()
        info.SetIcon(wx.Icon("telsy_logo.png", wx.BITMAP_TYPE_PNG))
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

# -----------------------------------------------------------

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
        self.pkpath = "" # public key name and path
        self.pkname = "" # only public key name
        self.username = self.GetParent().lblUserName.GetLabel()
        self.userfolder = "/users/" + self.username # ciphertext folder
        self.policy = "" # policy
        #self.encfile = "users/" + self.username + "/plaintexts/" # name of the un-encrypted file

        # read attributes and policies from file policies.txt
        allpolicies = []
        with open('policies.txt', 'r') as fpol:
            #allpolicies = fpol.readlines()
            allpolicies = fpol.read().splitlines()
        fpol.closed
        
        for temp in allpolicies:
            self.chcShowPolicies.Append(temp)

    # -----------------------------------------------------------
    # methods definitions

    def OnChooseFile(self, event):
        dlg = wx.FileDialog(self, "Scegli un file",  
                            os.getcwd(), "", "*.*", wx.OPEN)
        dlg.SetDirectory(os.getcwd() + self.userfolder + "/plaintexts")
        if dlg.ShowModal() == wx.ID_OK:
            self.filepath = dlg.GetPath()
            self.filename = dlg.GetFilename()
            #self.encfile = self.encfile + self.filename + ".enc"

            self.lblFileName.SetLabel(self.filepath)
        dlg.Destroy()

    def OnChoosePK(self, event):
        dlg = wx.FileDialog(self, "Scegli una chiave pubblica", 
                            os.getcwd(), "", "*.k", wx.OPEN)
        dlg.SetDirectory(os.getcwd() + "/public_parameters")
        if dlg.ShowModal() == wx.ID_OK:
            self.pkpath = dlg.GetPath()
            self.pkname = dlg.GetFilename()
            self.lblPKName.SetLabel(self.pkpath)
        dlg.Destroy()

    def OnCreatePolicy(self, event):
        dlg = DialogCreatePolicy(self)

        dlg.ShowModal()

        # update policies list
        allpolicies = []
        with open('policies.txt', 'r') as fpol:
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
        self.seclev = self.chcSecLev.GetStringSelection()
        self.policy = self.lblShowPolicy.GetLabel()
 
        # check policy
        # ...

        # INPUT checks
        if self.seclev == u"selezionare":
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
            # 1 - encrypt symmetric key with policy
            # python3 abe-encrypt.py '((ATTR1 or ATTR2) and (ATTR3 or ATTR4))'
            call(["python3", "abe-encrypt.py", self.pkname, self.policy, 
                  self.username])
            
            # copy symmetric.k.enc in encrypted_files/ folder
            call(["mv", 
                  os.getcwd() + self.userfolder + 
                    "/secret_keys/AES_sk/symmetric.k.enc", 
                  os.getcwd() + self.userfolder + 
                    "/ciphertexts/" + self.filename + ".k.enc"])
            # mv /users/utente1/secret_keys/symmetric.k.enc /users/utente1/ciphertexts/prova3.txt.k.enc
            
            # remove the symmetric key
            # call(["rm", self.userfolder + "secret_keys/" + "symmetric.k"])

            # 2 - encrypt file with symmetric key
            # python3 aescrypt.py -f prova.txt
            call(["python3", "aescrypt.py", "-f", self.filename, 
                  "symmetric.k", self.username])

            wx.MessageBox("Cifratura eseguita correttamente.\n\n" + 
                          "File:\n\n" + self.filepath + "\n\n" +
                          "Livello di sicurezza:\n\n" +  self.seclev + "\n\n" 
                          "Chiave pubblica:\n\n" + self.pkpath + "\n\n" + 
                          "Policy:\n\n" + self.policy + "\n\n"
                         )

# -----------------------------------------------------------

#inherit from the dlgEncrypt created in wxFowmBuilder and create DialogEncrypt
class DialogCreatePolicy(cpabe_gui.dlgCreatePolicy):
    #constructor
    def __init__(self,parent):
        #initialize parent class
        cpabe_gui.dlgCreatePolicy.__init__(self,parent)

        # read attributes and policies from file policies.txt
        allpolicies = []
        with open('policies.txt', 'r') as fpol:
            #allpolicies = fpol.readlines()
            allpolicies = fpol.read().splitlines()
        fpol.closed
                
    def OnAnd(self, event):
        # read attributes and policies from file policies.txt
        allpolicies = []
        with open('policies.txt', 'r') as fpol:
            allpolicies = fpol.read().splitlines()
        fpol.closed

        dlg = wx.MultiChoiceDialog( self, 
                                   "Scegli gli input",
                                   "Crea Formula con And", allpolicies)
 
        if (dlg.ShowModal() == wx.ID_OK):
            selections = dlg.GetSelections()
            if len(selections) == 1:
                wx.MessageBox("Selezionare almeno due elementi.", "Errore", wx.OK | wx.ICON_ERROR)
            else:
                atomic_policy = ""
                for i in range(len(selections)-1):
                    atomic_policy = atomic_policy + "(" + allpolicies[selections[i]] + ")" + " and " 
                atomic_policy = atomic_policy + "(" + allpolicies[selections[len(selections)-1]] + ")" + "" 

                self.txtAtomicPolicy.SetLabel(atomic_policy)

        dlg.Destroy()
            
    def OnOr(self, event):
        # read attributes and policies from file policies.txt
        allpolicies = []
        with open('policies.txt', 'r') as fpol:
            allpolicies = fpol.read().splitlines()
        fpol.closed

        dlg = wx.MultiChoiceDialog( self, 
                                   "Scegli gli input",
                                   "Crea Formula con Or", allpolicies)
 
        if (dlg.ShowModal() == wx.ID_OK):
            selections = dlg.GetSelections()
            if len(selections) == 1:
                wx.MessageBox("Selezionare almeno due elementi.", "Errore", wx.OK | wx.ICON_ERROR)
            else:
                atomic_policy = ""
                for i in range(len(selections)-1):
                    atomic_policy = atomic_policy + "(" + allpolicies[selections[i]] + ")" + " or " 
                atomic_policy = atomic_policy + "(" + allpolicies[selections[len(selections)-1]] + ")" + "" 

                self.txtAtomicPolicy.SetLabel(atomic_policy)

        dlg.Destroy()

    def OnNot(self, event):
        # read attributes and policies from file policies.txt
        allpolicies = []
        with open('policies.txt', 'r') as fpol:
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
        # read attributes and policies from file policies.txt
        allpolicies = []
        with open('policies.txt', 'r') as fpol:
            allpolicies = fpol.read().splitlines()
        fpol.closed
        
        # check if policy already exists
        if self.txtAtomicPolicy.GetLabel() in allpolicies:
            wx.MessageBox("La policy che si sta cercando di aggiungere e' gia' presente nell'elenco.", 
                          "Errore", wx.OK | wx.ICON_ERROR)
        else:
            with open('policies.txt', 'a') as fpol:
                fpol.write(self.txtAtomicPolicy.GetLabel() + "\n")
            fpol.closed
            wx.MessageBox("Policy aggiunta correttamente") #, "Messaggio", wx.OK | wx.ICON_INFORMATION

    def OnEnd(self, event):
        self.Destroy()

# -----------------------------------------------------------

#inherit from the dlgEncrypt created in wxFowmBuilder and create DialogEncrypt
class DialogDecrypt(cpabe_gui.dlgDecrypt):
    #constructor
    def __init__(self, parent):
        #initialize parent class
        cpabe_gui.dlgDecrypt.__init__(self, parent)

        # -----------------------------------------------------------
        # dialog variables definitions
        self.filepath = "" # file name and path
        self.filename = "" # only file name
        self.pkpath = "" # public key name and path
        self.pkname = "" # only public key name
        self.skpath = "" # secret key name and path
        self.skname = "" # only secret key name
        self.username = self.GetParent().lblUserName.GetLabel()
        self.userfolder = "/users/" + self.username # ciphertext folder

    # -----------------------------------------------------------
    # methods definitions

    def OnChooseFile(self, event):
        dlg = wx.FileDialog(self, "Scegli un file",  os.getcwd(), "", "*.*", wx.OPEN)
        dlg.SetDirectory(os.getcwd() + self.userfolder + "/ciphertexts")
        if dlg.ShowModal() == wx.ID_OK:
            self.filepath = dlg.GetPath()
            self.filename = dlg.GetFilename() 
            # remove .enc extension
            self.filename = self.filename[0:len(self.filename)-4]

            wx.MessageBox("trying to decrypt file: " + self.filename)

            self.lblFileName.SetLabel(self.filepath)
        dlg.Destroy()

    def OnChoosePK(self, event):
        dlg = wx.FileDialog(self, "Scegli una chiave pubblica", os.getcwd(), "", "*.k", wx.OPEN)
        dlg.SetDirectory(os.getcwd() + "/public_parameters")
        if dlg.ShowModal() == wx.ID_OK:
            self.pkpath = dlg.GetPath()
            self.pkname = dlg.GetFilename() 
            self.lblPKName.SetLabel(self.pkpath)
        dlg.Destroy()

    def OnChooseSK(self, event):
        dlg = wx.FileDialog(self, "Scegli una chiave segreta", os.getcwd(), "", "*.k", wx.OPEN)
        dlg.SetDirectory(os.getcwd() + self.userfolder + "/secret_keys/ABE_sk")
        if dlg.ShowModal() == wx.ID_OK:
            self.skpath = dlg.GetPath()
            self.skname = dlg.GetFilename() 
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
            # 1 - move files to decrypt 
            # ABE encrypted key
            # in folder ../users/utente/secret_keys/AES_sk/symmetric.k.enc
            call(["mv", 
                  os.getcwd() + self.userfolder + 
                    "/ciphertexts/" + self.filename + ".k.enc",
                  os.getcwd() + self.userfolder + 
                    "/secret_keys/AES_sk/symmetric.k.enc"])
            # encrypted file, in folder ../users/utente/plaintexts/
            call(["mv", 
                  os.getcwd() + self.userfolder + 
                    "/ciphertexts/" + self.filename + ".enc",
                  os.getcwd() + self.userfolder + 
                    "/plaintexts/" + self.filename + ".enc"])

            # 2 - decrypt the symmetric key with ABE decrypt
            call(["python3", "abe-decrypt.py", self.pkname, self.skname, 
                  self.filename + ".k.enc", self.username])

            # 3 - decrypt file with AES decrypt
            # 4 - clean folder


            # 1 - encrypt symmetric key with policy
            # python3 abe-encrypt.py '((ATTR1 or ATTR2) and (ATTR3 or ATTR4))'
            call(["python3", "abe-encrypt.py", self.pkname, self.policy, 
                  self.username])
            
            # copy symmetric.k.enc in encrypted_files/ folder
            call(["mv", 
                  os.getcwd() + self.userfolder + 
                    "/secret_keys/AES_sk/symmetric.k.enc", 
                  os.getcwd() + self.userfolder + 
                    "/ciphertexts/" + self.filename + ".k.enc"])
            # mv /users/utente1/secret_keys/symmetric.k.enc /users/utente1/ciphertexts/prova3.txt.k.enc
            
            # remove the symmetric key
            # call(["rm", self.userfolder + "secret_keys/" + "symmetric.k"])

            # 2 - encrypt file with symmetric key
            # python3 aescrypt.py -f prova.txt
            call(["python3", "aescrypt.py", "-f", self.filename, 
                  "symmetric.k", self.username])

            wx.MessageBox("Cifratura eseguita correttamente.\n\n" + 
                          "File:\n\n" + self.filepath + "\n\n" +
                          "Livello di sicurezza:\n\n" +  self.seclev + "\n\n" 
                          "Chiave pubblica:\n\n" + self.pkpath + "\n\n" + 
                          "Policy:\n\n" + self.policy + "\n\n"
                         )


# -----------------------------------------------------------
# MAIN 
#mandatory in wx, create an app, False stands for not rederiction stdin/stdout
#refer manual for details
app = wx.App(False)
 
#create an object of CPABE
frame = CPABE(None)
frame.SetIcon(wx.Icon("telsy_logo.ico", wx.BITMAP_TYPE_ICO))
#show the frame
frame.Show(True)
#start the applications
app.MainLoop()
