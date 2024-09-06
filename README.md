# Overview

### Purpose

The code is designed for handling and analyzing LC-ICP-MS (Liquid Chromatography-Inductively Coupled Plasma Mass Spectrometry) data. It includes functionality for loading raw data, performing calibration, applying internal standard corrections, and quantifying element concentrations.

### Key Components

1. **Data Handling and Loading**
   - **`RawICPMSData` Class**:
     - Manages raw LC-ICP-MS data.
     - Loads data from `.csv` files.
     - Extracts and organizes information such as intensities, times, elements, and time labels.
     - Provides methods for visualizing raw data.

2. **Integration**
   - **`Integrate` Class**:
     - Calculates the area under the curve for signal traces within a specified time range.
     - Useful for quantifying the amount of analyte based on its signal intensity over time.

3. **Calibration and Quantification**
   - **`Dataset` Class**:
     - Manages the entire workflow from loading data to quantification.
     - **Loading Raw Data**:
       - Loads and organizes raw ICP-MS data files from a specified directory.
     - **Calibration**:
       - Performs calibration using standard concentration files.
       - Creates a `Calibration` object for further use in quantification.
     - **Internal Standard Correction**:
       - Applies correction based on an internal standard (e.g., "115In").
       - Computes the baseline for the internal standard to correct measurements.
     - **Quantification**:
       - Quantifies concentrations of specific elements using calibration data and internal standard corrections.
       - Integrates data over specified time ranges and produces a DataFrame of quantified concentrations.

### Summary

The code provides a comprehensive toolkit for processing LC-ICP-MS data, including:
- **Data Import**: Load and process raw data files.
- **Calibration**: Set up and apply calibration curves based on known standards.
- **Correction**: Apply internal standard corrections to improve accuracy.
- **Quantification**: Calculate and report the concentrations of elements in samples.

It integrates various aspects of data handling and analysis into a coherent workflow, facilitating efficient and accurate analysis of LC-ICP-MS data.

--- 

## Example Python Script

```python
from lcicpms.dataset import Dataset

# Initialize Dataset object with the directory paths
raw_data_dir = 'path/to/raw_data'
cal_data_dir = 'path/to/calibration_data'
dataset = Dataset(raw_data_dir=raw_data_dir, cal_data_dir=cal_data_dir)

# Load raw data
dataset.load_raw_data(dir=raw_data_dir)

# Perform calibration
dataset.run_calibration(
    cal_std_concs=[0, 10, 25, 50, 100, 200],
    cal_keywords_by_conc=['std_0', 'std_1', 'std_2', 'std_3', 'std_4', 'std_5']
)


# Quantify elements (internal standard correction done automatically)
dataset.quantitate(
    time_range=(0, 1200),  # Specify your time range (seconds)
    cal_std_concs=[0, 10, 25, 50, 100, 200],
    cal_keywords_by_conc=['std_0', 'std_1', 'std_2', 'std_3', 'std_4', 'std_5']
)

# Print results
print(dataset.concentrations_df)
```
---

# Documentation

## Module: `lcicpms`

This module provides tools for handling LC-ICP-MS data, including integration, calibration, and quantification.

---

## `RawICPMSData` Class

### Overview
Handles raw LC-ICP-MS data, loading from files, and extracting relevant information for further processing.

### Attributes
- **`raw_data_file (str)`**: Path to the raw ICP-MS data file.
- **`data_type (str)`**: Describes the raw file data type (set when data is loaded).
- **`min_time (float)`**: Minimum time in the separation.
- **`max_time (float)`**: Maximum time in the separation.
- **`intensities (dict)`**: Dictionary of arrays containing intensities collected over time, with elements as keys.
- **`times (dict)`**: Dictionary of arrays containing time points of intensity measurements, with elements as keys.
- **`elements (list)`**: List of elements in the raw file.
- **`time_labels (dict)`**: List of time labels.
- **`raw_data_df (DataFrame)`**: DataFrame containing the raw data.

### Methods

- **`__init__(self, raw_data_file: str = None)`**
  - **Description**: Initializes the `RawICPMSData` object and loads data from the specified file.
  - **Args**:
    - `raw_data_file (str)`: Path to the raw ICP-MS data file.

- **`load_data(self)`**
  - **Description**: Determines the data type of the raw data file and loads the data. Currently supports only `.csv` files.

- **`get_elements_and_time_labels(self)`**
  - **Description**: Extracts elements and time labels from the raw data file.

- **`get_intensities(self)`**
  - **Description**: Extracts and stores the intensities of each element from the DataFrame.

- **`get_times(self)`**
  - **Description**: Extracts and stores the time points for each element from the DataFrame.

- **`plot_raw_data(self, elements: list = None)`**
  - **Description**: Plots raw data for specified elements or all elements if none are specified.
  - **Args**:
    - `elements (list)`: List of elements to plot.

---

## `Integrate` Class

### Overview
Provides functionality to integrate signal traces to calculate the area under the curve.

### Methods

- **`integrate(intensities, times, time_range: tuple = None)`**
  - **Description**: Computes the area under the signal trace curve within a specified time range.
  - **Args**:
    - `intensities`: Array of intensity values.
    - `times`: Array of time points corresponding to the intensities.
    - `time_range (tuple)`: Tuple specifying the start and end times for integration. If `None`, integrates over the entire range.
  - **Returns**: 
    - `float`: Calculated peak area under the curve.

- **`other()`**
  - **Description**: Placeholder method for additional processing (currently commented out).

---

## `Dataset` Class

### Overview
Manages raw LC-ICP-MS data, performs calibration, applies internal standard corrections, and quantifies element concentrations.

### Attributes
- **`raw_data_dir (str)`**: Directory containing raw ICP-MS data files.
- **`cal_data_dir (str)`**: Directory containing calibration files.
- **`skip_keywords (list)`**: List of keywords to exclude certain files.
- **`raw_data_dict (dict)`**: Dictionary of loaded raw data files.
- **`cal_icpms_obj_dict (dict)`**: Dictionary of calibration files for each concentration.
- **`_cal_has_run (bool)`**: Flag indicating whether calibration has been performed.
- **`cal (Calibration)`**: Calibration object with standard concentrations and elements.
- **`concentrations_df (DataFrame)`**: DataFrame of quantified concentrations.

### Methods

- **`__init__(self, raw_data_dir: str = None, cal_data_dir: str = None, skip_keywords: list = ['results'])`**
  - **Description**: Initializes the `Dataset` object with directories for raw and calibration data.
  - **Args**:
    - `raw_data_dir (str)`: Directory for raw data files.
    - `cal_data_dir (str)`: Directory for calibration files.
    - `skip_keywords (list)`: Keywords to filter out certain files (default: `['results']`).

- **`load_raw_data(self, dir: str)`**
  - **Description**: Loads raw ICP-MS data files from the specified directory.
  - **Args**:
    - `dir (str)`: Directory from which to load raw data.
  - **Returns**:
    - `dict`: Dictionary of file paths and `RawICPMSData` objects.

- **`run_calibration(self, cal_std_concs: list = [0, 10, 25, 50, 100, 200], cal_keywords_by_conc: list = ['std_0', 'std_1', 'std_2', 'std_3', 'std_4', 'std_5'])`**
  - **Description**: Performs calibration using standard concentrations and associated files.
  - **Args**:
    - `cal_std_concs (list)`: List of standard concentrations (default: `[0, 10, 25, 50, 100, 200]`).
    - `cal_keywords_by_conc (list)`: Keywords to identify files for each concentration (default: `['std_0', 'std_1', 'std_2', 'std_3', 'std_4', 'std_5']`).

- **`internal_std_correction(self)`**
  - **Description**: Applies internal standard correction using the element "115In". Computes baseline for correction.
  - **Returns**:
    - `float`: Baseline value for "115In".
  - **Raises**:
    - `Exception`: If calibration hasn't been run or "115In" is not found.

- **`quantitate(self, time_range: tuple = (-1, -1), elements: list = ['Fe', 'Co', 'Mn', 'Ni', 'Cu'], cal_std_concs: list = [0, 10, 25, 50, 100, 200], cal_keywords_by_conc: list = ['std_0', 'std_1', 'std_2', 'std_3', 'std_4', 'std_5'])`**
  - **Description**: Quantifies concentrations of specified elements using calibration data and internal standard correction.
  - **Args**:
    - `time_range (tuple)`: Tuple indicating time range for integration (default: `(-1, -1)`).
    - `elements (list)`: List of elements to quantify (default: `['Fe', 'Co', 'Mn', 'Ni', 'Cu']`).
    - `cal_std_concs (list)`: List of standard concentrations (default: `[0, 10, 25, 50, 100, 200]`).
    - `cal_keywords_by_conc (list)`: Keywords to identify calibration files (default: `['std_0', 'std_1', 'std_2', 'std_3', 'std_4', 'std_5']`).
  - **Returns**:
    - `DataFrame`: DataFrame with quantified concentrations for each element.

---
