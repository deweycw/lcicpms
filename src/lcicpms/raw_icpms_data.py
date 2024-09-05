'''
@author: Christian Dewey
@date: Jul 26, 2024
'''
from pandas import DataFrame

from lcicpms.in_out import get_data_from_csv

class RawICPMSData:

    def __init__(self, raw_data_file : str = None):

        # name of raw ICPMS file 
        self.raw_data_file = raw_data_file
        # str describing raw file data type; defined when data is loaded
        self.data_type : str = None
        # min time in the separation
        self.min_time : float = -1.0
        # max time in the separation 
        self.max_time : float = -1.0
        # dictionary of arrays containing intensities collected through time, elements are keys 
        self.intensities : dict = {}
        # dictionary of arrays containing time point of intensity measurement, elements are keys
        self.times : dict = {}
        # list of elements in raw file
        self.elements : list = []
        # list of time labels 
        self.time_labels : dict = []
        # dataframe containing raw data 
        self.raw_data_df : DataFrame = None

        self.load_data()
        self.get_elements_and_time_labels()
        self.get_intensities()
        self.get_times()

        
    def load_data(self):
        '''
        Determines data type of raw data file and loads the data. Currently only .csv files are valid. 
        '''
        if self.raw_data_file.split('.')[-1] == 'csv':
            self.data_type = 'csv'
            self.raw_data_df = get_data_from_csv(self.raw_data_file)


    def get_elements_and_time_labels(self):
        '''
        Gets the elements and time labels from the raw data file.
        '''
        if self.data_type == 'csv':

            for col in self.raw_data_df.columns:

                if ('Time' not in col) and ('time' not in col) and ('Number' not in col):

                    self.elements.append(col)
                
                elif ('Time' in col) or ('time'  in col):
                    
                    self.time_labels.append(col)

    def get_intensities(self):
        '''
        Gets np array of intensities of each element in dataframe and stores in dict. 
        '''

        self.intensities = {e: self.raw_data_df[e].to_numpy() for e in self.elements}

    def get_times(self):
        '''
        Gets np array of times of for each element
        '''
        time_labels_dict = {e: [l for l in self.time_labels if e in l][0] for e in self.elements}
        
        self.times = {e: self.raw_data_df[time_labels_dict[e]].to_numpy() for e in self.elements}

    def plot_raw_data(self, elements : list = None):
        import matplotlib.pyplot as plt

        if elements == None:

            elements = self.elements

        fig, ax = plt.subplots()
        maxy = 0 
        for e in elements:
            ax.plot(self.times[e], self.intensities[e], label=e)
            if max(self.intensities[e]) > maxy:
                maxy = max(self.intensities[e])
                ax.set_ylim(0,maxy*1.01)
        ax.legend(frameon=False)
        title = self.raw_data_file.split('/')[-1]
        fig.suptitle(title)
        plt.show()