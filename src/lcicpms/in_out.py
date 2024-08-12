'''
@author: Christian Dewey
@date: Jul 27, 2024
'''

from pandas import read_csv

def get_data_from_csv(path_to_rawfile=None):
    return read_csv(path_to_rawfile, sep=None, engine="python")