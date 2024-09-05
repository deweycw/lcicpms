'''
@author: Christian Dewey
@date: Jul 27, 2024
'''
from lcicpms.integrate import Integrate
from lcicpms.raw_icpms_data import RawICPMSData

from sklearn import  linear_model
from sklearn.metrics import mean_squared_error, r2_score
from numpy import array

class Curve:
    def __init__(self, element ):
        self.element = element
        self.concentrations = []
        self.peak_areas = []
        self.lm = None
        self.r2 = None
        self.mse = None
        self.m = None
        self.b = None
        self.prediction = None


class Calibration:

    def __init__(self, concentrations : list | dict, elements : list, rawfiles : list):
        
        self.elements = elements
        self.rawfiles = rawfiles

        self.curves = {e:Curve(e) for e in elements}

        self.build_curve(concentrations)
        self.run_regression()

    def build_curve(self, concentrations : list | dict):

        rawfiles = self.rawfiles

        if type(concentrations) == list:
            elements = self.elements
            concentrations = {e: {c:file for c,file in zip(concentrations,rawfiles)} for e in elements}

        elif type(concentrations) == dict:
            elements = list(concentrations.keys())
            concentrations = {e: {c:file for c,file in zip(concentrations,rawfiles)} for e in elements}

        for e in elements:
            for c,f in concentrations[e].items():
                raw = RawICPMSData(f)
                peak_area = Integrate.integrate(raw.intensities[e],raw.times[e])
                self.curves[e].concentrations.append(c)
                self.curves[e].peak_areas.append(peak_area)

    def plot_curves(self, ax = None):
        import matplotlib.pyplot as plt
        
        elements = list(self.curves.keys())
 
        for e in elements:
            #fig, ax = plt.subplots()
            X = self.curves[e].peak_areas
            Y = self.curves[e].concentrations
            pred = self.curves[e].prediction
            
            plt.scatter(X,Y)
            plt.plot(X, pred, color = 'C1')
            plt.title(e + ' MSE =  %.2f' %self.curves[e].mse)
            plt.xlabel('Peak Area (counts)')
            plt.ylabel('Concentration')
            plt.show()


    def run_regression(self):
        
        elements = list(self.curves.keys())
        for e in elements:
            peak_areas = self.curves[e].peak_areas
            X = array(peak_areas).reshape(-1, 1)
            concs = self.curves[e].concentrations
            y = array(concs)

            regr = linear_model.LinearRegression(fit_intercept=True)
            regr.fit(X, y)

            y_pred = regr.predict(X)

            self.curves[e].lm = regr
            self.curves[e].b = regr.intercept_
            self.curves[e].m = regr.coef_[0]
            self.curves[e].mse = mean_squared_error(y, y_pred)
            self.curves[e].r2 = r2_score(y, y_pred)
            self.curves[e].prediction = y_pred

