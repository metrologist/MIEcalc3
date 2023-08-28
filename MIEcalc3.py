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
from os import path
from matplotlib import cm


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
        # assisting with Pyinstaller packaging,
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            print('running in a PyInstaller bundle')
        else:
            print('running in a normal Python process')
        print(path.dirname(__file__))  # this is the root folder, temporary in the case of the bundled app


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
        error = site.site_error_terms()  # total_error_list, overall_error_list, XX  (all are lists)
        self.m_statusBar1.SetStatusText('Calculation finished', 2)
        # self.report_graph.figure.clear(True)  # continuing challenge to correctly clear graph
        self.Create3DGraph(self.report_graph, self.n_profiles, 'error_axes_3D')
        # site-cat dictionary as tuples of allowable % error and % uncertainty
        # site_cat = {'1': (2.5, 0.6), '2': (2.5,0.6), '3': (1.25, 0.3), '4': (1.25, 0.3), '5': (0.75, 0.2) }
        # category = site_cat['4'][0]  # not yet clear where the metering installation category would be entered

        for ii in range(len(error[0])):  # iterates the full calculation through each load profile
            # Plot the error
            r = error[2][ii]  # installation's X as determined by the profile
            no_of_points = len(r)
            X = np.zeros(no_of_points)
            Y = np.zeros(no_of_points)
            Z = np.zeros(no_of_points)
            Z1 = np.zeros(no_of_points)
            Z2 = np.zeros(no_of_points)
            # Z3 = np.zeros(no_of_points)  # for + site limit
            # Z4 = np.zeros(no_of_points)  # for - site limit
            for i in range(no_of_points):
                X[i] = r[i][0]
                Y[i] = r[i][1]
                Z[i] = error[0][ii][i].x
                uZ = error[0][ii][i].u
                dfZ = error[0][ii][i].df
                kZ = t.ppf(0.975, dfZ)  # note scipy t
                Z1[i] = Z[i] + uZ * kZ
                Z2[i] = Z[i] - uZ * kZ
                # Z3[i] = category  # for site cat limits
                # Z4[i] = - category  # for site cat limits
            edge_no = np.sqrt(no_of_points)  # assuming an nxn grid
            dummy = np.zeros((int(edge_no), int(edge_no)), dtype=float)  # assumes nxn
            ZZ = np.reshape(Z, np.shape(dummy))
            XX = np.reshape(X, np.shape(dummy))
            YY = np.reshape(Y, np.shape(dummy))
            ZZ1 = np.reshape(Z1, np.shape(dummy))
            ZZ2 = np.reshape(Z2, np.shape(dummy))
            # ZZ3 = np.reshape(Z3, np.shape(dummy))  # for site cat limits
            # ZZ4 = np.reshape(Z4, np.shape(dummy))  # for site cat limits
            with warnings.catch_warnings():  # get 'converting masked element to nan'
                warnings.simplefilter("ignore")
                np.seterr(invalid='ignore')
                # self.report_graph.ax.plot_surface(XX, YY, ZZ, rstride=1, cstride=1, cmap='jet')
                # self.report_graph.ax.plot_wireframe(XX, YY, ZZ1)
                # self.report_graph.ax.plot_wireframe(XX, YY, ZZ2)
                # self.error_axes_3D[ii].set_title(ii + 1)
                self.error_axes_3D[ii].text2D(0.05, 0.95, ii+1, transform=self.error_axes_3D[ii].transAxes)
                self.error_axes_3D[ii].set_xlim3d(left=0, right=120)  # fix axes range
                self.error_axes_3D[ii].set_ylim3d(bottom=-30, top=90)
                self.error_axes_3D[ii].plot_surface(XX, YY, ZZ, rstride=1, cstride=1, cmap='jet')
                self.error_axes_3D[ii].plot_wireframe(XX, YY, ZZ1)
                self.error_axes_3D[ii].plot_wireframe(XX, YY, ZZ2)
                # self.error_axes_3D[ii].plot_wireframe(XX, YY, ZZ3, color='red')  # for site cat limits
                # self.error_axes_3D[ii].plot_wireframe(XX, YY, ZZ4, color='red')  # for site cat limits
                np.seterr(invalid='print')
                self.error_axes_3D[ii].view_init(elev=5, azim=-45, roll=0)  # for site cat limits
                self.report_graph.canvas.draw()
            self.report_graph.ax.autoscale(enable=True, axis='both', tight=True)
            self.error_axes_3D[ii].autoscale(enable=True, axis='both', tight=True)  # do not autoscale
            self.report_graph.canvas.draw()
        # create contour plot
        grid_size = 20
        error_cap = 1.5  # maximum value allowed in contour plot
        Z, X, Y = site.site_error_bypoint(1, 120,-30, 60, error_cap, grid_size )
        self.CreateContour(self.report_contour)
        # cp = self.report_contour.ax.contourf(X, Y, Z, locator=ticker.LogLocator(),cmap=cm.PuBu_r)
        cp = self.report_contour.axes.contourf(X, Y, Z, cmap=cm.rainbow)
        self.report_contour.figure.colorbar(cp, ticks=[0, 0.1, 0.25, 0.5, 0.75, 1.0, 1.25,2.0, 2.5])
        self.add_2Dtoolbar(self.report_contour)
        self.report_contour.Fit()
        self.report_contour.Enable(enable=True)
        self.report_contour.SendSizeEventToParent()

        # create report
        self.m_statusBar1.SetStatusText('Generating report', 0)
        self.reporter(error[1], site.temp)  # note that the site temperature is needed for the report
        self.wxreport()
        self.m_statusBar1.SetStatusText('Report ready', 0)
    def OnAutoCalc(self, event):
        self.PushAutocalc()

    def PushAutocalc(self):
        """
        Button push for "Process opened project files" button, proceeds to load all
        data files and then executes 'grand_finale'.
        """
        self.m_button26.Enable(False)  # grey out immediately after first push
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
        self.m_button26.Enable(True)  # restore once calculation finished
        self.m_button26.SetBackgroundColour(colour='YELLOW')  # can run again, but colour is a reminder
    ##########End Manage Calculation & Report###########


if __name__ == '__main__':
    app = wx.App()
    frame = MIECALC(None)
    frame.Show()
    app.MainLoop()