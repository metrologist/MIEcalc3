import wx
import os
from formbuild import MyFrame1
import extras


class ProjectFrame(MyFrame1):
    """
    Manages the selection of notebook pages and the sizing of grids.
    """

    def __init__(self, parent):
        """
        Sets up title, icon and notebook structure. Defaults to displaying report notebook.
        :param parent: MyFrame1 from formbuild.py
        """
        self.cwd = os.getcwd()  # identifies working directory at startup.
        MyFrame1.__init__(self, parent)
        iconFile = os.path.join(self.cwd, 'MSL2.ico')
        icon1 = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon1)
        self.SetTitle(u"Metering Installation Error Calculator\
        (June 2021, v1.1)")  # keep title and version up to date.
        self.notebooks = {'Report notebook': self.m_notebook1, 'Meter notebook': self.m_notebook11,
                          'CT notebook': self.CT_notebook, 'VT notebook': self.VT_notebook,
                          'Load notebook': self.m_notebook14, 'Site notebook': self.m_notebook15}
        self.BookSelect('Report notebook')

    # Select which notebook to show from 'Select View' menu events
    def OnReportSelect(self, event):
        self.BookSelect('Report notebook')

    def OnMeterSelect(self, event):
        self.BookSelect('Meter notebook')

    def OnCTSelect(self, event):
        self.BookSelect('CT notebook')

    def OnVTSelect(self, event):
        self.BookSelect('VT notebook')

    def OnLoadSelect(self, event):
        self.BookSelect('Load notebook')

    def OnSiteSelect(self, event):
        self.BookSelect('Site notebook')

    def BookSelect(self, book_name):
        """
        Allows selection of any of the 6 notebooks, *book_number* from the
        'select notebook' menu.
        """
        for x in self.notebooks:
            if x != book_name:
                self.notebooks[x].Hide()
        self.notebooks[book_name].Show()
        self.m_statusBar1.SetStatusText(book_name, 0)
        self.SendSizeEvent()

    # Respond to events generated to set up the wxGrids
    def OnSetCTRows(self, event):  # in CT notebook
        """
        Spinner for setting number of grid rows for the CT.
        """
        self.SetRows(self.row_spin3, self.CTratio_data)
        self.SetRows(self.row_spin3, self.CTphase_data)

    def OnSetVTRows(self, event):  # in VT notebook
        """
        Spinner for setting the number of grid rows for the VT.
        """
        self.SetRows(self.row_spin31, self.VTratio_data)
        self.SetRows(self.row_spin31, self.VTphase_data)

    def OnSetMeterRows(self, event):  # in meter notebook
        self.SetRows(self.row_spin11, self.meter_data)

    def SetRows(self, spinner, grid):
        """
        For using a wx spin control, *spinner* to set *grid* size for manual
        entry.
        """
        rows = spinner.GetValue()
        self.SetGridRows(grid, rows)

    def SetGridRows(self, grid_name, no_of_rows):
        """
        Set grid, *grid_name*, to have rows, *no_of_rows*.
        """
        grid_name.ClearGrid()  # clear all data first
        change_rows = no_of_rows - grid_name.GetNumberRows()
        if change_rows > 0:
            grid_name.AppendRows(change_rows)  # always to end
        elif change_rows < 0:
            grid_name.DeleteRows(0, -change_rows)  # from posn 0

    def SetGridCols(self, grid_name, no_of_cols):
        """
        Set grid, *grid_name*, to have columns, *no_of_cols*.
        """
        grid_name.ClearGrid()  # clear all data first
        change_cols = no_of_cols - grid_name.GetNumberCols()
        if change_cols > 0:
            grid_name.AppendCols(change_cols)  # always to end
        elif change_cols < 0:
            grid_name.DeleteRows(0, -change_cols)  # from posn 0


if __name__ == '__main__':
    app = wx.App()
    frame = ProjectFrame(None)
    frame.Show()
    app.MainLoop()
