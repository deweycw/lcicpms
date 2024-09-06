'''
@author: Christian Dewey
@date: Jul 27, 2024
'''

from lcicpms.raw_icpms_data import RawICPMSData
from lcicpms.calibration import Calibration
from lcicpms.in_out import export_df
from lcicpms.integrate import Integrate
import lcicpms.utils as utils

class Quantitate:
    """
    A class to perform quantitation of elements using LC-ICP-MS data. It applies
    calibration curves to raw LC-ICP-MS data to compute concentrations over a given time range.
    """

    def run(raw_icpms_data: RawICPMSData = None, 
            calibration: Calibration = None,
            elements: list = [], 
            time_range: tuple = (-1, -1), 
            istd_baseline: float = -1.0, 
            istd_time_range: tuple = (-1, -1),
            baseline_subtraction: bool = False, 
            unit: str = 'ppb'):
        """
        Perform quantitation for a specified list of elements over a time range.

        Args:
            raw_icpms_data (RawICPMSData): An instance of RawICPMSData containing 
                                           raw ICP-MS intensities and times.
            calibration (Calibration): An instance of Calibration containing 
                                       calibration curves for elements.
            elements (list): A list of element names (strings) to be quantified.
            time_range (tuple): A tuple representing the start and end times 
                                (in seconds) for quantitation. Defaults to (-1, -1),
                                which indicates using the entire time range.
            istd_baseline (float): The baseline value for internal standard correction. 
                                   If > 0, internal standard correction is applied.
                                   Defaults to -1.0 (no correction).
            istd_time_range (tuple): A tuple representing the time range for the 
                                     internal standard. Defaults to (-1, -1).
            baseline_subtraction (bool): If True, baseline subtraction is applied. 
                                         Defaults to False.
            unit (str): The unit of the concentration (e.g., 'ppb'). Defaults to 'ppb'.

        Returns:
            dict: A dictionary containing:
                - 'areas': DataFrame of integrated peak areas for each element.
                - 'concentrations': DataFrame of concentrations calculated for each element.
                - 'internal_std_correction': The internal standard correction factor applied.
        
        """
        
        intensities = raw_icpms_data.intensities
        times = raw_icpms_data.times

        istd_correction = 1 

        if istd_baseline > 0:
            istd_trange = utils.get_peak_start_end_times(istd_time_range, times['115In'])
            istd_area = Integrate.integrate(intensities['115In'], times['115In'], istd_trange)
            istd_correction = istd_baseline / istd_area
            

        peak_areas = {}
        concentrations = {}
        trange = [-1,-1]

        for element in elements:

            trange = utils.get_peak_start_end_times(time_range, times[element])
            area = Integrate.integrate(intensities[element], times[element], trange)

            peak_areas[element] =  float(area) * istd_correction

            calibration_curve = calibration.curves[element]
            m =  calibration_curve.m
            b = calibration_curve.b
            concentrations[element] = float(m * area * istd_correction + b )
        
        return {'areas':export_df(peak_areas, trange), 'concentrations':export_df(concentrations, trange), 'internal_std_correction':istd_correction}