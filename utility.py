from load_utility import Load_Utility
import wx


class UTILITY(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY,
                          title=u"Utility For Creating Load Profile Files",
                          pos=wx.DefaultPosition, size=wx.Size(700, 500),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.pnl = wx.Panel(self)
        self.pnl.sizer = wx.BoxSizer(wx.VERTICAL)
        self.staticText1 = wx.StaticText(self.pnl, wx.ID_ANY,
                                             u"Enter output filename",
                                             pos=(5,10))
        self.staticText1.Wrap(-1)
        self.textCtrl1 = wx.TextCtrl(self.pnl, size=(400, 20), pos=(40, 30))
        self.textCtrl1.SetMaxLength(0)
        self.pnl.sizer.Add(self.textCtrl1, -1, wx.ALL, 5)
        self.staticText2 =wx.StaticText(self.pnl, wx.ID_ANY, u"Normal Distribution", pos=(10, 80))
        self.staticText3 = wx.StaticText(self.pnl, wx.ID_ANY, u"Mean current", pos=(10, 110))
        self.staticText4 = wx.StaticText(self.pnl, wx.ID_ANY, u"Current stdev", pos=(10, 135))
        self.staticText5 = wx.StaticText(self.pnl, wx.ID_ANY, u"Mean phase", pos=(10, 160))
        self.staticText6 = wx.StaticText(self.pnl, wx.ID_ANY, u"Phase stdev", pos=(10, 185))
        self.textCtrl2 = wx.TextCtrl(self.pnl, size=(100, 20), pos=(100, 105))
        self.textCtrl2.SetMaxLength(0)
        self.pnl.sizer.Add(self.textCtrl2, -1, wx.ALL, 5)
        self.textCtrl3 = wx.TextCtrl(self.pnl, size=(100, 20), pos=(100, 130))
        self.textCtrl3.SetMaxLength(0)
        self.pnl.sizer.Add(self.textCtrl3, -1, wx.ALL, 5)
        self.textCtrl4 = wx.TextCtrl(self.pnl, size=(100, 20), pos=(100, 155))
        self.textCtrl4.SetMaxLength(0)
        self.pnl.sizer.Add(self.textCtrl4, -1, wx.ALL, 5)
        self.textCtrl5 = wx.TextCtrl(self.pnl, size=(100, 20), pos=(100, 180))
        self.textCtrl5.SetMaxLength(0)
        self.pnl.sizer.Add(self.textCtrl5, -1, wx.ALL, 5)

        self.staticText7 = wx.StaticText(self.pnl, wx.ID_ANY, u"Uniform Distribution", pos=(250, 80))
        self.staticText8 = wx.StaticText(self.pnl, wx.ID_ANY, u"Minimum current", pos=(250, 110))
        self.staticText9 = wx.StaticText(self.pnl, wx.ID_ANY, u"Maximum current", pos=(250, 135))
        self.staticText10 = wx.StaticText(self.pnl, wx.ID_ANY, u"Minimum phase", pos=(250, 160))
        self.staticText11 = wx.StaticText(self.pnl, wx.ID_ANY, u"Maximum Phase", pos=(250, 185))
        self.textCtrl6 = wx.TextCtrl(self.pnl, size=(100, 20), pos=(350, 105))
        self.textCtrl6.SetMaxLength(0)
        self.pnl.sizer.Add(self.textCtrl6, -1, wx.ALL, 5)
        self.textCtrl7 = wx.TextCtrl(self.pnl, size=(100, 20), pos=(350, 130))
        self.textCtrl7.SetMaxLength(0)
        self.pnl.sizer.Add(self.textCtrl7, -1, wx.ALL, 5)
        self.textCtrl8 = wx.TextCtrl(self.pnl, size=(100, 20), pos=(350, 155))
        self.textCtrl8.SetMaxLength(0)
        self.pnl.sizer.Add(self.textCtrl8, -1, wx.ALL, 5)
        self.textCtrl9 = wx.TextCtrl(self.pnl, size=(100, 20), pos=(350, 180))
        self.textCtrl9.SetMaxLength(0)
        self.pnl.sizer.Add(self.textCtrl9, -1, wx.ALL, 5)

        self.Create_normal = wx.Button(self.pnl, wx.ID_ANY, u"Create Normal Profile", pos=(80, 230))
        self.pnl.sizer.Add(self.Create_normal, 0, wx.ALL, 5)
        self.Create_normal.Bind(wx.EVT_BUTTON, self.OnNormal)

        self.Create_uniform = wx.Button(self.pnl, wx.ID_ANY, u"Create Uniform Profile", pos=(330, 230))
        self.pnl.sizer.Add(self.Create_uniform, 0, wx.ALL, 5)
        self.Create_uniform.Bind(wx.EVT_BUTTON, self.OnUniform)

        self.staticText12 = wx.StaticText(self.pnl, wx.ID_ANY,
                                         u"Enter input kWh, kvarh filename",
                                         pos=(5, 300))
        self.staticText12.Wrap(-1)
        self.textCtrl10 = wx.TextCtrl(self.pnl, size=(400, 20), pos=(40, 320))
        self.textCtrl10.SetMaxLength(0)
        self.pnl.sizer.Add(self.textCtrl10, -1, wx.ALL, 5)

        self.Create_real = wx.Button(self.pnl, wx.ID_ANY, u"Create Real Profile", pos=(80, 350))
        self.pnl.sizer.Add(self.Create_real, 0, wx.ALL, 5)
        self.Create_real.Bind(wx.EVT_BUTTON, self.OnReal)

    def OnNormal(self, event):
        print('Normal calculation')

    def OnUniform(self, event):
        print('Uniform calculation')

    def OnReal(self, event):
        print('Real calculation')



def main():
    app = wx.App()
    ex = UTILITY(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
