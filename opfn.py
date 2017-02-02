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

    def __init__(self, blank_data):
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


def get_istd_area(peak_data_list, istd_rt_low, istd_rt_high, istd_area_target, istd_area_tolerance):
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
        raise IstdError("No acceptable internal standard peaks found.")
    elif len(istd_peak_list) > 1:
        raise IstdError("More than one acceptable internal standard peak found.")
    else:
        return istd_peak_list[0]  # istd area


def mean(list):
    """
    Calculates the mean of a given list of numbers.
    :param list: List of numbers
    :return: Mean of the list.
    """
    return sum(list) / len(list)