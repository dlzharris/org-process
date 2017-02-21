import glob
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
    # User inputs

    # Make list of all blank files in directory
    dir = r'C:\code\projects\org-process\extras\analysis-reports'
    blank_data_list = []
    blank_pattern = dir + '\*' + opx.BLANK_TAG + '*'
    blank_file_list = glob.glob(blank_pattern)

    for f in blank_file_list:
        blank = get_data_from_report(f)[2]
        blank_data_list.append(blank)

    blank_average = op.BlankAverage(
        blank_data=blank_data_list,
        istd_rt=opx.DEF_IST_RT,
        istd_rt_tolerance=opx.DEF_ISTD_RT_TOLERANCE,
        istd_area_target=opx.DEF_ISTD_AREA_TARGET,
        istd_area_tolerance=opx.DEF_ISTD_AREA_TOLERANCE)

    # Make list of all sample files in directory (includes QC)
    sample_file_list = [x for x in glob.glob(dir + '\*') if x not in blank_file_list]

    # Iterate through sample files and calculate results
    for f in sample_file_list:
        sample_name, analysis_time, peak_data = get_data_from_report(f)

        # Calculate C6-C10
        if opx.DEF_ANALYSIS_C6_C10:
            i_c6 = 1
            i_c10 = op.get_fraction_end_index(peak_data, opx.C6_C10_END)
            conc_c6_c10 = op.calculate_sample_concentration(
                    peak_data_list=peak_data,
                    blank=blank_average,
                    low_index=i_c6,
                    high_index=i_c10,
                    istd_rt=opx.DEF_IST_RT,  # USER INPUT
                    istd_rt_tolerance=opx.DEF_ISTD_RT_TOLERANCE,  # USER INPUT
                    istd_area_target=opx.DEF_ISTD_AREA_TARGET,  # USER INPUT
                    istd_area_tolerance=opx.DEF_ISTD_AREA_TOLERANCE,  # USER INPUT
                    calibration_slope=4.2608,  # USER INPUT
                    calibration_intercept=0,  # USER INPUT
                    istd_concentration=opx.DEF_ISTD_CONC_C6_C10,  # USER INPUT
                    dilution_factor=opx.DEF_DILUTION_FACTOR_C6_C10)  # USER INPUT

        # Calculate C10-C16
        if not opx.DEF_ANALYSIS_C6_C10:
            i_c16 = op.get_fraction_end_index(peak_data, opx.C10_C16_END)
            conc_c6_c10 = op.calculate_sample_concentration(
                peak_data_list=peak_data,
                blank=blank_average,
                low_index=i_c10,
                high_index=i_c16,
                istd_rt=opx.DEF_IST_RT,  # USER INPUT
                istd_rt_tolerance=opx.DEF_ISTD_RT_TOLERANCE,  # USER INPUT
                istd_area_target=opx.DEF_ISTD_AREA_TARGET,  # USER INPUT
                istd_area_tolerance=opx.DEF_ISTD_AREA_TOLERANCE,  # USER INPUT
                calibration_slope=4.2608,  # USER INPUT
                calibration_intercept=0,  # USER INPUT
                istd_concentration=opx.DEF_ISTD_CONC_C10_C40,  # USER INPUT
                dilution_factor=opx.DEF_DILUTION_FACTOR_C10_C40)  # USER INPUT

            # Calculate C16-C34
            i_c34 = op.get_fraction_end_index(peak_data, opx.C16_C34_END)
            conc_c16_c34 = op.calculate_sample_concentration(
                peak_data_list=peak_data,
                blank=blank_average,
                low_index=i_c16,
                high_index=i_c34,
                istd_rt=opx.DEF_IST_RT,  # USER INPUT
                istd_rt_tolerance=opx.DEF_ISTD_RT_TOLERANCE,  # USER INPUT
                istd_area_target=opx.DEF_ISTD_AREA_TARGET,  # USER INPUT
                istd_area_tolerance=opx.DEF_ISTD_AREA_TOLERANCE,  # USER INPUT
                calibration_slope=4.2608,  # USER INPUT
                calibration_intercept=0,  # USER INPUT
                istd_concentration=opx.DEF_ISTD_CONC_C10_C40,  # USER INPUT
                dilution_factor=opx.DEF_DILUTION_FACTOR_C10_C40)  # USER INPUT

            # Calculate C34-C40
            i_c40 = op.get_fraction_end_index(peak_data, opx.C34_C40_END)
            conc_c34_c40 = op.calculate_sample_concentration(
                peak_data_list=peak_data,
                blank=blank_average,
                low_index=i_c34,
                high_index=i_c40,
                istd_rt=opx.DEF_IST_RT,  # USER INPUT
                istd_rt_tolerance=opx.DEF_ISTD_RT_TOLERANCE,  # USER INPUT
                istd_area_target=opx.DEF_ISTD_AREA_TARGET,  # USER INPUT
                istd_area_tolerance=opx.DEF_ISTD_AREA_TOLERANCE,  # USER INPUT
                calibration_slope=4.2608,  # USER INPUT
                calibration_intercept=0,  # USER INPUT
                istd_concentration=opx.DEF_ISTD_CONC_C10_C40,  # USER INPUT
                dilution_factor=opx.DEF_DILUTION_FACTOR_C10_C40)  # USER INPUT



if __name__ == "__main__":
    main()

