__author__ = 'Daniel Harris'
__date__ = '02 February 2017'
__email__ = 'daniel.harris@dpi.nsw.gov.au'
__version__ = '0.1'


###############################################################################
# Constants
###############################################################################
# Excel report constants
SAMPLE_NAME_COLUMN = 21
SAMPLE_NAME_ROW = 1
ANALYSIS_TIME_COLUMN = 21
ANALYSIS_TIME_ROW = 4
PEAK_INDEX_COLUMN = 0
PEAK_START_COLUMN = 2
PEAK_END_COLUMN = 8
RT_COLUMN = 5
AREA_COLUMN = 15

# Retention time boundaries
C6_C10_START = 4.016
C6_C10_END = 13.836
C10_C16_START = 7.781
C10_C16_END = 12.60
C16_C34_START = 12.60
C16_C34_END = 29.68
C34_C40_START = 29.68
C34_C40_END = 32.80

# Peak data indexes
PEAK_LS_IDX = 0
PEAK_LS_START = 1
PEAK_LS_RT = 2
PEAK_LS_END = 3
PEAK_LS_AREA = 4

# Filename flags
BLANK_TAG = 'BLK'

# Default values
DEF_IST_RT = 6.445
DEF_ISTD_RT_TOLERANCE = 0.045
DEF_ISTD_AREA_TARGET = 92767
DEF_ISTD_AREA_TOLERANCE = 11834
DEF_ISTD_CONC_C6_C10 = 2
DEF_ISTD_CONC_C10_C40 = 51.19
DEF_DILUTION_FACTOR_C6_C10 = 2
DEF_DILUTION_FACTOR_C10_C40 = 0.005
DEF_ANALYSIS_C6_C10 = True