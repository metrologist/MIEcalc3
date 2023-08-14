import wx
from formbooks import ProjectFrame
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg
from matplotlib.figure import Figure
from math import ceil, sqrt


class GraphForm(ProjectFrame):

    def __init__(self, parent):
        """
        Adds canvases to ProjectFrame for the various graphs in the notebooks
        """
        ProjectFrame.__init__(self, parent)
        # add matplotlib graph that was not in wxFormBuilder
        self.load_axes_3D = []  # a list of the axes for multiple 3D plots of load
        self.error_axes_3D = []  # a list of the axes for multiple 3D plots of total error
        self.meter_axes_3D = []  # a list of the axes for multiple 3D meter plots ... not used
        self.Create3DGraph(self.report_graph, 1, 'error_axes_3D')  # report notebook
        self.Create2DGraph(self.CT_graph_1, "Current / %")  # CT notebook
        self.Create2DGraph(self.VT_graph_1, "Voltage/ %")  # VT notebook
        self.Create3DGraph(self.meter_graph, 1, 'meter_axes_3D')  # Meter notebook
        self.Create3DGraph(self.load_graph, 1, 'load_axes_3D')  # Load notebook
        self.load_graph.ax.set_zlabel('Energy')  # Load has energy for z axis

    def Create2DGraph(self, panel, xlabel):
        """
        A 2D graph is created in *panel* with the x axis labelled with *xlabel*.
        """
        panel.figure = Figure(None)
        panel.figure.set_facecolor('white')
        panel.canvas = FigureCanvas(panel, -1, panel.figure)
        panel.axes1 = panel.figure.add_subplot(2, 1, 1)
        panel.axes2 = panel.figure.add_subplot(2, 1, 2)
        # these labels should be plot specific
        panel.axes1.set_xlabel(xlabel)
        panel.axes1.set_ylabel('Error / %')
        panel.axes2.set_xlabel(xlabel)
        panel.axes2.set_ylabel('Phase / crad')
        ##         panel.figure.tight_layout() # leads to cropping of y-axis legend in report
        panel.sizer = wx.BoxSizer(wx.VERTICAL)
        panel.sizer.Add(panel.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        panel.SetSizer(panel.sizer)
        panel.Fit()
        self.add_2Dtoolbar(panel)

    def add_2Dtoolbar(self, panel):
        """
        Adds the standard matplotlib toolbar that provides extra viewing
        features (e.g., pan and zoom).
        """
        panel.toolbar = NavigationToolbar2WxAgg(panel.canvas)
        panel.toolbar.Realize()
        tw, th = panel.toolbar.GetSize()
        fw, fh = panel.canvas.GetSize()
        panel.toolbar.SetSize(wx.Size(fw, th))
        panel.sizer.Add(panel.toolbar, 0, wx.LEFT | wx.EXPAND)
        # update the axes menu on the toolbar
        panel.toolbar.update()

    def Create3DGraph(self, panel, n, target):
        """

        :param panel: wx panel that will display the graph, panel name used to identify axes
        :param n: the number of 3D graphs to be displayed
        :param target:  name of the specific graph either error_axes_3D or load_axes_3D which needs mutlitple axes
        :return:
        """
        rows = ceil(n / ceil(sqrt(n)))  # choose rows, columns to fit the number of graphs required
        cols = ceil(sqrt(n))
        panel.figure = Figure(None)
        panel.canvas = FigureCanvas(panel, -1, panel.figure)
        for i in range(1, n + 1):  # draw n sets of axes in the grid
            panel.ax = panel.figure.add_subplot(rows, cols, i, projection='3d')
            if target == 'error_axes_3D':
                self.error_axes_3D.append(panel.ax)
            elif target == 'load_axes_3D':
                self.load_axes_3D.append(panel.ax)
            panel.figure.set_facecolor('white')
            panel.figure.tight_layout()
            # these labels should be selected later for specific components
            panel.ax.set_xlabel('Current / %')
            panel.ax.set_ylabel('Phase / degree')
            panel.ax.set_zlabel('Error / %')
        panel.sizer = wx.BoxSizer(wx.VERTICAL)
        panel.sizer.Add(panel.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        panel.SetSizer(panel.sizer)
        panel.Fit()
        self.add_2Dtoolbar(panel)
        # panel.canvas.draw()  # not clear if this is necessary ... sometimes the first subplot was not rotating

    def OnClearAllGraphs(self, event):
        self.pushClearAllGraphs()

    def pushClearAllGraphs(self):
        """
        Clears all drawn graphs by axes.
        """
        #Note the draw() calls only needed if a graph is being viewed when
        #the graph is cleared.  The hidden graphs get redrwn when next viewed.
        graphs_2D = [self.VT_graph_1, self.CT_graph_1]
        for y in graphs_2D:
            the_xlabel = y.axes1.get_xlabel()
            the_ylabel = y.axes1.get_ylabel()
            y.axes1.clear()
            y.axes1.set_xlabel(the_xlabel)
            y.axes1.set_ylabel(the_ylabel)
            the_xlabel = y.axes2.get_xlabel()
            the_ylabel = y.axes2.get_ylabel()
            y.axes2.clear()
            y.axes2.set_xlabel(the_xlabel)
            y.axes2.set_ylabel(the_ylabel)
            y.canvas.draw()

        graphs_3D = [self.meter_graph, self.report_graph, self.load_graph]

        all_axes = [self.meter_axes_3D, self.error_axes_3D, self.load_axes_3D ]
        for i in range(len(all_axes)):
            if i ==0:  # the meter graph is different, why?
                the_x = graphs_3D[i].ax.get_xlabel()
                the_y = graphs_3D[i].ax.get_ylabel()
                the_z = graphs_3D[i].ax.get_zlabel()
                graphs_3D[i].ax.clear()
                graphs_3D[i].ax.set_xlabel(the_x)  # and now the labels are restored
                graphs_3D[i].ax.set_ylabel(the_y)
                graphs_3D[i].ax.set_zlabel(the_z)
                graphs_3D[i].canvas.draw()
            else:
                for j in range(len(all_axes[i])):
                    the_x = all_axes[i][j].get_xlabel()
                    the_y = all_axes[i][j].get_ylabel()
                    the_z = all_axes[i][j].get_zlabel()
                    all_axes[i][j].clear()
                    all_axes[i][j].set_xlabel(the_x)  # and now the labels are restored
                    all_axes[i][j].set_ylabel(the_y)
                    all_axes[i][j].set_zlabel(the_z)
                    graphs_3D[i].canvas.draw()
            # graphs_3D[i].figure.clf()
            # if i>=0:  # do not clear meter figure
            #     graphs_3D[i].figure.clf()
            # graphs_3D[i].Close()
            # graphs_3D[i].canvas.draw()


        # for y in graphs_3D:  # clears axes to be ready for re-using
        #     the_x = y.ax.get_xlabel()
        #     the_y = y.ax.get_ylabel()
        #     the_z = y.ax.get_zlabel()
        #     y.ax.clear()  # all axes are cleared
        #     y.ax.set_xlabel(the_x)  # and now the labels are restored
        #     y.ax.set_ylabel(the_y)
        #     y.ax.set_zlabel(the_z)
        #     y.canvas.draw()
        # # graphs_3D[2].figure.clf()  # load_graph will be completely redrawn (in case number of subplots changes).
        # graphs_3D[1].figure.clf()  # report_graph will be completely redrawn (in case number of subplots changes).
        # # self.report_graph.Close()
        self.load_axes_3D = []  # forget old axes list
        self.error_axes_3D = []  # forget old axes list
        self.meter_axes_3D = []  # forget old axes list, but there is only 1 meter ?

    def OnQuit(self, event):
        """
        Closes the frame and terminates the program from 'Quit' in the 'File'
        menu.  No 'are you sure?' dialogue.
        """
        self.Destroy()

if __name__ == '__main__':
    app = wx.App()
    frame = GraphForm(None)
    frame.Show()
    app.MainLoop()
