# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.richtext
import wx.grid
import wx.html

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Metering Installation Error Calculator         ( beta 0.1.1 July 2012)", pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Setup = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.Setup.Hide()

		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		self.m_button26 = wx.Button( self.Setup, wx.ID_ANY, u"Process opened project files", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button26.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

		bSizer6.Add( self.m_button26, 0, wx.ALL, 5 )

		self.m_button1 = wx.Button( self.Setup, wx.ID_ANY, u"Process manually created files", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button1.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT, False, wx.EmptyString ) )

		bSizer6.Add( self.m_button1, 0, wx.ALL, 5 )

		self.report_richText = wx.richtext.RichTextCtrl( self.Setup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.WANTS_CHARS|wx.BORDER_NONE )
		bSizer6.Add( self.report_richText, 1, wx.EXPAND |wx.ALL, 5 )


		self.Setup.SetSizer( bSizer6 )
		self.Setup.Layout()
		bSizer6.Fit( self.Setup )
		self.m_notebook1.AddPage( self.Setup, u"Certificate Report", True )
		self.report_graph = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_notebook1.AddPage( self.report_graph, u"Total error graph", False )
		self.report_files = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText22 = wx.StaticText( self.report_files, wx.ID_ANY, u"Project directory", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText22.Wrap( -1 )

		bSizer8.Add( self.m_staticText22, 0, wx.ALL, 5 )

		self.file_table = wx.grid.Grid( self.report_files, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.file_table.CreateGrid( 10, 1 )
		self.file_table.EnableEditing( True )
		self.file_table.EnableGridLines( True )
		self.file_table.EnableDragGridSize( False )
		self.file_table.SetMargins( 0, 0 )

		# Columns
		self.file_table.SetColSize( 0, 131 )
		self.file_table.EnableDragColMove( False )
		self.file_table.EnableDragColSize( True )
		self.file_table.SetColLabelSize( 30 )
		self.file_table.SetColLabelValue( 0, u"File name" )
		self.file_table.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.file_table.EnableDragRowSize( True )
		self.file_table.SetRowLabelSize( 150 )
		self.file_table.SetRowLabelValue( 0, u"Meter calibration" )
		self.file_table.SetRowLabelValue( 1, u"Meter influences" )
		self.file_table.SetRowLabelValue( 2, u"VT calibration" )
		self.file_table.SetRowLabelValue( 3, u"VT error influences" )
		self.file_table.SetRowLabelValue( 4, u"VT phase influences" )
		self.file_table.SetRowLabelValue( 5, u"CT calibration" )
		self.file_table.SetRowLabelValue( 6, u"CT error influences" )
		self.file_table.SetRowLabelValue( 7, u"CT phase influences" )
		self.file_table.SetRowLabelValue( 8, u"Site influences" )
		self.file_table.SetRowLabelValue( 9, u"Load" )
		self.file_table.SetRowLabelAlignment( wx.ALIGN_LEFT, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.file_table.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer8.Add( self.file_table, 0, wx.ALL, 5 )

		self.m_textCtrl3 = wx.TextCtrl( self.report_files, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 600,200 ), wx.TE_MULTILINE )
		self.m_textCtrl3.SetMaxLength( 0 )
		bSizer8.Add( self.m_textCtrl3, 0, wx.ALL, 5 )


		self.report_files.SetSizer( bSizer8 )
		self.report_files.Layout()
		bSizer8.Fit( self.report_files )
		self.m_notebook1.AddPage( self.report_files, u"Input file list and messages", False )

		bSizer1.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )

		# self.m_button27 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		# bSizer1.Add( self.m_button27, 0, wx.ALL, 5 )

		self.m_notebook11 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_notebook11.Hide()

		self.Meter = wx.Panel( self.m_notebook11, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer61 = wx.BoxSizer( wx.VERTICAL )

		self.m_button42 = wx.Button( self.Meter, wx.ID_ANY, u"Load influence data", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer61.Add( self.m_button42, 0, wx.ALL, 5 )

		self.meter_table = wx.grid.Grid( self.Meter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.meter_table.CreateGrid( 7, 6 )
		self.meter_table.EnableEditing( True )
		self.meter_table.EnableGridLines( True )
		self.meter_table.EnableDragGridSize( False )
		self.meter_table.SetMargins( 0, 0 )

		# Columns
		self.meter_table.SetColSize( 0, 129 )
		self.meter_table.SetColSize( 1, 80 )
		self.meter_table.SetColSize( 2, 80 )
		self.meter_table.SetColSize( 3, 80 )
		self.meter_table.SetColSize( 4, 80 )
		self.meter_table.EnableDragColMove( False )
		self.meter_table.EnableDragColSize( True )
		self.meter_table.SetColLabelSize( 30 )
		self.meter_table.SetColLabelValue( 0, u"Item" )
		self.meter_table.SetColLabelValue( 1, u"value" )
		self.meter_table.SetColLabelValue( 2, u"units" )
		self.meter_table.SetColLabelValue( 3, u"stdev" )
		self.meter_table.SetColLabelValue( 4, u"distrib" )
		self.meter_table.SetColLabelValue( 5, u"dof" )
		self.meter_table.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.meter_table.EnableDragRowSize( True )
		self.meter_table.SetRowLabelSize( 0 )
		self.meter_table.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.meter_table.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer61.Add( self.meter_table, 0, wx.ALL, 5 )

		self.m_button11 = wx.Button( self.Meter, wx.ID_ANY, u"Generate summary file", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer61.Add( self.m_button11, 0, wx.ALL, 5 )

		self.meter_richText = wx.richtext.RichTextCtrl( self.Meter, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.WANTS_CHARS|wx.BORDER_NONE )
		bSizer61.Add( self.meter_richText, 1, wx.EXPAND |wx.ALL, 5 )


		self.Meter.SetSizer( bSizer61 )
		self.Meter.Layout()
		bSizer61.Fit( self.Meter )
		self.m_notebook11.AddPage( self.Meter, u"Meter Summary", True )
		self.m_scrolledWindow11 = wx.ScrolledWindow( self.m_notebook11, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow11.SetScrollRate( 5, 5 )
		fgSizer111 = wx.FlexGridSizer( 8, 2, 0, 0 )
		fgSizer111.SetFlexibleDirection( wx.BOTH )
		fgSizer111.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText111 = wx.StaticText( self.m_scrolledWindow11, wx.ID_ANY, u"Select number of rows for manual entry", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText111.Wrap( -1 )

		fgSizer111.Add( self.m_staticText111, 0, wx.ALL, 5 )

		self.m_staticText211 = wx.StaticText( self.m_scrolledWindow11, wx.ID_ANY, u"Select model for curve fit", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText211.Wrap( -1 )

		fgSizer111.Add( self.m_staticText211, 0, wx.ALL, 5 )

		self.row_spin11 = wx.SpinCtrl( self.m_scrolledWindow11, wx.ID_ANY, u"5", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 1000, 5 )
		fgSizer111.Add( self.row_spin11, 0, wx.ALL, 5 )

		eqn_choice_MeterChoices = [ u"0: mean", u"1: plane", u"2: tan", u"3: tan-ln" ]
		self.eqn_choice_Meter = wx.Choice( self.m_scrolledWindow11, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, eqn_choice_MeterChoices, 0 )
		self.eqn_choice_Meter.SetSelection( 0 )
		fgSizer111.Add( self.eqn_choice_Meter, 0, wx.ALL, 5 )

		self.m_button1011 = wx.Button( self.m_scrolledWindow11, wx.ID_ANY, u"Load Meter Data", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer111.Add( self.m_button1011, 0, wx.ALL, 5 )

		self.Meter_staticText = wx.StaticText( self.m_scrolledWindow11, wx.ID_ANY, u"y = a0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Meter_staticText.Wrap( -1 )

		fgSizer111.Add( self.Meter_staticText, 0, wx.ALL, 5 )

		self.m_button211 = wx.Button( self.m_scrolledWindow11, wx.ID_ANY, u"Plot Data", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer111.Add( self.m_button211, 0, wx.ALL, 5 )

		self.m_button1811 = wx.Button( self.m_scrolledWindow11, wx.ID_ANY, u"Generate Fit", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer111.Add( self.m_button1811, 0, wx.ALL, 5 )

		self.meter_data = wx.grid.Grid( self.m_scrolledWindow11, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.meter_data.CreateGrid( 5, 5 )
		self.meter_data.EnableEditing( True )
		self.meter_data.EnableGridLines( True )
		self.meter_data.EnableDragGridSize( True )
		self.meter_data.SetMargins( 0, 0 )

		# Columns
		self.meter_data.EnableDragColMove( False )
		self.meter_data.EnableDragColSize( True )
		self.meter_data.SetColLabelSize( 30 )
		self.meter_data.SetColLabelValue( 0, u"X" )
		self.meter_data.SetColLabelValue( 1, u"Y" )
		self.meter_data.SetColLabelValue( 2, u"Z" )
		self.meter_data.SetColLabelValue( 3, u"U" )
		self.meter_data.SetColLabelValue( 4, u"k" )
		self.meter_data.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.meter_data.EnableDragRowSize( True )
		self.meter_data.SetRowLabelSize( 80 )
		self.meter_data.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.meter_data.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		fgSizer111.Add( self.meter_data, 0, wx.ALL, 5 )

		self.Meter_fit_grid = wx.grid.Grid( self.m_scrolledWindow11, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.Meter_fit_grid.CreateGrid( 7, 4 )
		self.Meter_fit_grid.EnableEditing( True )
		self.Meter_fit_grid.EnableGridLines( True )
		self.Meter_fit_grid.EnableDragGridSize( False )
		self.Meter_fit_grid.SetMargins( 0, 0 )

		# Columns
		self.Meter_fit_grid.EnableDragColMove( False )
		self.Meter_fit_grid.EnableDragColSize( True )
		self.Meter_fit_grid.SetColLabelSize( 0 )
		self.Meter_fit_grid.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.Meter_fit_grid.EnableDragRowSize( True )
		self.Meter_fit_grid.SetRowLabelSize( 0 )
		self.Meter_fit_grid.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.Meter_fit_grid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		fgSizer111.Add( self.Meter_fit_grid, 0, wx.ALL, 5 )


		self.m_scrolledWindow11.SetSizer( fgSizer111 )
		self.m_scrolledWindow11.Layout()
		fgSizer111.Fit( self.m_scrolledWindow11 )
		self.m_notebook11.AddPage( self.m_scrolledWindow11, u"Meter Data", False )
		self.meter_graph = wx.Panel( self.m_notebook11, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_notebook11.AddPage( self.meter_graph, u"Meter Plot", False )

		bSizer1.Add( self.m_notebook11, 1, wx.EXPAND |wx.ALL, 5 )

		self.CT_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.CT_notebook.Hide()

		self.CTSummary = wx.Panel( self.CT_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer62 = wx.BoxSizer( wx.VERTICAL )

		self.m_button12 = wx.Button( self.CTSummary, wx.ID_ANY, u"Load influence data", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer62.Add( self.m_button12, 0, wx.ALL, 5 )

		self.CT_table = wx.grid.Grid( self.CTSummary, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.CT_table.CreateGrid( 4, 6 )
		self.CT_table.EnableEditing( True )
		self.CT_table.EnableGridLines( True )
		self.CT_table.EnableDragGridSize( False )
		self.CT_table.SetMargins( 0, 0 )

		# Columns
		self.CT_table.SetColSize( 0, 129 )
		self.CT_table.SetColSize( 1, 80 )
		self.CT_table.SetColSize( 2, 80 )
		self.CT_table.SetColSize( 3, 80 )
		self.CT_table.SetColSize( 4, 80 )
		self.CT_table.EnableDragColMove( False )
		self.CT_table.EnableDragColSize( True )
		self.CT_table.SetColLabelSize( 30 )
		self.CT_table.SetColLabelValue( 0, u"Item" )
		self.CT_table.SetColLabelValue( 1, u"value" )
		self.CT_table.SetColLabelValue( 2, u"units" )
		self.CT_table.SetColLabelValue( 3, u"stdev" )
		self.CT_table.SetColLabelValue( 4, u"distrib" )
		self.CT_table.SetColLabelValue( 5, u"dof" )
		self.CT_table.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.CT_table.EnableDragRowSize( True )
		self.CT_table.SetRowLabelSize( 0 )
		self.CT_table.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.CT_table.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer62.Add( self.CT_table, 0, wx.ALL, 5 )

		self.CT_table1 = wx.grid.Grid( self.CTSummary, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.CT_table1.CreateGrid( 2, 6 )
		self.CT_table1.EnableEditing( True )
		self.CT_table1.EnableGridLines( True )
		self.CT_table1.EnableDragGridSize( False )
		self.CT_table1.SetMargins( 0, 0 )

		# Columns
		self.CT_table1.SetColSize( 0, 129 )
		self.CT_table1.SetColSize( 1, 80 )
		self.CT_table1.SetColSize( 2, 80 )
		self.CT_table1.SetColSize( 3, 80 )
		self.CT_table1.SetColSize( 4, 80 )
		self.CT_table1.EnableDragColMove( False )
		self.CT_table1.EnableDragColSize( True )
		self.CT_table1.SetColLabelSize( 30 )
		self.CT_table1.SetColLabelValue( 0, u"Item" )
		self.CT_table1.SetColLabelValue( 1, u"value" )
		self.CT_table1.SetColLabelValue( 2, u"units" )
		self.CT_table1.SetColLabelValue( 3, u"stdev" )
		self.CT_table1.SetColLabelValue( 4, u"distrib" )
		self.CT_table1.SetColLabelValue( 5, u"dof" )
		self.CT_table1.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.CT_table1.EnableDragRowSize( True )
		self.CT_table1.SetRowLabelSize( 0 )
		self.CT_table1.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.CT_table1.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer62.Add( self.CT_table1, 0, wx.ALL, 5 )

		self.m_button111 = wx.Button( self.CTSummary, wx.ID_ANY, u"Generate summary file", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer62.Add( self.m_button111, 0, wx.ALL, 5 )

		self.CT_richText = wx.richtext.RichTextCtrl( self.CTSummary, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.WANTS_CHARS|wx.BORDER_NONE )
		bSizer62.Add( self.CT_richText, 1, wx.EXPAND |wx.ALL, 5 )

		self.CT_richText1 = wx.richtext.RichTextCtrl( self.CTSummary, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.WANTS_CHARS|wx.BORDER_NONE )
		bSizer62.Add( self.CT_richText1, 1, wx.EXPAND |wx.ALL, 5 )


		self.CTSummary.SetSizer( bSizer62 )
		self.CTSummary.Layout()
		bSizer62.Fit( self.CTSummary )
		self.CT_notebook.AddPage( self.CTSummary, u"CT Summary", True )
		self.m_scrolledWindow3 = wx.ScrolledWindow( self.CT_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow3.SetScrollRate( 5, 5 )
		fgSizer13 = wx.FlexGridSizer( 10, 2, 0, 0 )
		fgSizer13.SetFlexibleDirection( wx.BOTH )
		fgSizer13.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_button103 = wx.Button( self.m_scrolledWindow3, wx.ID_ANY, u"Load CT Data", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer13.Add( self.m_button103, 0, wx.ALL, 5 )

		self.m_staticText38 = wx.StaticText( self.m_scrolledWindow3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText38.Wrap( -1 )

		fgSizer13.Add( self.m_staticText38, 0, wx.ALL, 5 )

		self.m_staticText23 = wx.StaticText( self.m_scrolledWindow3, wx.ID_ANY, u"Select ratio error model", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText23.Wrap( -1 )

		fgSizer13.Add( self.m_staticText23, 0, wx.ALL, 5 )

		self.m_staticText37 = wx.StaticText( self.m_scrolledWindow3, wx.ID_ANY, u"Select phase error model", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText37.Wrap( -1 )

		fgSizer13.Add( self.m_staticText37, 0, wx.ALL, 5 )

		eqn_choice_CTratioChoices = [ u"0: mean", u"1: straight line", u"2: log" ]
		self.eqn_choice_CTratio = wx.Choice( self.m_scrolledWindow3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, eqn_choice_CTratioChoices, 0 )
		self.eqn_choice_CTratio.SetSelection( 0 )
		fgSizer13.Add( self.eqn_choice_CTratio, 0, wx.ALL, 5 )

		eqn_choice_CTphaseChoices = [ u"0: mean", u"1: straight line", u"2: log" ]
		self.eqn_choice_CTphase = wx.Choice( self.m_scrolledWindow3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, eqn_choice_CTphaseChoices, 0 )
		self.eqn_choice_CTphase.SetSelection( 0 )
		fgSizer13.Add( self.eqn_choice_CTphase, 0, wx.ALL, 5 )

		self.CTratio_staticText = wx.StaticText( self.m_scrolledWindow3, wx.ID_ANY, u"y = a0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.CTratio_staticText.Wrap( -1 )

		fgSizer13.Add( self.CTratio_staticText, 0, wx.ALL, 5 )

		self.CTphase_staticText = wx.StaticText( self.m_scrolledWindow3, wx.ID_ANY, u"y = a0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.CTphase_staticText.Wrap( -1 )

		fgSizer13.Add( self.CTphase_staticText, 0, wx.ALL, 5 )

		self.CTratio_fit_grid = wx.grid.Grid( self.m_scrolledWindow3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.CTratio_fit_grid.CreateGrid( 7, 4 )
		self.CTratio_fit_grid.EnableEditing( True )
		self.CTratio_fit_grid.EnableGridLines( True )
		self.CTratio_fit_grid.EnableDragGridSize( False )
		self.CTratio_fit_grid.SetMargins( 0, 0 )

		# Columns
		self.CTratio_fit_grid.EnableDragColMove( False )
		self.CTratio_fit_grid.EnableDragColSize( True )
		self.CTratio_fit_grid.SetColLabelSize( 0 )
		self.CTratio_fit_grid.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.CTratio_fit_grid.EnableDragRowSize( True )
		self.CTratio_fit_grid.SetRowLabelSize( 0 )
		self.CTratio_fit_grid.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.CTratio_fit_grid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		fgSizer13.Add( self.CTratio_fit_grid, 0, wx.ALL, 5 )

		self.CTphase_fit_grid = wx.grid.Grid( self.m_scrolledWindow3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.CTphase_fit_grid.CreateGrid( 7, 4 )
		self.CTphase_fit_grid.EnableEditing( True )
		self.CTphase_fit_grid.EnableGridLines( True )
		self.CTphase_fit_grid.EnableDragGridSize( False )
		self.CTphase_fit_grid.SetMargins( 0, 0 )

		# Columns
		self.CTphase_fit_grid.EnableDragColMove( False )
		self.CTphase_fit_grid.EnableDragColSize( True )
		self.CTphase_fit_grid.SetColLabelSize( 0 )
		self.CTphase_fit_grid.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.CTphase_fit_grid.EnableDragRowSize( True )
		self.CTphase_fit_grid.SetRowLabelSize( 0 )
		self.CTphase_fit_grid.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.CTphase_fit_grid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		fgSizer13.Add( self.CTphase_fit_grid, 0, wx.ALL, 5 )

		self.m_staticText13 = wx.StaticText( self.m_scrolledWindow3, wx.ID_ANY, u"Select number of rows for manual entry", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )

		fgSizer13.Add( self.m_staticText13, 0, wx.ALL, 5 )

		self.m_staticText131 = wx.StaticText( self.m_scrolledWindow3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText131.Wrap( -1 )

		fgSizer13.Add( self.m_staticText131, 0, wx.ALL, 5 )

		self.row_spin3 = wx.SpinCtrl( self.m_scrolledWindow3, wx.ID_ANY, u"5", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 1000, 1 )
		fgSizer13.Add( self.row_spin3, 0, wx.ALL, 5 )

		self.m_staticText46 = wx.StaticText( self.m_scrolledWindow3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText46.Wrap( -1 )

		fgSizer13.Add( self.m_staticText46, 0, wx.ALL, 5 )

		self.m_button23 = wx.Button( self.m_scrolledWindow3, wx.ID_ANY, u"Plot Ratio  Data", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer13.Add( self.m_button23, 0, wx.ALL, 5 )

		self.m_button231 = wx.Button( self.m_scrolledWindow3, wx.ID_ANY, u"Plot Phase Data", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer13.Add( self.m_button231, 0, wx.ALL, 5 )

		self.m_button183 = wx.Button( self.m_scrolledWindow3, wx.ID_ANY, u"Generate Ratio Fit", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer13.Add( self.m_button183, 0, wx.ALL, 5 )

		self.m_button193 = wx.Button( self.m_scrolledWindow3, wx.ID_ANY, u"Generate Phase Fit", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer13.Add( self.m_button193, 0, wx.ALL, 5 )

		self.CTratio_data = wx.grid.Grid( self.m_scrolledWindow3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.CTratio_data.CreateGrid( 5, 4 )
		self.CTratio_data.EnableEditing( True )
		self.CTratio_data.EnableGridLines( True )
		self.CTratio_data.EnableDragGridSize( True )
		self.CTratio_data.SetMargins( 0, 0 )

		# Columns
		self.CTratio_data.EnableDragColMove( False )
		self.CTratio_data.EnableDragColSize( True )
		self.CTratio_data.SetColLabelSize( 30 )
		self.CTratio_data.SetColLabelValue( 0, u"I" )
		self.CTratio_data.SetColLabelValue( 1, u"E" )
		self.CTratio_data.SetColLabelValue( 2, u"U" )
		self.CTratio_data.SetColLabelValue( 3, u"k" )
		self.CTratio_data.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.CTratio_data.EnableDragRowSize( True )
		self.CTratio_data.SetRowLabelSize( 80 )
		self.CTratio_data.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.CTratio_data.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		fgSizer13.Add( self.CTratio_data, 0, wx.ALL, 5 )

		self.CTphase_data = wx.grid.Grid( self.m_scrolledWindow3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.CTphase_data.CreateGrid( 5, 4 )
		self.CTphase_data.EnableEditing( True )
		self.CTphase_data.EnableGridLines( True )
		self.CTphase_data.EnableDragGridSize( True )
		self.CTphase_data.SetMargins( 0, 0 )

		# Columns
		self.CTphase_data.EnableDragColMove( False )
		self.CTphase_data.EnableDragColSize( True )
		self.CTphase_data.SetColLabelSize( 30 )
		self.CTphase_data.SetColLabelValue( 0, u"I" )
		self.CTphase_data.SetColLabelValue( 1, u"phi" )
		self.CTphase_data.SetColLabelValue( 2, u"U" )
		self.CTphase_data.SetColLabelValue( 3, u"k" )
		self.CTphase_data.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.CTphase_data.EnableDragRowSize( True )
		self.CTphase_data.SetRowLabelSize( 80 )
		self.CTphase_data.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.CTphase_data.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		fgSizer13.Add( self.CTphase_data, 0, wx.ALL, 5 )


		self.m_scrolledWindow3.SetSizer( fgSizer13 )
		self.m_scrolledWindow3.Layout()
		fgSizer13.Fit( self.m_scrolledWindow3 )
		self.CT_notebook.AddPage( self.m_scrolledWindow3, u"CT Data", False )
		self.CT_graph_1 = wx.Panel( self.CT_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.CT_notebook.AddPage( self.CT_graph_1, u"CT Plots", False )

		bSizer1.Add( self.CT_notebook, 1, wx.EXPAND |wx.ALL, 5 )

		self.VT_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.VT_notebook.Hide()

		self.VTSummary = wx.Panel( self.VT_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer621 = wx.BoxSizer( wx.VERTICAL )

		self.m_button121 = wx.Button( self.VTSummary, wx.ID_ANY, u"Load influence data", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer621.Add( self.m_button121, 0, wx.ALL, 5 )

		self.VT_table = wx.grid.Grid( self.VTSummary, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.VT_table.CreateGrid( 4, 6 )
		self.VT_table.EnableEditing( True )
		self.VT_table.EnableGridLines( True )
		self.VT_table.EnableDragGridSize( False )
		self.VT_table.SetMargins( 0, 0 )

		# Columns
		self.VT_table.SetColSize( 0, 129 )
		self.VT_table.SetColSize( 1, 80 )
		self.VT_table.SetColSize( 2, 80 )
		self.VT_table.SetColSize( 3, 80 )
		self.VT_table.SetColSize( 4, 80 )
		self.VT_table.EnableDragColMove( False )
		self.VT_table.EnableDragColSize( True )
		self.VT_table.SetColLabelSize( 30 )
		self.VT_table.SetColLabelValue( 0, u"Item" )
		self.VT_table.SetColLabelValue( 1, u"value" )
		self.VT_table.SetColLabelValue( 2, u"units" )
		self.VT_table.SetColLabelValue( 3, u"stdev" )
		self.VT_table.SetColLabelValue( 4, u"distrib" )
		self.VT_table.SetColLabelValue( 5, u"dof" )
		self.VT_table.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.VT_table.EnableDragRowSize( True )
		self.VT_table.SetRowLabelSize( 0 )
		self.VT_table.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.VT_table.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer621.Add( self.VT_table, 0, wx.ALL, 5 )

		self.VT_table1 = wx.grid.Grid( self.VTSummary, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.VT_table1.CreateGrid( 2, 6 )
		self.VT_table1.EnableEditing( True )
		self.VT_table1.EnableGridLines( True )
		self.VT_table1.EnableDragGridSize( False )
		self.VT_table1.SetMargins( 0, 0 )

		# Columns
		self.VT_table1.SetColSize( 0, 129 )
		self.VT_table1.SetColSize( 1, 80 )
		self.VT_table1.SetColSize( 2, 80 )
		self.VT_table1.SetColSize( 3, 80 )
		self.VT_table1.SetColSize( 4, 80 )
		self.VT_table1.EnableDragColMove( False )
		self.VT_table1.EnableDragColSize( True )
		self.VT_table1.SetColLabelSize( 30 )
		self.VT_table1.SetColLabelValue( 0, u"Item" )
		self.VT_table1.SetColLabelValue( 1, u"value" )
		self.VT_table1.SetColLabelValue( 2, u"units" )
		self.VT_table1.SetColLabelValue( 3, u"stdev" )
		self.VT_table1.SetColLabelValue( 4, u"distrib" )
		self.VT_table1.SetColLabelValue( 5, u"dof" )
		self.VT_table1.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.VT_table1.EnableDragRowSize( True )
		self.VT_table1.SetRowLabelSize( 0 )
		self.VT_table1.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.VT_table1.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer621.Add( self.VT_table1, 0, wx.ALL, 5 )

		self.m_button1111 = wx.Button( self.VTSummary, wx.ID_ANY, u"Generate summary file", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer621.Add( self.m_button1111, 0, wx.ALL, 5 )

		self.VT_richText = wx.richtext.RichTextCtrl( self.VTSummary, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.WANTS_CHARS|wx.BORDER_NONE )
		bSizer621.Add( self.VT_richText, 1, wx.EXPAND |wx.ALL, 5 )

		self.VT_richText1 = wx.richtext.RichTextCtrl( self.VTSummary, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.WANTS_CHARS|wx.BORDER_NONE )
		bSizer621.Add( self.VT_richText1, 1, wx.EXPAND |wx.ALL, 5 )


		self.VTSummary.SetSizer( bSizer621 )
		self.VTSummary.Layout()
		bSizer621.Fit( self.VTSummary )
		self.VT_notebook.AddPage( self.VTSummary, u"VT Summary", True )
		self.m_scrolledWindow31 = wx.ScrolledWindow( self.VT_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow31.SetScrollRate( 5, 5 )
		fgSizer131 = wx.FlexGridSizer( 10, 2, 0, 0 )
		fgSizer131.SetFlexibleDirection( wx.BOTH )
		fgSizer131.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_button1031 = wx.Button( self.m_scrolledWindow31, wx.ID_ANY, u"Load VT Data", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer131.Add( self.m_button1031, 0, wx.ALL, 5 )

		self.m_staticText381 = wx.StaticText( self.m_scrolledWindow31, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText381.Wrap( -1 )

		fgSizer131.Add( self.m_staticText381, 0, wx.ALL, 5 )

		self.m_staticText231 = wx.StaticText( self.m_scrolledWindow31, wx.ID_ANY, u"Select ratio error model", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText231.Wrap( -1 )

		fgSizer131.Add( self.m_staticText231, 0, wx.ALL, 5 )

		self.m_staticText371 = wx.StaticText( self.m_scrolledWindow31, wx.ID_ANY, u"Select phase error model", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText371.Wrap( -1 )

		fgSizer131.Add( self.m_staticText371, 0, wx.ALL, 5 )

		eqn_choice_VTratioChoices = [ u"0: mean", u"1: straight line", u"2: log" ]
		self.eqn_choice_VTratio = wx.Choice( self.m_scrolledWindow31, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, eqn_choice_VTratioChoices, 0 )
		self.eqn_choice_VTratio.SetSelection( 0 )
		fgSizer131.Add( self.eqn_choice_VTratio, 0, wx.ALL, 5 )

		eqn_choice_VTphaseChoices = [ u"0: mean", u"1: straight line", u"2: log" ]
		self.eqn_choice_VTphase = wx.Choice( self.m_scrolledWindow31, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, eqn_choice_VTphaseChoices, 0 )
		self.eqn_choice_VTphase.SetSelection( 0 )
		fgSizer131.Add( self.eqn_choice_VTphase, 0, wx.ALL, 5 )

		self.VTratio_staticText = wx.StaticText( self.m_scrolledWindow31, wx.ID_ANY, u"y = a0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.VTratio_staticText.Wrap( -1 )

		fgSizer131.Add( self.VTratio_staticText, 0, wx.ALL, 5 )

		self.VTphase_staticText = wx.StaticText( self.m_scrolledWindow31, wx.ID_ANY, u"y = a0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.VTphase_staticText.Wrap( -1 )

		fgSizer131.Add( self.VTphase_staticText, 0, wx.ALL, 5 )

		self.VTratio_fit_grid = wx.grid.Grid( self.m_scrolledWindow31, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.VTratio_fit_grid.CreateGrid( 7, 4 )
		self.VTratio_fit_grid.EnableEditing( True )
		self.VTratio_fit_grid.EnableGridLines( True )
		self.VTratio_fit_grid.EnableDragGridSize( False )
		self.VTratio_fit_grid.SetMargins( 0, 0 )

		# Columns
		self.VTratio_fit_grid.EnableDragColMove( False )
		self.VTratio_fit_grid.EnableDragColSize( True )
		self.VTratio_fit_grid.SetColLabelSize( 0 )
		self.VTratio_fit_grid.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.VTratio_fit_grid.EnableDragRowSize( True )
		self.VTratio_fit_grid.SetRowLabelSize( 0 )
		self.VTratio_fit_grid.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.VTratio_fit_grid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		fgSizer131.Add( self.VTratio_fit_grid, 0, wx.ALL, 5 )

		self.VTphase_fit_grid = wx.grid.Grid( self.m_scrolledWindow31, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.VTphase_fit_grid.CreateGrid( 7, 4 )
		self.VTphase_fit_grid.EnableEditing( True )
		self.VTphase_fit_grid.EnableGridLines( True )
		self.VTphase_fit_grid.EnableDragGridSize( False )
		self.VTphase_fit_grid.SetMargins( 0, 0 )

		# Columns
		self.VTphase_fit_grid.EnableDragColMove( False )
		self.VTphase_fit_grid.EnableDragColSize( True )
		self.VTphase_fit_grid.SetColLabelSize( 0 )
		self.VTphase_fit_grid.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.VTphase_fit_grid.EnableDragRowSize( True )
		self.VTphase_fit_grid.SetRowLabelSize( 0 )
		self.VTphase_fit_grid.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.VTphase_fit_grid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		fgSizer131.Add( self.VTphase_fit_grid, 0, wx.ALL, 5 )

		self.m_staticText132 = wx.StaticText( self.m_scrolledWindow31, wx.ID_ANY, u"Select number of rows for manual entry", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText132.Wrap( -1 )

		fgSizer131.Add( self.m_staticText132, 0, wx.ALL, 5 )

		self.m_staticText1311 = wx.StaticText( self.m_scrolledWindow31, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1311.Wrap( -1 )

		fgSizer131.Add( self.m_staticText1311, 0, wx.ALL, 5 )

		self.row_spin31 = wx.SpinCtrl( self.m_scrolledWindow31, wx.ID_ANY, u"5", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 1000, 1 )
		fgSizer131.Add( self.row_spin31, 0, wx.ALL, 5 )

		self.m_staticText461 = wx.StaticText( self.m_scrolledWindow31, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText461.Wrap( -1 )

		fgSizer131.Add( self.m_staticText461, 0, wx.ALL, 5 )

		self.m_button232 = wx.Button( self.m_scrolledWindow31, wx.ID_ANY, u"Plot Ratio  Data", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer131.Add( self.m_button232, 0, wx.ALL, 5 )

		self.m_button2311 = wx.Button( self.m_scrolledWindow31, wx.ID_ANY, u"Plot Phase Data", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer131.Add( self.m_button2311, 0, wx.ALL, 5 )

		self.m_button1831 = wx.Button( self.m_scrolledWindow31, wx.ID_ANY, u"Generate Ratio Fit", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer131.Add( self.m_button1831, 0, wx.ALL, 5 )

		self.m_button1931 = wx.Button( self.m_scrolledWindow31, wx.ID_ANY, u"Generate Phase Fit", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer131.Add( self.m_button1931, 0, wx.ALL, 5 )

		self.VTratio_data = wx.grid.Grid( self.m_scrolledWindow31, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.VTratio_data.CreateGrid( 5, 4 )
		self.VTratio_data.EnableEditing( True )
		self.VTratio_data.EnableGridLines( True )
		self.VTratio_data.EnableDragGridSize( True )
		self.VTratio_data.SetMargins( 0, 0 )

		# Columns
		self.VTratio_data.EnableDragColMove( False )
		self.VTratio_data.EnableDragColSize( True )
		self.VTratio_data.SetColLabelSize( 30 )
		self.VTratio_data.SetColLabelValue( 0, u"V" )
		self.VTratio_data.SetColLabelValue( 1, u"E" )
		self.VTratio_data.SetColLabelValue( 2, u"U" )
		self.VTratio_data.SetColLabelValue( 3, u"k" )
		self.VTratio_data.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.VTratio_data.EnableDragRowSize( True )
		self.VTratio_data.SetRowLabelSize( 80 )
		self.VTratio_data.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.VTratio_data.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		fgSizer131.Add( self.VTratio_data, 0, wx.ALL, 5 )

		self.VTphase_data = wx.grid.Grid( self.m_scrolledWindow31, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.VTphase_data.CreateGrid( 5, 4 )
		self.VTphase_data.EnableEditing( True )
		self.VTphase_data.EnableGridLines( True )
		self.VTphase_data.EnableDragGridSize( True )
		self.VTphase_data.SetMargins( 0, 0 )

		# Columns
		self.VTphase_data.EnableDragColMove( False )
		self.VTphase_data.EnableDragColSize( True )
		self.VTphase_data.SetColLabelSize( 30 )
		self.VTphase_data.SetColLabelValue( 0, u"V" )
		self.VTphase_data.SetColLabelValue( 1, u"phi" )
		self.VTphase_data.SetColLabelValue( 2, u"U" )
		self.VTphase_data.SetColLabelValue( 3, u"k" )
		self.VTphase_data.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.VTphase_data.EnableDragRowSize( True )
		self.VTphase_data.SetRowLabelSize( 80 )
		self.VTphase_data.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.VTphase_data.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		fgSizer131.Add( self.VTphase_data, 0, wx.ALL, 5 )


		self.m_scrolledWindow31.SetSizer( fgSizer131 )
		self.m_scrolledWindow31.Layout()
		fgSizer131.Fit( self.m_scrolledWindow31 )
		self.VT_notebook.AddPage( self.m_scrolledWindow31, u"VT Data", False )
		self.VT_graph_1 = wx.Panel( self.VT_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.VT_notebook.AddPage( self.VT_graph_1, u"VT Plots", False )

		bSizer1.Add( self.VT_notebook, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_notebook14 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_notebook14.Hide()

		self.Setup4 = wx.Panel( self.m_notebook14, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer64 = wx.BoxSizer( wx.VERTICAL )

		self.m_button14 = wx.Button( self.Setup4, wx.ID_ANY, u"Summary", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer64.Add( self.m_button14, 0, wx.ALL, 5 )

		self.load_richText = wx.richtext.RichTextCtrl( self.Setup4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.WANTS_CHARS|wx.BORDER_NONE )
		bSizer64.Add( self.load_richText, 1, wx.EXPAND |wx.ALL, 5 )


		self.Setup4.SetSizer( bSizer64 )
		self.Setup4.Layout()
		bSizer64.Fit( self.Setup4 )
		self.m_notebook14.AddPage( self.Setup4, u"Load Summary", True )
		self.m_scrolledWindow5 = wx.ScrolledWindow( self.m_notebook14, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow5.SetScrollRate( 5, 5 )
		fgSizer15 = wx.FlexGridSizer( 8, 2, 0, 0 )
		fgSizer15.SetFlexibleDirection( wx.BOTH )
		fgSizer15.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText15 = wx.StaticText( self.m_scrolledWindow5, wx.ID_ANY, u"Half hour data", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )

		fgSizer15.Add( self.m_staticText15, 0, wx.ALL, 5 )

		self.load_data = wx.TextCtrl( self.m_scrolledWindow5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 500,-1 ), 0 )
		self.load_data.SetMaxLength( 0 )
		fgSizer15.Add( self.load_data, 0, wx.ALL, 5 )

		self.m_staticText33 = wx.StaticText( self.m_scrolledWindow5, wx.ID_ANY, u"Load Profile", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )

		fgSizer15.Add( self.m_staticText33, 0, wx.ALL, 5 )

		self.load_values = wx.TextCtrl( self.m_scrolledWindow5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 500,-1 ), 0 )
		self.load_values.SetMaxLength( 0 )
		fgSizer15.Add( self.load_values, 0, wx.ALL, 5 )

		self.Create_load_profile = wx.Button( self.m_scrolledWindow5, wx.ID_ANY, u"Create Load Profile (from *.txt)", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer15.Add( self.Create_load_profile, 0, wx.ALL, 5 )

		self.Plot_load_profile = wx.Button( self.m_scrolledWindow5, wx.ID_ANY, u"Plot Load Profile (from *.csv)", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer15.Add( self.Plot_load_profile, 0, wx.ALL, 5 )


		self.m_scrolledWindow5.SetSizer( fgSizer15 )
		self.m_scrolledWindow5.Layout()
		fgSizer15.Fit( self.m_scrolledWindow5 )
		self.m_notebook14.AddPage( self.m_scrolledWindow5, u"Load Data", False )
		self.load_graph = wx.Panel( self.m_notebook14, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_notebook14.AddPage( self.load_graph, u"Load Plot", False )

		bSizer1.Add( self.m_notebook14, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_notebook15 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_notebook15.Hide()

		self.Site = wx.Panel( self.m_notebook15, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer65 = wx.BoxSizer( wx.VERTICAL )

		self.m_button15 = wx.Button( self.Site, wx.ID_ANY, u"Load site data", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer65.Add( self.m_button15, 0, wx.ALL, 5 )

		self.site_table = wx.grid.Grid( self.Site, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.site_table.CreateGrid( 7, 6 )
		self.site_table.EnableEditing( True )
		self.site_table.EnableGridLines( True )
		self.site_table.EnableDragGridSize( False )
		self.site_table.SetMargins( 0, 0 )

		# Columns
		self.site_table.SetColSize( 0, 129 )
		self.site_table.SetColSize( 1, 80 )
		self.site_table.SetColSize( 2, 80 )
		self.site_table.SetColSize( 3, 80 )
		self.site_table.SetColSize( 4, 80 )
		self.site_table.EnableDragColMove( False )
		self.site_table.EnableDragColSize( True )
		self.site_table.SetColLabelSize( 30 )
		self.site_table.SetColLabelValue( 0, u"Item" )
		self.site_table.SetColLabelValue( 1, u"value" )
		self.site_table.SetColLabelValue( 2, u"units" )
		self.site_table.SetColLabelValue( 3, u"width" )
		self.site_table.SetColLabelValue( 4, u"distrib" )
		self.site_table.SetColLabelValue( 5, u"dof" )
		self.site_table.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.site_table.EnableDragRowSize( True )
		self.site_table.SetRowLabelSize( 0 )
		self.site_table.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.site_table.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer65.Add( self.site_table, 0, wx.ALL, 5 )

		self.m_button112 = wx.Button( self.Site, wx.ID_ANY, u"Generate summary file", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer65.Add( self.m_button112, 0, wx.ALL, 5 )

		self.site_richText = wx.richtext.RichTextCtrl( self.Site, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.WANTS_CHARS|wx.BORDER_NONE )
		bSizer65.Add( self.site_richText, 1, wx.EXPAND |wx.ALL, 5 )


		self.Site.SetSizer( bSizer65 )
		self.Site.Layout()
		bSizer65.Fit( self.Site )
		self.m_notebook15.AddPage( self.Site, u"Site Summary", True )

		bSizer1.Add( self.m_notebook15, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_statusBar1 = self.CreateStatusBar( 3, wx.STB_SIZEGRIP, wx.ID_ANY )
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menu1 = wx.Menu()
		self.m_menuItem1 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Open", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_menuItem1 )

		self.m_menuItem2 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Save", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_menuItem2 )
		self.m_menuItem2.Enable( False )

		self.m_menuItem10 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Print report", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_menuItem10 )

		self.m_menuItem11 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Print preview", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_menuItem11 )

		self.m_menu1.AppendSeparator()

		self.m_menuItem3 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Quit", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_menuItem3 )

		self.m_menubar1.Append( self.m_menu1, u"File" )

		self.m_menu2 = wx.Menu()
		self.m_menuItem4 = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"Overall Report", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu2.Append( self.m_menuItem4 )

		self.m_menuItem5 = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"Meter", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu2.Append( self.m_menuItem5 )

		self.m_menuItem6 = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"CT", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu2.Append( self.m_menuItem6 )

		self.m_menuItem7 = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"VT", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu2.Append( self.m_menuItem7 )

		self.m_menuItem8 = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"Load Profile", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu2.Append( self.m_menuItem8 )

		self.m_menuItem9 = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"Site Conditions", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu2.Append( self.m_menuItem9 )

		self.m_menubar1.Append( self.m_menu2, u"Select Notebook" )

		self.m_menu3 = wx.Menu()
		self.m_menuItem12 = wx.MenuItem( self.m_menu3, wx.ID_ANY, u"Take snapshot", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu3.Append( self.m_menuItem12 )

		self.m_menuItem13 = wx.MenuItem( self.m_menu3, wx.ID_ANY, u"Print snaphsot", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu3.Append( self.m_menuItem13 )

		self.m_menubar1.Append( self.m_menu3, u"Snapshot" )

		self.m_menu4 = wx.Menu()
		self.m_menuItem14 = wx.MenuItem( self.m_menu4, wx.ID_ANY, u"Clear all graphs", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu4.Append( self.m_menuItem14 )

		self.m_menuItem17 = wx.MenuItem( self.m_menu4, wx.ID_ANY, u"Clear all text", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu4.Append( self.m_menuItem17 )

		self.m_menuItem18 = wx.MenuItem( self.m_menu4, wx.ID_ANY, u"Clear temporary files", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu4.Append( self.m_menuItem18 )

		self.m_menubar1.Append( self.m_menu4, u"Clear" )

		self.m_menu5 = wx.Menu()
		self.m_menuItem15 = wx.MenuItem( self.m_menu5, wx.ID_ANY, u"Help Topics", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu5.Append( self.m_menuItem15 )

		self.m_menu5.AppendSeparator()

		self.m_menuItem16 = wx.MenuItem( self.m_menu5, wx.ID_ANY, u"About MIEcaclulator", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu5.Append( self.m_menuItem16 )

		self.m_menubar1.Append( self.m_menu5, u"Help" )

		self.SetMenuBar( self.m_menubar1 )


		self.Centre( wx.BOTH )

		# Connect Events
		self.m_notebook1.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnNbookPageChange )
		self.m_button26.Bind( wx.EVT_BUTTON, self.OnAutoCalc )
		self.m_button1.Bind( wx.EVT_BUTTON, self.OnGUMcalc )
		self.m_notebook11.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnNbookPageChange )
		self.m_button42.Bind( wx.EVT_BUTTON, self.OnLoadMeterInf )
		self.m_button11.Bind( wx.EVT_BUTTON, self.OnMeterSummary )
		self.row_spin11.Bind( wx.EVT_SPINCTRL, self.OnSetMeterRows )
		self.row_spin11.Bind( wx.EVT_TEXT, self.OnSetMeterRows )
		self.eqn_choice_Meter.Bind( wx.EVT_CHOICE, self.OnMeterModel )
		self.m_button1011.Bind( wx.EVT_BUTTON, self.OnLoadMeterData )
		self.m_button211.Bind( wx.EVT_BUTTON, self.OnPlotMeter )
		self.m_button1811.Bind( wx.EVT_BUTTON, self.Fit_Meter )
		self.CT_notebook.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnNbookPageChange )
		self.m_button12.Bind( wx.EVT_BUTTON, self.OnLoadCTInf )
		self.m_button111.Bind( wx.EVT_BUTTON, self.OnCTSummary )
		self.m_button103.Bind( wx.EVT_BUTTON, self.OnLoadCTData )
		self.eqn_choice_CTratio.Bind( wx.EVT_CHOICE, self.OnCTratioModel )
		self.eqn_choice_CTphase.Bind( wx.EVT_CHOICE, self.OnCTphaseModel )
		self.row_spin3.Bind( wx.EVT_SPINCTRL, self.OnSetCTRows )
		self.row_spin3.Bind( wx.EVT_TEXT, self.OnSetCTRows )
		self.m_button23.Bind( wx.EVT_BUTTON, self.OnPlotCTratio )
		self.m_button231.Bind( wx.EVT_BUTTON, self.OnPlotCTphase )
		self.m_button183.Bind( wx.EVT_BUTTON, self.Fit_CTratio )
		self.m_button193.Bind( wx.EVT_BUTTON, self.Fit_CTphase )
		self.VT_notebook.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnNbookPageChange )
		self.m_button121.Bind( wx.EVT_BUTTON, self.OnLoadVTInf )
		self.m_button1111.Bind( wx.EVT_BUTTON, self.OnVTSummary )
		self.m_button1031.Bind( wx.EVT_BUTTON, self.OnLoadVTData )
		self.eqn_choice_VTratio.Bind( wx.EVT_CHOICE, self.OnVTratioModel )
		self.eqn_choice_VTphase.Bind( wx.EVT_CHOICE, self.OnVTphaseModel )
		self.row_spin31.Bind( wx.EVT_SPINCTRL, self.OnSetVTRows )
		self.row_spin31.Bind( wx.EVT_TEXT, self.OnSetCTRows )
		self.m_button232.Bind( wx.EVT_BUTTON, self.OnPlotVTratio )
		self.m_button2311.Bind( wx.EVT_BUTTON, self.OnPlotVTphase )
		self.m_button1831.Bind( wx.EVT_BUTTON, self.Fit_VTratio )
		self.m_button1931.Bind( wx.EVT_BUTTON, self.Fit_VTphase )
		self.m_notebook14.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnNbookPageChange )
		self.m_button14.Bind( wx.EVT_BUTTON, self.OnLoadSummary )
		self.Create_load_profile.Bind( wx.EVT_BUTTON, self.OnCreateLoadProfile )
		self.Plot_load_profile.Bind( wx.EVT_BUTTON, self.OnPlotLoadProfile )
		self.m_notebook15.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnNbookPageChange )
		self.m_button15.Bind( wx.EVT_BUTTON, self.OnLoadSiteInf )
		self.m_button112.Bind( wx.EVT_BUTTON, self.OnSiteSummary )
		self.Bind( wx.EVT_MENU, self.OnOpenFile, id = self.m_menuItem1.GetId() )
		self.Bind( wx.EVT_MENU, self.OnSave, id = self.m_menuItem2.GetId() )
		self.Bind( wx.EVT_MENU, self.OnPrint, id = self.m_menuItem10.GetId() )
		self.Bind( wx.EVT_MENU, self.OnPrintPreview, id = self.m_menuItem11.GetId() )
		self.Bind( wx.EVT_MENU, self.OnQuit, id = self.m_menuItem3.GetId() )
		self.Bind( wx.EVT_MENU, self.OnReportSelect, id = self.m_menuItem4.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMeterSelect, id = self.m_menuItem5.GetId() )
		self.Bind( wx.EVT_MENU, self.OnCTSelect, id = self.m_menuItem6.GetId() )
		self.Bind( wx.EVT_MENU, self.OnVTSelect, id = self.m_menuItem7.GetId() )
		self.Bind( wx.EVT_MENU, self.OnLoadSelect, id = self.m_menuItem8.GetId() )
		self.Bind( wx.EVT_MENU, self.OnSiteSelect, id = self.m_menuItem9.GetId() )
		self.Bind( wx.EVT_MENU, self.OnSnapshot, id = self.m_menuItem12.GetId() )
		self.Bind( wx.EVT_MENU, self.OnPrintSnap, id = self.m_menuItem13.GetId() )
		self.Bind( wx.EVT_MENU, self.OnClearAllGraphs, id = self.m_menuItem14.GetId() )
		self.Bind( wx.EVT_MENU, self.OnClearText, id = self.m_menuItem17.GetId() )
		self.Bind( wx.EVT_MENU, self.OnClearFiles, id = self.m_menuItem18.GetId() )
		self.Bind( wx.EVT_MENU, self.OnHelpTopic, id = self.m_menuItem15.GetId() )
		self.Bind( wx.EVT_MENU, self.OnAbout, id = self.m_menuItem16.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnNbookPageChange( self, event ):
		event.Skip()

	def OnAutoCalc( self, event ):
		event.Skip()

	def OnGUMcalc( self, event ):
		event.Skip()


	def OnLoadMeterInf( self, event ):
		event.Skip()

	def OnMeterSummary( self, event ):
		event.Skip()

	def OnSetMeterRows( self, event ):
		event.Skip()


	def OnMeterModel( self, event ):
		event.Skip()

	def OnLoadMeterData( self, event ):
		event.Skip()

	def OnPlotMeter( self, event ):
		event.Skip()

	def Fit_Meter( self, event ):
		event.Skip()


	def OnLoadCTInf( self, event ):
		event.Skip()

	def OnCTSummary( self, event ):
		event.Skip()

	def OnLoadCTData( self, event ):
		event.Skip()

	def OnCTratioModel( self, event ):
		event.Skip()

	def OnCTphaseModel( self, event ):
		event.Skip()

	def OnSetCTRows( self, event ):
		event.Skip()


	def OnPlotCTratio( self, event ):
		event.Skip()

	def OnPlotCTphase( self, event ):
		event.Skip()

	def Fit_CTratio( self, event ):
		event.Skip()

	def Fit_CTphase( self, event ):
		event.Skip()


	def OnLoadVTInf( self, event ):
		event.Skip()

	def OnVTSummary( self, event ):
		event.Skip()

	def OnLoadVTData( self, event ):
		event.Skip()

	def OnVTratioModel( self, event ):
		event.Skip()

	def OnVTphaseModel( self, event ):
		event.Skip()

	def OnSetVTRows( self, event ):
		event.Skip()


	def OnPlotVTratio( self, event ):
		event.Skip()

	def OnPlotVTphase( self, event ):
		event.Skip()

	def Fit_VTratio( self, event ):
		event.Skip()

	def Fit_VTphase( self, event ):
		event.Skip()


	def OnLoadSummary( self, event ):
		event.Skip()

	def OnCreateLoadProfile( self, event ):
		event.Skip()

	def OnPlotLoadProfile( self, event ):
		event.Skip()


	def OnLoadSiteInf( self, event ):
		event.Skip()

	def OnSiteSummary( self, event ):
		event.Skip()

	def OnOpenFile( self, event ):
		event.Skip()

	def OnSave( self, event ):
		event.Skip()

	def OnPrint( self, event ):
		event.Skip()

	def OnPrintPreview( self, event ):
		event.Skip()

	def OnQuit( self, event ):
		event.Skip()

	def OnReportSelect( self, event ):
		event.Skip()

	def OnMeterSelect( self, event ):
		event.Skip()

	def OnCTSelect( self, event ):
		event.Skip()

	def OnVTSelect( self, event ):
		event.Skip()

	def OnLoadSelect( self, event ):
		event.Skip()

	def OnSiteSelect( self, event ):
		event.Skip()

	def OnSnapshot( self, event ):
		event.Skip()

	def OnPrintSnap( self, event ):
		event.Skip()

	def OnClearAllGraphs( self, event ):
		event.Skip()

	def OnClearText( self, event ):
		event.Skip()

	def OnClearFiles( self, event ):
		event.Skip()

	def OnHelpTopic( self, event ):
		event.Skip()

	def OnAbout( self, event ):
		event.Skip()


###########################################################################
## Class MyFrame2
###########################################################################

class MyFrame2 ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 618,416 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( 617,415 ), wx.Size( 618,416 ) )

		bSizer10 = wx.BoxSizer( wx.VERTICAL )

		self.m_htmlWin2 = wx.html.HtmlWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 600,380 ), wx.html.HW_SCROLLBAR_AUTO )
		bSizer10.Add( self.m_htmlWin2, 0, wx.ALL, 5 )


		self.SetSizer( bSizer10 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnCloseH )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnCloseH( self, event ):
		event.Skip()


###########################################################################
## Class MyDialog1
###########################################################################

class MyDialog1 ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Help", pos = wx.DefaultPosition, size = wx.Size( 617,415 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer9 = wx.BoxSizer( wx.VERTICAL )

		self.m_htmlWin1 = wx.html.HtmlWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 600,380 ), wx.html.HW_SCROLLBAR_AUTO )
		bSizer9.Add( self.m_htmlWin1, 0, wx.ALL, 5 )


		self.SetSizer( bSizer9 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnCloseHelp )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnCloseHelp( self, event ):
		event.Skip()


