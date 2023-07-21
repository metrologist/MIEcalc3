import wx
from reporting import REPORT
import csv
import components as comp
import functions
import numpy as np
import warnings
from scipy.stats import t
import extras
import sys


class MIECALC(REPORT):

    def __init__(self, parent):
        """
        Adds the overall calculation process.
        """
        REPORT.__init__(self, parent)
        log = self.m_textCtrl3  # where stdout will be redirected
        redir = extras.RedirectText(log)
        sys.stdout = redir
        sys.stderr = redir  # not sure this is desirable for normal users, but helps with debugging
        self.m_button26.Enable(False)  # 'Process project file' button initially greyed out


    #######################Creating Summary Files###########################
    def OnMeterSummary(self, event):
        self.PushMeterSummary()

    def PushMeterSummary(self):
        """
        Button to create csv summary file for meter.
        """
        self.create_summary(self.eqn_choice_Meter, self.meter_table, self.Meter_fit_grid, self.meter_richText, 'meter',
                            self.e_data('_meter.csv'))

    def create_site_inf_summary(self, table, text, sfile):
        """
        This is a special case of *create_summary* as the site only has influence
        variables.  It could be made a conditional subset of create_summary.
        Creates a csv *sfile* from the data in *table* and also displays it in the
        relevant *text* window.
        """
        writer = csv.writer(open(sfile, 'w', newline=''), 'excel')
        row = []
        text.Clear()
        text.AppendText(sfile)
        row.append(sfile)
        writer.writerow(row)
        text.Newline()
        row = []
        table_rows = table.GetNumberRows()
        for i in range(table_rows):
            self.both(row, text, str(table.GetCellValue(i, 1)))
            self.both(row, text, (str(table.GetCellValue(i, 3))))
            self.both(row, text, str(table.GetCellValue(i, 5)))
            self.both(row, text, table.GetCellValue(i, 0))
            text.Newline()
            writer.writerow(row)
            row = []

    def create_summary(self, choice, table, grid, text, component, cfile):
        """
        Primarily produces a csv file of coefficients and influences for use
        in COMPONENT classes.  Fitting coefficients are from *grid* and
        influence data is from *table*.The content of the csv file, *cfile* is
        echoed in the rich text box, *text*.  Note that this is where the degrees
        of freedom for *b0*, the bias coefficient, are set to 50.
        """
        writer = csv.writer(open(cfile, 'w', newline=''), 'excel')
        row = []
        text.Clear()
        text.AppendText(cfile)
        row.append(cfile)
        writer.writerow(row)
        text.Newline()
        row = []
        text.AppendText(str(choice.GetSelection()))
        row.append(choice.GetSelection())
        writer.writerow(row)
        text.Newline()
        row = []
        gridrows = grid.GetNumberRows()
        no_coeffs = int((gridrows - 5) / 2.0)
        for i in range(no_coeffs):
            self.both(row, text, grid.GetCellValue(i + 1, 2))
            self.both(row, text, grid.GetCellValue(i + 1, 3))
            self.both(row, text, grid.GetCellValue(no_coeffs + 2, 1))
            self.both(row, text, grid.GetCellValue(i + 1, 0) + ' ' + component)
            text.Newline()
            writer.writerow(row)
            row = []
        # get the covariance matrix
        a = no_coeffs + 5  # a and b are grid offsets
        b = 1
        for i in range(no_coeffs):
            for j in range(no_coeffs):
                self.both(row, text, grid.GetCellValue(a + i, b + j))

        text.Newline()
        writer.writerow(row)
        row = []
        self.both(row, text, str(grid.GetCellValue(no_coeffs + 1, 2)))
        self.both(row, text, str(grid.GetCellValue(no_coeffs + 1, 3)))
        self.both(row, text, '50')  # force d.o.f. for b0
        self.both(row, text, grid.GetCellValue(no_coeffs + 1, 0) + ' ' + component)
        text.Newline()
        writer.writerow(row)
        row = []
        table_rows = table.GetNumberRows()
        for i in range(table_rows):
            self.both(row, text, str(table.GetCellValue(i, 1)))
            self.both(row, text, (str(table.GetCellValue(i, 3))))
            self.both(row, text, str(table.GetCellValue(i, 5)))
            self.both(row, text, table.GetCellValue(i, 0))
            text.Newline()
            writer.writerow(row)
            row = []

    def JoinErrorPhase(self, error, phase, joined):
        """
        Concatenates the *error* and *phase* files produced by 'create_summary'
        into the single *joined* file that does not include the header row of the
        phase file.  This is overhead management to produce the required csv file.
        """
        reader1 = csv.reader(open(error, 'r'))
        reader2 = csv.reader(open(phase, 'r'))
        writer = csv.writer(open(joined, 'w', newline=''))
        rownum = 0
        for row in reader1:
            if rownum == 0:
                writer.writerow(str(self.e_data('_CT.csv')))  # why are characters separated??
            else:
                writer.writerow(row)
            rownum += 1
        end_row = rownum
        for row in reader2:
            if rownum == end_row:
                pass
            else:
                writer.writerow(row)
            rownum += 1

    def OnCTSummary(self, event):
        self.PushCTSummary()

    def PushCTSummary(self):
        """
        Button to automatically put all CT data into csv files.
        """
        self.create_summary(self.eqn_choice_CTratio, self.CT_table, self.CTratio_fit_grid, self.CT_richText, 'CT_e',
                            self.e_data('_CTe.csv'))
        self.create_summary(self.eqn_choice_CTphase, self.CT_table1, self.CTphase_fit_grid, self.CT_richText1, 'CT_p',
                            self.e_data('_CTp.csv'))
        self.JoinErrorPhase(self.e_data('_CTe.csv'), self.e_data('_CTp.csv'), self.e_data('_CT.csv'))

    def OnVTSummary(self, event):
        self.PushVTSummary()

    def PushVTSummary(self):
        """
        Button push to automatically put all VT data into csv files.
        """
        self.create_summary(self.eqn_choice_VTratio, self.VT_table, self.VTratio_fit_grid, self.VT_richText, 'VT_e',
                            self.e_data('_VTe.csv'))
        self.create_summary(self.eqn_choice_VTphase, self.VT_table1, self.VTphase_fit_grid, self.VT_richText1, 'VT_p',
                            self.e_data('_VTp.csv'))
        self.JoinErrorPhase(self.e_data('_VTe.csv'), self.e_data('_VTp.csv'), self.e_data('_VT.csv'))

    def OnSiteSummary(self, event):
        self.PushSiteSummary()

    def PushSiteSummary(self):
        """
        Button push to automatically put all CT data into csv files.
        """
        self.create_site_inf_summary(self.site_table, self.site_richText, self.e_data('_site.csv'))

    ####################End of Creating Summary Files########################

    ############Manage Calculation & Reports############
    def OnGUMcalc(self, event):
        self.PushGUMcalc()

    def PushGUMcalc(self):
        """
        Executes grand_finale assuming that all data has been loaded either from
        file or manually. This is run when the 'Process manually created files'
        button is pushed.
        """
        self.projwd = self.m_textCtrl999.GetValue()  # the project working directory can be altered
        self.m_staticText22.SetLabel('Project directory:  ' + self.projwd)  # display on 'Input file list and messages'
        self.m_statusBar1.SetStatusText('Calculation started', 2)
        self.m_statusBar1.SetStatusText('Meter calculation', 0)
        self.PushLoadMeterData()
        self.PushPlotMeter()
        print('Meter data')
        self.PushFit_Meter()
        self.PushLoadMeterInf()
        self.PushMeterSummary()
        self.m_statusBar1.SetStatusText('CT calculation', 0)
        self.PushLoadCTData()
        self.PushPlotCTphase()
        self.PushPlotCTratio()
        print('CT ratio data')
        self.PushFit_CTratio()
        print('CT phase data')
        self.PushFit_CTphase()
        self.PushLoadCTInf()
        self.PushCTSummary()
        self.m_statusBar1.SetStatusText('VT calculation', 0)
        self.PushLoadVTData()
        self.PushPlotVTphase()
        self.PushPlotVTratio()
        print('VT ratio data')
        self.PushFit_VTratio()
        print('VT phase data')
        self.PushFit_VTphase()
        print('')
        self.PushLoadVTInf()
        self.PushVTSummary()
        self.m_statusBar1.SetStatusText('Load processing', 0)
        self.PushPlotLoadProfile()
        self.PushLoadSiteInf()
        self.PushSiteSummary()
        self.m_statusBar1.SetStatusText('Overall calculation', 0)
        self.grand_finale()

    def grand_finale(self):
        """
        The error is calculated at the (current, phase) points provided in the
        load profile as given in load.csv.  A plot of the overall error against
        current and phase angle is created and a screen report that has the key
        results and graphs is generated.
        """
        # assemble components and calculate the error
        profile = comp.LOAD('default', self.csv_profile, self.profile_list)  # data files from the lists
        model = functions.MODEL('model')  # pick up the standard model functions to pass into component objects
        meter = comp.METER('default', '1 element', model, self.e_data('_meter.csv'))
        ct = comp.TRAN('name', 'single', model, self.e_data('_CT.csv'))
        vt = comp.TRAN('name', 'single', model, self.e_data('_VT.csv'))
        site = comp.INSTALLATION('name', meter, ct, vt, profile, self.e_data('_site.csv'))
        error = site.site_error_terms()
        self.m_statusBar1.SetStatusText('Calculation finished', 2)
        self.Create3DGraph(self.report_graph, self.n_profiles, 'error_axes_3D')

        for ii in range(len(error[0])):  # iterates the full calculation through each load profile
            # Plot the error
            r = error[2][ii]  # installation's X as determined by the profile
            no_of_points = len(r)
            X = np.zeros(no_of_points)
            Y = np.zeros(no_of_points)
            Z = np.zeros(no_of_points)
            Z1 = np.zeros(no_of_points)
            Z2 = np.zeros(no_of_points)
            for i in range(no_of_points):
                X[i] = r[i][0]
                Y[i] = r[i][1]
                Z[i] = error[0][ii][i].x
                uZ = error[0][ii][i].u
                dfZ = error[0][ii][i].df
                kZ = t.ppf(0.975, dfZ)  # note scipy t
                Z1[i] = Z[i] + uZ * kZ
                Z2[i] = Z[i] - uZ * kZ
            edge_no = np.sqrt(no_of_points)  # assuming an nxn grid
            dummy = np.zeros((int(edge_no), int(edge_no)), dtype=float)  # assumes nxn
            ZZ = np.reshape(Z, np.shape(dummy))
            XX = np.reshape(X, np.shape(dummy))
            YY = np.reshape(Y, np.shape(dummy))
            ZZ1 = np.reshape(Z1, np.shape(dummy))
            ZZ2 = np.reshape(Z2, np.shape(dummy))
            with warnings.catch_warnings():  # get 'converting masked element to nan'
                warnings.simplefilter("ignore")
                np.seterr(invalid='ignore')
                # self.report_graph.ax.plot_surface(XX, YY, ZZ, rstride=1, cstride=1, cmap='jet')
                # self.report_graph.ax.plot_wireframe(XX, YY, ZZ1)
                # self.report_graph.ax.plot_wireframe(XX, YY, ZZ2)
                self.error_axes_3D[ii].plot_surface(XX, YY, ZZ, rstride=1, cstride=1, cmap='jet')
                self.error_axes_3D[ii].plot_wireframe(XX, YY, ZZ1)
                self.error_axes_3D[ii].plot_wireframe(XX, YY, ZZ2)
                np.seterr(invalid='print')
            # self.report_graph.ax.autoscale(enable=True, axis='both', tight=True)
            self.error_axes_3D[ii].autoscale(enable=True, axis='both', tight=True)
            self.report_graph.canvas.draw()
            # create report
            self.m_statusBar1.SetStatusText('Generating report', 0)
            self.reporter(error[1][ii])
            self.wxreport()
    def OnAutoCalc(self, event):
        self.PushAutocalc()

    def PushAutocalc(self):
        """
        Button push for "Process opened project files" button, proceeds to load all
        data files and then executes 'grand_finale'.
        """
        self.m_statusBar1.SetStatusText('Autocalculation started', 2)
        self.m_statusBar1.SetStatusText('Meter calculation', 0)
        self.PushLoadMeterData()
        self.PushPlotMeter()
        print('Meter data')
        self.PushFit_Meter()
        self.PushLoadMeterInf()
        self.PushMeterSummary()
        self.m_statusBar1.SetStatusText('CT calculation', 0)
        self.PushLoadCTData()
        self.PushPlotCTphase()
        self.PushPlotCTratio()
        print('CT ratio data')
        self.PushFit_CTratio()
        print('CT phase data')
        self.PushFit_CTphase()
        self.PushLoadCTInf()
        self.PushCTSummary()
        self.m_statusBar1.SetStatusText('VT calculation', 0)
        self.PushLoadVTData()
        self.PushPlotVTphase()
        self.PushPlotVTratio()
        print('VT ratio data')
        self.PushFit_VTratio()
        print('VT phase data')
        self.PushFit_VTphase()
        print('')
        self.PushLoadVTInf()
        self.PushVTSummary()
        self.m_statusBar1.SetStatusText('Load processing', 0)
        self.PushPlotLoadProfile()
        self.PushLoadSiteInf()
        self.PushSiteSummary()
        self.m_statusBar1.SetStatusText('Overall calculation', 0)
        self.grand_finale()
    ##########End Manage Calculation & Report###########


if __name__ == '__main__':
    app = wx.App()
    frame = MIECALC(None)
    frame.Show()
    app.MainLoop()