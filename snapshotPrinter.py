#######################################################################
# snapshotPrinter.py
#
# Created: 12/26/2007 by mld
#
# Description: Displays screenshot image using html and then allows
#              the user to print it.
#######################################################################
"""
An experimental module for taking an image of the displayed frame.  In practice
there are relatively simple alternatives.  The matplotlib tool bar now
functions for saving png images of plots.  The standard
"shift-ctrl-alt-prtscn" copies a frame image to the windows clipboard and this
can be pasted into Word or Excel for printing.  This module will probably be
removed unless there is a need to run the program on Linux.
"""
import os
import wx
from wx.html import HtmlEasyPrinting, HtmlWindow

class SnapshotPrinter(wx.Frame):
    """
    Experimental class for taking a snapshot of the GUI 'Frame'.  It is accessed
    through the 'Snapshot' item on the menu bar.
    """

    #----------------------------------------------------------------------
    def __init__(self, temp_path, title='Snapshot Printer'):
        wx.Frame.__init__(self, None, wx.ID_ANY, title, size=(900, 700))

        self.panel = wx.Panel(self, wx.ID_ANY)
        self.printer = HtmlEasyPrinting(name='Printing', parentWindow=None)
        self.temp_path = temp_path
        self.html = HtmlWindow(self.panel)
        self.html.SetRelatedFrame(self, self.GetTitle())

        if not os.path.exists(os.path.join(self.temp_path, 'screenshot.htm')):
            self.createHtml()
        self.createHtml()
        self.html.LoadPage(os.path.join(self.temp_path, 'screenshot.htm'))

        pageSetupBtn = wx.Button(self.panel, wx.ID_ANY, 'Page Setup')
        printBtn = wx.Button(self.panel, wx.ID_ANY, 'Print')
        cancelBtn = wx.Button(self.panel, wx.ID_ANY, 'Cancel')

        self.Bind(wx.EVT_BUTTON, self.onSetup, pageSetupBtn)
        self.Bind(wx.EVT_BUTTON, self.onPrint, printBtn)
        self.Bind(wx.EVT_BUTTON, self.onCancel, cancelBtn)

        sizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer.Add(self.html, 1, wx.GROW)
        btnSizer.Add(pageSetupBtn, 0, wx.ALL, 5)
        btnSizer.Add(printBtn, 0, wx.ALL, 5)
        btnSizer.Add(cancelBtn, 0, wx.ALL, 5)
        sizer.Add(btnSizer)

        self.panel.SetSizer(sizer)
        self.panel.SetAutoLayout(True)
##         self.Show()

    #----------------------------------------------------------------------
    def createHtml(self):
        """
        Creates an html file in the temp_path directory of the application
        that contains the information to display the snapshot. Note that page
        needs to be smaller than frame.
        """
        first = '<html>\n<body>\n<center><img src='
        second = ' width = 800 height = 600></center>\n</body>\n</html>'
        html = first +os.path.join(self.temp_path, 'myImage.png') +second
        f = open(os.path.join(self.temp_path, 'screenshot.htm'), 'w')
        f.write(html)
        f.close()

    #----------------------------------------------------------------------
    def onSetup(self, event):
        self.printer.PageSetup()

    #----------------------------------------------------------------------
    def onPrint(self, event):
        self.sendToPrinter()

    #----------------------------------------------------------------------
    def sendToPrinter(self):
        """
        Generates the html and prints it.
        """
        self.printer.GetPrintData().SetPaperId(wx.PAPER_LETTER)
        self.printer.PrintFile(self.html.GetOpenedPage())

    #----------------------------------------------------------------------
    def onCancel(self, event):
        self.Close()
