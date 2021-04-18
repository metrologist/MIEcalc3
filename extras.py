"""
This module is a convenient place to put code for managing the GUI and
I/O stuff.  Some features are still experimental/buggy.
"""

import wx
import wx.adv
from wx.html import HtmlWindow
import os
import sys
# import snapshotPrinter
from formbuild import MyFrame2 #for the help dialog
import csv
import xlrd  # for xls and xlsm
import openpyxl  # for xlsx and xlsxm
from PIL import Image

class RedirectText(object):
    """
    A thread-safe class for redirecting stdout/stderr.  It initialises with
    *aWxTextCtrl* to identify the text box to which the output is being
    directed.
    """
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self, string):
        """
        Writes 'string' to the text box using wx.CallAfter to manage thread issues.
        However, seems to prevent use of GetValue() to recover text, so disabled.
        """
        self.out.WriteText(string)
##         wx.CallAfter(self.out.WriteText, string) #remove CallAfter for no threads.

class VIEW(object):
    """
    A collection of methods for manipulating images required for reporting or
    printing out intermediate notebook pages. Also menu items for clearing
    graphs and displaying help.  Initiates with *frame* which is self from
    the MainFrame to ensure there is access to all GUI features.
    """
    def __init__(self, frame):
        self.frame = frame #need for screenshot

    def TakeScreenShot(self, temp_path):
        """
        Takes a screenshot of the screen at a given position and size and places
        it in myImage.png in directory *temp_path*.
        """
        rect = self.frame.GetRect()
        # see http://aspn.activestate.com/ASPN/Mail/Message/wxpython-users/3575899
        # created by Andrea Gavana
        # adjust widths for Linux (figured out by John Torres
        # http://article.gmane.org/gmane.comp.python.wxpython/67327)
    ## 	if sys.platform == 'linux2':
    ## 		client_x, client_y = self.ClientToScreen((0, 0))
    ## 		border_width = client_x - rect.x
    ## 		title_bar_height = client_y - rect.y
    ## 		rect.width += (border_width * 2)
    ## 		rect.height += title_bar_height + border_width
        #Create a DC for the whole screen area
        dcScreen = wx.ScreenDC()

        #Create a Bitmap that will hold the screenshot image later on
        #Note that the Bitmap must have a size big enough to hold the screenshot
        #-1 means using the current default colour depth
        bmp = wx.EmptyBitmap(rect.width, rect.height)

        #Create a memory DC that will be used for actually taking the screenshot
        memDC = wx.MemoryDC()

        #Tell the memory DC to use our Bitmap
        #all drawing action on the memory DC will go to the Bitmap now
        memDC.SelectObject(bmp)

        #Blit (in this case copy) the actual screen on the memory DC
        #and thus the Bitmap
        memDC.Blit(0, #Copy to this X coordinate
                0, #Copy to this Y coordinate
                rect.width, #Copy this width
                rect.height, #Copy this height
                dcScreen, #From where do we copy?
                rect.x, #What's the X offset in the original DC?
                rect.y  #What's the Y offset in the original DC?
                )

        #Select the Bitmap out of the memory DC by selecting a new
        #uninitialized Bitmap
        memDC.SelectObject(wx.NullBitmap)

        img = bmp.ConvertToImage()
        fileName = os.path.join(temp_path, "myImage.png")
        img.SaveFile(fileName, wx.BITMAP_TYPE_PNG)

    # def onPrint(self, temp_path):
    #     """
    #     Send screenshot to the printer using folder *temp_path* to hold a
    #     temporary copy of the file.
    #     """
    #     printer = snapshotPrinter.SnapshotPrinter(temp_path)
    #     printer.sendToPrinter()
    #     printer.Close()

    def scaleImage(self, image, size):
        """
        Takes an image file, *image*, resizes it to the size tuple of width and
        height in *size* and writes the scaled image to the file name with a
        '1' appended.
        """
        image_file = image
        img_org = Image.open(image_file)
        # get the size of the original image
        #width_org, height_org = img_org.size
        # set the resizing factor so the aspect ratio can be retained
        # factor > 1.0 increases size
        # factor < 1.0 decreases size
        #factor = scale
        width = int(size[0])
        height = int(size[1])
        # best down-sizing filter
        img_anti = img_org.resize((width, height), Image.ANTIALIAS)
        # split image filename into name and extension
        image1_file = image_file[:-4]+'1.png'
        img_anti.save(image1_file)


    def OnAboutBox(self):
        """
        Presents basic creator/copyright information when the 'About
        MIEcalculator' option is slected from the 'Help' menu bar item.
        """
        description = """MIEcalculator calculates the error and uncertainty for a metering installation.
    """

        licence = """This version is provided for teaching purposes in MSL's 'Traceable Electrical Energy Metering' workshop.

    MIEcalculator is provided in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

    The code is written in Python 3.9.2.  It uses open source modules GTC, wxPython,
    matplotlib, scipy, numpy, xlrd, openpyxl and python-docx. It also uses Python modules developed for
    Gum Tree Calculator (GTC 0.9.8).
    """

        info = wx.adv.AboutDialogInfo()
    ##     info.SetIcon(wx.Icon('hunter.png', wx.BITMAP_TYPE_PNG))
        info.SetName('MIEcalculator')
        info.SetVersion('1.1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2011-2021 Measurement Standards Laboratory of New Zealand')
        info.SetWebSite('https://measurement.govt.nz')
        info.SetLicence(licence)
        info.AddDeveloper('Keith Jones (keith.jones@measurement.govt.nz)')
        wx.adv.AboutBox(info)

    def OnHelp(self):
        """
        Displays html help file.
        """
    #     dialog = bare_gui.MyDialog1(None)
        dialog = MyFrame2(None)
    ##     html = dialog.m_htmlWin1
        html = dialog.m_htmlWin2
        name = os.path.join(self.frame.cwd, 'Help', 'UserGuide.htm')
        html.LoadPage(name)
        dialog.Show()
    ##     dialog.ShowModal()
    ##     dialog.Destroy()

    def OnClose(self):
        print('closing dialog')
    ##     self.dialog.Destroy()
    ##     self.Destroy()

    def ClearText(self):
        """
        Clears textctrl, all richtextctrls and all grids for both data input and
        result displays.  After the fit_grids are cleared it is essential to reload
        the initial coefficient information using using the calls to the selected
        models.
        """
        self.frame.m_textCtrl3.Clear()
        self.frame.report_richText.Clear()
        self.frame.meter_richText.Clear()
        self.frame.CT_richText.Clear()
        self.frame.CT_richText1.Clear()
        self.frame.VT_richText.Clear()
        self.frame.VT_richText1.Clear()
        self.frame.load_richText.Clear()
        self.frame.site_richText.Clear()
        self.frame.load_data.Clear()
        self.frame.load_values.Clear()

        self.frame.file_table.ClearGrid()

        self.frame.meter_table.ClearGrid()
        self.frame.meter_data.ClearGrid()
        self.frame.Meter_fit_grid.ClearGrid()
        self.frame.onMeterModel()

        self.frame.CT_table.ClearGrid()
        self.frame.CT_table1.ClearGrid()
        self.frame.CTratio_data.ClearGrid()
        self.frame.CTphase_data.ClearGrid()
        self.frame.CTratio_fit_grid.ClearGrid()
        self.frame.onCTratioModel()
        self.frame.CTphase_fit_grid.ClearGrid()
        self.frame.onCTphaseModel()

        self.frame.VT_table.ClearGrid()
        self.frame.VT_table1.ClearGrid()
        self.frame.VTratio_data.ClearGrid()
        self.frame.VTphase_data.ClearGrid()
        self.frame.VTratio_fit_grid.ClearGrid()
        self.frame.onVTratioModel()
        self.frame.VTphase_fit_grid.ClearGrid()
        self.frame.onVTphaseModel()

        self.frame.site_table.ClearGrid()

class EXCEL(object):
    """
    Reads data from Excel and converts into csv files.
    """

    def excel_to_csv(self, directory, excel_input):
        """
        This reads an xls spread sheet, *excel input* in *directory*, formatted
        to hold all metering input information.The format matches that
        for the 11 csv files that are produced when the data is loaded directly
        into the grids in the GUI.  Excel uses 11 worksheets and each worksheet
        is converted to its corresponding csv file for feeding into MIEcalculator.

        The workbook must have worksheets named meter, meter_inf, VT, VTe_inf,
        VTp_inf, CT, CTe_inf, CTp_inf, site_inf and load.
        """
        wb = xlrd.open_workbook(os.path.join(directory, excel_input))
        sheet_names = wb.sheet_names()
        target_names = ['project', 'meter', 'meter_inf', 'VT', 'VTe_inf', 'VTp_inf',
        'CT', 'CTe_inf', 'CTp_inf', 'site_inf', 'load']
        a = set(target_names)
        assert len(a.intersection(sheet_names)) == len(target_names), 'missing worksheet(s)?'
        dirname = os.path.join(directory, 'xls_temp')

        try:
            os.makedirs(dirname)
        except OSError:
            if os.path.isdir(dirname):
                pass
            else:
                # There was an error on creation, so make sure we know about it
                raise

        # should allow for project page to have variations on the file names
        sh = wb.sheet_by_name(target_names[0])
        file_names = [u'project.csv'] #start with default project.csv
        for rownum in range(sh.nrows):
            file_names.append(sh.row_values(rownum)[0])

        for i in range(len(file_names)):
            sh = wb.sheet_by_name(target_names[i])
            with open(os.path.join(dirname, file_names[i]), 'w', newline='') as f:
                if file_names[i][-3:] == 'csv':
                    c = csv.writer(f)
                elif file_names[i][-3:] == 'txt': #txt file will be tab delimited
                    c = csv.writer(f, dialect='excel-tab')
                for r in range(sh.nrows):
                    c.writerow(sh.row_values(r))

    def excelx_to_csv(self, directory, excel_input):
        """
        As for excel_to _csv but using openpyxl for xlsm and xlsx spreadsheets.
        :param directory: Usually the xls_tmp directory
        :param excel_input:  Excel file name
        :return:
        """
        wb = openpyxl.load_workbook(os.path.join(directory, excel_input), data_only=True)
        sheet_names = wb.sheetnames
        target_names = ['project', 'meter', 'meter_inf', 'VT', 'VTe_inf', 'VTp_inf',
                        'CT', 'CTe_inf', 'CTp_inf', 'site_inf', 'load']
        a = set(target_names)
        assert len(a.intersection(sheet_names)) == len(target_names), 'missing worksheet(s)?'
        dirname = os.path.join(directory, 'xls_temp')

        try:
            os.makedirs(dirname)
        except OSError:
            if os.path.isdir(dirname):
                pass
            else:
                # There was an error on creation, so make sure we know about it
                raise

        # should allow for project page to have variations on the file names
        sh = wb[target_names[0]]
        file_names = [u'project.csv']  # start with default project.csv
        for row in sh.values:
            file_names.append(row[0])
        for i in range(len(file_names)):
            sh = wb[target_names[i]]
            with open(os.path.join(dirname, file_names[i]), 'w', newline='') as f:
                if file_names[i][-3:] == 'csv':
                    c = csv.writer(f)
                elif file_names[i][-3:] == 'txt': #txt file will be tab delimited
                    c = csv.writer(f, dialect='excel-tab')
                for r in sh.values:
                    c.writerow(r)