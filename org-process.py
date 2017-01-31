import xlrd

file = r'C:\Users\harrisdn\Downloads\16_0475_1_AnalysisReport.xls'

# Set up global constants
SAMPLE_NAME_COLUMN = 21
SAMPLE_NAME_ROW = 1
ANALYSIS_TIME_COLUMN = 21
ANALYSIS_TIME_ROW = 4
PEAK_INDEX_COLUMN = 0
PEAK_START_COLUMN = 2
PEAK_END_COLUMN = 8
RT_COLUMN = 5
AREA_COLUMN = 15

# Open the Excel workbook
gcms_book = xlrd.open_workbook(file)
sheet = gcms_book.sheet_by_index(0)

# Collate sample metadata
sample_name = sheet.cell(SAMPLE_NAME_ROW, SAMPLE_NAME_COLUMN).value
analysis_time = sheet.cell(ANALYSIS_TIME_ROW, ANALYSIS_TIME_COLUMN).value

# Find beginning of integration peak list
n = 0
while sheet.cell(n, PEAK_INDEX_COLUMN).value != "Integration Peak List":
    n += 1
PEAK_LIST_START_ROW = n + 2

# Find end of integration peak list
n = PEAK_LIST_START_ROW
while sheet.cell_type(n, PEAK_INDEX_COLUMN) not in (xlrd.XL_CELL_BLANK, xlrd.XL_CELL_EMPTY):
    n += 1
PEAK_LIST_END_ROW = n

# Import peak and rt data
peaks = sheet.col_values(PEAK_INDEX_COLUMN, PEAK_LIST_START_ROW, PEAK_LIST_END_ROW)
starts = sheet.col_values(PEAK_START_COLUMN, PEAK_LIST_START_ROW, PEAK_LIST_END_ROW)
rts = sheet.col_values(RT_COLUMN, PEAK_LIST_START_ROW, PEAK_LIST_END_ROW)
ends = sheet.col_values(PEAK_END_COLUMN, PEAK_LIST_START_ROW, PEAK_LIST_END_ROW)
areas = sheet.col_values(AREA_COLUMN, PEAK_LIST_START_ROW, PEAK_LIST_END_ROW)

peak_data = zip(peaks, starts, rts, ends, areas)





