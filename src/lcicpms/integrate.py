'''
@author: Christian Dewey
@date: Jul 27, 2024
'''
from numpy import where

class Integrate:

    def integrate(intensities, times, time_range : tuple = None):
        '''
        Returns area under signal trace curve between specified time range. 
        '''

        if time_range == None:
            i_tmin = 0
            i_tmax = len(times)-2

        else:
            i_tmin = int(where(abs(times - time_range[0]) == min(abs(times - time_range[0])) )[0][0])
            i_tmax = int(where(abs(times - time_range[1]) == min(abs(times - time_range[1])) )[0][0])

        peak_area = 0
        dt = 0

        for i in range(i_tmin, i_tmax):
            
            dt1_intensities = intensities[i]
            dt2_intensities = intensities[i+1]
            
            dt_I_min = min([dt1_intensities,dt2_intensities])
            dt_I_max = max([dt1_intensities,dt2_intensities])
            
            dt = (times[i+1] - times[i])

            rect_area = dt * dt_I_min
            top_area = dt * (dt_I_max - dt_I_min) * 0.5
            d_peak_area = rect_area + top_area

            peak_area = peak_area + d_peak_area  

        return peak_area

    def other():   
        #print('yes base subtract')
        if self._view.baseSubtract == True:
            #print('yes base subtract')
            baseline_height_1 = self._data.iloc[i_tmin,me_col_ind] / corr_factor
            baseline_height_2 =  self._data.iloc[i_tmax,me_col_ind] / corr_factor
            baseline_timeDelta = (self._data.iloc[i_tmax,me_col_ind - 1] - self._data.iloc[i_tmin,me_col_ind - 1])/60 #minutes
            #print('baseline_height_1: %.2f' % baseline_height_1)
            #print('baseline_height_2: %.2f' % baseline_height_2)
            #print('timeDelta: %.2f' % baseline_timeDelta)

            min_base_height = min([baseline_height_1, baseline_height_2])
            max_base_height = max([baseline_height_1, baseline_height_2])
            #print('min_base_height: %.2f' % min_base_height)
            #print('max_base_height: %.2f' % max_base_height)
            baseline_area_1 = min_base_height * baseline_timeDelta
            baseline_area_2 = (max_base_height - min_base_height) * baseline_timeDelta * 0.5
            #print('baseline_area_1: %.2f' % baseline_area_1)
            #print('baseline_area_2: %.2f' % baseline_area_2)
            
            #print('summed_area: %.2f' % summed_area)
            baseline_area = baseline_area_1 + baseline_area_2
            summed_area = summed_area - baseline_area
            summed_area = max(summed_area,0)
            #print('baseline_area: %.2f' % baseline_area)
            

        cal_curve = self._view.calCurves[metal]	
        slope = cal_curve['m']
        intercept = cal_curve['b']
        conc_ppb = slope * summed_area + intercept
        conc_uM = conc_ppb / self._view.masses[metal]
        
        peakAreas[metal] = '%.1f' % summed_area
        metalConcs[metal] = '%.3f' % conc_uM
        print('\n' + metal + ' uM: %.3f' % conc_uM)
        print(metal  + ' peak area: %.1f' % summed_area)
