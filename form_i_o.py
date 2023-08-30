import wx
from formgraphs import GraphForm
import functions
import os
import sys
import csv
import extras
from numpy import zeros, sqrt
from utility import UTILITY


class IOForm(GraphForm):

    def __init__(self, parent):
        """
        Handles data in  and out of the GUI
        """
        GraphForm.__init__(self, parent)
        self.proj_file = 'bbb'
        self.dirname = 'ccc'
        self.projwd = r'no path'  # must avoid accidental deletion with clearing temporary files
        # forcing default equation choice for properly filled in grid
        self.model = functions.MODEL('for_labels')
        self.eqn_choice_CTratio.SetSelection(2)
        self.log_line(self.CTratio_staticText, self.CTratio_fit_grid)
        self.eqn_choice_CTphase.SetSelection(2)
        self.log_line(self.CTphase_staticText, self.CTphase_fit_grid)
        self.eqn_choice_VTratio.SetSelection(1)
        self.straight_line(self.VTratio_staticText, self.VTratio_fit_grid)
        self.eqn_choice_VTphase.SetSelection(1)
        self.straight_line(self.VTphase_staticText, self.VTphase_fit_grid)
        self.eqn_choice_Meter.SetSelection(3)
        self.tan_surface2(self.Meter_staticText, self.Meter_fit_grid)
        self.report_txt = []  # list of strings for writing to the reports
        self.report_images = []  # list of image buffers for pasting graphs in word report
        self.report_images_wx = []  # list of scaled wx images for placing in wx.richtext
        self.profile_list = []  # in anticipation of having more than one load profile as a txt file
        self.error_list = []  # in anticipation of having more than one error profile selected region?
        self.n_profiles = 1  # assume a default of one load profile before a spreadsheet is loaded
        self.csv_profile = ['_load.csv']  # a matching set of csv files for the processed normalised load profiles
        self.iec = '-'  # iec class will be in the input file for newer projects (August 2023 onwards)
    def OnOpenFile(self, event):
        """
        Opens either a csv file with a list of component csv files, or opens
        an excel spreadsheet formatted so that component csv files can be
        created.  All data is read in from the component csv files.
        """
        # In this case, the dialog is created within the method because
        # the directory name, etc, may be changed during the running of the
        # application. In theory, you could create one earlier, store it in
        # your frame object and change it when it was called to reflect
        # current parameters / values
        wildcard = "Project source (*.csv; *.xls; *.xlsx; *.xlsm)|*.csv;*.xls; *.xlsx; *.xlsm|" \
                   "All files (*.*)|*.*"

        dlg = wx.FileDialog(self, "Choose a project file", self.dirname, "", wildcard, wx.FD_OPEN | wx.FD_MULTIPLE)

        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilenames()[0]
            dirname = dlg.GetDirectory()
            self.proj_file = os.path.join(dirname, filename)
            self.m_statusBar1.SetStatusText(filename, 1)
            self.projwd = dirname  # remember the project working directory
            print('Reading data ... please wait.')
            if filename[-3:] == 'xls':
                # extras.EXCEL().excel_to_csv(dirname, filename)
                extras.EXCEL().excelx_to_csv(dirname, filename, False)  # false for xls not xlsx
                filename = 'project.csv'  # default output of excel_to_csv
                dirname = os.path.join(dirname, 'mie_temp')
                self.projwd = dirname
            elif filename[-4:] == 'xlsx' or filename[-4:] == 'xlsm':
                extras.EXCEL().excelx_to_csv(dirname, filename, True)  # true for xlsx not xls
                filename = 'project.csv'  # default output of excel_to_csv
                dirname = os.path.join(dirname, 'mie_temp')
                self.projwd = dirname
            if dirname is None:  # this happens if no selection is made so an error arises from the next steps
                dlg.Destroy()
            else:
                # now read information from the selected or created csv file and place in file table
                self.LoadProjFiles(os.path.join(dirname, filename))
                self.m_staticText22.SetLabel('Project directory:  ' + self.projwd)
                self.m_textCtrl999.WriteText(self.projwd)
                self.m_button26.Enable(True)  # 'Process project file' button available once file is loaded
                self.m_button26.SetBackgroundColour(colour='GREEN')
                dlg.Destroy()
                # shift focus to the processing page
                self.BookSelect('Main/Report notebook')  # defaults to the Main/Report notebook (was called Report Notebook)
                self.m_notebook1.ChangeSelection(0)  # defaults to the 'Main' tab



    def LoadProjFiles(self, proj_file):
        """
        The list of file names held in *proj_file* is loaded into the GUI
        file_table.  All calls for input data should call the names in this
        table.  There is no error checking!!!
        """
        # assume a new calculation is wanted, so clear all old inputs/outputs stored in GUI and temp files
        self.profile_list = []  # reset for repeat loading, otherwise it continues to increment
        self.error_list = []  # reset for repeat loading, otherwise it continues to increment?
        self.pushClearAllGraphs()
        self.PushClearText()
        self.report_text = []  # these 3 report lists need to be reset, otherwise get the old report with the new data!
        self.report_images = []
        self.report_images_wx = []
        reader = csv.reader(open(proj_file, 'r'))
        project_files = []
        for row in reader:
            project_files.append(row)
        for i in range(len(project_files)):
            if project_files[i][0][-3:]=='txt':  # the load files must be all at the end and are added as a list
                self.profile_list.append(os.path.join(self.projwd, project_files[i][0]))
            else:
                self.file_table.SetCellValue(i, 0, project_files[i][0])
        self.n_profiles = len(self.profile_list)  # have now confirmed the number of profiles to calculate
        self.file_table.SetCellValue(len(project_files) - len(self.profile_list), 0, repr(self.profile_list))
        # can now create the multiple plot axes for the load
        self.Create3DGraph(self.load_graph, self.n_profiles, 'load_axes_3D')
        # noting that the 'load' file calculation is different, set up for
        # choice of *.txt for plotting csv from e_data folder or directly from
        # the csv file.
        name = self.file_table.GetCellValue(9, 0)
        if name[-3:] == 'csv':
            self.load_values.SetValue(os.path.join(self.projwd, name))
            self.load_data.SetValue('')  # no raw txt file

        elif name[-1:] == "]":  # have now reached the list of load files, just go back to the list
            self.csv_profile = []
            for prof in self.profile_list:  # create a matching list of csv loadcsvfiles
                self.csv_profile.append(prof[:-3] + 'csv')
            self.load_values.SetValue(repr(self.csv_profile))
            self.load_data.SetValue(repr(self.profile_list))
        else:
            print('problem with load file!!', project_files)


    def OnClearFiles(self, event):
        self.PushClearFiles()

    def PushClearFiles(self):
        """
        Files that have been created in the mie_temp directory are deleted.  This
        is good house-keeping and avoids hiding bugs that prevent a new csv
        data file from being created.
        """
        folder = self.projwd
        if folder != 'no path':
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except OSError:
                    print("OS error:", sys.exc_info()[0])
        else:
            print("No working folder, files not cleared")

    def OnMeterModel(self, event):
        self.onMeterModel()

    def onMeterModel(self):
        """
        Set up fitting info for meter function chosen in 'choice box'.
        """
        choice = str(self.eqn_choice_Meter.GetSelection())[0]  # first character
        label_options = {'0': self.smean_only, '1': self.flat_plane, '2': self.tan_surface1, '3': self.tan_surface2}
        label_options[choice](self.Meter_staticText, self.Meter_fit_grid)

    def OnCTratioModel(self, event):
        self.onCTratioModel()

    def onCTratioModel(self):
        """
        Set up fitting info for CT ratio function chosen in 'choice box'.
        """
        choice = str(self.eqn_choice_CTratio.GetSelection())[0]  # first character
        label_options = {'0': self.mean_only, '1': self.straight_line, '2': self.log_line}
        label_options[choice](self.CTratio_staticText, self.CTratio_fit_grid)

    def OnCTphaseModel(self, event):
        self.onCTphaseModel()

    def onCTphaseModel(self):
        """
        Set up fitting info for CT phase function chosen in 'choice box'.
        """
        choice = str(self.eqn_choice_CTphase.GetSelection())[0]  # first character
        label_options = {'0': self.mean_only, '1': self.straight_line, '2': self.log_line}
        label_options[choice](self.CTphase_staticText, self.CTphase_fit_grid)

    def OnVTratioModel(self, event):
        self.onVTratioModel()

    def onVTratioModel(self):
        """
        Sset up fitting info for VT ratio function chosen in 'choice box'.
        """
        choice = str(self.eqn_choice_VTratio.GetSelection())[0]  # first character
        label_options = {'0': self.mean_only, '1': self.straight_line, '2': self.log_line}
        label_options[choice](self.VTratio_staticText, self.VTratio_fit_grid)

    def OnVTphaseModel(self, event):
        self.onVTphaseModel()

    def onVTphaseModel(self):
        """
        Set up fitting info for VT phase function chosen in 'choice box'.
        """
        choice = str(self.eqn_choice_VTphase.GetSelection())[0]  # first character
        label_options = {'0': self.mean_only, '1': self.straight_line, '2': self.log_line}
        label_options[choice](self.VTphase_staticText, self.VTphase_fit_grid)

    def mean_only(self, static, grid):
        """
        Sets correct size of *grid* for the 'f_mean' function and sets the
        *static* label.
        """
        static.SetLabel(self.model.f_mean.label)
        self.fitting_grid_layout(grid, self.model.f_mean.no)

    def smean_only(self, static, grid):
        """
        Sets correct size of *grid* for the 's_mean' function and sets the
        *static* label.
        """
        static.SetLabel(self.model.f_smean.label)
        self.fitting_grid_layout(grid, self.model.f_smean.no)

    def straight_line(self, static, grid):  # one option on laying out table
        """
        Sets correct size of *grid* for the 'f_line' function and sets the
        *static* label.
        """
        # writes equation as static text
        static.SetLabel(self.model.f_line.label)
        # sets up table size for reporting fit
        self.fitting_grid_layout(grid, self.model.f_line.no)

    def log_line(self, static, grid):
        """
        Sets correct size of *grid* for the 'f_logline' function and sets the
        *static' label*.
        """
        static.SetLabel(self.model.f_logline.label)
        self.fitting_grid_layout(grid, self.model.f_logline.no)

    def flat_plane(self, static, grid):  # one option on laying out table
        """
        Sets correct size of *grid* for the 'f_plane' function and sets the
        *static* label.
        """
        # writes equation as static text
        static.SetLabel(self.model.f_plane.label)
        self.fitting_grid_layout(grid, self.model.f_plane.no)

    def tan_surface1(self, static, grid):
        """
        Sets correct size of *grid* for the 'f_tan_s1' function and sets the
        *static* label.
        """
        # writes equation as static text
        static.SetLabel(self.model.f_tan_s1.label)
        self.fitting_grid_layout(grid, self.model.f_tan_s1.no)

    def tan_surface2(self, static, grid):
        """
        Sets correct size of *grid* for the 'f_tan_s2' function and sets the
        *static* label.
        """
        # writes equation as static text
        static.SetLabel(self.model.f_tan_s2.label)
        self.fitting_grid_layout(grid, self.model.f_tan_s2.no)

    def fitting_grid_layout(self, grid_name, no_of_params):
        """
        Lays out grid, *grid_name*, for displaying fit parameter results with
        *no_of_params* coefficients.
        """
        # no_of_params = len(param_set)
        # force grid reduction before re-sizing
        no_of_rows = 5 + 2 * no_of_params
        if no_of_params < 3:
            no_of_cols = 4
        else:
            no_of_cols = no_of_params + 1
        # essential to set columns before rows, but why?????
        self.SetGridCols(grid_name, no_of_cols)
        self.SetGridRows(grid_name, no_of_rows)
        grid_name.SetCellValue(0, 1, 'initial value')
        grid_name.SetCellValue(0, 2, 'returned value')
        grid_name.SetCellValue(0, 3, 'stdev')
        grid_name.SetCellValue(1 + no_of_params, 0, 'b0')
        grid_name.SetCellValue(1 + no_of_params, 2, '0.0')
        grid_name.SetCellValue(2 + no_of_params, 0, 'dof')
        grid_name.SetCellValue(3 + no_of_params, 0, 'red chisq')
        grid_name.SetCellValue(4 + no_of_params, 0, 'cov')
        for i in range(no_of_params):
            grid_name.SetCellValue(i + 1, 0, str('a' + str(i)))
            grid_name.SetCellValue(i + 1, 1, '0.0')
            grid_name.SetCellValue(i + 5 + no_of_params, 0, str('a' + str(i)))
        for j in range(no_of_params):
            grid_name.SetCellValue(4 + no_of_params, j + 1, str('a' + str(j)))

    def fitting_grid_results(self, grid_name, parameters, dof, red_chisq, cov, ub):
        """
        Puts calculated results,(*parameters*, *dof*, *red_chisq*, *cov*, *ub*
        in the selected display grid, *grid_name*.
        """
        no_of_params = len(parameters)
        grid_name.SetCellValue(1 + no_of_params, 3, repr(ub))
        grid_name.SetCellValue(2 + no_of_params, 1, repr(dof))
        grid_name.SetCellValue(3 + no_of_params, 1, repr(red_chisq))
        for i in range(no_of_params):
            grid_name.SetCellValue(i + 1, 2, repr(parameters[i]))
            grid_name.SetCellValue(i + 1, 3, repr(sqrt(cov[i, i])))
            for j in range(no_of_params):
                grid_name.SetCellValue(i + 5 + no_of_params, j + 1, repr(cov[i, j]))

    def get_2Dgrid_data(self, grid_name):
        """
        Loads X, Y, u data from the input grid, *grid_name* into arrays for
        calculation purposes.
        """
        n = grid_name.GetNumberRows()
        X = zeros(n)
        Y = zeros(n)
        uy = zeros(n)
        k = zeros(n)
        for i in range(n):
            X[i] = float(grid_name.GetCellValue(i, 0))
            Y[i] = float(grid_name.GetCellValue(i, 1))
            uy[i] = float(grid_name.GetCellValue(i, 2))
            k[i] = float(grid_name.GetCellValue(i, 3))
        return n, X, Y, uy, k

    def get_3Dgrid_data(self, grid_name):
        """
        Loads X, Y, Z, u data from the input grid, *grid_name*, into arrays for
        calculation.
        """
        # note that X contains x,y pairs!
        n = grid_name.GetNumberRows()
        X = zeros((n, 2))
        Z = zeros(n)
        uz = zeros(n)
        k = zeros(n)
        for i in range(n):
            X[i, 0] = float(grid_name.GetCellValue(i, 0))
            X[i, 1] = float(grid_name.GetCellValue(i, 1))
            Z[i] = float(grid_name.GetCellValue(i, 2))
            uz[i] = float(grid_name.GetCellValue(i, 3))
            k[i] = float(grid_name.GetCellValue(i, 4))
        return n, X, Z, uz, k

    def get_params(self, n, grid_name):
        """
        Loads *n* intitial values of coefficients from the input grid,
        *grid_name* into PARAMETER classes for starting the least-squares
        calculation.
        """
        p = list()
        for i in range(n):
            value = float(grid_name.GetCellValue(i + 1, 1))
            name = grid_name.GetCellValue(i + 1, 0)
            a = functions.PARAMETER(value, name)
            p.append(a)
        return p

    def OnLoadCTData(self, event):  # from CT notebook
        self.PushLoadCTData()

    def PushLoadCTData(self):
        """
        Loads CT data from csv file to the GUI grid.
        """
        data = os.path.join(self.projwd, self.file_table.GetCellValue(5, 0))
        self.LoadTGrid(self.CTratio_data, self.CTphase_data, data, self.CT_richText)

    def OnLoadVTData(self, event):  # from VT notebook
        self.PushLoadVTData()

    def PushLoadVTData(self):
        """
        Loads VT data from csv file to the GUI grid.
        """
        data = os.path.join(self.projwd, self.file_table.GetCellValue(2, 0))
        self.LoadTGrid(self.VTratio_data, self.VTphase_data, data, self.VT_richText)

    def OnLoadMeterData(self, event):  # from meter notebook
        self.PushLoadMeterData()

    def PushLoadMeterData(self):
        """
        Loads meter data from csv file to the GUI grid.
        """
        data = os.path.join(self.projwd, self.file_table.GetCellValue(0, 0))
        self.LoadGrid(self.meter_data, data)

    def OnLoadMeterInf(self, event):  # from meter notebook
        self.PushLoadMeterInf()

    def PushLoadMeterInf(self):
        """
        Loads meter influence data from csv file to the GUI grid.
        """
        data = os.path.join(self.projwd, self.file_table.GetCellValue(1, 0))
        self.LoadGrid(self.meter_table, data)

    def OnLoadCTInf(self, event):  # from CT notebook
        self.PushLoadCTInf()

    def PushLoadCTInf(self):
        """
        Loads CT influence data from csv file to the GUI grid.
        """
        data = os.path.join(self.projwd, self.file_table.GetCellValue(6, 0))
        data1 = os.path.join(self.projwd, self.file_table.GetCellValue(7, 0))
        self.LoadGrid(self.CT_table, data)  # error terms
        self.LoadGrid(self.CT_table1, data1)  # phase terms

    def OnLoadVTInf(self, event):  # from VT notebook
        self.PushLoadVTInf()

    def PushLoadVTInf(self):
        """
        Loads VT influence data from csv file to the GUI grid.
        """
        data = os.path.join(self.projwd, self.file_table.GetCellValue(3, 0))
        data1 = os.path.join(self.projwd, self.file_table.GetCellValue(4, 0))
        self.LoadGrid(self.VT_table, data)  # error terms
        self.LoadGrid(self.VT_table1, data1)  # phase terms

    def OnLoadSiteInf(self, event):  # from meter notebook
        self.PushLoadSiteInf()

    def PushLoadSiteInf(self):
        """
        Loads site data from csv file to the GUI grid.
        """
        data = os.path.join(self.projwd, self.file_table.GetCellValue(8, 0))
        self.LoadGrid(self.site_table, data)

    def SaveGrid(self, grid_name, file_name):
        """
        Saves any grid, *grid_name*, to any file, *file_name* as a csv file.
        """
        writer = csv.writer(open(file_name, 'wb'))  # assumes file exists
        a = (grid_name.GetNumberRows(), grid_name.GetNumberCols())
        writer.writerow(a)  # header is no. of rows, no. of columns
        for i in range(grid_name.GetNumberRows()):
            a = list()
            for j in range(grid_name.GetNumberCols()):
                a.append(grid_name.GetCellValue(i, j))
            writer.writerow(a)
        # The approach can be extended to a 'save project'/'load project'
        # by either having a list of files or a single appended file for all.
        # LoadGrid and SaveGrid must stay compatible.

    def LoadGrid(self, grid_name, file_name):
        """
        Loads a csv file, *file_name*, to a grid, *grid_name*.  The csv file
        starts with the number of rows and columns required in the grid.  There
        is no checking that the file is formatted correctly.
        """
        reader = csv.reader(open(file_name, 'r'))  # assumes file exists
        # need to read row, col, set size of grid, then load grid
        rownum = 0  # starting reference
        for row in reader:
            if rownum == 0:
                header = row  # extracts grid size info in header
                if file_name[-9:] == 'meter.csv':  # looking for the IEC class in the meter.csv file
                    if header[2]!= '':  # old projects should be blank
                        self.iec = header[2]  # the meter file has the IEC class following the row/column count
                    else:
                        self.iec = '-'
                no_rows = int(float(header[0]))  # int(float()) needed to cope with csv
                no_columns = int(float(header[1]))
                self.SetGridRows(grid_name, no_rows)
            else:
                if rownum <= no_rows:  # in case csv file has final blank rows
                    for i in range(no_columns):
                        grid_name.SetCellValue(rownum - 1, i, row[i])
                else:
                    return
            rownum += 1
        # need to consider error checks on file!..k in table, header row!!

    def LoadTGrid(self, grid_real, grid_phase, file_name, text):
        """
        Loads a transformer csv file, *file_name*, to 2 grids, *grid_real* and
        *grid_phase*.
        """
        reader = csv.reader(open(file_name, 'r'))  # assumes file exists
        # need to read row, col, set size of grid, then load grid
        rownum = 0  # starting reference
        for row in reader:
            if rownum == 0:
                text.AppendText(repr(row))  # puts header on summary page
            else:
                if rownum == 1:
                    header = row  # extracts grid size info in header
                    no_rows = int(float(header[0]))
                    no_columns = int(float(header[1]))
                    self.SetGridRows(grid_real, no_rows)
                    self.SetGridRows(grid_phase, no_rows)
                else:
                    if rownum <= no_rows + 1:  # in case csv file has final blank rows
                        for i in range(no_columns - 3):
                            grid_real.SetCellValue(rownum - 2, i, row[i])
                            if i == 0:
                                grid_phase.SetCellValue(rownum - 2, i, row[i])
                        for i in range(no_columns - 3, no_columns):
                            grid_phase.SetCellValue(rownum - 2, i - 3, row[i])
                    else:
                        return
            rownum += 1
        # need to consider error checks on file!

    def OnAbout(self, event):
        """
        About Box *event*.
        """
        extras.VIEW(self).OnAboutBox()

    def OnHelpTopic(self, event):
        """
        Help file *event*.
        """
        extras.VIEW(self).OnHelp()

    def OnCloseHelp(self, event):
        """
        Close help *event*.
        """
        extras.VIEW(self).OnClose()

    def OnCloseH(self, event):
        extras.VIEW(self).OnClose()

    def OnClearText(self, event):
        """
        Clear text *event*.
        """
        self.PushClearText()
    def PushClearText(self):
        extras.VIEW(self).ClearText()

    def OnLoadUtility(self, event):
        print('Load utility')
        dialog = UTILITY(None)
        dialog.Show()

if __name__ == '__main__':
    app = wx.App()
    frame = IOForm(None)
    frame.Show()
    app.MainLoop()
