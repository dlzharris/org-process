import xlrd

# Set up global constants
SAMPLE_NAME_COLUMN = 22
SAMPLE_NAME_ROW = 1
ANALYSIS_TIME_COLUMN = 22
ANALYSIS_TIME_ROW = 4
RT_COLUMN = 5
AREA_COLUMN = 15
PEAK_INDEX_COLUMN = 0

# Open the Excel workbook
gcms_book = xlrd.open_workbook(file)
sheet = gcms_book.sheet_by_index(0)

# Collate sample metadata
sample_name = sheet.cell(SAMPLE_NAME_ROW, SAMPLE_NAME_COLUMN)
analysis_time = sheet.cell(ANALYSIS_TIME_ROW, ANALYSIS_TIME_COLUMN)

# Import peak and rt data




