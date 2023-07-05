import wx
import wx.richtext as richtext
from formeqns import EqnForm
import os
import GTC as gtc
import docx
import time
from PIL import Image
import io


class REPORT(EqnForm):

    def __init__(self, parent):
        """
        All the writing processes for the final reporting
        """
        EqnForm.__init__(self, parent)

    def OnSave(self, event):
        """
        Saves a Word version of the report with a suggested folder and file name.
        The default is to save it in the same folder as the Excel spread sheet
        while appending .docx to the full Excel file name.
        """
        wildcard = "Project report (*.docx)|*.docx|" \
                   "All files (*.*)|*.*"
        dirname = self.projwd[:-9]  # the one above xls_temp (remove 9 characters)
        dlg = wx.FileDialog(self, "Choose folder to save report", defaultDir=dirname,
                            defaultFile=self.proj_file + '.docx',
                            wildcard=wildcard, style=wx.FD_SAVE)

        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            docx_file = os.path.join(dirname, filename)
            # create and save word report
            self.wordreport(docx_file)
        dlg.Destroy()

    def OnPrint(self, event):
        self.PrintNow()

    def PrintNow(self):
        """
        Prints the rich text report without preview but with a printer dialog.
        Printing to a system pdf printer can be a convenient way of saving a
        record of the report.
        """
        rtp = richtext.RichTextPrinting("Print")
        localtime = time.asctime(time.localtime(time.time()))
        footer = self.m_statusBar1.GetStatusText(1) + ' printed on ' + localtime
        rtp.SetFooterText(footer)  # reads file name
        rtp.PrintBuffer(self.report_richText.GetBuffer())

    def both(self, row, rich, value):
        """
        This simultaneously sends *value* to *row* to write to the file and
        writes the same *value* to the *rich* text window.  There should be a
        more elegant way to do this.
        """
        rich.AppendText(value)
        rich.AppendText(', ')
        row.append(value)

    def reporter(self, final_error):
        """
        Creates strings, including numerical values calculated from the GTC
        ureal *final_error*, for feeding into reports. It also returns a list of
        png files for inclusion in reports.
        """
        self.report_txt = []  # vital to clear these lists before writing a new report
        self.report_images = []
        self.report_images_wx = []
        # overall_error = final_error
        uncertainty = final_error.u * gtc.reporting.k_factor(final_error.df)
        maximum = final_error.x + uncertainty
        minimum = final_error.x - uncertainty

        # summarising uncertainty
        meterCal = ['a0 meter', 'a1 meter', 'a2 meter', 'a3 meter', 'b0 meter', 'Meter annual drift']
        meterInf = ['Meter field dependence', 'Meter temperature coefficient', 'Meter frequency dependence',
                    'Meter voltage dependence', 'Meter harmonic dependence']
        ctCal = ['a0 CT_e', 'a0 CT_p', 'a1 CT_e', 'a1 CT_p', 'a2 CT_e', 'a2 CT_p', 'b0 CT_e', 'b0 CT_p',
                 'CT calibration temperature', 'CT calibration burden']
        ctInf = ['CT temperature coefficient of error', 'CT temperature coefficient of phase',
                 'CT burden coefficient of error', 'CT burden coefficient of phase']
        vtCal = ['a0 VT_e', 'a0 VT_p', 'a1 VT_e', 'a1 VT_p', 'a2 VT_e', 'a2 VT_p', 'b0 VT_e', 'b0 VT_p',
                 'VT calibration temperature', 'VT calibration burden']
        vtInf = ['VT temperature coefficient of error', 'VT temperature coefficient of phase',
                 'VT burden coefficient of error', 'VT burden coefficient of phase']
        siteInf = ['Site EM field', 'Site temperature', 'Site voltage', 'Site frequency', 'Site harmonics',
                   'Site VT burden', 'Site CT burden']
        complist = [meterCal, meterInf, ctCal, ctInf, vtCal, vtInf, siteInf]
        xx = self.model.budget_by_label(final_error, complist)
        excluding_site = xx[0] + xx[1] + xx[2] + xx[3] + xx[4] + xx[5]
        normalised_share = [xx[0] / excluding_site, xx[1] / excluding_site, xx[2] / excluding_site,
                            xx[3] / excluding_site, xx[4] / excluding_site, xx[5] / excluding_site]

        # prepare text/strings needed for any output version
        self.report_txt.append('Metering Installation Error Report')  # 0
        self.report_txt.append('The error calculated for the given load profile is ')  # 1
        self.report_txt.append("%+ 0.2f %s" % (final_error.x, '%.'))  # 2
        self.report_txt.append('The expanded uncertainty at an estimated 95% level of confidence is')  # 3
        self.report_txt.append("%s %0.2f %s" % ('', uncertainty, '%.'))  # 4
        self.report_txt.append('The uncertainty interval extends from ')  # 5
        self.report_txt.append("%+ 0.2f %s to %+0.2f %s" % (minimum, '%', maximum, '%.'))  # 6
        self.report_txt.append('Uncertainty contribution by component as a percentage of total variance,')  # 7
        self.report_txt.append('Meter:')  # 8
        self.report_txt.append("%s %0.2G %s" % (' ', (normalised_share[0] + normalised_share[1]) * 100, ' %'))  # 9
        self.report_txt.append('CT:')  # 10
        self.report_txt.append("%s %0.2G %s" % (' ', (normalised_share[2] + normalised_share[3]) * 100, ' %'))  # 11
        self.report_txt.append('VT:')  # 12
        self.report_txt.append("%s %0.2G %s" % (' ', (normalised_share[4] + normalised_share[5]) * 100, ' %'))  # 13
        self.report_txt.append('A full list of components contributing to the total uncertainty can be found in the')  # 14
        self.report_txt.append('report workbook tab, "Input file list and messages".')  # 15
        self.report_txt.append('Installation error over the phase and current ranges that match the load profile.')  # 16
        self.report_txt.append('Annual load profile used for this error calculation.')  # 17
        self.report_txt.append(
            'Component calibration data with calculated fits over the calibration ranges shown overleaf.')  # 18
        self.report_txt.append('Current Transformer')  # 19
        self.report_txt.append('Voltage Transformer')  # 20
        self.report_txt.append('Meter')  # 21

        # gather graphs for reporting
        image = self.buffer_image_wx(self.report_graph.canvas)
        self.report_images_wx.append(image[0])
        self.report_images.append(image[1])
        image = self.buffer_image_wx(self.load_graph.canvas)
        self.report_images_wx.append(image[0])
        self.report_images.append(image[1])
        image = self.buffer_image_wx(self.CT_graph_1.canvas)
        self.report_images_wx.append(image[0])
        self.report_images.append(image[1])
        image = self.buffer_image_wx(self.VT_graph_1.canvas)
        self.report_images_wx.append(image[0])
        self.report_images.append(image[1])
        image = self.buffer_image_wx(self.meter_graph.canvas)
        self.report_images_wx.append(image[0])
        self.report_images.append(image[1])

    def buffer_image_wx(self, plot_canvas):
        """

        Takes the plot on a canvas and prints it to a buffer which is then scaled
        and created as a wx richtext compatible image. The size (360, 270) could be
        an input parameter.
        :param plot_canvas: is a canvas in wx holding a graph
        :return:
        """
        buffer = io.BytesIO()
        plot_canvas.print_figure(buffer, format='png', dpi=300)
        buffer.seek(0)
        img1 = Image.open(buffer)
        img = img1.resize((360, 270), Image.LANCZOS)
        image = wx.Image(img.size[0], img.size[1])
        image.SetData(img.convert("RGB").tobytes())
        return image, buffer

    def wxreport(self):
        """
        Takes the *t_strings* and *image_files* lists prepared in 'reporter'
        and writes the report to the wxRichText panel in the GUI.
        """
        t_strings = self.report_txt
        # write to the wxRichText panel
        report = self.report_richText
        report.BeginFontSize(14)
        report.BeginBold()
        report.WriteText(t_strings[0])
        report.Newline()
        report.EndBold()
        report.EndFontSize()
        report.BeginFontSize(10)
        report.WriteText(t_strings[1])
        report.BeginBold()
        report.WriteText(t_strings[2])
        report.EndBold()
        report.Newline()
        report.WriteText(t_strings[3])
        report.BeginBold()
        report.WriteText(t_strings[4])
        report.EndBold()
        report.Newline()
        report.WriteText(t_strings[5])
        report.WriteText(t_strings[6])
        report.Newline()
        report.Newline()
        report.WriteText(t_strings[7])
        report.Newline()
        report.WriteText(t_strings[8])
        report.WriteText('\t')
        report.WriteText(t_strings[9])
        report.Newline()
        report.WriteText(t_strings[10])
        report.WriteText('\t\t')
        report.WriteText(t_strings[11])
        report.Newline()
        report.WriteText(t_strings[12])
        report.WriteText('\t\t')
        report.WriteText(t_strings[13])
        report.Newline()
        report.WriteText(t_strings[14])
        report.Newline()
        report.WriteText(t_strings[15])
        report.Newline()
        report.Newline()

        # add graph images to report, first rescaling them to fit a simple printout.
        # image resolution is degraded by the scaling.
        report.WriteText(t_strings[16])
        report.Newline()

        report.WriteImage(self.report_images_wx[0])  # insert image buffer in wx rich text
        report.Newline()
        report.Newline()
        report.WriteText(t_strings[17])
        report.Newline()

        report.WriteImage(self.report_images_wx[1])
        report.Newline()
        report.WriteText(t_strings[18])
        report.Newline()
        report.Newline()
        report.BeginFontSize(8)
        report.BeginBold()
        report.WriteText(t_strings[19])
        report.Newline()

        report.WriteImage(self.report_images_wx[2])
        report.Newline()
        report.WriteText(t_strings[20])
        report.Newline()

        report.WriteImage(self.report_images_wx[3])
        report.Newline()
        report.WriteText(t_strings[21])
        report.Newline()

        report.WriteImage(self.report_images_wx[4])
        report.Newline()
        report.EndBold()

    def wordreport(self, docx_file):
        """
        Takes the *t_strings* and *image_files* lists prepared in 'reporter' and writes
        the report to a word document. The document will display the text in the
        default styles in the Word installation used to view the file.  The image
        files retain their native resolution. By default, the name and folder of
        the Excel input file is used simply with .docx added at the end. A folder
        'templates' is assumed to hold default.docx on which to build the report.
        """
        t_strings = self.report_txt
        assert len(t_strings) > 0, "Nothing to report.  Run calculation before attempting to save"
        template = os.path.join(self.cwd, 'templates', 'default.docx')
        document = docx.Document(template)
        document.add_heading(t_strings[0], level=0)
        localtime = time.asctime(time.localtime(time.time()))
        identifier = '(Data source: ' + self.m_statusBar1.GetStatusText(1) + '. Error calculated: ' + localtime + '.)'
        document.add_heading(identifier, level=1)
        document.add_paragraph(t_strings[1] + t_strings[2])
        document.add_paragraph(t_strings[3] + t_strings[4])
        document.add_paragraph(t_strings[5] + t_strings[6])
        document.add_heading(t_strings[16], level=2)
        image_files = self.report_images
        document.add_picture(image_files[0], width=docx.shared.Mm(100))
        document.add_heading(t_strings[17], level=2)
        document.add_picture(image_files[1], width=docx.shared.Mm(100))
        document.add_heading(t_strings[18][:-16] + '.', level=2)
        document.add_heading(t_strings[19] + '.', level=3)
        document.add_picture(image_files[2], width=docx.shared.Mm(100))
        document.add_heading(t_strings[20] + '.', level=3)
        document.add_picture(image_files[3], width=docx.shared.Mm(100))
        document.add_heading(t_strings[21] + '.', level=3)
        document.add_picture(image_files[4], width=docx.shared.Mm(100))
        document.add_page_break()
        document.add_heading('Additional Information', level=1)
        document.add_heading('Uncertainty Contribution Summary', level=2)
        document.add_paragraph(t_strings[7] + ' ' + t_strings[8] + t_strings[9] + ', '
                               + t_strings[10] + t_strings[11] + ', ' + t_strings[12] + t_strings[13] + '.')
        document.add_heading('Text Output From Calculation Process', level=2)
        no_lines = self.m_textCtrl3.GetNumberOfLines()
        for x in range(no_lines):
            output_notes = self.m_textCtrl3.GetLineText(x)
            document.add_paragraph(output_notes)
        document.save(docx_file)


if __name__ == '__main__':
    app = wx.App()
    frame = REPORT(None)
    frame.Show()
    app.MainLoop()