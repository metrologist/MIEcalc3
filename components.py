"""
The components module brings together the component information ready for a
full GUM calculation. Function choices, fitting coefficients and influence
parameters are gathered from csv files for the components.  The csv files are
generated in MIEcalculator.py.

It is a convenience to have all the data stored in csv files for processing.
The csv files can be created from a spread sheet (see extras module) or from
data manually entered into the gui (see graph_gui module).
"""
import GTC as gtc  # l.c. for convenience only
import numpy as np  # can differentiate, e.g. np.log from gtc.log
import csv  # for reading data
import operator


class COMPONENT(object):
    """
    This is the basis for the 'TRAN' and 'METER' classes. All
    data gathered from csv files assumed to be in the correct format.The detail
    of file and data formats is subject to change.
    """

    ##     def __init__(self):
    ##         # these values will be set by the methods that read them from csv files.
    ##         self.summary = []
    ##         self.err_choice = 0.0
    ##         self.err_no = 0.0
    ##         self.err_a = 0.0
    ##         self.err_b = 0.0
    ##         self.err_alpha = 0.0
    ##         self.t0 = 0.0

    def LoadCoeffs(self):
        """
        'LoadCoeffs()' opens a csv file formatted by line as

        * 'file name'
        * 'integer' for function choice
        * 'value', 'uncertainty', 'dof', 'label' of first coefficient
        * 'value', 'uncertainty', 'dof', 'label' of second coefficient
        * ...
        * 'correlation coefficient','correllation coefficient'...
        * 'value', 'uncertainty', 'dof', 'label' of b0 coefficient
        * 'value', 'uncertainty', 'dof', 'label' of temperature coefficient
        * 'value', 'uncertainty', 'dof', 'label' of calibration temperature
        * 'value', 'uncertainty', 'dof', 'label' of other influence coefficients
        * ...
        All these elements are returned in 'summary' as a list of lines.
        """
        # file is not initialised in COMPONENT, but this is left to the derived classes.
        reader = csv.reader(open(self.file, 'r'))  # assumes file exists
        self.summary = list()
        for row in reader:
            self.summary.append(row)

    def ureal_from_list(self, flist):  # for convenience in MakeUreal
        """
        Takes the *flist* of three floats and a label and returns a GTC ureal.
        """
        return gtc.ureal(float(flist[0]), float(flist[1]), float(flist[2]),
                         flist[3])

    def commonMakeUreals(self):
        """
        Takes the 'summary' list generated by 'LoadCoeffs' and, common to all
        components, turns the fit coefficents into correlated GTC ureals.  It
        also converts the calibration temperature and temperature coefficient
        into GTC ureals, but leaves the other influence coefficients for
        processing by 'specificMakeUreals' implemented in the 'METER' and
        'TRAN' classes.
        """
        self.err_choice = str(self.summary[1][0])  # error function label
        self.err_no = self.fit_fn[self.err_choice].no  # no. of coeffs in error fn
        # prepare for a multiple_ureal
        cov_matrix = np.zeros((self.err_no, self.err_no))
        coeffs = []
        label = []
        for i in range(2, 2 + self.err_no):  # assembles the fit coefficent as a ureal
            coeffs.append(float(self.summary[i][0]))
            label.append(self.summary[i][3])
        dof = float(self.summary[2][2])  # all fit parameters have same dof
        for i in range(self.err_no):
            for j in range(self.err_no):
                cov_matrix[i, j] = float(self.summary[2 + self.err_no][i * self.err_no + j])

        self.err_a = self.model.fit_ureals(coeffs, cov_matrix, dof, label)
        self.err_b = self.ureal_from_list(self.summary[2 + self.err_no + 1])
        self.err_alpha = self.ureal_from_list(self.summary[2 + self.err_no + 2])
        self.t0 = self.ureal_from_list(self.summary[2 + self.err_no + 3])

    def cal_error(self, X):
        """
        The calibration error at each current/voltage/phase point in list *X* is
        returned.  Calibration data has been fitted by an appropriate function
        chosen by matching the 'err_choice' integer with a 'MODEL' function as
        mapped in the 'METER' and 'TRAN' classes when initialising their 'fit_fn'
        dictionaries.
        """
        # it anticipates that derived classes will define a 'fit_fn'
        return self.fit_fn[self.err_choice].fn(X, self.err_a)

    def b_error(self, X):
        """
        Generates a list of identical 'err_b' values (from 'commonMakeUreals')
        that is the same length as *X*.  This is for calculation convenience.
        """
        return [self.err_b for x in X]

    def temp_error(self, X, temp):
        """
        Generates a list of identical temperature corrections due to 'temp'
        that is the same length as *X*.  This is for calculation convenience.
        """
        return [self.model.influence1(temp, self.t0, self.err_alpha) for x in X]

    def list_sum(self, fn_list):
        """
        Takes the list of functions in *fn_list* that all return equal length
        lists of numbers and returns a single list that is an element by element
        summation of each of the function lists.
        """
        a = len(fn_list[0])
        assert [len(i) == a for i in fn_list], 'lists must be of equal length'
        result = map(sum, zip(*fn_list))  # improved method
        return list(result)  # converts map to list

    def list_mult(self, fn_list):
        """
        Takes two only functions in *fnlist* that both return equal length lists of
        numbers and returns a single list that is an element by element
        multiplication of each of the function lists.
        """
        a = len(fn_list[0])
        assert [len(i) == a for i in fn_list], 'lists must be of equal length'
        result = [a * b for a, b in zip(fn_list[0], fn_list[1])]
        return list(result)  # converts map to list


class TRAN(COMPONENT):
    """
    The 'TRAN' class adds to the 'MODEL' class with error and phase functions
    suitable for fitting the calibration data for a transformer.  Additional
    influence functions are included to incorporate uncertainty and corrections
    due to influence effects on the error and phase. For example, temperature
    variations in the field are likely to exceed those experienced during lab
    calibration.  At present only 'file' is used from the input parameters with
    'name', 'phases' and 'model' being placeholders for items that might be
    useful either in the final report or, possibly, for allowing influence
    functions that depend on the transformer manufacturer's type.  The methods
    'total_error(X, temp, burden)' and 'total_phase(X, temp, burden)' give the
    final results for error and phase where 'X' is a list of I or V, 'temp' is
    the site temperature and 'burden' is the connected burden, the last two
    being uncertain reals.  Other methods give access to the internal steps,
    but are not normally used.

    It initialises with an arbitrary 'name', and yet unused 'phases' and 'model'
    arguments.  'file' must be the summary csv file for the transformer.

    """

    def __init__(self, name, phases, model, file):
        self.name = name  # e.g serial number or other key
        self.phases = phases  # e.g. RYB or single
        self.model = model  # gives access to the model functions
        self.file = file  # of coefficients
        # this dictionary of fit functions might differ between CT and VT
        # FUNC attaches the number of coefficients in the function
        self.fit_fn = {'0': model.f_mean, '1': model.f_line,
                       '2': model.f_logline}
        # coefficients loaded from file and processed on intialisation
        self.LoadCoeffs()
        self.commonMakeUreals()
        self.specificMakeUreals()

    def specificMakeUreals(self):
        """
        Converts the entries specific to transformers in the 'summary' list
        into GTC ureals, starting on the next list item after 'commonMakeUreals'.
        Both methods are run when the class is initialised.
        """
        phase_start = 8 + self.err_no  # starting row for phase data
        self.ph_choice = str(self.summary[phase_start][0])
        self.ph_no = self.fit_fn[self.ph_choice].no  # no. of coeffs in phase function
        self.err_gamma = self.ureal_from_list(self.summary[2 + self.err_no + 4])
        self.cal_burden = self.ureal_from_list(self.summary[2 + self.err_no + 5])
        # prepare for a multiple_ureal
        cov_matrix = np.zeros((self.ph_no, self.ph_no))
        coeffs = []
        label = []
        for i in range(phase_start + 1, phase_start + 1 + self.ph_no):  # assembles the fit coefficent as a ureal
            coeffs.append(float(self.summary[i][0]))
            label.append(self.summary[i][3])
        dof = float(self.summary[2][2])  # all fit parameters have same dof
        for i in range(self.ph_no):
            for j in range(self.ph_no):
                cov_matrix[i, j] = float(self.summary[2 + self.ph_no][i * self.ph_no + j])

        self.ph_a = self.model.fit_ureals(coeffs, cov_matrix, dof, label)
        ref_row = phase_start + 1 + self.ph_no
        self.ph_b = self.ureal_from_list(self.summary[ref_row + 1])
        self.ph_alpha = self.ureal_from_list(self.summary[ref_row + 2])
        self.ph_gamma = self.ureal_from_list(self.summary[ref_row + 3])

    def cal_phase(self, X):
        """
        The phase calibration error at each current/voltage point in list *X* is
        returned.  Calibration data has been fitted by an appropriate function
        chosen by matching the 'err_choice' integer with a 'MODEL' function as
        mapped in the 'METER' and 'TRAN' classes when initialising their 'fit_fn'
        dictionaries.
        """
        return self.fit_fn[self.ph_choice].fn(X, self.ph_a)

    def b_phase(self, X):
        """
        The 'b' coefficient in the fitted curve is not *X* dependent but this
        method has been constructed to produce a list of identical values for
        all elements of *X*. This is a convenience for the error summing
        algorithm, but will be reviewed.
        """
        return [self.ph_b for x in X]

    def temp_phase(self, X, temp):
        """
        The 'b' coefficient in the fitted curve is not *X* dependent but this
        method has been constructed to produce a list of identical values for
        all elements of *X*. This is a convenience for the error summing
        algorithm, but will be reviewed.
        """
        return [self.model.influence1(temp, self.t0, self.ph_alpha) for x in X]

    def burden_error(self, X, burden):
        """
        Returns the relative error in *burden* with respect to the
        calibration burden. Multiplying this by the measured error or phase
        displacement gives the additional error due to variation in burden.
        There is no *X* dependence but the number is returned as a list of the
        same lenght as *X* containing all equal values.
        """
        return [(burden - self.cal_burden) / self.cal_burden for x in X]

    def total_ind_error(self, X, temp, burden):
        """
        Returns a list of influence errors for each current/voltage phase point
        in list *X* as calculated at temperature *temp* for the chosen *burden*.
        The _ind_ in the name is now redundant (at one stage errors independent
        of current/voltage were separated out).
        """
        return self.list_sum([self.b_error(X),
                              self.list_mult([self.list_sum([self.temp_error(X, temp), self.burden_error(X, burden)]),
                                              self.cal_error(X)])])

    def total_ind_phase(self, X, temp, burden):
        """
        Returns a list of influence phase errors for each current/voltage point
        in list *X* as calculated at temperature *temp* for the chosen *burden*.
        The _ind_ in the name is now redundant (at one stage errors independent
        of current/voltage were separated out).
        """
        return self.list_sum([self.b_phase(X),
                              self.list_mult([self.list_sum([self.temp_phase(X, temp), self.burden_error(X, burden)]),
                                              self.cal_phase(X)])])

    def total_error(self, X, temp, burden):
        """
        This method is called externally to provide the total error (influence
        and calibration) for current/voltage points in *X* at the given *temp*
        and *burden*.
        """
        return self.list_sum([self.cal_error(X), self.total_ind_error(X, temp, burden)])

    def total_phase(self, X, temp, burden):
        """
        This method is called externally to provide the total phase error
        (influence and calibration) for current/voltage points in *X* at the
        given *temp* and *burden*.
        """
        return self.list_sum([self.cal_phase(X), self.total_ind_phase(X, temp, burden)])


class METER(COMPONENT):
    """
    The 'METER' class adds specific meter uncertainty components to the
    'COMPONENT' class.  For a meter, X refers to current and phase angle tuples.
    The method 'm_total_error' gives the total error for the meter.

    It initialises with an arbitrary *name*, and yet unused *elements* and *model*
    arguments.  *file* must be the summary csv file for the meter.
    """

    def __init__(self, name, elements, model, file):
        self.name = name  # e.g serial number or other key
        self.elements = elements  # i.e. single, two or three
        self.model = model  # gives access to the model functions
        self.file = file  # of coefficients
        # FUNC attaches the number of coefficients in the function
        self.fit_fn = {'0': model.f_smean, '1': model.f_plane,
                       '2': model.f_tan_s1, '3': model.f_tan_s2}
        # coefficients loaded from file and processed on intialisation
        self.LoadCoeffs()
        self.commonMakeUreals()
        self.specificMakeUreals()

    def specificMakeUreals(self):
        """
        Converts the entries specific to meters in the 'summary' list into GTC
        ureals, starting on the next list item after 'commonMakeUreals'. Both
        methods are run when the class is initialised
        """
        start = 6 + self.err_no  # start row for the specific meter influences
        self.m_annual = self.ureal_from_list(self.summary[start])
        self.m_volt = self.ureal_from_list(self.summary[start + 1])
        self.m_freq = self.ureal_from_list(self.summary[start + 2])
        self.m_field = self.ureal_from_list(self.summary[start + 3])
        self.m_harm = self.ureal_from_list(self.summary[start + 4])

    def drift_error(self, X, years):
        """
        Allows for a simple time drift.  This does not explicitly depend on *X*.
        At present the *X* dependence is a device for allowing this
        error to be treated identically to an influence that might be *X*
        dependent.  This approach will be reviewed.
        """
        return [self.model.influence1(years, 0.0, self.m_annual) for x in X]

    def volt_error(self, X, volts):
        """
        Error due to meter voltage dependence is calculated for all current-
        phase points in *X* at voltage *volts* given as a percentage difference
        from nominal 100% voltage (230 V or 63.5 V).
        """
        return [self.model.influence1(volts, 0.0, self.m_volt) for x in X]

    def freq_error(self, X, freq):
        """
        Error due to meter frequency dependence is calculated for all current-
        phase points in *X* at frewqency *freq* given as percentage difference
        from nominal 50 Hz.
        """
        return [self.model.influence1(freq, 0.0, self.m_freq) for x in X]

    def field_error(self, X, field):
        """
        Error dued to external magnetic fields is calculated for all current-
        phase points in *X*.  A simple linear dependence on *field* is assumed
        relative to a nominal zero field.  There is no *X* dependence.
        """
        return [self.model.influence1(field, 0.0, self.m_field) for x in X]

    def harm_error(self, X, harm):
        """
        Error dued to harmonics is calculated for all current-phase points in
        *X*.  A simple linear dependence on *harm* is assumed relative to nominal
        zero harmonics.  There is no *X* dependence.
        """
        return [self.model.influence1(harm, 0.0, self.m_harm) for x in X]

    def m_total_ind(self, X, temp, year, volts, freq, field, harm):
        """
        Returns a list of influence errors for each current-phase point in list
        *X* as calculated at temperature *temp*, for drift time *year* for the
        chosen *burden*. The _ind_ in the name is now redundant (at one stage
        errors independent of current/voltage were separated out).
        """
        return self.list_sum([self.b_error(X),
                              self.temp_error(X, temp), self.drift_error(X, year),
                              self.volt_error(X, volts), self.freq_error(X, freq),
                              self.field_error(X, field), self.harm_error(X, harm)])

    def m_total_error(self, X, temp, year, volts, freq, field, harm):
        """
        This method is called externally to provide the total meter error
        (influence and calibration) for each current-phase point in list
        *X* as calculated at temperature *temp*, for drift time *year*, voltage
        *volts*, frequency *freq*, external magnetic field *field* and harmonic
        levels *harm*.
        """
        return self.list_sum([self.cal_error(X), self.m_total_ind(X, temp, year, volts, freq, field, harm)])


class LOAD(object):
    """
    The LOAD class returns a standard load profile based on either actual or
    estimated energy transmitted through an installation.  The standard output
    is a list of (current, phase, normalised energy), where the energy has been
    normalised to add to unity over the full profile. Note that the phase angle
    magnitude is limited to be less than 89.9 degrees and the current to be
    greater than 0.1%.  This avoids extreme extrapolation of the fitting functions.

    It initialises with an arbitrary *name* and an output *csv_file* that either
    results from processing the nominal half-hour data in *txt_file* or could
    have been created independently.  The csv file is used for plotting and error
    calculation.

    """

    def __init__(self, name, csv_file, txt_file):
        self.name = name
        self.csvfile = csv_file
        self.txtfile = txt_file

    def normalise_hist(self):
        """
        Returns a list of (current, phase) tuples and a corresponding normalised
        list of energies.  This is suitable for error calculation and is
        compatible with the csv file produced by 'hist_from_raw'.
        """
        reader = csv.reader(open(self.csvfile, 'r'))
        load = []
        for row in reader:
            load.append(row)
        load = load[1:]  # remove header line with dx, dy, dz
        r = []
        z = []
        sum = 0
        for i in range(len(load)):
            r.append((float(load[i][0]), float(load[i][1])))
            z.append(float(load[i][2]))
            sum = sum + float(load[i][2])
        for i in range(len(z)):
            z[i] = z[i] / sum
        return r, z

    def hist_from_raw(self, raw_file, plotable_file):
        """
        Takes a text file, *raw_file*, of current, phase and watt hours assumed
        to be for equal time intervals (e.g. half hour).  This is processed into
        an energy histogram as a load profile in the form of a csv file,
        *plotable_file*.
        """
        load_data = np.loadtxt(raw_file)
        current = load_data[:, 0]
        phase = load_data[:, 1]
        energy = load_data[:, 2] / 1.0e6  # data assumed kWh, converting to GWh : not necessary??
        c_max = max(current)  # find maximum/minimum values
        c_min = min(current)
        p_max = max(phase)
        p_min = min(phase)
        # do not allow negative or zero values for current
        min_cur = 0.1  # 0.1%
        if c_max < min_cur:
            print('Load error, low or negative current')
            c_max = min_cur
        if c_min < min_cur:
            print('Load error, low or negative current')
            c_min = min_cur
        if p_max > 89.9:
            print('Load phase limited to 89.9 degrees maximum')
            p_max = 89.9
        if p_min < -89.9:
            print('Load phase limited to -89.9 degrees minimum')
            p_min = -89.9

        print('Max current = %2.2f %s, Min current = %2.2f %s, Max phase = %2.2f %s, Min phase = %2.2f %s' % (
        c_max, '%', c_min, '%', p_max, ' degrees', p_min, ' degrees'))
        print()
        hist, xedges, yedges = np.histogram2d(current, phase, bins=(20, 20), range=[[c_min, c_max], [p_min, p_max]],
                                              weights=energy)  # note that bins must be nxn to be compatible with grand_finale
        hist = np.transpose(hist)  # new in version beta 0.3.1
        # get data for plotting
        elements = (len(xedges) - 1) * (len(yedges) - 1)
        # this is some hand crafting of box size, moving 0.25 from the edge
        xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25)
        xpos = xpos.flatten()
        ypos = ypos.flatten()
        zpos = np.zeros(elements)
        # drawing a box of side length '8' starting at the corner 'edge + 0.25'
        ##         dx = 8 * np.ones_like(zpos)
        dx = 2 * np.ones_like(zpos)  # length 2 instead
        dy = dx.copy()
        dz = hist.flatten()

        # Simplest to assign the current/phase point a the centre of the histogram box
        # to the z value.
        x = np.zeros(len(xedges) - 1)
        for i in range(len(xedges) - 1):
            x[i] = (xedges[i] + xedges[i + 1]) / 2  # centre x
        y = np.zeros(len(yedges) - 1)
        for i in range(len(yedges) - 1):
            y[i] = (yedges[i] + yedges[i + 1]) / 2  # centre y
        x_current, y_phase = np.meshgrid(x, y)
        xlist = x_current.flatten()
        ylist = y_phase.flatten()
        r = []  # list of current, phase, Gwh tuples,
        # first line is box size
        r.append((dx[0], dy[0], zpos[0]))
        for i in range(len(xlist)):
            r.append((xlist[i], ylist[i], dz[i], xpos[i], ypos[i]))
            # note the file has the both the calculation and plotting points
        writer = csv.writer(open(plotable_file, 'w', newline=''))
        writer.writerows(r)
        return xpos, ypos, zpos, dx, dy, dz


class INSTALLATION(object):
    """
    The INSTALLATION class is for capturing all the information for a metering
    installation so that the overall error can be returned.  Components of
    METER, TRAN and LOAD classes are incorporated on initialisation.

    It initialises with an arbitrary *name*, METER class *meter*, TRAN class
    *ct*, TRAN class *vt*, LOAD class *load* and a csv file *conditions*.
    """

    def __init__(self, name, meter, ct, vt, load, conditions):

        self.name = name
        self.meter = meter
        self.ct = ct
        self.vt = vt
        self.load = load
        self.conditions = conditions
        self.make_inst_ureals()
        self.comp = COMPONENT()  # provides access to component methods

    def make_inst_ureals(self):
        """
        Converts site conditions in the csv 'conditions' file into GTC ureals.
        The file is assumed to be in the format

        * 'file name'
        * 'value', 'uncertainty', 'dof', 'label' of site temperature
        * ...                                    of site  voltage
        * ...                                      ...    frequency
        * ...                                             harmonics
        * ...                                             CT burden
        * ...                                             VT burden
        * ...                                             Site EM field
        * ...                                             Period of certification
        """
        reader = csv.reader(open(self.conditions, 'r'))
        summary = []
        for row in reader:
            summary.append(row)
        self.temp = gtc.ureal(float(summary[1][0]), float(summary[1][1]),
                              float(summary[1][2]), summary[1][3])
        self.volt = gtc.ureal(float(summary[2][0]), float(summary[2][1]),
                              float(summary[2][2]), summary[2][3])
        self.freq = gtc.ureal(float(summary[3][0]), float(summary[3][1]),
                              float(summary[3][2]), summary[3][3])
        self.harm = gtc.ureal(float(summary[4][0]), float(summary[4][1]),
                              float(summary[4][2]), summary[4][3])
        self.ct_bd = gtc.ureal(float(summary[5][0]), float(summary[5][1]),
                               float(summary[5][2]), summary[5][3])
        self.vt_bd = gtc.ureal(float(summary[6][0]), float(summary[6][1]),
                               float(summary[6][2]), summary[6][3])
        self.field = gtc.ureal(float(summary[7][0]), float(summary[7][1]),
                               float(summary[7][2]), summary[7][3])
        self.year = gtc.ureal(float(summary[8][0]), float(summary[8][1]),
                              float(summary[8][2]), summary[8][3])

    def site_error_terms(self):
        """
        This method returns:
        1. total error listed by point
        2. the overall error when weighted by the site's load profile.
        3. the current/phase points at which the calculations are made.

        All the calculations are kept together in this method for clarity on the
        propagation of GTC ureals.

        Note that site voltage is treated as an uncertain number with the VT
        magnitude and phase angle errors having no current dependence. The
        error that results from the VT phase angle error does of course vary
        with power factor.

        Note also that the influence functions are still returning lists of
        equal values set to have the same length as X, i.e. the number of points
        at which the errors are calculated.
        """
        # the load profile defines the points at which the error is calculated
        X, z = self.load.normalise_hist()
        # break out the current and phase angle part of X
        current = []
        angle = []
        voltage = []  # a list of common value uncertain voltages
        for i in range(len(X)):
            current.append(X[i][0] * (1 - self.freq / 100.0))  # frequency changes flux, higher frequency, lower flux
            angle.append(X[i][1])
            voltage.append(self.volt + 100.0 - self.freq)  # volt is entered (as uncertain zero) and added to 100%
        # similarly frequency is added because varying the frequency (in %) is the same as varying the voltage (but opposite sign)

        meter_part = self.meter.m_total_error(X, self.temp, self.year, self.volt,
                                              self.freq, self.field, self.harm)
        ct_error_part = self.ct.total_error(current, self.temp, self.ct_bd)
        ct_phase_part = self.ct.total_phase(current, self.temp, self.ct_bd)
        vt_error_part = self.vt.total_error(voltage, self.temp, self.vt_bd)
        vt_phase_part = self.vt.total_phase(voltage, self.temp, self.vt_bd)
        total_error = []
        for i in range(len(X)):
            total_error.append(meter_part[i] + ct_error_part[i] + vt_error_part[i]
                               + np.tan(angle[i] * np.pi / 180.0) * (ct_phase_part[i] - vt_phase_part[i]))

        """
        Calculating the 'overall error' requires a multiplication of error with
        a normalised load profile.
        """
        assert len(total_error) == len(z), 'error list and z list of equal length'
        assert abs(sum(z) - 1.0) < 1.0e-12, 'z normalised to unity'
        overall_error = sum(map(operator.mul, total_error, z))
        print('\n','Budget for overall error by coefficients')
        self.budget(overall_error)

        return total_error, overall_error, X

    def budget(self, a):
        """
        A GTC utility for listing the uncertainty budget for *a*.
        """
        print('\n\n')
        print('error = {0:.3f}, standard uncertainty = {1:.3f}, degrees of freedom = {2:.1f}'.format(a.x, a.u, a.df))
        for l, u, id_thing in gtc.reporting.budget(a, trim=0.0):
            print('%s: %G' % (l, u))
        print('\n')


if __name__ == "__main__":
    print('\n', 'Testing Components')
    print('\n', 'Test LOAD class')
    print('Expect to see a 3D scatter plot, showing empty and full bins.')
    load = LOAD('test1', 'dummy.csv', 'dummy.txt')  # note dummy files not used
    load.hist_from_raw('Tests\\myload2.txt', 'Tests\\myload.csv')
    load2 = LOAD('test2', 'Tests\\myload.csv', 'dummy.txt')
    r, z = load2.normalise_hist()
    print('r = ', r)
    print('z = ',z)

    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt

    x = []
    y = []
    for rr in r:
        x.append(rr[0])
        y.append(rr[1])
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, c='r', marker='o')
    ax.set_xlabel('Current/%')
    ax.set_ylabel('Phase/degrees')
    ax.set_zlabel('Energy')
    plt.show()

