from lcicpms.integrate import Integrate
from numpy import array 

def get_peak_start_end_times(time_range : tuple = (-1, -1), all_times : array = None):

    if time_range[0] == -1:
        tmin = min(all_times)
    else:
        tmin = time_range[0]

    if time_range[1] == -1:
        tmax = max(all_times)
    else:
        tmax = time_range[1]

    return (tmin, tmax)


def get_peak_area(intensities : dict = None, times : dict = None, time_range : tuple = (-1,-1)):

    trange = get_peak_start_end_times(time_range, times)

    area = Integrate.integrate(intensities, times, trange)

    return area 