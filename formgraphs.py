import wx
from formbooks import ProjectFrame
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg
from matplotlib.figure import Figure


class GraphForm(ProjectFrame):

    def __init__(self, parent):
        """
        Adds canvases to ProjectFrame for the various graphs in the notebooks
        """
        ProjectFrame.__init__(self, parent)
        # add matplotlib graph that was not in wxFormBuilder
        self.Create3DGraph(self.report_graph)  # report notebook
        self.Create2DGraph(self.CT_graph_1, "Current / %")  # CT notebook
        self.Create2DGraph(self.VT_graph_1, "Voltage/ %")  # VT notebook
        self.Create3DGraph(self.meter_graph)  # Meter notebook
        self.Create3DGraph(self.load_graph)  # Load notebook
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

    def Create3DGraph(self, panel):
        """
        A 3D graph is created on *panel*.
        """
        panel.figure = Figure(None)
        panel.canvas = FigureCanvas(panel, -1, panel.figure)
        panel.ax = panel.figure.add_subplot(111, projection='3d')
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

    def OnClearAllGraphs(self, event):
        self.pushClearAllGraphs()

    def pushClearAllGraphs(self):
        """
        Clears all drawn graphs by line and collections. This may compromise
        the autoscaling behaviour when the graphs are re-used.
        """
        #Note the draw() calls only needed if a graph is being viewed when
        #the graph is cleared.  The hidden graphs get redrwn when next viewed.
        self.VT_graph_1.axes1.lines = [] # all 2D lines
        self.VT_graph_1.axes1.collections = [] #vertical error bars
        self.VT_graph_1.axes2.lines = []
        self.VT_graph_1.axes2.collections = []
        self.VT_graph_1.canvas.draw()

        self.CT_graph_1.axes1.lines = []
        self.CT_graph_1.axes1.collections = []
        self.CT_graph_1.axes2.lines = []
        self.CT_graph_1.axes2.collections = []
        self.CT_graph_1.canvas.draw()

        self.meter_graph.ax.collections = []
        self.meter_graph.ax.lines = [] # error bar lines
        self.meter_graph.canvas.draw()
        self.report_graph.ax.collections = []
        self.report_graph.canvas.draw()
        self.load_graph.ax.collections = []
        self.load_graph.canvas.draw()

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
