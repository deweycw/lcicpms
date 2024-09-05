from lcicpms.raw_icpms_data import RawICPMSData
from lcicpms.integrate import Integrate
from lcicpms.quantitate import Quantitate
from lcicpms.calibration import Calibration
import os
import matplotlib.pyplot as plt

def load_csvs(data_dir):
    flist = [data_dir + f for f in os.listdir(data_dir) if '.csv' in f]

    test_csv = flist[0]

    icpms_obj = RawICPMSData(test_csv)
    #icpms_obj.plot_raw_data(['56Fe', '63Cu', '115In'])

    return icpms_obj

def integrate_test(data):
    area = Integrate.integrate(intensities=data.intensities['63Cu'], times=data.times['63Cu'])

def calibrate_test(cal_dir):
    rawfiles = [f for f in os.listdir(cal_dir) if '.csv' in f]
    rawfiles_dict = {'0_ppb':rawfiles[-2],
                '10_ppb':rawfiles[3],
                '25_ppb':rawfiles[-1],
                '50_ppb':rawfiles[1],
                '100_ppb':rawfiles[2],
                '200_ppb':rawfiles[0]}
    
    rawfiles = [cal_dir + rawfiles_dict[c] for c in rawfiles_dict.keys()]
    
    cal = Calibration(concentrations=[0,10,25,50,100,200], elements = data.elements, rawfiles = rawfiles)
    return cal

def quantitate_test(data, cal_dir):

    cal = calibrate_test(cal_dir)
    conc = Quantitate.run(data,
                          cal,
                          data.elements)
    
    print(conc['concentrations'])


if __name__ == '__main__':

    data_dir = "/Users/christiandewey/Code/lcicpms/test-data/"
    cal_dir = "/Users/christiandewey/Code/lcicpms/test-data/standards/"

    data = load_csvs(cal_dir)

    quantitate_test(data, cal_dir)




