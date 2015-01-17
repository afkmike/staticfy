# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class main_window
###########################################################################

class main_window ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Staticfy Django Integration Tool", pos = wx.DefaultPosition, size = wx.Size( 964,552 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer99 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Choose Processing Method", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		bSizer99.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		processing_type_comboChoices = [ u"Single File", u"Whole Dir" ]
		self.processing_type_combo = wx.ComboBox( self, wx.ID_ANY, u"Single File", wx.DefaultPosition, wx.DefaultSize, processing_type_comboChoices, 0 )
		self.processing_type_combo.SetSelection( 0 )
		bSizer99.Add( self.processing_type_combo, 0, wx.ALL, 5 )
		
		self.process_type_panel = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer99.Add( self.process_type_panel, 0, wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer99, 0, wx.EXPAND, 5 )
		
		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer20 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"File Type:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		bSizer20.Add( self.m_staticText8, 0, wx.ALL, 5 )
		
		file_type_selectorChoices = [ u"HTML", u"Python" ]
		self.file_type_selector = wx.ComboBox( self, wx.ID_ANY, u"HTML", wx.DefaultPosition, wx.DefaultSize, file_type_selectorChoices, 0 )
		self.file_type_selector.SetSelection( 0 )
		bSizer20.Add( self.file_type_selector, 0, wx.ALL, 5 )
		
		self.actions_panel = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer20.Add( self.actions_panel, 1, wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer20, 0, wx.EXPAND, 5 )
		
		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.console = wx.TextCtrl( self, wx.ID_ANY, u"Log contents will be displayed here. You can also find a copy of the log in your Staticfy/logs folder.", wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_DONTWRAP|wx.TE_MULTILINE|wx.TE_READONLY )
		bSizer5.Add( self.console, 1, wx.EXPAND, 5 )
		
		
		bSizer3.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.clear_log = wx.Button( self, wx.ID_ANY, u"Clear Log", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.clear_log.SetDefault() 
		bSizer4.Add( self.clear_log, 0, wx.ALL, 5 )
		
		self.submit_log = wx.Button( self, wx.ID_ANY, u"Submit Log", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.submit_log, 0, wx.ALL, 5 )
		
		
		bSizer3.Add( bSizer4, 0, 0, 5 )
		
		
		bSizer1.Add( bSizer3, 1, wx.ALIGN_BOTTOM|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_statusBar1 = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		self.m_menubar1 = wx.MenuBar( 0 )
		self.File = wx.Menu()
		self.exit = wx.MenuItem( self.File, wx.ID_ANY, u"Exit"+ u"\t" + u"alt+F4", u"Exit the program", wx.ITEM_NORMAL )
		self.File.AppendItem( self.exit )
		
		self.m_menubar1.Append( self.File, u"File" ) 
		
		self.Help = wx.Menu()
		self.about = wx.MenuItem( self.Help, wx.ID_ANY, u"About", u"Version and Author Information", wx.ITEM_NORMAL )
		self.Help.AppendItem( self.about )
		
		self.m_menubar1.Append( self.Help, u"Help" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.processing_type_combo.Bind( wx.EVT_COMBOBOX, self.show_picker_type )
		self.file_type_selector.Bind( wx.EVT_COMBOBOX, self.show_actions )
		self.clear_log.Bind( wx.EVT_BUTTON, self.clear_log_contents )
		self.submit_log.Bind( wx.EVT_BUTTON, self.submit_log_contents )
		self.Bind( wx.EVT_MENU, self.close_program, id = self.exit.GetId() )
		self.Bind( wx.EVT_MENU, self.show_about_dialog, id = self.about.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def show_picker_type( self, event ):
		event.Skip()
	
	def show_actions( self, event ):
		event.Skip()
	
	def clear_log_contents( self, event ):
		event.Skip()
	
	def submit_log_contents( self, event ):
		event.Skip()
	
	def close_program( self, event ):
		event.Skip()
	
	def show_about_dialog( self, event ):
		event.Skip()
	

###########################################################################
## Class diff_view
###########################################################################

class diff_view ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Filename + Diff View", pos = wx.DefaultPosition, size = wx.Size( 982,589 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer13 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Files Affected :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		bSizer14.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		files_comboChoices = []
		self.files_combo = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, files_comboChoices, 0 )
		bSizer14.Add( self.files_combo, 0, wx.ALL, 5 )
		
		self.show_file = wx.Button( self, wx.ID_ANY, u"Show", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.show_file, 0, wx.ALL, 5 )
		
		self.m_button12 = wx.Button( self, wx.ID_ANY, u"Open In Editor", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.m_button12, 0, wx.ALL, 5 )
		
		
		bSizer14.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer15.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_button10 = wx.Button( self, wx.ID_ANY, u"Revert This File", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer15.Add( self.m_button10, 0, wx.ALL, 5 )
		
		self.m_button11 = wx.Button( self, wx.ID_ANY, u"Revert All Files", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer15.Add( self.m_button11, 0, wx.ALL, 5 )
		
		
		bSizer14.Add( bSizer15, 0, wx.ALIGN_RIGHT|wx.RIGHT, 5 )
		
		
		bSizer13.Add( bSizer14, 0, wx.EXPAND, 5 )
		
		bSizer16 = wx.BoxSizer( wx.HORIZONTAL )
		
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Original File :" ), wx.VERTICAL )
		
		self.orig_file = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_DONTWRAP|wx.TE_MULTILINE|wx.TE_READONLY )
		sbSizer1.Add( self.orig_file, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer16.Add( sbSizer1, 1, wx.EXPAND, 5 )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Modified File :" ), wx.VERTICAL )
		
		self.mod_file = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_DONTWRAP|wx.TE_MULTILINE|wx.TE_READONLY )
		sbSizer2.Add( self.mod_file, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer16.Add( sbSizer2, 1, wx.EXPAND, 5 )
		
		
		bSizer13.Add( bSizer16, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer13 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.show_file.Bind( wx.EVT_BUTTON, self.show_selected_file )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def show_selected_file( self, event ):
		event.Skip()
	

###########################################################################
## Class html_actions
###########################################################################

class html_actions ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"HTML Actions" ), wx.VERTICAL )
		
		bSizer18 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer19 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.extends = wx.CheckBox( self, wx.ID_ANY, u"Extends :", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer19.Add( self.extends, 0, wx.ALL, 5 )
		
		self.base_file = wx.TextCtrl( self, wx.ID_ANY, u"base.html", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer19.Add( self.base_file, 0, wx.ALL, 5 )
		
		
		bSizer18.Add( bSizer19, 0, wx.EXPAND, 5 )
		
		self.static_res = wx.CheckBox( self, wx.ID_ANY, u"Link Static Resources", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.static_res, 0, wx.ALL, 5 )
		
		self.rem_html_tags = wx.CheckBox( self, wx.ID_ANY, u"Remove <html> and </html> tags", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.rem_html_tags, 0, wx.ALL, 5 )
		
		self.url_conf = wx.CheckBox( self, wx.ID_ANY, u"Configure URLs", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.url_conf, 0, wx.ALL, 5 )
		
		self.dis_rel_path = wx.CheckBox( self, wx.ID_ANY, u"Disable Relative Paths\n(delete all instances of ../)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.dis_rel_path.SetValue(True) 
		self.dis_rel_path.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		bSizer18.Add( self.dis_rel_path, 0, wx.ALL, 5 )
		
		self.def_blocks = wx.CheckBox( self, wx.ID_ANY, u"Default Inheritance Blocks\n{% block head_block %}\n        and\n{% block body_content %}", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.def_blocks, 0, wx.ALL, 5 )
		
		
		sbSizer3.Add( bSizer18, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( sbSizer3 )
		self.Layout()
		
		# Connect Events
		self.url_conf.Bind( wx.EVT_CHECKBOX, self.sync_rel_path )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def sync_rel_path( self, event ):
		event.Skip()
	

###########################################################################
## Class about_dialog
###########################################################################

class about_dialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"About", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer15 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"\n        Staticfy DIT\n        Version 1.0\n\n©2015 AFK Concepts\n", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		bSizer15.Add( self.m_staticText4, 0, wx.ALL, 5 )
		
		
		self.SetSizer( bSizer15 )
		self.Layout()
		bSizer15.Fit( self )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

