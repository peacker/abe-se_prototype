# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Nov 10 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class CpAbeFrame
###########################################################################

class CpAbeFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Dimostratore CPABE", pos = wx.DefaultPosition, size = wx.Size( 1000,900 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.statusBar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		self.m_menubar4 = wx.MenuBar( 0 )
		self.menuFile = wx.Menu()
		self.menuFileClose = wx.MenuItem( self.menuFile, wx.ID_ANY, u"Esci"+ u"\t" + u"Ctrl + q", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuFile.AppendItem( self.menuFileClose )
		
		self.m_menubar4.Append( self.menuFile, u"File" ) 
		
		self.menuHelp = wx.Menu()
		self.menuHelpInfo = wx.MenuItem( self.menuHelp, wx.ID_ANY, u"Info", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuHelp.AppendItem( self.menuHelpInfo )
		
		self.m_menubar4.Append( self.menuHelp, u"Aiuto" ) 
		
		self.SetMenuBar( self.m_menubar4 )
		
		self.m_toolBar1 = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY ) 
		self.btnLogout = wx.Button( self.m_toolBar1, wx.ID_ANY, u"Logout", wx.DefaultPosition, wx.DefaultSize, 0|wx.NO_BORDER|wx.NO_BORDER )
		self.btnLogout.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, True, wx.EmptyString ) )
		
		self.m_toolBar1.AddControl( self.btnLogout )
		self.m_toolBar1.Realize() 
		
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class pnlClientCPABE
###########################################################################

class pnlClientCPABE ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 583,786 ), style = wx.TAB_TRAVERSAL )
		
		self.SetFont( wx.Font( 11, 74, 90, 90, False, "Sans" ) )
		
		gbSizer9 = wx.GridBagSizer( 0, 0 )
		gbSizer9.SetFlexibleDirection( wx.BOTH )
		gbSizer9.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText39 = wx.StaticText( self, wx.ID_ANY, u"Nome utente:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText39.Wrap( -1 )
		gbSizer9.Add( self.m_staticText39, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.lblUserName = wx.StaticText( self, wx.ID_ANY, u"NO_USER", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblUserName.Wrap( -1 )
		self.lblUserName.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		gbSizer9.Add( self.lblUserName, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.ntbFunc = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.pnlEncrypt = wx.Panel( self.ntbFunc, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer11 = wx.GridBagSizer( 10, 10 )
		gbSizer11.SetFlexibleDirection( wx.BOTH )
		gbSizer11.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.lblFileToEncrypt = wx.StaticText( self.pnlEncrypt, wx.ID_ANY, u"Scegli un file da cifrare:", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
		self.lblFileToEncrypt.Wrap( -1 )
		gbSizer11.Add( self.lblFileToEncrypt, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		bSizer35 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btnChooseFileToEncrypt = wx.Button( self.pnlEncrypt, wx.ID_ANY, u"File...", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer35.Add( self.btnChooseFileToEncrypt, 0, wx.ALL, 5 )
		
		self.lblFileToEncryptName = wx.StaticText( self.pnlEncrypt, wx.ID_ANY, u"Nessuna selezione effettuata...", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblFileToEncryptName.Wrap( -1 )
		bSizer35.Add( self.lblFileToEncryptName, 0, wx.ALL, 5 )
		
		
		gbSizer11.Add( bSizer35, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )
		
		self.lblPolicy = wx.StaticText( self.pnlEncrypt, wx.ID_ANY, u"Crea una policy:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblPolicy.Wrap( -1 )
		gbSizer11.Add( self.lblPolicy, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.lblShowPolicy = wx.StaticText( self.pnlEncrypt, wx.ID_ANY, u"Nessuna policy creata", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblShowPolicy.Wrap( -1 )
		gbSizer11.Add( self.lblShowPolicy, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
		
		bSizer38 = wx.BoxSizer( wx.VERTICAL )
		
		self.btnCreatePolicy = wx.Button( self.pnlEncrypt, wx.ID_ANY, u"Crea", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer38.Add( self.btnCreatePolicy, 0, wx.ALL, 5 )
		
		chcShowPoliciesChoices = [ u"Seleziona esistente" ]
		self.chcShowPolicies = wx.Choice( self.pnlEncrypt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 200,-1 ), chcShowPoliciesChoices, 0 )
		self.chcShowPolicies.SetSelection( 0 )
		self.chcShowPolicies.SetFont( wx.Font( 11, 74, 90, 90, False, "Sans" ) )
		
		bSizer38.Add( self.chcShowPolicies, 0, wx.ALL, 5 )
		
		
		gbSizer11.Add( bSizer38, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )
		
		self.m_staticline3 = wx.StaticLine( self.pnlEncrypt, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer11.Add( self.m_staticline3, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND|wx.ALL, 5 )
		
		self.btnEncrypt = wx.Button( self.pnlEncrypt, wx.ID_ANY, u"Cifra", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer11.Add( self.btnEncrypt, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )
		
		
		self.pnlEncrypt.SetSizer( gbSizer11 )
		self.pnlEncrypt.Layout()
		gbSizer11.Fit( self.pnlEncrypt )
		self.ntbFunc.AddPage( self.pnlEncrypt, u"Cifra", True )
		self.pnlDecrypt = wx.Panel( self.ntbFunc, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer12 = wx.GridBagSizer( 10, 10 )
		gbSizer12.SetFlexibleDirection( wx.BOTH )
		gbSizer12.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.lblFileToDecrypt = wx.StaticText( self.pnlDecrypt, wx.ID_ANY, u"Scegli un file da decifrare:", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
		self.lblFileToDecrypt.Wrap( -1 )
		gbSizer12.Add( self.lblFileToDecrypt, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		bSizer47 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btnChooseFileToDecrypt = wx.Button( self.pnlDecrypt, wx.ID_ANY, u"File...", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer47.Add( self.btnChooseFileToDecrypt, 0, wx.ALL, 5 )
		
		self.lblFileToDecryptName = wx.StaticText( self.pnlDecrypt, wx.ID_ANY, u"Nessuna selezione effettuata...", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblFileToDecryptName.Wrap( -1 )
		bSizer47.Add( self.lblFileToDecryptName, 0, wx.ALL, 5 )
		
		
		gbSizer12.Add( bSizer47, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )
		
		self.lstEncFilesData = wx.ListCtrl( self.pnlDecrypt, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		gbSizer12.Add( self.lstEncFilesData, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )
		
		self.btnUpdateFileTable = wx.Button( self.pnlDecrypt, wx.ID_ANY, u"Aggiorna", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer12.Add( self.btnUpdateFileTable, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.m_staticline31 = wx.StaticLine( self.pnlDecrypt, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer12.Add( self.m_staticline31, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND|wx.ALL, 5 )
		
		self.btnDecrypt = wx.Button( self.pnlDecrypt, wx.ID_ANY, u"Decifra", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		gbSizer12.Add( self.btnDecrypt, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )
		
		
		gbSizer12.AddGrowableCol( 1 )
		gbSizer12.AddGrowableRow( 3 )
		
		self.pnlDecrypt.SetSizer( gbSizer12 )
		self.pnlDecrypt.Layout()
		gbSizer12.Fit( self.pnlDecrypt )
		self.ntbFunc.AddPage( self.pnlDecrypt, u"Decifra", False )
		self.pnlCloud = wx.Panel( self.ntbFunc, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer121 = wx.GridBagSizer( 10, 10 )
		gbSizer121.SetFlexibleDirection( wx.BOTH )
		gbSizer121.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.lblFileToUpload = wx.StaticText( self.pnlCloud, wx.ID_ANY, u"Scegli un file da caricare nel cloud:", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
		self.lblFileToUpload.Wrap( -1 )
		gbSizer121.Add( self.lblFileToUpload, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText461 = wx.StaticText( self.pnlCloud, wx.ID_ANY, u"Aggiungi parole chiave:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText461.Wrap( -1 )
		gbSizer121.Add( self.m_staticText461, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.txtKeywords = wx.TextCtrl( self.pnlCloud, wx.ID_ANY, u"parola1, parola2, parola3", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer121.Add( self.txtKeywords, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )
		
		bSizer471 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btnChooseFileToUpload = wx.Button( self.pnlCloud, wx.ID_ANY, u"File...", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer471.Add( self.btnChooseFileToUpload, 0, wx.ALL, 5 )
		
		self.lblFileToUploadName = wx.StaticText( self.pnlCloud, wx.ID_ANY, u"Nessuna selezione effettuata...", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblFileToUploadName.Wrap( -1 )
		bSizer471.Add( self.lblFileToUploadName, 0, wx.ALL, 5 )
		
		
		gbSizer121.Add( bSizer471, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )
		
		self.btnUpload = wx.Button( self.pnlCloud, wx.ID_ANY, u"Carica sul cloud", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer121.Add( self.btnUpload, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline14 = wx.StaticLine( self.pnlCloud, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer121.Add( self.m_staticline14, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText45 = wx.StaticText( self.pnlCloud, wx.ID_ANY, u"Contenuto cloud:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText45.Wrap( -1 )
		self.m_staticText45.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		gbSizer121.Add( self.m_staticText45, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.lstCloudEncFilesData = wx.ListCtrl( self.pnlCloud, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,200 ), wx.LC_REPORT )
		gbSizer121.Add( self.lstCloudEncFilesData, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )
		
		self.btnUpdateCloudFileTable = wx.Button( self.pnlCloud, wx.ID_ANY, u"Aggiorna", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer121.Add( self.btnUpdateCloudFileTable, wx.GBPosition( 7, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.m_staticText471 = wx.StaticText( self.pnlCloud, wx.ID_ANY, u"Filtra per parola chiave:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText471.Wrap( -1 )
		gbSizer121.Add( self.m_staticText471, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.txtSearchKeywords = wx.TextCtrl( self.pnlCloud, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer121.Add( self.txtSearchKeywords, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )
		
		self.btnDownload = wx.Button( self.pnlCloud, wx.ID_ANY, u"Scarica selezione in locale", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer121.Add( self.btnDownload, wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )
		
		
		gbSizer121.AddGrowableCol( 1 )
		gbSizer121.AddGrowableRow( 0 )
		gbSizer121.AddGrowableRow( 1 )
		
		self.pnlCloud.SetSizer( gbSizer121 )
		self.pnlCloud.Layout()
		gbSizer121.Fit( self.pnlCloud )
		self.ntbFunc.AddPage( self.pnlCloud, u"Trasferimento file", False )
		self.pnlViewFoldersContent = wx.Panel( self.ntbFunc, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer8 = wx.GridBagSizer( 0, 0 )
		gbSizer8.SetFlexibleDirection( wx.BOTH )
		gbSizer8.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText40 = wx.StaticText( self.pnlViewFoldersContent, wx.ID_ANY, u"Parametri pubblici", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText40.Wrap( -1 )
		gbSizer8.Add( self.m_staticText40, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText42 = wx.StaticText( self.pnlViewFoldersContent, wx.ID_ANY, u"Chiavi segrete", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText42.Wrap( -1 )
		gbSizer8.Add( self.m_staticText42, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText43 = wx.StaticText( self.pnlViewFoldersContent, wx.ID_ANY, u"File in chiaro", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText43.Wrap( -1 )
		gbSizer8.Add( self.m_staticText43, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText44 = wx.StaticText( self.pnlViewFoldersContent, wx.ID_ANY, u"File cifrati", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText44.Wrap( -1 )
		gbSizer8.Add( self.m_staticText44, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		lstPPChoices = []
		self.lstPP = wx.ListBox( self.pnlViewFoldersContent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, lstPPChoices, 0 )
		gbSizer8.Add( self.lstPP, wx.GBPosition( 1, 0 ), wx.GBSpan( 3, 1 ), wx.ALL|wx.EXPAND, 5 )
		
		lstSKChoices = []
		self.lstSK = wx.ListBox( self.pnlViewFoldersContent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, lstSKChoices, 0 )
		gbSizer8.Add( self.lstSK, wx.GBPosition( 1, 1 ), wx.GBSpan( 3, 1 ), wx.ALL|wx.EXPAND, 5 )
		
		lstFileChoices = []
		self.lstFile = wx.ListBox( self.pnlViewFoldersContent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, lstFileChoices, 0 )
		gbSizer8.Add( self.lstFile, wx.GBPosition( 1, 2 ), wx.GBSpan( 3, 1 ), wx.ALL|wx.EXPAND, 5 )
		
		lstEncFileChoices = []
		self.lstEncFile = wx.ListBox( self.pnlViewFoldersContent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, lstEncFileChoices, 0 )
		gbSizer8.Add( self.lstEncFile, wx.GBPosition( 1, 3 ), wx.GBSpan( 3, 1 ), wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline10 = wx.StaticLine( self.pnlViewFoldersContent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer8.Add( self.m_staticline10, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 4 ), wx.EXPAND |wx.ALL, 5 )
		
		self.btnUpdate = wx.Button( self.pnlViewFoldersContent, wx.ID_ANY, u"Aggiorna", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer8.Add( self.btnUpdate, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 4 ), wx.ALL|wx.EXPAND, 5 )
		
		
		gbSizer8.AddGrowableCol( 0 )
		gbSizer8.AddGrowableCol( 1 )
		gbSizer8.AddGrowableCol( 2 )
		gbSizer8.AddGrowableCol( 3 )
		gbSizer8.AddGrowableCol( 4 )
		gbSizer8.AddGrowableRow( 1 )
		gbSizer8.AddGrowableRow( 2 )
		gbSizer8.AddGrowableRow( 3 )
		
		self.pnlViewFoldersContent.SetSizer( gbSizer8 )
		self.pnlViewFoldersContent.Layout()
		gbSizer8.Fit( self.pnlViewFoldersContent )
		self.ntbFunc.AddPage( self.pnlViewFoldersContent, u"Visualizza contenuto cartelle", False )
		
		gbSizer9.Add( self.ntbFunc, wx.GBPosition( 3, 0 ), wx.GBSpan( 2, 2 ), wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer9.Add( self.m_staticline2, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND|wx.ALL, 5 )
		
		lstAttributesChoices = []
		self.lstAttributes = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, lstAttributesChoices, 0 )
		self.lstAttributes.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
		
		gbSizer9.Add( self.lstAttributes, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText401 = wx.StaticText( self, wx.ID_ANY, u"Attributi:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText401.Wrap( -1 )
		gbSizer9.Add( self.m_staticText401, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticline9 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer9.Add( self.m_staticline9, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )
		
		self.m_bitmap1 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"telsy_logo_20x20.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.Size( 20,20 ), 0 )
		gbSizer9.Add( self.m_bitmap1, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 2 ), wx.ALIGN_CENTER|wx.ALL, 5 )
		
		
		gbSizer9.AddGrowableCol( 1 )
		
		self.SetSizer( gbSizer9 )
		self.Layout()
	
	def __del__( self ):
		pass
	

###########################################################################
## Class pnlAuthorityCPABE
###########################################################################

class pnlAuthorityCPABE ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL )
		
		gbSizer5 = wx.GridBagSizer( 0, 0 )
		gbSizer5.SetFlexibleDirection( wx.BOTH )
		gbSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText30 = wx.StaticText( self, wx.ID_ANY, u"AUTHORITY", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText30.Wrap( -1 )
		self.m_staticText30.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		gbSizer5.Add( self.m_staticText30, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 2 ), wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticline10 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer5.Add( self.m_staticline10, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )
		
		self.m_notebook2 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.pnlSetup = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer10 = wx.GridBagSizer( 0, 0 )
		gbSizer10.SetFlexibleDirection( wx.BOTH )
		gbSizer10.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText31 = wx.StaticText( self.pnlSetup, wx.ID_ANY, u"Generazione Master/Public key:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )
		gbSizer10.Add( self.m_staticText31, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText301 = wx.StaticText( self.pnlSetup, wx.ID_ANY, u"Selezionare livello di sicurezza e curva:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText301.Wrap( -1 )
		gbSizer10.Add( self.m_staticText301, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		chcSecLevAndCurveChoices = []
		self.chcSecLevAndCurve = wx.Choice( self.pnlSetup, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chcSecLevAndCurveChoices, 0 )
		self.chcSecLevAndCurve.SetSelection( 0 )
		gbSizer10.Add( self.chcSecLevAndCurve, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.btnSetup = wx.Button( self.pnlSetup, wx.ID_ANY, u"Genera", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer10.Add( self.btnSetup, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )
		
		
		self.pnlSetup.SetSizer( gbSizer10 )
		self.pnlSetup.Layout()
		gbSizer10.Fit( self.pnlSetup )
		self.m_notebook2.AddPage( self.pnlSetup, u"Setup", True )
		self.pnlKeygen = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer11 = wx.GridBagSizer( 0, 0 )
		gbSizer11.SetFlexibleDirection( wx.BOTH )
		gbSizer11.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText45 = wx.StaticText( self.pnlKeygen, wx.ID_ANY, u"Nome utente:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText45.Wrap( -1 )
		gbSizer11.Add( self.m_staticText45, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.txtNewUser = wx.TextCtrl( self.pnlKeygen, wx.ID_ANY, u"nuovoutente", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.txtNewUser.SetMinSize( wx.Size( 400,-1 ) )
		
		gbSizer11.Add( self.txtNewUser, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
		
		self.m_staticText46 = wx.StaticText( self.pnlKeygen, wx.ID_ANY, u"Password:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText46.Wrap( -1 )
		gbSizer11.Add( self.m_staticText46, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.txtNewPassword = wx.TextCtrl( self.pnlKeygen, wx.ID_ANY, u"123", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtNewPassword.Enable( False )
		self.txtNewPassword.SetMinSize( wx.Size( 400,-1 ) )
		
		gbSizer11.Add( self.txtNewPassword, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
		
		self.btnGenUser = wx.Button( self.pnlKeygen, wx.ID_ANY, u"Crea Utente", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer11.Add( self.btnGenUser, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline111 = wx.StaticLine( self.pnlKeygen, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer11.Add( self.m_staticline111, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 3 ), wx.EXPAND |wx.ALL, 5 )
		
		chcChooseUserToDeleteChoices = []
		self.chcChooseUserToDelete = wx.Choice( self.pnlKeygen, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chcChooseUserToDeleteChoices, 0 )
		self.chcChooseUserToDelete.SetSelection( 0 )
		gbSizer11.Add( self.chcChooseUserToDelete, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )
		
		self.btnDeleteUser = wx.Button( self.pnlKeygen, wx.ID_ANY, u"Rimuovi Utente", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer11.Add( self.btnDeleteUser, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )
		
		
		self.pnlKeygen.SetSizer( gbSizer11 )
		self.pnlKeygen.Layout()
		gbSizer11.Fit( self.pnlKeygen )
		self.m_notebook2.AddPage( self.pnlKeygen, u"Gestione utenti", False )
		
		gbSizer5.Add( self.m_notebook2, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticline11 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer5.Add( self.m_staticline11, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )
		
		self.m_bitmap1 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"telsy_logo_20x20.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.Size( 20,20 ), 0 )
		gbSizer5.Add( self.m_bitmap1, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 2 ), wx.ALIGN_CENTER|wx.ALL, 5 )
		
		
		gbSizer5.AddGrowableCol( 1 )
		
		self.SetSizer( gbSizer5 )
		self.Layout()
		gbSizer5.Fit( self )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class dlgLogin
###########################################################################

class dlgLogin ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Login", pos = wx.DefaultPosition, size = wx.Size( 500,-1 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		gbSizer10 = wx.GridBagSizer( 0, 0 )
		gbSizer10.SetFlexibleDirection( wx.BOTH )
		gbSizer10.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText22 = wx.StaticText( self, wx.ID_ANY, u"Login UTENTE", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText22.Wrap( -1 )
		gbSizer10.Add( self.m_staticText22, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 2 ), wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText23 = wx.StaticText( self, wx.ID_ANY, u"Login AUTHORITY", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText23.Wrap( -1 )
		gbSizer10.Add( self.m_staticText23, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 2 ), wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText24 = wx.StaticText( self, wx.ID_ANY, u"Nome Utente:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText24.Wrap( -1 )
		gbSizer10.Add( self.m_staticText24, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		chcUsernameChoices = []
		self.chcUsername = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chcUsernameChoices, 0 )
		self.chcUsername.SetSelection( 0 )
		gbSizer10.Add( self.chcUsername, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticline7 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		gbSizer10.Add( self.m_staticline7, wx.GBPosition( 0, 2 ), wx.GBSpan( 4, 1 ), wx.EXPAND|wx.ALL, 5 )
		
		self.m_staticText25 = wx.StaticText( self, wx.ID_ANY, u"Password:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText25.Wrap( -1 )
		gbSizer10.Add( self.m_staticText25, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.txtUsrPwd = wx.TextCtrl( self, wx.ID_ANY, u"123", wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD )
		self.txtUsrPwd.SetMaxLength( 0 ) 
		gbSizer10.Add( self.txtUsrPwd, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText26 = wx.StaticText( self, wx.ID_ANY, u"Password:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText26.Wrap( -1 )
		gbSizer10.Add( self.m_staticText26, wx.GBPosition( 2, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.txtAuthPwd = wx.TextCtrl( self, wx.ID_ANY, u"123", wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD )
		self.txtAuthPwd.SetMaxLength( 0 ) 
		gbSizer10.Add( self.txtAuthPwd, wx.GBPosition( 2, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.btnUsrLogin = wx.Button( self, wx.ID_ANY, u"Login come UTENTE", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer10.Add( self.btnUsrLogin, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )
		
		self.btnAuthLogin = wx.Button( self, wx.ID_ANY, u"Login come AUTHORITY", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer10.Add( self.btnAuthLogin, wx.GBPosition( 3, 3 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( gbSizer10 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class dlgCreatePolicy
###########################################################################

class dlgCreatePolicy ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Crea Policy", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer39 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer40 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer41 = wx.BoxSizer( wx.VERTICAL )
		
		self.btnAnd = wx.Button( self, wx.ID_ANY, u"and", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer41.Add( self.btnAnd, 0, wx.ALL, 5 )
		
		
		bSizer40.Add( bSizer41, 1, wx.EXPAND, 5 )
		
		bSizer42 = wx.BoxSizer( wx.VERTICAL )
		
		self.btnOr = wx.Button( self, wx.ID_ANY, u"or", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer42.Add( self.btnOr, 0, wx.ALL, 5 )
		
		
		bSizer40.Add( bSizer42, 1, wx.EXPAND, 5 )
		
		bSizer43 = wx.BoxSizer( wx.VERTICAL )
		
		self.btnNot = wx.Button( self, wx.ID_ANY, u"not", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btnNot.Enable( False )
		
		bSizer43.Add( self.btnNot, 0, wx.ALL, 5 )
		
		
		bSizer40.Add( bSizer43, 1, wx.EXPAND, 5 )
		
		
		bSizer39.Add( bSizer40, 1, wx.EXPAND, 5 )
		
		bSizer44 = wx.BoxSizer( wx.VERTICAL )
		
		self.txtAtomicPolicy = wx.StaticText( self, wx.ID_ANY, u"Nessuna policy creata", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtAtomicPolicy.Wrap( -1 )
		bSizer44.Add( self.txtAtomicPolicy, 0, wx.ALL, 5 )
		
		
		bSizer39.Add( bSizer44, 1, wx.EXPAND|wx.FIXED_MINSIZE, 5 )
		
		bSizer45 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btnAddToList = wx.Button( self, wx.ID_ANY, u"Aggiungi all'elenco", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer45.Add( self.btnAddToList, 0, wx.ALL, 5 )
		
		
		bSizer39.Add( bSizer45, 1, wx.EXPAND|wx.FIXED_MINSIZE, 5 )
		
		bSizer46 = wx.BoxSizer( wx.VERTICAL )
		
		self.btnFine = wx.Button( self, wx.ID_ANY, u"Fine", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer46.Add( self.btnFine, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
		
		
		bSizer39.Add( bSizer46, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer39 )
		self.Layout()
		bSizer39.Fit( self )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class LoginFrame
###########################################################################

class LoginFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

