"""
Attempt at code to reflect ideas on how to deal with actual burden differing from the burden used for calibration.
Essentially want to test the basics before embedding it in MIEcalc.
"""
from GTC import ureal

def relative_burden(burden, cal_burden):
    """
    Returns the relative error in *burden* with respect to the
    calibration burden.
    """
    print(name)  # this will be carried in as self.name in the class
    if name == 'CT':
        rel_brdn_error = (burden - cal_burden) / cal_burden
        mag = abs(rel_brdn_error)
        print('mag = ', mag)
        if mag > 0.2:  # i.e. not within 20 % of the calibration burden
            print()
            print('WARNING')
            print('Actual CT burden more than 20 % away from burden used for calibration.')
            print('CT error calculation may not be valid.','\n')
    elif name == 'VT':
        rel_brdn_error = (burden - cal_burden) / cal_burden
        if rel_brdn_error.x != 0:
            print('Actual VT burden must be the same as the burden at which the VT was calibrated.')
            print('VT error may not be valid.')
    else:
        print('Not named as either a CT or VT, relative error set to zero')
        rel_brdn_error = 0

    return rel_brdn_error

def burden_error_delta(rel_bdn, e, f):
    """

    :param rel_bdn: from 0 (equal) to 1 (zero actual burden)
    :param e: the error calculated for the transformer
    :param f: the factor for estimating the zero burden error from the error calibrated at the calibration burden
    :return: the change in error due to the change in burden
    """
    print(name)  # this will be carried in as self.name in the class
    if name == 'CT':
        if e.x > 0:
            print('Positive transformer error cannot be automatically corrected for burden change.')
            min_e = e.x  # will return zero
        else:
            min_e = e.x * factor  # disconnecting the uncertainty in cal_error
        delta = rel_bdn * (e.x - min_e)
    elif name == 'VT':  # warning already given about VT needing a burden identical to the calibration burden
        delta =0
    else:
        print('Not named as either a CT or VT, delta error set to zero')
        delta = 0
    return delta

name = 'CT'  # must be CT or VT
cal_burden = 1.0  # ohm
bdn = 1.0
u_bdn = bdn / 10
burden = ureal(bdn, u_bdn, label= name + ' actual burden')  # ohm or siemen
cal_error = ureal(0.2, 0.02)  # usual relative calibration error
factor = ureal(0.35,0.15)  # the factor could be 0.2 or 0.5



rel_burden = relative_burden(burden, cal_burden)
print('burden relative error ',rel_burden)
delta_error = burden_error_delta(rel_burden, cal_error, factor)
print('change in error due to burden ',delta_error)
print('original calibration error', cal_error)
print('error corrected for burden ', cal_error + delta_error)