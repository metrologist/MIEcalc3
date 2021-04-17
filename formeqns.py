import wx
from form_i_o import IOForm
import numpy as np
import GTC as gtc
import warnings
import components as comp
from scipy.stats import t
import csv
import os


class EqnForm(IOForm):

    def __init__(self, parent):
        """
        Adds the fitting process.
        """
        IOForm.__init__(self, parent)

    def e_data(self, name):
        """
        Convenient way to add current working directory file path to *name* for
        temporary files placed in the e_data folder.
        """
        return os.path.join(self.cwd, 'e_data', name)

    #############Calculating and plotting fits############################
    def fit_2D(self, function, input_grid, output_grid, graph, axes):
        """
        Takes data from the named GUI data *input_grid* and returns fit
        statistics to the relevant *output_grid*.  The resulting function is
        plotted on the relevant *graph* and *axes*.  Using the GUI to hold
        data is a convenience that also allows manual entry and editing of data.
        It would be better practice to revert to only using the GUI for display.
        """
        n, X, Y, uy, k = self.get_2Dgrid_data(input_grid)
        sigy = uy / k  # element by element, standard deviation
        b_var = self.model.average_var(uy, k)
        p = self.get_params(function.no, output_grid)
        # do fit using Levenberg-Marquardt
        p2, cov, info, mesg, success = self.model.fit(function.fn, p, X, Y, sigy)  # allows weighting
        if success in [1, 2, 3, 4]:
            # print the results into the display grid
            self.m_statusBar1.SetStatusText(function.label + ' : converged', 2)
            dof = len(X) - len(p)
            chisq = sum(info["fvec"] * info["fvec"])
            red_chisq = chisq / dof
            fit_check = self.model.fit_qual(b_var, red_chisq, dof)
            ub0 = fit_check[0]
            temp_b0 = gtc.ureal(0, ub0)
            print(fit_check[1])
            self.fitting_grid_results(output_grid, p2, dof, red_chisq, cov, ub0)
            # plot the results
            minX = np.min(X)
            maxX = np.max(X)
            Xrange = maxX - minX
            XX = np.arange(minX - 0.01 * Xrange, maxX + 0.01 * Xrange, Xrange / 100.0)
            label = []  # labels are required for fit_ureals
            for coefficient in p:
                label.append(coefficient.name)
            ucoeffs = self.model.fit_ureals(p2, cov * red_chisq, dof, label)  # note use of red_chisq
            for_plotting = function.fn(XX, ucoeffs)
            Y = np.zeros(len(for_plotting))
            U = np.zeros(len(for_plotting))
            for i in range(len(for_plotting)):
                Y[i] = for_plotting[i].x
                temp_value = for_plotting[i] + temp_b0  # first add type B
                U[i] = temp_value.u * t.ppf(0.975, temp_value.df)  # *gtc.reporting.k_factor(temp_value.df)# expanded U
            ##                 U[i] = for_plotting[i].u #note this is a 1 sigma plot
            axes.plot(XX, Y + U, 'b--')
            axes.plot(XX, Y - U, 'b--')
            axes.plot(XX, Y, 'b-')
            graph.canvas.draw()
        else:
            self.m_statusBar1.SetStatusText(function.label + ': not converged', 2)
            print(mesg)

    def fit_3D(self, function, input_grid, output_grid, graph):
        """
        Takes data from the relevant data *input_grid* and returns fit
        statistics to the relevant *output_grid*.  The resulting function is
        plotted on the relevant mplot3D *graph*.  Using the GUI to hold
        data is a convenience that also allows manual entry and editing of data.
        It would be better practice to revert to only using the GUI for display.
        """
        # calls the relevant function with a generic return of parameters and plots
        # read data from grid
        n, XY, Z, uz, k = self.get_3Dgrid_data(input_grid)
        sigz = uz / k  # element by element, sigma
        p = self.get_params(function.no, output_grid)
        b_var = self.model.average_var(uz, k)
        # do fit using Levenberg-Marquardt
        p2, cov, info, mesg, success = self.model.fit(function.fn, p, XY, Z, sigz)  # allows weighting
        if success in [1, 2, 3, 4]:
            # print the results into the display grid
            self.m_statusBar1.SetStatusText(function.label + ': converged', 2)
            dof = len(XY) - len(p)
            chisq = sum(info["fvec"] * info["fvec"])
            red_chisq = chisq / dof
            fit_check = self.model.fit_qual(b_var, red_chisq, dof)
            ub0 = fit_check[0]
            temp_b0 = gtc.ureal(0, ub0)
            print(fit_check[1])
            self.fitting_grid_results(output_grid, p2, dof, red_chisq, cov, ub0)
            # plot the results
            minXY = np.min(XY, 0)
            maxXY = np.max(XY, 0)
            minX = minXY[0]
            maxX = maxXY[0]
            minY = minXY[1]
            maxY = maxXY[1]
            Xrange = maxX - minX
            Yrange = maxY - minY
            X = np.arange(minX, maxX, Xrange / 100.0)
            Y = np.arange(minY, maxY, Yrange / 100.0)
            X, Y = np.meshgrid(X, Y)
            r = np.ravel(X)
            s = np.ravel(Y)
            RS = np.zeros((len(r), 2))
            for i in range(len(r)):
                RS[i, 0] = r[i]
                RS[i, 1] = s[i]
            label = []  # labels are required for fit_ureals
            for coefficient in p:
                label.append(coefficient.name)
            ucoeffs = self.model.fit_ureals(p2, cov * red_chisq, dof, label)  # note use of red_chisq
            for_plotting = function.fn(RS, ucoeffs)
            ZZ = np.zeros(len(RS))
            UU = np.zeros(len(RS))
            ##             Zup = np.zeros(len(RS))
            ##             Zlow = np.zeros(len(RS))
            for i in range(len(RS)):
                ZZ[i] = for_plotting[i].x
                temp_value = for_plotting[i] + temp_b0  # first add type B
                UU[i] = temp_value.u * t.ppf(0.975, temp_value.df)  # *gtc.reporting.k_factor(temp_value.df) #expanded U
            ##                 upper_lower = gtc.reporting.uncertainty_interval(for_plotting[i]+ temp_b0) #might be more efficient?
            ##                 Zup[i] = upper_lower[1]
            ##                 Zlow[i] = upper_lower[0]
            ##                 UU[i] = for_plotting[i].u #note this is a 1 sigma plot
            Z1 = ZZ
            Z2 = np.reshape(Z1, np.shape(X))
            Z3 = Z1 + UU
            Z4 = np.reshape(Z3, np.shape(X))
            Z3 = Z1 - UU
            Z6 = np.reshape(Z3, np.shape(X))
            with warnings.catch_warnings():  # get 'converting masked element to nan'
                warnings.simplefilter("ignore")
                np.seterr(invalid='ignore')
                graph.ax.plot_surface(X, Y, Z2, rstride=10, cstride=10, cmap='jet')  # fitted function
                graph.ax.plot_wireframe(X, Y, Z4, rstride=10, cstride=10)  # plus uncertainty
                graph.ax.plot_wireframe(X, Y, Z6, rstride=10, cstride=10)  # minus uncertainty
                np.seterr(invalid='print')
            graph.ax.autoscale(enable=True, axis='both', tight=True)
            graph.canvas.draw()

        else:
            self.m_statusBar1.SetStatusText(function.label + ': not converged', 2)
            print(mesg)

    #############End of calculating and plotting fits#####################

    ####################Managing Function Fit Events###########
    # the various fit button events look to see what function was selected
    def Fit_CTratio(self, event):
        self.PushFit_CTratio()

    def PushFit_CTratio(self):
        """
        Button to run fitting calculation for CT error.
        """
        # assign definitions to a dictionary for selection
        options = {'0': self.mean_fit1, '1': self.line_fit1, '2': self.log_fit}
        # carry out fit for function chosen in 'choice box'
        choice = str(self.eqn_choice_CTratio.GetSelection())[0]  # first character
        options[choice](self.CTratio_data, self.CTratio_fit_grid, self.CT_graph_1, self.CT_graph_1.axes1)

    def Fit_CTphase(self, event):
        self.PushFit_CTphase()

    def PushFit_CTphase(self):
        """
        Button to run fitting calculation for CT phase.
        """
        # assign definitions to a dictionary for selection
        options = {'0': self.mean_fit1, '1': self.line_fit1, '2': self.log_fit}
        # carry out fit for function chosen in 'choice box'
        choice = str(self.eqn_choice_CTphase.GetSelection())[0]  # first character
        options[choice](self.CTphase_data, self.CTphase_fit_grid, self.CT_graph_1, self.CT_graph_1.axes2)

    def Fit_VTratio(self, event):
        self.PushFit_VTratio()

    def PushFit_VTratio(self):
        """
        Button to run fitting calculation for VT error.
        """
        # assign definitions to a dictionary for selection
        options = {'0': self.mean_fit1, '1': self.line_fit1, '2': self.log_fit}
        # carry out fit for function chosen in 'choice box'
        choice = str(self.eqn_choice_VTratio.GetSelection())[0]  # first character
        options[choice](self.VTratio_data, self.VTratio_fit_grid, self.VT_graph_1, self.VT_graph_1.axes1)

    def Fit_VTphase(self, event):
        self.PushFit_VTphase()

    def PushFit_VTphase(self):
        """
        Button to run fitting calculation for VT phase.
        """
        # assign definitions to a dictionary for selection
        options = {'0': self.mean_fit1, '1': self.line_fit1, '2': self.log_fit}
        # carry out fit for function chosen in 'choice box'
        choice = str(self.eqn_choice_VTphase.GetSelection())[0]  # first character
        options[choice](self.VTphase_data, self.VTphase_fit_grid, self.VT_graph_1, self.VT_graph_1.axes2)

    def Fit_Meter(self, event):
        # assign definitions to a dictionary for selection
        self.PushFit_Meter()

    def PushFit_Meter(self):
        """
        Button to run fitting calculation for meter.
        """
        options = {'0': self.mean_sfit1, '1': self.plane_sfit1, '2': self.tan_sfit1, '3': self.tan_sfit2}
        # carry out fit for function chosen in 'choice box'
        choice = str(self.eqn_choice_Meter.GetSelection())[0]  # first character
        options[choice](self.meter_data, self.Meter_fit_grid, self.meter_graph)

    # The dictionary approach above may not be the best choice.

    def OnCreateLoadProfile(self, event):
        self.PushCreateLoadProfile()

    def PushCreateLoadProfile(self):
        """
        Button to create load profile from half-hour data and store in csv file.
        """
        profile = comp.LOAD('half-hour', self.load_values.GetValue(), self.load_data.GetValue())
        profile.hist_from_raw(self.load_data.GetValue(), self.e_data('_load.csv'))  # this creates the output file
        # it also returns graphing information, but this is not used here
        # suggests comp.LOAD should be rethought

    def OnPlotLoadProfile(self, event):
        self.PushPlotLoadProfile()

    def PushPlotLoadProfile(self):
        """
        Button to create 3D histogram from csv file, but will first create the
        csv file using 'PushCreateLoadProfile' if GUI has loaded a txt rather
        than a csv file.
        """
        # this uses the .csv file to plot (either created by LOAD or provided independently)
        # self.LoadProfile(self.load_data.GetValue(), self.load_values.GetValue())
        if self.load_data.GetValue()[-3:] == 'txt':
            self.PushCreateLoadProfile()
        reader = csv.reader(open(self.load_values.GetValue(), 'r'))
        load = []
        for row in reader:
            load.append(row)  # everything including header line
        # header line has x,y box size
        x = float(load[0][0])
        y = float(load[0][1])
        z = float(load[0][2])
        # remove first line
        load = load[1:]
        # confused by dz and zpos...suspicious something is transposed
        # note that the x,y plot points are not the centre of the box
        n = len(load)
        xpos = np.zeros(n)
        ypos = np.zeros(n)
        zpos = np.zeros(n)
        dx = np.zeros(n)
        dy = np.zeros(n)
        dz = np.zeros(n)
        for i in range(n):
            xpos[i] = float(load[i][3])
            ypos[i] = float(load[i][4])
            zpos[i] = z
            dx[i] = x
            dy[i] = y
            dz[i] = float(load[i][2])
        with warnings.catch_warnings():  # get 'converting masked element to nan'
            warnings.simplefilter("ignore")
            np.seterr(invalid='ignore')  # since numpy 1.5.1 this additional error handling is required
            self.load_graph.ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b', zsort='average')
            np.seterr(invalid='print')
            self.load_graph.ax.autoscale(enable=True, axis='both', tight=True)

    def mean_fit1(self, datagrid, fitgrid, graph, axes):
        """
        Takes 2D data from *datagrid*, fits against the f_mean function, puts
        results in *fitgrid* and plots on relevant *graph* and *axes*.
        """
        self.fit_2D(self.model.f_mean, datagrid, fitgrid, graph, axes)

    def line_fit1(self, datagrid, fitgrid, graph, axes):
        """
        Takes 2D data from *datagrid*, fits against the f_line function, puts
        results in *fitgrid* and plots on relevant *graph* and *axes*.
        """
        self.fit_2D(self.model.f_line, datagrid, fitgrid, graph, axes)

    def log_fit(self, datagrid, fitgrid, graph, axes):
        """
        Takes 2D data from *datagrid*, fits against the f_logline function, puts
        results in *fitgrid* and plots on relevant *graph* and *axes*.
        """
        self.fit_2D(self.model.f_logline, datagrid, fitgrid, graph, axes)

    def mean_sfit1(self, datagrid, fitgrid, graph):
        """
        Takes 3D data from *datagrid*, fits against the f_mean function, puts
        results in *fitgrid* and plots on relevant 3D *graph*.
        """
        self.fit_3D(self.model.f_smean, datagrid, fitgrid, graph)

    def plane_sfit1(self, datagrid, fitgrid, graph):
        """
        Takes 3D data from *datagrid*, fits against the f_plane function, puts
        results in *fitgrid* and plots on relevant 3D *graph*.
        """
        self.fit_3D(self.model.f_plane, datagrid, fitgrid, graph)

    def tan_sfit1(self, datagrid, fitgrid, graph):
        """
        Takes 3D data from *datagrid*, fits against the f_tan_s1 function, puts
        results in *fitgrid* and plots on relevant 3D *graph*.
        """
        self.fit_3D(self.model.f_tan_s1, datagrid, fitgrid, graph)

    def tan_sfit2(self, datagrid, fitgrid, graph):
        """
        Takes 3D data from *datagrid*, fits against the f_tan_s2 function, puts
        results in *fitgrid* and plots on relevant 3D *graph*.
        """
        self.fit_3D(self.model.f_tan_s2, datagrid, fitgrid, graph)

    ####################End Managing Function Fit Events##################

    #################Data Plotting#####################
    #    def OnPlotGraph(self, event):# now from overview page
    #        self.Plot2DGraph(self.data_grid, self.graph_panel, 1)

    def OnPlotCTratio(self, event):  # from CT page
        self.PushPlotCTratio()

    def PushPlotCTratio(self):
        """
        Plots the CT error calibration data.
        """
        self.Plot2DGraph(self.CTratio_data, self.CT_graph_1, 1)

    def OnPlotCTphase(self, event):  # from CT page
        self.PushPlotCTphase()

    def PushPlotCTphase(self):
        """
        Plots the CT phase calibration data.
        """
        self.Plot2DGraph(self.CTphase_data, self.CT_graph_1, 2)

    def OnPlotVTratio(self, event):  # from VT page
        self.PushPlotVTratio()

    def PushPlotVTratio(self):
        """
        Plots the VT error calibration data.
        """
        self.Plot2DGraph(self.VTratio_data, self.VT_graph_1, 1)

    def OnPlotVTphase(self, event):  # from VT page
        self.PushPlotVTphase()

    def PushPlotVTphase(self):
        """
        PLots the VT phase calibration data.
        """
        self.Plot2DGraph(self.VTphase_data, self.VT_graph_1, 2)

    def OnPlotMeter(self, event):  # from meter page
        self.PushPlotMeter()

    def PushPlotMeter(self):
        """
        Plots the meter calibration data.
        """
        self.Plot3DGraph(self.meter_data, self.meter_graph)

    #    def OnPlotGraph3(self,event):
    #        self.Plot3DGraph(self.data_grid3, self.graph3D_panel)

    def Plot2DGraph(self, grid, panel, subplot):  # generic for VT & CT
        """
        Generic transformer plotting of data from relevant *grid* to a *subplot*
        established when the project initialised.
        """
        # assumes 2 subplots, 1 & 2 available
        x = list()  # start with empty list and append
        y = list()
        u = list()
        for i in range(grid.GetNumberRows()):
            # must be float() for errorbar to work
            x.append(float(grid.GetCellValue(i, 0)))
            y.append(float(grid.GetCellValue(i, 1)))
            u.append(float(grid.GetCellValue(i, 2)))
        if subplot == 1:
            axes = panel.axes1
        else:
            axes = panel.axes2
        axes.errorbar(x, y, u, fmt='ro')
        axes.relim()  # this and line below are needed if graph was previously cleared
        axes.autoscale_view(True, True, False)
        panel.canvas.draw()

    def Plot3DGraph(self, grid, panel):
        """
        Generic 3D plotting of data in *grid* to a graph *panel* established
        when the project initialised. Data in *grid* is assumed to be in
        columns of x, y, z, u where u is the uncertainty in z.
        """
        x = list()  # start with empty list and append
        y = list()
        z = list()
        u = list()
        for i in range(grid.GetNumberRows()):
            # clunky lines for error bars
            xi = float(grid.GetCellValue(i, 0))
            yi = float(grid.GetCellValue(i, 1))
            zi = float(grid.GetCellValue(i, 2))
            ui = float(grid.GetCellValue(i, 3))
            x.append(xi)
            y.append(yi)
            z.append(zi)
            u.append(ui)
            panel.ax.plot([xi, xi], [yi, yi], [zi + ui, zi - ui], 'b')
        panel.ax.scatter(x, y, z)
        panel.canvas.draw()
    ################End Data Plotting#################


if __name__ == '__main__':
    app = wx.App()
    frame = EqnForm(None)
    frame.Show()
    app.MainLoop()
