from lcicpms.raw_icpms_data import RawICPMSData
from lcicpms.integrate import Integrate
from lcicpms.quantitate import Quantitate
from lcicpms.calibration import Calibration
import os
from pandas import concat

def load_csvs(data_dir):
    flist = [data_dir + f for f in os.listdir(data_dir) if ('.csv' in f) & ('results' not in f)]

    icpms_objs_dict = {}
    for f in flist:
        icpms_obj = RawICPMSData(f)
        #icpms_obj.plot_raw_data(['59Co'])
        icpms_objs_dict[f] = icpms_obj
    return icpms_objs_dict

def calibrate(cal_dir, elements):

    rawfiles = [f for f in os.listdir(cal_dir) if '.csv' in f]
    rawfiles_dict = {'0_ppb':rawfiles[-2],
                '10_ppb':rawfiles[3],
                '25_ppb':rawfiles[-1],
                '50_ppb':rawfiles[1],
                '100_ppb':rawfiles[2],
                '200_ppb':rawfiles[0]}
    
    rawfiles = [cal_dir + rawfiles_dict[c] for c in rawfiles_dict.keys()]
    cal = Calibration(concentrations=[0,10,25,50,100,200], elements = elements, rawfiles = rawfiles)
    return cal

def internal_std_correction(cal_dir):

    rawfiles = [f for f in os.listdir(cal_dir) if '.csv' in f]
    rawfiles_dict = {'0_ppb':rawfiles[-2],
                '10_ppb':rawfiles[3],
                '25_ppb':rawfiles[-1],
                '50_ppb':rawfiles[1],
                '100_ppb':rawfiles[2],
                '200_ppb':rawfiles[0]}
    icpms_obj = RawICPMSData(cal_dir + rawfiles_dict['0_ppb'])
    istd_base = Integrate.integrate(icpms_obj.intensities['115In'],icpms_obj.times['115In'])
    return istd_base

def quantitate(data_dict, cal_dir, elements):

    cal = calibrate(cal_dir, elements)
    istd_base = internal_std_correction(cal_dir)
    conc_list = []
    for file, data in data_dict.items():

        for t_start in range(0,36*60-300,300): 
            print('running %s for %s' %(t_start, file))
            t_stop = t_start + 300
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

    concat(conc_list).to_csv(data_dir + 'results.csv', index=False)


if __name__ == '__main__':

    data_dir = "/Users/christiandewey/Code/lcicpms/test-data/"
    cal_dir = "/Users/christiandewey/Code/lcicpms/test-data/standards/"

    data_dict = load_csvs(data_dir)
    elements = data_dict[list(data_dict.keys())[0]].elements
    quantitate(data_dict, cal_dir, elements)




