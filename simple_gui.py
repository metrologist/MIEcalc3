import wx
import wx.richtext as rtc
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg
from matplotlib.figure import Figure
from math import ceil, sqrt
import numpy as np


class EXAMPLE(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY,
                          title=u"For Testing GUI Code Issues",
                          pos=wx.DefaultPosition, size=wx.Size(800, 600),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.m_menubar1 = wx.MenuBar(0)
        self.m_menu1 = wx.Menu()
        self.m_menuItem1 = wx.MenuItem(self.m_menu1, wx.ID_ANY, u"Draw 1 graph", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuItem1)
        self.m_menuItem2 = wx.MenuItem(self.m_menu1, wx.ID_ANY, u"Draw 4 graphs", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuItem2)
        self.m_menuItem2.Enable(True)
        self.m_menuItem3 = wx.MenuItem(self.m_menu1, wx.ID_ANY, u"Clear graphs", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuItem3)
        self.m_menuItem3.Enable(True)
        self.m_menu1.AppendSeparator()
        self.m_menubar1.Append(self.m_menu1, u"Actions")
        self.SetMenuBar(self.m_menubar1)
        self.Bind(wx.EVT_MENU, self.OnDraw1, id=self.m_menuItem1.GetId())
        self.Bind(wx.EVT_MENU, self.OnDraw4, id=self.m_menuItem2.GetId())
        self.Bind(wx.EVT_MENU, self.OnClear, id=self.m_menuItem3.GetId())
        self.pnl = wx.Panel(self)
        self.pnl.sizer = wx.BoxSizer(wx.VERTICAL)
        # self.n_profiles = 4
        # self.setup(self.n_profiles)

    def setup(self, number):
        pnl = self.pnl
        if pnl.IsFrozen():
            pnl.Thaw()
        n = number
        rows = ceil(n / ceil(sqrt(n)))  # choose rows, columns to fit the number of graphs required
        cols = ceil(sqrt(n))
        pnl.figure = Figure(None)
        pnl.canvas = FigureCanvas(pnl, -1, pnl.figure)
        self.axes_list = []
        for i in range(1, n + 1):  # draw n sets of axes in the grid
            pnl.ax = pnl.figure.add_subplot(rows, cols, i, projection='3d')
            self.axes_list.append(pnl.ax)
        # pnl.sizer = wx.BoxSizer(wx.VERTICAL)
        pnl.sizer.Add(pnl.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        pnl.SetSizer(pnl.sizer)
        pnl.Fit()
        self.add_2Dtoolbar(self.pnl)
        pnl.Enable(enable=True)
        pnl.SendSizeEventToParent()
        # return pnl

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

    def draw_graph(self):
        # setting up a parametric curve
        t = np.arange(0, 2 * np.pi + .1, 0.01)
        x, y, z = np.sin(t), np.cos(3 * t), np.sin(5 * t)
        estep = 15
        i = np.arange(t.size)
        zuplims = (i % estep == 0) & (i // estep % 3 == 0)
        zlolims = (i % estep == 0) & (i // estep % 3 == 2)
        for splot in self.axes_list:
            ax = splot
            ax.errorbar(x, y, z, 0.2, zuplims=zuplims, zlolims=zlolims, errorevery=estep)
            ax.set_xlabel("X label")
            ax.set_ylabel("Y label")
            ax.set_zlabel("Z label")

    def OnClear(self, event):
        print('Clear ', len(self.axes_list), 'axes.')
        sizer = self.pnl.GetSizer()
        sizer.Clear(True)
        self.pnl.Freeze()  # this seems to disconnect matplotlib from the old plots
        self.axes_list = []  # forget list

    def OnDraw1(self, event):
        self.n_profiles = 1
        print('Draw 1 subplot')
        self.setup(self.n_profiles)
        self.draw_graph()
        self.pnl.SendSizeEventToParent()

    def OnDraw4(self, event):
        print('Draw 4 subplots')
        self.n_profiles = 4
        # self.setup(self.n_profiles)
        self.setup(self.n_profiles)
        self.draw_graph()
        self.pnl.SendSizeEventToParent()

        # self.report_richText = rtc.RichTextCtrl(self.pnl, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
        #                                                 wx.DefaultSize,
        #                                                 0 | wx.VSCROLL | wx.HSCROLL | wx.WANTS_CHARS | wx.BORDER_NONE)
        # self.report_richText = rtc.RichTextCtrl(self.pnl, size = (600, 500))
        # bSizer1.Add(self.report_richText, 0, wx.EXPAND | wx.ALL, 5)
        # report = self.report_richText
        # report.BeginFontSize(14)
        # report.BeginBold()
        # report.WriteText('Hello')
        # report.Newline()
        # report.EndBold()
        # report.EndFontSize()
        # report.BeginFontSize(10)
        # report.BeginBold()
        # report.WriteText('Load Profile\t\tError\t\t\tUncertainty\t\tError-Uncertainty\tError+Uncertainty\n')
        # report.EndBold()
        # report.WriteText('      1\t\t\t-0.12 %\t\t  0.33 %\t\t  -0.46 %\t\t  0.21 %\n')
        # report.WriteText('      2\t\t\t-0.04 %\t\t  0.24 %\t\t  -0.28 %\t\t  0.20 %\n')
        # report.WriteText('      3\t\t\t-0.05 %\t\t  0.17 %\t\t  -0.22 %\t\t  0.12 %\n')


        # n = 4  # rows
        # m = 5  # columns
        # table_data = [['Load Profile', 'Error', 'Uncertainty', 'Error-Uncertainty', 'Error+Uncertainty']]
        # for i in range(n - 1):
        #     table_data.append(['1', '-0.12 %', '-0.12 %', '-0.12 %', '-0.12 %'])
        # table1 = report.WriteTable(n, m)
        # for i in range(n):
        #     for j in range(m):
        #         cell = table1.GetCell(i, j)
        #         cell.AddParagraph(table_data[i][j])
        # report.Newline()
        # report.EndFontSize()
        # print(table1.GetColumnCount())
        # cell = table1.GetCell(1, 1)
        # cell.SetProperties()
        # table1.SetCellProperties((1, 1), font )

        # bSizer2 = wx.BoxSizer(wx.VERTICAL)
        # self.report_Text = wx.TextCtrl(self.pnl, size=(600, 250))
        # bSizer2.Add(self.report_Text, 0, wx.EXPAND | wx.ALL, 5)
        # other =self.report_Text
        # other.WriteText("Hello, it's me ..")



def main():
    app = wx.App()
    ex = EXAMPLE(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()