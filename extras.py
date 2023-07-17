"""
This module is a convenient place to put code for managing the GUI and
I/O stuff.  Some features are still experimental/buggy.
"""

import wx
import wx.adv
import os
from formbuild import MyFrame2  # for the help dialog
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
        self.frame = frame  # need it for screenshot

    def scaleImage(self, image, size):
        """
        Takes an image file, *image*, resizes it to the size tuple of width and
        height in *size* and writes the scaled image to the file name with a
        '1' appended.
        """
        image_file = image
        img_org = Image.open(image_file)
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

    The code is written in Python 3.10.11.  It uses open source modules GTC, wxPython,
    matplotlib, scipy, numpy, xlrd, openpyxl and python-docx.
    """

        info = wx.adv.AboutDialogInfo()
    ##     info.SetIcon(wx.Icon('hunter.png', wx.BITMAP_TYPE_PNG))
        info.SetName('MIEcalculator')
        info.SetVersion('1.1.1')
        info.SetDescription(description)
        info.SetCopyright('(C) 2011-2023 Measurement Standards Laboratory of New Zealand')
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
        'CT', 'CTe_inf', 'CTp_inf', 'site_inf', 'load']  # picking up alternative load tab for .xls
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
                        'CT', 'CTe_inf', 'CTp_inf', 'site_inf', 'load']  # alternative load tab for xlsx

        # need to know how many load files exist
        if 'project' in sheet_names:  # if not, nothing will work!
            temp_file_list = []  # just looking for the txt files at this stage
            sh = wb['project']
            for row in sh.values:
                temp_file_list.append(row[0])
            nmb_profiles = 0
            for x in temp_file_list:
                if x[-3:]=='txt':
                    nmb_profiles += 1
        else:
            print('incorrectly formatted spreadsheet')
            raise
        # self.nmb_profiles is now set

        if nmb_profiles > 1:
            print('adding load names')  # does not print, stdout not redirected yet?
            for i in range(1, nmb_profiles):
                target_names.append('load' + str(i))

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