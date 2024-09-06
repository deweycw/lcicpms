'''
@author: Christian Dewey
@date: Jul 27, 2024
'''
from lcicpms.integrate import Integrate
from lcicpms.raw_icpms_data import RawICPMSData

from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from numpy import array

class Curve:
    """
    A class to represent a calibration curve for a specific element.

    Attributes:
        element (str): The element for which the curve is created.
        concentrations (list): A list to store concentrations of the element.
        peak_areas (list): A list to store the integrated peak areas for the element.
        lm (LinearRegression): Linear regression model for the calibration curve.
        r2 (float): The R-squared value of the regression.
        mse (float): The mean squared error of the regression.
        m (float): The slope of the calibration curve.
        b (float): The intercept of the calibration curve.
        prediction (ndarray): The predicted concentrations based on the regression.
    """
    def __init__(self, element):
        """
        Initializes the Curve instance with the specified element and sets up empty 
        lists for concentrations and peak areas.
        
        Args:
            element (str): The name of the element for which the curve is being created.
        """
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
    """
    A class to perform calibration of elements using LC-ICP-MS data. It generates 
    calibration curves and fits a linear regression model for each element.

    Attributes:
        elements (list): A list of elements to calibrate.
        rawfiles (list): A list of raw ICP-MS data files.
        curves (dict): A dictionary of Curve objects for each element.
    """
    def __init__(self, concentrations: list | dict, elements: list, rawfiles: list):
        """
        Initializes the Calibration instance and builds calibration curves for the elements.

        Args:
            concentrations (list | dict): A list or dictionary of known concentrations for calibration.
            elements (list): A list of element names to calibrate.
            rawfiles (list): A list of raw ICP-MS data files corresponding to the concentrations.
        """
        self.elements = elements
        self.rawfiles = rawfiles
        self.curves = {e: Curve(e) for e in elements}

        self.build_curve(concentrations)
        self.run_regression()

    def build_curve(self, concentrations: list | dict):
        """
        Builds the calibration curve for each element by integrating the peak areas from the raw data.

        Args:
            concentrations (list | dict): A list or dictionary of concentrations mapped to raw data files.
        """
        rawfiles = self.rawfiles

        if type(concentrations) == list:
            elements = self.elements
            concentrations = {e: {c: file for c, file in zip(concentrations, rawfiles)} for e in elements}

        elif type(concentrations) == dict:
            elements = list(concentrations.keys())
            concentrations = {e: {c: file for c, file in zip(concentrations, rawfiles)} for e in elements}

        for e in elements:
            for c, f in concentrations[e].items():
                raw = RawICPMSData(f)
                peak_area = Integrate.integrate(raw.intensities[e], raw.times[e])
                self.curves[e].concentrations.append(c)
                self.curves[e].peak_areas.append(peak_area)

    def plot_curves(self, ax=None):
        """
        Plots the calibration curves for each element using peak areas and concentrations.

        Args:
            ax (matplotlib.axes.Axes, optional): A matplotlib Axes object. If None, a new figure is created.
        """
        import matplotlib.pyplot as plt
        
        elements = list(self.curves.keys())

        for e in elements:
            X = self.curves[e].peak_areas
            Y = self.curves[e].concentrations
            pred = self.curves[e].prediction
            
            plt.scatter(X, Y)
            plt.plot(X, pred, color='C1')
            plt.title(f'{e} MSE = {self.curves[e].mse:.2f}')
            plt.xlabel('Peak Area (counts)')
            plt.ylabel('Concentration')
            plt.show()

    def run_regression(self):
        """
        Performs linear regression on the calibration data for each element to determine
        the relationship between peak areas and concentrations. The slope (m), intercept (b), 
        mean squared error (MSE), and R-squared value are computed for each element.
        """
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