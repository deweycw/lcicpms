'''
@author: Christian Dewey
@date: September 4, 2024
'''

import os 
from pandas import concat

from lcicpms.raw_icpms_data import RawICPMSData
from lcicpms.integrate import Integrate
from lcicpms.quantitate import Quantitate
from lcicpms.calibration import Calibration


class Dataset:
    """
    A class to handle raw LC-ICP-MS data, perform calibration, 
    internal standard corrections, and quantify element concentrations.
    
    Attributes:
        raw_data_dir (str): Directory containing raw ICP-MS data files.
        cal_data_dir (str): Directory containing calibration files.
        skip_keywords (list): List of keywords to exclude certain files.
        raw_data_dict (dict): Dictionary of loaded raw data files.
        cal_icpms_obj_dict (dict): Dictionary of calibration files.
        _cal_has_run (bool): Flag indicating whether calibration has been performed.
        cal (Calibration): Calibration object containing standard concentrations and elements.
        concentrations_df (DataFrame): Final concentrations of elements after quantification.
    """
    
    def __init__(self, raw_data_dir: str = None, 
                 cal_data_dir: str = None,
                 skip_keywords: list = ['results']):
        """
        Initialize the Dataset object with directories for raw and calibration data.
        
        Args:
            raw_data_dir (str): Directory containing raw data files.
            cal_data_dir (str): Directory containing calibration data files.
            skip_keywords (list): List of keywords to filter out unwanted files (default: ['results']).
        """
        self.raw_data_dir = raw_data_dir
        self.skip_keywords = skip_keywords
        self._cal_has_run = False
        self.raw_data_dict = self.load_raw_data(self.raw_data_dir)
        
        if cal_data_dir is None:
            self.cal_data_dir = raw_data_dir
        else:
            self.cal_data_dir = cal_data_dir


    def load_raw_data(self, dir):
        """
        Load raw ICP-MS data files from the specified directory.
        
        Args:
            dir (str): Directory to load raw data from.
        
        Returns:
            dict: Dictionary where keys are file paths and values are RawICPMSData objects.
        """
        print(f'loading all files in {dir}')
        flist = [os.path.join(dir, f)
                 for f in os.listdir(dir) 
                 if f.endswith('.csv') and not any(s in f for s in self.skip_keywords)]
        
        icpms_obj_dict = {}
        for f in flist:
            icpms_obj = RawICPMSData(f)
            icpms_obj_dict[f] = icpms_obj
        
        self.elements = icpms_obj.elements
        return icpms_obj_dict
    
    
    def run_calibration(self,
                        cal_std_concs: list = [0, 10, 25, 50, 100, 200], 
                        cal_keywords_by_conc: list = ['std_0', 'std_1', 'std_2', 'std_3', 'std_4', 'std_5']):
        """
        Perform calibration using known standard concentrations and associated files.
        
        Args:
            cal_std_concs (list): List of standard concentrations (default: [0, 10, 25, 50, 100, 200]).
            cal_keywords_by_conc (list): Keywords to identify files for each concentration (default: ['std_0', 'std_1', 'std_2', 'std_3', 'std_4', 'std_5']).
        """
        print(f'loading calibration files in {self.cal_data_dir}')
        flist = [os.path.join(self.cal_data_dir, f)
                 for f in os.listdir(self.cal_data_dir) 
                 if f.endswith('.csv') and not any(s in f for s in self.skip_keywords)]
        
        cal_files = [f for f in flist if any(s in f for s in cal_keywords_by_conc)]
        self.cal_icpms_obj_dict = {k: None for k in cal_keywords_by_conc}

        for k in cal_keywords_by_conc:
            for f in cal_files:
                if k in f:
                    cal_f = f
            self.cal_icpms_obj_dict[k] = cal_f
        
        ordered_cal_files = [os.path.join(self.cal_data_dir, self.cal_icpms_obj_dict[c]) for c in cal_keywords_by_conc]
        self._cal_has_run = True
        
        # Create Calibration object
        self.cal = Calibration(concentrations=cal_std_concs, elements=self.elements, rawfiles=ordered_cal_files)


    def internal_std_correction(self):
        """
        Perform internal standard correction using the element "115In".
        
        Returns:
            float: Baseline value for the internal standard "115In".
        
        Raises:
            Exception: If calibration hasn't been run or if "115In" is not found in the data.
        """
        if not self._cal_has_run:
            raise Exception("Run calibration data before internal standard correction!")
        
        print('running 115In internal standard correction')
        stds_list = list(self.cal_icpms_obj_dict.keys())
        icpms_obj = RawICPMSData(os.path.join(self.cal_data_dir, self.cal_icpms_obj_dict[stds_list[0]]))
        
        if '115In' not in icpms_obj.intensities:
            raise Exception("115In was not found in the raw data file. Cannot perform internal standard correction.")
        
        istd_base = Integrate.integrate(icpms_obj.intensities['115In'], icpms_obj.times['115In'])
        return istd_base
    

    def quantitate(self,
                   time_range: tuple = (-1, -1),
                   cal_std_concs: list = [0, 10, 25, 50, 100, 200], 
                   cal_keywords_by_conc: list = ['std_0', 'std_1', 'std_2', 'std_3', 'std_4', 'std_5']):
        """
        Quantify concentrations of all elements in raw file using calibration data and internal standard correction.
        
        Args:
            time_range (tuple): Tuple indicating time range for concentration integration (default: (-1, -1)).
            cal_std_concs (list): List of standard concentrations for calibration (default: [0, 10, 25, 50, 100, 200]).
            cal_keywords_by_conc (list): Keywords to identify calibration files (default: ['std_0', 'std_1', 'std_2', 'std_3', 'std_4', 'std_5']).
        
        Returns:
            DataFrame: DataFrame containing quantified concentrations for each element in each file.
        """
        if not self._cal_has_run:
            cal = self.run_calibration(cal_std_concs=cal_std_concs, cal_keywords_by_conc=cal_keywords_by_conc)
        else:
            cal = self.cal

        istd_base = self.internal_std_correction()

        conc_list = []
        for file, data in self.raw_data_dict.items():
            
            tmin = 'min time' if time_range[0] == -1 else time_range[0]
            tmax = 'max time' if time_range[1] == -1 else time_range[1]
                
            print(f'integrating from {tmin} to {tmax} for {file}')
            
            t_start, t_stop = time_range

            conc = Quantitate.run(data,
                                  cal,
                                  data.elements,
                                  time_range=(t_start, t_stop),
                                  istd_baseline=istd_base,
                                  istd_time_range=(60, 120))
            
            conc_df = conc['concentrations']
            conc_df['file'] = file.split('/')[-1]
            conc_df['int_std_correction'] = conc['internal_std_correction']
            conc_list.append(conc_df)

        self.concentrations_df = concat(conc_list)
