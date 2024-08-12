'''
@author: Christian Dewey
@date: Jul 27, 2024
'''

from pandas import DataFrame

from quantitate import Quantitate
from raw_icpms_data import RawICPMSData
import utils 
from calibration import Calibration

class ChromaFeature:

    def __init__(self, time_range, elements : list = [], feature_name : str = None, internal_std_element : str = '115In', internal_std_correction : float = 1.0):

        # name of feature 
        self.feature_name = feature_name
        # time range of feature
        self.time_range = time_range
        # elements to consider
        self.elements = elements
        # concentrations
        self.concentrations : dict = {}
        # intensities
        self.peak_areas : dict = {}

        self._internal_std_element = internal_std_element
        self._internal_std_correction = internal_std_correction



    def run_quantitation(self,raw_icpms_data : RawICPMSData = None, calibration : Calibration = None, unit : str = 'ppb', internal_std_correction : bool = False, baseline_subtraction : bool = False):
        '''
        Runs the quantitation function for elements over specified time range 
        '''
        elements = self.elements
        time_range = self.time_range

        self.concentrations = Quantitate.run(raw_icpms_data, calibration, elements, time_range, internal_std_correction, baseline_subtraction, unit)


    def export_concentrations_as_dataframe(self, unit : str = 'ppb'):

        trange = utils.get_peak_start_end_times(self.time_range, self.all_times)

        concentrations = {e+'_'+unit:self.concentrations[e] for e in self.elements}
        params = {'Feature Name': self.feature_name, 'Start Time': trange[0], 'Stop Time': trange[1], 'Int. Std. Corr. Factor': self._internal_std_correction, 'Int. Std. Element': self._internal_std_element}

        output_dict = {**params, **concentrations}

        output_df = DataFrame(output_dict)

        return output_df
    

    def export_concentrations_as_csv(self, fname, elements = None):
        '''
        Exports concentrations to csv file specified as fname. 
        '''

        output_df = self.export_concentrations_as_dataframe()
    
        output_df.to_csv(fname, index=False)