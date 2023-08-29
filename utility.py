from load_utility import Load_Utility
import wx
import os


class UTILITY(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY,
                          title=u"Utility For Creating Load Profile Files",
                          pos=wx.DefaultPosition, size=wx.Size(700, 500),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        iconFile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'UTIL.ico')
        icon1 = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon1)
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
        self.staticText3 = wx.StaticText(self.pnl, wx.ID_ANY, u"Mean current %", pos=(10, 110))
        self.staticText4 = wx.StaticText(self.pnl, wx.ID_ANY, u"Current stdev %", pos=(10, 135))
        self.staticText5 = wx.StaticText(self.pnl, wx.ID_ANY, u"Mean phase", pos=(10, 160))
        self.staticText6 = wx.StaticText(self.pnl, wx.ID_ANY, u"Phase stdev", pos=(10, 185))
        self.textCtrl2 = wx.TextCtrl(self.pnl, size=(50, 20), pos=(100, 105))
        self.textCtrl2.SetMaxLength(0)
        self.pnl.sizer.Add(self.textCtrl2, -1, wx.ALL, 5)
        self.textCtrl3 = wx.TextCtrl(self.pnl, size=(50, 20), pos=(100, 130))
        self.textCtrl3.SetMaxLength(0)
        self.pnl.sizer.Add(self.textCtrl3, -1, wx.ALL, 5)
        self.textCtrl4 = wx.TextCtrl(self.pnl, size=(50, 20), pos=(100, 155))
        self.textCtrl4.SetMaxLength(0)
        self.pnl.sizer.Add(self.textCtrl4, -1, wx.ALL, 5)
        self.textCtrl5 = wx.TextCtrl(self.pnl, size=(50, 20), pos=(100, 180))
        self.textCtrl5.SetMaxLength(0)
        self.pnl.sizer.Add(self.textCtrl5, -1, wx.ALL, 5)

        self.staticText7 = wx.StaticText(self.pnl, wx.ID_ANY, u"Uniform Distribution", pos=(250, 80))
        self.staticText8 = wx.StaticText(self.pnl, wx.ID_ANY, u"Minimum current %", pos=(250, 110))
        self.staticText9 = wx.StaticText(self.pnl, wx.ID_ANY, u"Maximum current %", pos=(250, 135))
        self.staticText10 = wx.StaticText(self.pnl, wx.ID_ANY, u"Minimum phase", pos=(250, 160))
        self.staticText11 = wx.StaticText(self.pnl, wx.ID_ANY, u"Maximum Phase", pos=(250, 185))
        self.textCtrl6 = wx.TextCtrl(self.pnl, size=(50, 20), pos=(365, 105))
        self.textCtrl6.SetMaxLength(0)
        self.pnl.sizer.Add(self.textCtrl6, -1, wx.ALL, 5)
        self.textCtrl7 = wx.TextCtrl(self.pnl, size=(50, 20), pos=(365, 130))
        self.textCtrl7.SetMaxLength(0)
        self.pnl.sizer.Add(self.textCtrl7, -1, wx.ALL, 5)
        self.textCtrl8 = wx.TextCtrl(self.pnl, size=(50, 20), pos=(365, 155))
        self.textCtrl8.SetMaxLength(0)
        self.pnl.sizer.Add(self.textCtrl8, -1, wx.ALL, 5)
        self.textCtrl9 = wx.TextCtrl(self.pnl, size=(50, 20), pos=(365, 180))
        self.textCtrl9.SetMaxLength(0)
        self.pnl.sizer.Add(self.textCtrl9, -1, wx.ALL, 5)

        self.Create_normal = wx.Button(self.pnl, wx.ID_ANY, u"Create Normal Profile", pos=(80, 230))
        self.pnl.sizer.Add(self.Create_normal, 0, wx.ALL, 5)
        self.Create_normal.Bind(wx.EVT_BUTTON, self.OnNormal)

        self.Create_uniform = wx.Button(self.pnl, wx.ID_ANY, u"Create Uniform Profile", pos=(340, 230))
        self.pnl.sizer.Add(self.Create_uniform, 0, wx.ALL, 5)
        self.Create_uniform.Bind(wx.EVT_BUTTON, self.OnUniform)

        self.staticText12 = wx.StaticText(self.pnl, wx.ID_ANY,
                                         u"Enter input kWh, kvarh Excel filename",
                                         pos=(5, 300))
        self.staticText12.Wrap(-1)
        self.textCtrl10 = wx.TextCtrl(self.pnl, size=(400, 20), pos=(40, 320))
        self.textCtrl10.SetMaxLength(0)
        self.pnl.sizer.Add(self.textCtrl10, -1, wx.ALL, 5)

        self.staticText16 = wx.StaticText(self.pnl, wx.ID_ANY, u"Worksheet name", pos=(10, 350))

        self.staticText13 = wx.StaticText(self.pnl, wx.ID_ANY, u"Base current / A", pos=(10, 375))
        self.staticText14 = wx.StaticText(self.pnl, wx.ID_ANY, u"Voltage / V", pos=(10, 400))
        self.staticText15 = wx.StaticText(self.pnl, wx.ID_ANY, u"Number of phases", pos=(10, 425))

        self.textCtrl14 = wx.TextCtrl(self.pnl, size=(100, 20), pos=(110, 350))
        self.textCtrl14.SetMaxLength(0)
        self.pnl.sizer.Add(self.textCtrl14, -1, wx.ALL, 5)

        self.textCtrl11 = wx.TextCtrl(self.pnl, size=(50, 20), pos=(110, 375))
        self.textCtrl11.SetMaxLength(0)
        self.pnl.sizer.Add(self.textCtrl11, -1, wx.ALL, 5)
        self.textCtrl12 = wx.TextCtrl(self.pnl, size=(50, 20), pos=(110, 400))
        self.textCtrl12.SetMaxLength(0)
        self.pnl.sizer.Add(self.textCtrl12, -1, wx.ALL, 5)
        self.textCtrl13 = wx.TextCtrl(self.pnl, size=(50, 20), pos=(110, 425))
        self.textCtrl13.SetMaxLength(0)
        self.pnl.sizer.Add(self.textCtrl13, -1, wx.ALL, 5)

        self.Create_real = wx.Button(self.pnl, wx.ID_ANY, u"Create Real Profile", pos=(330, 350))
        self.pnl.sizer.Add(self.Create_real, 0, wx.ALL, 5)
        self.Create_real.Bind(wx.EVT_BUTTON, self.OnReal)

    def OnNormal(self, event):
        output_file = self.textCtrl1.GetValue()
        mean_current = float(self.textCtrl2.GetValue())
        current_sd = float(self.textCtrl3.GetValue())
        mean_phase = float(self.textCtrl4.GetValue())
        phase_sd = float(self.textCtrl5.GetValue())
        inputs ={'type': 'normal', 'centre_angle': (mean_phase, phase_sd), 'centre_current': (mean_current, current_sd) }
        load = Load_Utility(inputs, output_file)
        load.normal()

    def OnUniform(self, event):
        output_file = self.textCtrl1.GetValue()
        min_current = float(self.textCtrl6.GetValue())
        max_current = float(self.textCtrl7.GetValue())
        min_phase = float(self.textCtrl8.GetValue())
        max_phase = float(self.textCtrl9.GetValue())
        inputs = {'type': 'uniform', 'angle_range': (min_phase, max_phase),
                  'current_range': (min_current, max_current)}
        load = Load_Utility(inputs, output_file)
        load.uniform()


    def OnReal(self, event):
        output_file = self.textCtrl1.GetValue()
        input_file =self.textCtrl10.GetValue()
        current = float(self.textCtrl11.GetValue())
        voltage = float(self.textCtrl12.GetValue())
        n_phases = int(self.textCtrl13.GetValue())
        worksheet = self.textCtrl14.GetValue()
        # print(output_file)
        # print(input_file)
        # print(current)
        # print(voltage)
        # print(n_phases)
        # print(worksheet)
        # print('Real calculation')
        inputs = {'type': 'kwkvar_file', 'file_name': (input_file, worksheet)}
        load = Load_Utility(inputs, output_file)
        load.kwkvar(current, voltage, n_phases)



def main():
    app = wx.App()
    ex = UTILITY(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
