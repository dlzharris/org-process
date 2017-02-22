import csv
import opx

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
    def __init__(self, blank_data, istd_rt, istd_rt_tolerance, istd_area_target, istd_area_tolerance):

        # Create required empty lists
        areas_c6_c10 = []
        areas_c10_c16 = []
        areas_c16_c34 = []
        areas_c34_c40 = []

        # For each blank item
        for blank in blank_data:
            if opx.DEF_ANALYSIS_C6_C10:
                # Find bounding indexes for C6-C10 fraction
                i_c10 = get_fraction_end_index(blank, opx.C6_C10_END)
                sum_c6_c10 = sum_areas(blank, 0, i_c10)
                areas_c6_c10.append(sum_c6_c10)
                # Calculate average peak area
                self.area_c6_c10 = mean(areas_c6_c10)

            if not opx.DEF_ANALYSIS_C6_C10:
                # Find bounding indexes for C10-C16 fraction
                i_c10 = get_fraction_start_index(blank, opx.C10_C16_START)
                i_c16 = get_fraction_end_index(blank, opx.C10_C16_END)
                sum_c10_c16 = sum_areas(blank, i_c10, i_c16)
                areas_c10_c16.append(sum_c10_c16)
                # Find bounding indexes for C16-C34 fraction
                i_c34 = get_fraction_end_index(blank, opx.C16_C34_END)
                sum_c16_c34 = sum_areas(blank, i_c16, i_c34)
                areas_c16_c34.append(sum_c16_c34)
                # Find bounding indexes for C34-C40 fraction
                i_c40 = get_fraction_end_index(blank, opx.C34_C40_END)
                sum_c34_c40 = sum_areas(blank, i_c34, i_c40)
                areas_c34_c40.append(sum_c34_c40)
                # Calculate average peak areas
                self.area_c10_c16 = mean(areas_c10_c16)
                self.area_c16_c34 = mean(areas_c16_c34)
                self.area_c34_c40 = mean(areas_c34_c40)

        self.istd = mean([get_istd_area(x, istd_rt, istd_rt_tolerance, istd_area_target, istd_area_tolerance) for x in blank_data])
        self.area = None

###############################################################################
# Functions
###############################################################################
def sum_areas(peak_data_list, low_index, high_index):
    """
    Sums the peak areas given a set of bounding indices for the peak data list
    :param peak_data_list: Peak area list for the sample
    :param low_index: Index of first peak to sum
    :param high_index: Index of final peak in list to sum
    :return: Total area between the bounding indices.
    """
    areas = [x[opx.PEAK_LS_AREA] for x in peak_data_list[low_index:high_index]]
    return sum(areas)


def get_istd_area(peak_data_list, istd_rt, istd_rt_tolerance, istd_area_target, istd_area_tolerance):
    """
    Get the peak area for the given internal standard
    :param peak_data_list: Peak area list for the sample
    :param istd_rt_low: Lowest retention time for the internal standard
    :param istd_rt_high: Highest retention time for the intenral standard
    :param istd_area_target: Target area for the internal standard
    :param istd_area_tolerance: Acceptable percent tolerance (expressed as a decimal) for istd area
    :return: Peak area integration for the internal standard
    """
    # Calculate acceptable retention time window
    istd_rt_low = istd_rt - istd_rt_tolerance
    istd_rt_high = istd_rt + istd_rt_tolerance
    # Calculate acceptable upper and lower limits
    lower_limit = istd_area_target - istd_area_tolerance
    upper_limit = istd_area_target + istd_area_tolerance

    # Find all peaks in istd range
    istd_peak_list = [x[opx.PEAK_LS_AREA] for x in peak_data_list if istd_rt_low <= x[opx.PEAK_LS_RT] <= istd_rt_high
                      and lower_limit <= x[opx.PEAK_LS_AREA] <= upper_limit]

    # Test for presence of a single acceptable peak
    if len(istd_peak_list) == 0:
        raise IstdError("No acceptable internal standard peaks found.")
    elif len(istd_peak_list) > 1:
        raise IstdError("More than one acceptable internal standard peak found.")
    else:
        return istd_peak_list[0]  # istd area


def get_fraction_end_index(peak_data_list, rt_end):
    """
    Finds the ending index for the peaks list for the retention time wanted
    :param peak_data_list: Peak area list for the sample
    :param rt_end: Ending retention time for boundaries
    :return: Integer representing the ending index.
    """
    # Get the differences for each peak and find the closest to zero that
    end_indexes = [(x[opx.PEAK_LS_IDX], x[opx.PEAK_LS_END] - rt_end) for x in peak_data_list if
                   x[opx.PEAK_LS_END] - rt_end >= 0]
    # Get ending index
    end_tuple = min(end_indexes, key = lambda i: i[1])
    return end_tuple[0]


def get_fraction_start_index(peak_data_list, rt_start):
    """
    Finds the starting index for the peaks list for the retention times wanted
    :param peak_data_list: Peak area list for the sample
    :param rt_start: Starting retention time for boundaries
    :return: Integer representing the starting index.
    """
    # Get the differences for each peak and find the closest to zero that
    start_indexes = [(x[opx.PEAK_LS_IDX], abs(x[opx.PEAK_LS_START] - rt_start)) for x in peak_data_list if
                   x[opx.PEAK_LS_START] - rt_start <= 0]
    # Get starting index
    try:
        start_tuple = min(start_indexes, key=lambda i: i[1])
        start_idx = start_tuple[0]
    except ValueError:
        # First detected peak starts after target retention time
        start_idx = 1
    return start_idx


def mean(list):
    """
    Calculates the mean of a given list of numbers.
    :param list: List of numbers
    :return: Mean of the list.
    """
    return sum(list) / len(list)


def calculate_sample_concentration(peak_data_list, blank, low_index, high_index, istd_rt, istd_rt_tolerance,
                                   istd_area_target, istd_area_tolerance, calibration_slope, calibration_intercept,
                                   istd_concentration, dilution_factor):
    """
    Calculate the concentration of a compound in a sample
    :param peak_data_list: Peak area list for the sample
    :param blank: Instance of BlankAverage class
    :param low_index: Index of first peak to sum
    :param high_index: Index of final peak in list to sum
    :param istd_rt_low: Lowest retention time for the internal standard
    :param istd_rt_high: Highest retention time for the intenral standard
    :param istd_area_target: Target area for the internal standard
    :param istd_area_tolerance: Acceptable percent tolerance (expressed as a decimal) for istd area
    :return: Final corrected concentration for compound in sample.
    """
    area = sum_areas(peak_data_list, low_index, high_index)
    istd = get_istd_area(peak_data_list, istd_rt, istd_rt_tolerance, istd_area_target, istd_area_tolerance)

    istd_blank_corrected = istd * (blank.area / blank.istd)
    area_blank_corrected = area - istd_blank_corrected

    response_ratio = area_blank_corrected / istd
    concentration_ratio = (response_ratio - calibration_intercept) / calibration_slope

    concentration_vial = concentration_ratio * istd_concentration
    concentration_sample = concentration_vial * dilution_factor

    return round(concentration_sample, opx.DEF_DECIMAL_PLACES)


def write_to_csv(data_list, out_filepath, fieldnames_list):
    """
    Write a list of data dictionaries to a csv file
    :param data_list: List of dictionaries to be written. Each dictionary
        represents one line of data to be written
    :param out_filepath: Path to file object to be written to
    :param fieldnames_list: List of fieldnames to be used when writing
    :return: No return value
    """
    with open(out_filepath, 'wb') as f:
        writer = csv.DictWriter(
            f,
            delimiter=',',
            extrasaction='ignore',
            fieldnames=fieldnames_list
        )
        writer.writeheader()
        writer.writerows(data_list)
    return True
