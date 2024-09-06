'''
@author: Christian Dewey
@date: Jul 26, 2024
'''
from pandas import DataFrame
from lcicpms.in_out import get_data_from_csv

class RawICPMSData:
    """
    A class to represent and process raw ICP-MS data from a file.

    Attributes:
        raw_data_file (str): The file path of the raw ICP-MS data.
        data_type (str): The type of the raw data file (e.g., 'csv').
        min_time (float): The minimum time value in the separation.
        max_time (float): The maximum time value in the separation.
        intensities (dict): A dictionary containing intensities for each element, with elements as keys.
        times (dict): A dictionary containing time points for each element, with elements as keys.
        elements (list): A list of elements in the raw file.
        time_labels (list): A list of time labels extracted from the raw file.
        raw_data_df (DataFrame): A pandas DataFrame containing the raw data from the file.
    """
    
    def __init__(self, raw_data_file: str = None):
        """
        Initializes the RawICPMSData object by loading the data from the provided file.

        Args:
            raw_data_file (str, optional): The file path to the raw ICP-MS data file. Defaults to None.
        """
        # name of raw ICPMS file 
        self.raw_data_file = raw_data_file
        # str describing raw file data type; defined when data is loaded
        self.data_type: str = None
        # min time in the separation
        self.min_time: float = -1.0
        # max time in the separation 
        self.max_time: float = -1.0
        # dictionary of arrays containing intensities collected through time, elements are keys 
        self.intensities: dict = {}
        # dictionary of arrays containing time point of intensity measurement, elements are keys
        self.times: dict = {}
        # list of elements in raw file
        self.elements: list = []
        # list of time labels 
        self.time_labels: list = []
        # dataframe containing raw data 
        self.raw_data_df: DataFrame = None

        self.load_data()
        self.get_elements_and_time_labels()
        self.get_intensities()
        self.get_times()

    def load_data(self):
        """
        Determines the data type of the raw data file and loads the data.
        Currently, only .csv files are supported.
        """
        if self.raw_data_file.split('.')[-1] == 'csv':
            self.data_type = 'csv'
            self.raw_data_df = get_data_from_csv(self.raw_data_file)

    def get_elements_and_time_labels(self):
        """
        Extracts the elements and time labels from the raw data file, depending on the data type.
        The elements and time labels are identified by examining column names.
        """
        if self.data_type == 'csv':
            for col in self.raw_data_df.columns:
                if ('Time' not in col) and ('time' not in col) and ('Number' not in col):
                    self.elements.append(col)
                elif ('Time' in col) or ('time' in col):
                    self.time_labels.append(col)

    def get_intensities(self):
        """
        Extracts the intensities of each element from the raw data and stores them in a dictionary.
        The intensities are converted to NumPy arrays for easier processing.
        """
        self.intensities = {e: self.raw_data_df[e].to_numpy() for e in self.elements}

    def get_times(self):
        """
        Extracts the time points corresponding to each element and stores them in a dictionary.
        The time labels are used to map the correct time values to each element.
        """
        time_labels_dict = {e: [l for l in self.time_labels if e in l][0] for e in self.elements}
        self.times = {e: self.raw_data_df[time_labels_dict[e]].to_numpy() for e in self.elements}

    def plot_raw_data(self, elements: list = None):
        """
        Plots the raw ICP-MS data for the specified elements using matplotlib.

        Args:
            elements (list, optional): A list of elements to plot. If None, all elements are plotted.
        """
        import matplotlib.pyplot as plt

        if elements is None:
            elements = self.elements

        fig, ax = plt.subplots()
        maxy = 0
        for e in elements:
            ax.plot(self.times[e], self.intensities[e], label=e)
            if max(self.intensities[e]) > maxy:
                maxy = max(self.intensities[e])
                ax.set_ylim(0, maxy * 1.01)
        ax.legend(frameon=False)
        title = self.raw_data_file.split('/')[-1]
        fig.suptitle(title)
        plt.show()