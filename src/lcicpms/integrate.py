'''
@author: Christian Dewey
@date: Jul 27, 2024
'''
from numpy import where

class Integrate:
    """
    A class to handle integration of signal traces over a given time range.
    """

    @staticmethod
    def integrate(intensities, times, time_range: tuple = None):
        """
        Computes the area under the signal trace curve between a specified time range.

        This function performs trapezoidal integration on the provided intensities and times,
        returning the total area within the time range. If no time range is provided, it will
        integrate over the entire signal.

        Args:
            intensities (array-like): The intensities corresponding to each time point.
            times (array-like): The time points at which the intensities were measured.
            time_range (tuple, optional): The start and end times for the integration. 
                                          If None, the entire signal is integrated. Defaults to None.

        Returns:
            float: The computed area under the curve between the specified time range.
        """
        if time_range is None:
            i_tmin = 0
            i_tmax = len(times) - 2
        else:
            i_tmin = int(where(abs(times - time_range[0]) == min(abs(times - time_range[0])))[0][0])
            i_tmax = int(where(abs(times - time_range[1]) == min(abs(times - time_range[1])))[0][0])

        peak_area = 0
        dt = 0

        for i in range(i_tmin, i_tmax):
            dt1_intensities = intensities[i]
            dt2_intensities = intensities[i + 1]
            
            dt_I_min = min([dt1_intensities, dt2_intensities])
            dt_I_max = max([dt1_intensities, dt2_intensities])
            
            dt = (times[i + 1] - times[i])

            rect_area = dt * dt_I_min
            top_area = dt * (dt_I_max - dt_I_min) * 0.5
            d_peak_area = rect_area + top_area

            peak_area += d_peak_area

        return peak_area