__author__ = 'Daniel Harris'
__date__ = '02 February 2017'
__email__ = 'daniel.harris@dpi.nsw.gov.au'
__version__ = '0.1'


###############################################################################
# Custom exception classes
###############################################################################
class IstdError(Exception):
    """ Custom excption for ISTD errors."""
    pass


###############################################################################
# Custom classes
###############################################################################
class BlankAverage:

    def __init__(self, blank_data):
        pass
