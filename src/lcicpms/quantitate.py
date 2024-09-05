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

    def run(raw_icpms_data : RawICPMSData = None, 
            calibration : Calibration = None,
            elements : list = [], 
            time_range : tuple = (-1,-1), 
            istd_baseline : float = -1.0, 
            istd_time_range : tuple = (-1,-1),
            baseline_subtraction : bool = False, 
            unit : str = 'ppb'):
        '''
        Runs the quantiation over specified time range for passed elements. Returns dictionary with elements as keys, concentrations as values.
        '''

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
