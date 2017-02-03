import xlrd
import op
import opx


def get_data_from_report(file):
    """
    Gets retention time and peak area data from a MassHunter-generated Excel report
    :param file: Fully resolved location and file name of target report file
    :return: List of tuples of each peak, retention time and area of sample
    """
    # Open the Excel workbook
    gcms_book = xlrd.open_workbook(file)
    sheet = gcms_book.sheet_by_index(0)

    # Collate sample metadata
    sample_name = sheet.cell(opx.SAMPLE_NAME_ROW, opx.SAMPLE_NAME_COLUMN).value
    analysis_time = sheet.cell(opx.ANALYSIS_TIME_ROW, opx.ANALYSIS_TIME_COLUMN).value

    # Find beginning of integration peak list
    n = 0
    while sheet.cell(n, opx.PEAK_INDEX_COLUMN).value != "Integration Peak List":
        n += 1
    PEAK_LIST_START_ROW = n + 2

    # Find end of integration peak list
    n = PEAK_LIST_START_ROW
    while sheet.cell_type(n, opx.PEAK_INDEX_COLUMN) not in (xlrd.XL_CELL_BLANK, xlrd.XL_CELL_EMPTY):
        n += 1
    PEAK_LIST_END_ROW = n

    # Import peak and rt data
    peaks = sheet.col_values(opx.PEAK_INDEX_COLUMN, PEAK_LIST_START_ROW, PEAK_LIST_END_ROW)
    starts = sheet.col_values(opx.PEAK_START_COLUMN, PEAK_LIST_START_ROW, PEAK_LIST_END_ROW)
    rts = sheet.col_values(opx.RT_COLUMN, PEAK_LIST_START_ROW, PEAK_LIST_END_ROW)
    ends = sheet.col_values(opx.PEAK_END_COLUMN, PEAK_LIST_START_ROW, PEAK_LIST_END_ROW)
    areas = sheet.col_values(opx.AREA_COLUMN, PEAK_LIST_START_ROW, PEAK_LIST_END_ROW)

    peaks = map(int, peaks)
    peak_data = zip(peaks, starts, rts, ends, areas)

    return sample_name, analysis_time, peak_data


def check_dir_validity(dir_path):
    # TODO: check_dir_validity(dir_path)
    # Check that the supplied folder has the required blanks and other QC samples.
    pass


def main():
    """Run the org-process app."""
    FILE = r'C:\code\projects\org-process\extras\analysis-reports\16_0475_1_AnalysisReport.xls'
    sample_name, analysis_time, peak_data = get_data_from_report(FILE)

    # User inputs

    # Make list of all blank files in directory
    # Make list of all sample files in directory (includes QC)

    # blank_data_list = []
    # For each file in BLANKS
    #    blank = get_data_from_report(file)
    #    blank_data_list.append(blank)
    # blank_average = op.BlankAverage(all the stuff)

    # for each sample file in selected directory
        # calculate sample concentration



if __name__ == "__main__":
    main()

