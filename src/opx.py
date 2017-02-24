"""
Module: opx.py
Global constants and default values used in the Org-Process application.

Author: Daniel Harris
Title: Data & Procedures Officer
Organisation: DPI Water
Date modified: 24/02/2017
"""

__author__ = 'Daniel Harris'
__date__ = '24 February 2017'
__email__ = 'daniel.harris@dpi.nsw.gov.au'
__version__ = '1.0'


###############################################################################
# Constants
###############################################################################
# Excel report constants
SAMPLE_NAME_ROW = 1
ANALYSIS_TIME_ROW = 4
PEAK_INDEX_COLUMN = 0

# Variable columns
SAMPLE_NAME_COLUMN = 26
ANALYSIS_TIME_COLUMN = 26
PEAK_START_COLUMN = 2
PEAK_END_COLUMN = 8
RT_COLUMN = 5
AREA_COLUMN = 14

# Retention time boundaries
C6_C10_START = 4.016
C6_C10_END = 13.30
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
DEF_ISTD_RT_C6_C10 = 6.445
DEF_ISTD_RT_TOLERANCE_C6_C10 = 0.045
DEF_ISTD_AREA_TARGET_C6_C10 = 92767
DEF_ISTD_AREA_TOLERANCE_C6_C10 = 61834

DEF_ISTD_RT_C10_C40 = 30.817
DEF_ISTD_RT_TOLERANCE_C10_C40 = 0.117
DEF_ISTD_AREA_TARGET_C10_C40 = 285359
DEF_ISTD_AREA_TOLERANCE_C10_C40 = 110000

DEF_ISTD_CONC_C6_C10 = 2
DEF_ISTD_CONC_C10_C40 = 51.19

DEF_DILUTION_FACTOR_C6_C10 = 2
DEF_DILUTION_FACTOR_C10_C40 = 0.005

DEF_CALIBRATION_SLOPE = 3.3164
DEF_CALIBRATION_INTERCEPT = -0.3160

DEF_ANALYSIS_C6_C10 = True
DEF_DECIMAL_PLACES = 3

# CSV Options
FIELDNAMES_C6_C10 = ['sample_name', 'analysis_time', 'conc_c6_c10']
FIELDNAMES_C10_C40 = ['sample_name', 'analysis_time', 'conc_c10_c16', 'conc_c16_c34', 'conc_c34_c40']
