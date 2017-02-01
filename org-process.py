import xlrd
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


def get_bounding_indexes():
    # TODO: get_bounding_indexes()
    pass


def sum_areas(peak_data_list, low_index, high_index):
    """
    Sums the peak areas given a set of bounding indices for the peak data list
    :param peak_data_list: Peak area list for the sample
    :param low_index: Index of first peak to sum
    :param high_index: Index of final peak in list to sum
    :return: Total area between the bounding indices.
    """
    areas = [x[4] for x in peak_data_list[low_index:high_index + 1]]
    return sum(areas)


def get_istd_area(peak_data_list, istd_rt_target, istd_rt_low, istd_rt_high, istd_area_target, istd_area_tolerance):
    """
    Get the peak area for the given internal standard
    :param peak_data_list: Peak area list for the sample
    :param istd_rt: Retention time for the given internal standard
    :return: Peak area integration for the internal standard
    """
    # Calculate acceptable upper and lower limits
    lower_limit = istd_area_target - istd_area_tolerance
    upper_limit = istd_area_target + istd_area_tolerance

    # Find all peaks in istd range
    istd_peak_list = [x[4] for x in peak_data_list if istd_rt_low >= x[2] >= istd_rt_high and lower_limit <= x[4] <= upper_limit]

    # Test for presence of a single acceptable peak
    if len(istd_peak_list) == 0:
        # TODO: Error signal for no istds found
        print "No acceptable internal standard peaks found"
    elif len(istd_peak_list) > 1:
        # TODO: Error signal for multiple istds found
        print "More than one acceptable internal standard peak found"
    else:
        istd_area = istd_peak_list[0]

    return istd_area


def main():
    """Run the org-process app."""
    FILE = r'C:\code\projects\org-process\extras\analysis-reports\16_0475_1_AnalysisReport.xls'
    sample_name, analysis_time, peak_data = get_data_from_report(FILE)

    # User inputs
    #



if __name__ == "__main__":
    main()

