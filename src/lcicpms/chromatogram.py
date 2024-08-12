'''
@author: Christian Dewey
@date: Jul 27, 2024
'''
import matplotlib.pyplot as plt
from numpy import where 

from raw_icpms_data import RawICPMSData
from calibration import Calibration
from chroma_feature import ChromaFeature
import utils

class Chromatogram:

    def __init__(self, raw_data_file : str = None):

        self.raw_icpms_data = RawICPMSData(raw_data_file)
        self.calibration : Calibration = None
        self.sample_name : str = None
        self.chroma_features : dict = {}

        # internal standard 
        self.internal_std_element : str = '115In'
        # internal std correction factor
        self.internal_std_correction : float = None
        # units for concentration 
        self.concentration_unit : str = 'ppb' 
        # valid concentration units
        self._valid_conc_units = ['ppb' ,'ppm', 'ppt','uM','mM','M']

    
    def plot_chromatogram(self, elements : list = ['115In'], time_range : tuple = (-1,-1)):
        '''
        Plots chromatograms for passed elements over passed time_range.
        '''
                
        times = self.raw_icpms_data.times
        intensities = self.raw_icpms_data.intensities

        fig, ax = plt.subplots()

        for element in elements:

            trange = utils.get_peak_start_end_times(time_range, times[element])        
            range_indices = where((times[element] > trange[0]) & (where(times[element] < trange[1])))

            x = trange[range_indices]
            y = intensities[element][range_indices]

            ax.plot(x, y, label=element)

        plt.show()

    
    def add_chroma_feature(self, time_range : tuple = (-1,-1), elements : list = [], feature_name: str = None):

        n = 1
        if feature_name == None:
            if len(self.chroma_features.keys()) > 0:
                for k in self.chroma_features.keys():
                    if 'Unknown Feature ' in k:
                        i = k.split(' ')[-1]
                        if i > n:
                            n = i 
            feature_name = 'Unknown Feature ' + str(n)
        
        self.chroma_features[feature_name] = ChromaFeature(time_range, elements, feature_name, self.internal_std_element, self.internal_std_correction)


    def run_quantitation_on_all_features(self, unit : str = 'ppb', internal_std_correction : bool = False, baseline_subtraction : bool = False):

        feature_keys = list(self.chroma_features.keys())

        if len(feature_keys) == 0:

            raise Exception('No features have been defined for this chromatogram.')

        for key in feature_keys:

            self.chroma_features[key].run_quantitation(self.raw_icpms_data, self.calibration, unit, internal_std_correction, baseline_subtraction)
