'''
@author: Christian Dewey
@date: Jul 27, 2024
'''

from raw_icpms_data import RawICPMSData
from calibration import Calibration

import utils 

class Quantitate:

    def run(self, raw_icpms_data : RawICPMSData = None, calibration : Calibration = None, elements : list = [], time_range : tuple = (-1,-1), internal_std_correction : bool = False, baseline_subtraction : bool = False, unit : str = 'ppb'):
        '''
        Runs the quantiation over specified time range for passed elements. Returns dictionary with elements as keys, concentrations as values.
        '''

        intensities = raw_icpms_data.intensities
        times = raw_icpms_data.times

        peak_areas = {}
        concentrations = {}

        for element in elements:

            area = utils.get_peak_area(intensities, times, element, time_range)

            peak_areas[element] =  area 

            calibration_curve = Calibration.curves[element]
            m =  calibration_curve.m
            b = calibration_curve.b
            concentrations[element] = m * area + b 

            return concentrations
