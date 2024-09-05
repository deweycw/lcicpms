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

    def __init__(self, raw_data_dir : str = None, 
                 cal_data_dir : str = None,
                 skip_keywords : list = ['results']):

        self.raw_data_dir = raw_data_dir
        self.skip_keywords = skip_keywords

        self._cal_has_run = False

        self.raw_data_dict = self.load_raw_data(self.raw_data_dir)
        
        if cal_data_dir == None:
            self.cal_data_dir = raw_data_dir

        else:
            self.cal_data_dir = cal_data_dir



    def load_raw_data(self, dir):
        
        print(f'loading all files in {dir}')

        flist = [os.path.join(dir, f)
                 for f in os.listdir(dir) 
                 if f.endswith('.csv') and not any(s in f for s in self.skip_keywords) ]
        
        icpms_obj_dict = {}
        for f in flist:
            icpms_obj = RawICPMSData(f)
            icpms_obj_dict[f] = icpms_obj
        
        self.elements = icpms_obj.elements

        return icpms_obj_dict
    
    
    def run_calibration(self,
                            cal_std_concs : list = [0, 10, 25, 50, 100, 200 ], 
                            cal_keywords_by_conc : list = ['std_0', 'std_1', 'std_2', 'std_3', 'std_4', 'std_5']):
        
        print(f'loading calibration files in {self.cal_data_dir}')

        flist = [os.path.join(self.cal_data_dir, f)
                 for f in os.listdir(self.cal_data_dir) 
                 if f.endswith('.csv') and not any(s in f for s in self.skip_keywords) ]

        cal_files = [f for f in flist if any(s in f for s in cal_keywords_by_conc)]
        
        self.cal_icpms_obj_dict = {k: None for k in cal_keywords_by_conc}

        for k in cal_keywords_by_conc:

            for f in cal_files:
                if k in f:
                    cal_f = f

            self.cal_icpms_obj_dict[k] = cal_f
        
        ordered_cal_files = [os.path.join(self.cal_data_dir, self.cal_icpms_obj_dict[c]) for c in cal_keywords_by_conc]

        self._cal_has_run = True
        
        self.cal = Calibration(concentrations=cal_std_concs, elements=self.elements, rawfiles=ordered_cal_files)


    def internal_std_correction(self):
        
        if not self._cal_has_run:
            raise Exception("Run calibration data before internal standard correction!")

        print('running 115In internal standard correction')
        stds_list = list(self.cal_icpms_obj_dict.keys())
        icpms_obj = RawICPMSData(os.path.join(self.cal_data_dir, self.cal_icpms_obj_dict[stds_list[0]]))
        
        if '115In' not in icpms_obj.intensities:
            raise Exception("115In was not found in the raw data file. Cannot perform internal standard correction.")
        
        istd_base = Integrate.integrate(icpms_obj.intensities['115In'],icpms_obj.times['115In'])
        
        return istd_base
    

    def quantitate(self,
                   time_range : tuple = (-1,-1),
                   elements : list = ['Fe', 'Co', 'Mn', 'Ni', 'Cu'],
                   cal_std_concs : list = [0, 10, 25, 50, 100, 200 ], 
                   cal_keywords_by_conc : list = ['std_0', 'std_1', 'std_2', 'std_3', 'std_4', 'std_5']):

        if not self._cal_has_run:
            cal = self.run_calibration(elements=elements,cal_std_concs=cal_std_concs,cal_keywords_by_conc=cal_keywords_by_conc)
        else:
            cal = self.cal

        istd_base = self.internal_std_correction()

        conc_list = []
        for file, data in self.raw_data_dict.items():
            
            if time_range[0] == -1:
                tmin = 'min time'
            else:
                tmin = time_range[0]
            
            if time_range[1] == -1:
                tmax = 'max time'
            else:
                tmax = time_range[1]
                
            print(f'integrating from {tmin} to {tmax} for {file}')
            
            t_start = time_range[0]
            t_stop = time_range[1]

            conc = Quantitate.run(data,
                                cal,
                                data.elements,
                                time_range = (t_start,t_stop ),
                                istd_baseline = istd_base,
                                istd_time_range = (60,120))
            
            conc_df = conc['concentrations']
            conc_df['file'] = file.split('/')[-1]
            conc_df['int_std_correction'] = conc['internal_std_correction']
            conc_list.append(conc_df)

        self.concentrations_df = concat(conc_list)