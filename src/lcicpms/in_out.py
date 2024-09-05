'''
@author: Christian Dewey
@date: Jul 27, 2024
'''

from pandas import read_csv, DataFrame

def get_data_from_csv(path_to_rawfile=None):
    # start by finding header line
    df = read_csv(path_to_rawfile, sep=None, nrows= 5, engine="python")
    if any("Time" in c for c in list(df.columns)):
        istart = 0
    else:
        istart = 1
        for row in df.itertuples(): 
            if row[1].find('Time') != -1:
                break
            istart = istart + 1 
    df = read_csv(path_to_rawfile, sep=None, header = istart, engine="python")
    return df


def export_df(data : dict, time_range : tuple):
    columns = ['start', 'end'] + [e for e in data.keys()]
    data['start'] = float(time_range[0])
    data['end'] = float(time_range[1])
    for k in columns:
        data[k] = [data[k]]
    df = DataFrame(data, columns=data.keys())
    return df[columns]
