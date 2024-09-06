"""
@author: Christian Dewey
@date: September 4, 2024
"""

from lcicpms.dataset import Dataset  

def main():
    # Set up directories for raw and calibration data
    raw_data_dir = 'path/to/raw_data'
    cal_data_dir = 'path/to/calibration_data'
    
    # Initialize Dataset object
    dataset = Dataset(raw_data_dir=raw_data_dir, cal_data_dir=cal_data_dir)

    # Load and process raw data
    print("Loading raw data...")
    dataset.raw_data_dict = dataset.load_raw_data(raw_data_dir)

    # Perform calibration
    print("Running calibration...")
    dataset.run_calibration(
        cal_std_concs=[0, 10, 25, 50, 100, 200],
        cal_keywords_by_conc=['std0', 'std1', 'std2', 'std3', 'std4', 'std5'] # used to locate standards 
    )

    # Quantify elements
    print("Quantifying concentrations (internal std correction applied automatically)...")
    results = dataset.quantitate(
        time_range=(0, 1200),  # Example time range in seconds
        cal_std_concs=[0, 10, 25, 50, 100, 200],
        cal_keywords_by_conc=['std_0', 'std_1', 'std_2', 'std_3', 'std_4', 'std_5']
    )

    # Print results
    print("Quantification results:")
    print(results)

if __name__ == "__main__":
    main()