import glob
import op
import opx

from pprint import pprint


def check_dir_validity(dir_path):
    # TODO: check_dir_validity(dir_path)
    # Check that the supplied folder has the required blanks and other QC samples.
    pass


def main():
    """Run the org-process app."""
    # User inputs
    out_filepath = r'C:\code\projects\org-process\extras\results\results2.csv'

    # Make list of all blank files in directory
    dir = r'C:\code\projects\org-process\extras\analysis-reports\TRH Report'
    blank_data_list = []
    blank_pattern = dir + '\*' + opx.BLANK_TAG + '*'
    blank_file_list = glob.glob(blank_pattern)

    # Select the correct internal standard
    if opx.DEF_ANALYSIS_C6_C10:
        istd_rt = opx.DEF_ISTD_RT_C6_C10
        istd_rt_tolerance = opx.DEF_ISTD_RT_TOLERANCE_C6_C10
        istd_area_target = opx.DEF_ISTD_AREA_TARGET_C6_C10
        istd_area_tolerance = opx.DEF_ISTD_AREA_TOLERANCE_C6_C10
    else:
        istd_rt = opx.DEF_ISTD_RT_C10_C40
        istd_rt_tolerance = opx.DEF_ISTD_RT_TOLERANCE_C10_C40
        istd_area_target = opx.DEF_ISTD_AREA_TARGET_C10_C40
        istd_area_tolerance = opx.DEF_ISTD_AREA_TOLERANCE_C10_C40

    for f in blank_file_list:
        blank = op.get_data_from_report(f)[2]
        blank_data_list.append(blank)

    blank_average = op.BlankAverage(
        blank_data=blank_data_list,
        istd_rt=istd_rt,
        istd_rt_tolerance=istd_rt_tolerance,
        istd_area_target=istd_area_target,
        istd_area_tolerance=istd_area_tolerance)

    # Make exclude list for files that should not be analysed
    temp_files = glob.glob(dir + '~')
    excel_files = glob.glob(dir + '*.xls*')
    exclude_list = [x for x in glob.glob(dir + '\*') if x in temp_files and x not in excel_files]
    # Make list of all sample files in directory (includes QC)
    sample_file_list = [x for x in glob.glob(dir + '\*') if x not in blank_file_list and x not in exclude_list]

    # Initialise empty list for storing results
    result_set = []

    # Iterate through sample files and calculate results
    for f in sample_file_list:
        sample_name, analysis_time, peak_data = op.get_data_from_report(f)

        # Calculate C6-C10
        if opx.DEF_ANALYSIS_C6_C10:
            blank_average.area = blank_average.area_c6_c10
            i_c6 = 0
            i_c10 = op.get_fraction_end_index(peak_data, opx.C6_C10_END)
            conc_c6_c10 = op.calculate_sample_concentration(
                    peak_data_list=peak_data,
                    blank=blank_average,
                    low_index=i_c6,
                    high_index=i_c10,
                    istd_rt=istd_rt,  # USER INPUT
                    istd_rt_tolerance=istd_rt_tolerance,  # USER INPUT
                    istd_area_target=istd_area_target,  # USER INPUT
                    istd_area_tolerance=istd_area_tolerance,  # USER INPUT
                    calibration_slope=3.3164,  # USER INPUT
                    calibration_intercept=-0.3160,  # USER INPUT
                    istd_concentration=opx.DEF_ISTD_CONC_C6_C10,  # USER INPUT
                    dilution_factor=opx.DEF_DILUTION_FACTOR_C6_C10)  # USER INPUT

            result = {
                'sample_name': sample_name,
                'analysis_time': analysis_time,
                'conc_c6_c10': conc_c6_c10
            }

            result_set.append(result)

        # Calculate C10-C16
        # TODO: Analysis reports have different merged cell columns - how the fuck do we deal with this?
        if not opx.DEF_ANALYSIS_C6_C10:
            blank_average.area = blank_average.area_c10_c16
            i_c10 = op.get_fraction_start_index(peak_data, opx.C10_C16_START)
            i_c16 = op.get_fraction_end_index(peak_data, opx.C10_C16_END)
            conc_c10_c16 = op.calculate_sample_concentration(
                peak_data_list=peak_data,
                blank=blank_average,
                low_index=i_c10,
                high_index=i_c16,
                istd_rt=istd_rt,  # USER INPUT
                istd_rt_tolerance=istd_rt_tolerance,  # USER INPUT
                istd_area_target=istd_area_target,  # USER INPUT
                istd_area_tolerance=istd_area_tolerance,  # USER INPUT
                calibration_slope=3.3164,  # USER INPUT
                calibration_intercept=-0.3160,  # USER INPUT
                istd_concentration=opx.DEF_ISTD_CONC_C10_C40,  # USER INPUT
                dilution_factor=opx.DEF_DILUTION_FACTOR_C10_C40)  # USER INPUT

            # Calculate C16-C34
            blank_average.area = blank_average.area_c16_c34
            i_c34 = op.get_fraction_end_index(peak_data, opx.C16_C34_END)
            conc_c16_c34 = op.calculate_sample_concentration(
                peak_data_list=peak_data,
                blank=blank_average,
                low_index=i_c16,
                high_index=i_c34,
                istd_rt=istd_rt,  # USER INPUT
                istd_rt_tolerance=istd_rt_tolerance,  # USER INPUT
                istd_area_target=istd_area_target,  # USER INPUT
                istd_area_tolerance=istd_area_tolerance,  # USER INPUT
                calibration_slope=3.3164,  # USER INPUT
                calibration_intercept=-0.3160,  # USER INPUT
                istd_concentration=opx.DEF_ISTD_CONC_C10_C40,  # USER INPUT
                dilution_factor=opx.DEF_DILUTION_FACTOR_C10_C40)  # USER INPUT

            # Calculate C34-C40
            blank_average.area = blank_average.area_c34_c40
            i_c40 = op.get_fraction_end_index(peak_data, opx.C34_C40_END)
            conc_c34_c40 = op.calculate_sample_concentration(
                peak_data_list=peak_data,
                blank=blank_average,
                low_index=i_c34,
                high_index=i_c40,
                istd_rt=istd_rt,  # USER INPUT
                istd_rt_tolerance=istd_rt_tolerance,  # USER INPUT
                istd_area_target=istd_area_target,  # USER INPUT
                istd_area_tolerance=istd_area_tolerance,  # USER INPUT
                calibration_slope=3.3164,  # USER INPUT
                calibration_intercept=-0.3160,  # USER INPUT
                istd_concentration=opx.DEF_ISTD_CONC_C10_C40,  # USER INPUT
                dilution_factor=opx.DEF_DILUTION_FACTOR_C10_C40)  # USER INPUT

            result = {
                'sample_name': sample_name,
                'analysis_time': analysis_time,
                'conc_c10_c16': conc_c10_c16,
                'conc_c16_c34': conc_c16_c34,
                'conc_c34_c40': conc_c34_c40
            }

            result_set.append(result)

    # Write the result set to CSV file
    if opx.DEF_ANALYSIS_C6_C10:
        fieldnames = opx.FIELDNAMES_C6_C10
    else:
        fieldnames = opx.FIELDNAMES_C10_C40
    op.write_to_csv(result_set, out_filepath, fieldnames)

    # TODO: REMOVE THIS
    pprint(result_set)

if __name__ == "__main__":
    main()

