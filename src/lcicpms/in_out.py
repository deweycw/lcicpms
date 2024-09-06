'''
@author: Christian Dewey
@date: Jul 27, 2024
'''

from pandas import read_csv, DataFrame

def get_data_from_csv(path_to_rawfile=None):
    """
    Reads a raw ICP-MS data file from a CSV format and returns a pandas DataFrame.
    
    The function automatically detects the header row by searching for the 'Time' keyword.
    It uses this information to appropriately parse the file starting from the correct row.

    Args:
        path_to_rawfile (str, optional): The file path to the raw data CSV. Defaults to None.

    Returns:
        DataFrame: A pandas DataFrame containing the loaded raw data.
    """
    # Start by finding the header line
    df = read_csv(path_to_rawfile, sep=None, nrows=5, engine="python")
    if any("Time" in c for c in list(df.columns)):
        istart = 0
    else:
        istart = 1
        for row in df.itertuples(): 
            if row[1].find('Time') != -1:
                break
            istart += 1 
    df = read_csv(path_to_rawfile, sep=None, header=istart, engine="python")
    return df


def export_df(data: dict, time_range: tuple):
    """
    Exports data to a pandas DataFrame, including the start and end of a time range.
    
    The function takes in a dictionary of data and a time range, adding the start 
    and end times as columns. It ensures that the final DataFrame has 'start' and 
    'end' columns followed by the other data columns.

    Args:
        data (dict): A dictionary where keys are element names and values are the corresponding data.
        time_range (tuple): A tuple representing the start and end times of the time range.

    Returns:
        DataFrame: A pandas DataFrame with 'start', 'end', and element data columns.
    """
    columns = ['start', 'end'] + [e for e in data.keys()]
    data['start'] = float(time_range[0])
    data['end'] = float(time_range[1])
    for k in columns:
        data[k] = [data[k]]
    df = DataFrame(data, columns=data.keys())
    return df[columns]