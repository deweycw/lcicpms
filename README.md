Module 1: RawICPMSData

This module manages raw ICP-MS data, extracting relevant information such as element intensities and times.

	•	Class RawICPMSData:
	•	__init__(raw_data_file):
	•	Description: Loads raw ICP-MS data from the specified file and initializes various attributes.
	•	Arguments:
	•	raw_data_file (str): Path to the raw ICP-MS data file.
	•	load_data():
	•	Description: Loads the raw ICP-MS data from a CSV file and determines the data type.
	•	get_elements_and_time_labels():
	•	Description: Extracts element names and time labels from the raw data.
	•	get_intensities():
	•	Description: Extracts intensity data for each element and stores it in a dictionary.
	•	get_times():
	•	Description: Extracts time data for each element and stores it in a dictionary.
	•	plot_raw_data(elements=None):
	•	Description: Plots the raw intensity data for the specified elements.
	•	Arguments:
	•	elements (list, optional): List of elements to plot. If None, plots all available elements.
 
Module 2: Calibration

This module handles calibration curve creation and regression analysis based on raw ICP-MS data.

	•	Class Curve:
	•	Description: A helper class to store element-specific calibration curve data, including concentrations, peak areas, and linear regression results.
	•	Class Calibration:
	•	__init__(concentrations, elements, rawfiles):
	•	Description: Initializes the calibration object with element names, raw data files, and concentrations. Builds the calibration curves and runs linear regression.
	•	Arguments:
	•	concentrations (list|dict): List or dictionary of known concentrations.
	•	elements (list): List of elements for calibration.
	•	rawfiles (list): List of raw data file paths for each concentration.
	•	build_curve(concentrations):
	•	Description: Constructs calibration curves by integrating peak areas from raw ICP-MS data and associating them with known concentrations.
	•	Arguments:
	•	concentrations (list|dict): Concentrations for calibration.
	•	plot_curves(ax=None):
	•	Description: Plots calibration curves for each element with the corresponding linear regression.
	•	Arguments:
	•	ax (matplotlib axis, optional): Matplotlib axis for plotting. If None, a new axis is created.
	•	run_regression():
	•	Description: Runs linear regression on the peak areas vs. concentrations for each element to obtain the slope (m), intercept (b), mean squared error (mse), and R² score.

Module 3: Quantitate

This module provides functionality to quantify elements using raw ICP-MS data over a specified time range.

	•	Quantitate.run()
	•	Description: Performs quantification on specified elements within a defined time range, using raw ICP-MS data and calibration curves.
	•	Arguments:
	•	raw_icpms_data (RawICPMSData): Object containing raw ICP-MS data (default: None).
	•	calibration (Calibration): Calibration object for concentration determination (default: None).
	•	elements (list): List of elements to quantify (default: []).
	•	time_range (tuple): Tuple defining the start and end of the time range for quantification (default: (-1, -1)).
	•	istd_baseline (float): Baseline correction factor for internal standard (default: -1.0).
	•	istd_time_range (tuple): Time range for the internal standard (default: (-1, -1)).
	•	baseline_subtraction (bool): Whether to perform baseline subtraction (default: False).
	•	unit (str): Unit for the concentrations (default: 'ppb').
	•	Returns: Dictionary containing peak areas and concentrations.

Module 4: Integrate

This module handles integration of ICP-MS signal traces over a specified time range.

	•	Class Integrate:
	•	integrate(intensities, times, time_range=None):
	•	Description: Performs trapezoidal integration of signal intensities over a specified time range.
	•	Arguments:
	•	intensities (array-like): Signal intensities corresponding to the time points.
	•	times (array-like): Time points at which the intensities were measured.
	•	time_range (tuple, optional): The start and end times for the integration. If None, integrates over the entire signal.
	•	Returns: The computed area under the curve between the specified time range.
	•	other():
	•	Description: Placeholder method for handling baseline subtraction and calculating concentrations using a calibration curve (not fully implemented).

Usage

	•	Quantitation: To quantify elements using ICP-MS data, initialize a RawICPMSData object, a Calibration object, and call Quantitate.run() with the appropriate arguments.
	•	Calibration: Use the Calibration class to build calibration curves and perform linear regression, then visualize using plot_curves().
	•	Integration: Use the Integrate class to calculate the area under intensity curves over a specified time range.
 
Module 5: in_out

This module handles input and output operations, such as reading raw data from CSV files and exporting DataFrames.

	•	get_data_from_csv(path_to_rawfile=None):
	•	Description: Reads a raw ICP-MS data file from a CSV format, automatically detecting the header row, and returns a pandas DataFrame.
	•	Arguments:
	•	path_to_rawfile (str, optional): File path to the raw data CSV.
	•	Returns: pandas DataFrame containing the raw data.
	•	export_df(data, time_range):
	•	Description: Exports a dictionary of data and a time range to a pandas DataFrame. The resulting DataFrame contains ‘start’, ‘end’, and data columns.
	•	Arguments:
	•	data (dict): Dictionary where keys are element names and values are the corresponding data.
	•	time_range (tuple): Tuple representing the start and end times of the time range.
	•	Returns: pandas DataFrame with ‘start’, ‘end’, and element data columns.

