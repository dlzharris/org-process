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
    def __init__(self, blank_data, istd_rt_low, istd_rt_hight,
                 istd_area_target, istd_area_tolerance, low_index, high_index):
        self.istd = mean([get_istd_area(x, istd_rt_low, istd_rt_hight, istd_area_target, istd_area_tolerance) for x in blank_data])
        self.area = mean([sum_areas(x, low_index, high_index) for x in blank_data])


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
    areas = [x[opx.PEAK_LS_AREA] for x in peak_data_list[low_index:high_index + 1]]
    return sum(areas)


def get_istd_area(peak_data_list, istd_rt_low, istd_rt_high, istd_area_target, istd_area_tolerance):
    """
    Get the peak area for the given internal standard
    :param peak_data_list: Peak area list for the sample
    :param istd_rt_low: Lowest retention time for the internal standard
    :param istd_rt_high: Highest retention time for the intenral standard
    :param istd_area_target: Target area for the internal standard
    :param istd_area_tolerance: Acceptable percent tolerance (expressed as a decimal) for istd area
    :return: Peak area integration for the internal standard
    """
    # Calculate acceptable upper and lower limits
    lower_limit = istd_area_target - istd_area_tolerance
    upper_limit = istd_area_target + istd_area_tolerance

    # Find all peaks in istd range
    istd_peak_list = [x[opx.PEAK_LS_AREA] for x in peak_data_list if istd_rt_low >= x[opx.PEAK_LS_RT] >= istd_rt_high
                      and lower_limit <= x[opx.PEAK_LS_AREA] <= upper_limit]

    # Test for presence of a single acceptable peak
    if len(istd_peak_list) == 0:
        raise IstdError("No acceptable internal standard peaks found.")
    elif len(istd_peak_list) > 1:
        raise IstdError("More than one acceptable internal standard peak found.")
    else:
        return istd_peak_list[0]  # istd area


def get_fraction_boundary_indexes(peak_data_list, rt_end):
    """
    Finds the start and end indexes for the peaks list for the retention times wanted
    :param peak_data_list: Peak area list for the sample
    :param rt_start: Starting retention time for boundaries
    :param rt_end: Ending retention time for boundaries
    :return: Tuple containing the starting and ending indexes.
    """
    #TODO: Get all boundaries for all fractions, or just ends, or just for one fraction? Need to clarify structure.
    # Get the differences for each peak and find the closest to zero that
    # Get ending index
    end_indexes = [(x[opx.PEAK_LS_IDX], x[opx.PEAK_LS_END] - rt_end) for x in peak_data_list if x[opx.PEAK_LS_END] - rt_end >= 0]
    end_tuple = min(end_indexes, key = lambda i: i[1])
    return end_tuple[0]


def mean(list):
    """
    Calculates the mean of a given list of numbers.
    :param list: List of numbers
    :return: Mean of the list.
    """
    return sum(list) / len(list)


def calculate_sample_concentration(peak_data_list, blank, low_index, high_index, istd_rt_low,
                                   istd_rt_high, istd_area_target, istd_area_tolerance,
                                   calibration_slope, calibration_intercept, istd_concentration,
                                   dilution_factor):
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
    istd = get_istd_area(peak_data_list, istd_rt_low, istd_rt_high, istd_area_target, istd_area_tolerance)

    istd_blank_corrected = istd * (blank.area / blank.istd)
    area_blank_corrected = area - istd_blank_corrected

    response_ratio = area_blank_corrected / istd
    concentration_ratio = (response_ratio - calibration_slope) / calibration_intercept

    concentration_vial = concentration_ratio * istd_concentration
    concentration_sample = concentration_vial * dilution_factor

    return concentration_sample
