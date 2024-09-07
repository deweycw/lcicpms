Overview
========

Purpose
-------

The code is designed for handling and analyzing LC-ICP-MS (Liquid Chromatography-Inductively Coupled Plasma Mass Spectrometry) data. It includes functionality for loading raw data, performing calibration, applying internal standard corrections, and quantifying element concentrations.

Summary
-------

The code provides a comprehensive toolkit for processing LC-ICP-MS data, including:

- **Data Import**: Load and process raw data files.
- **Calibration**: Set up and apply calibration curves based on known standards.
- **Correction**: Apply internal standard corrections to improve accuracy.
- **Quantification**: Calculate and report the concentrations of elements in samples.

It integrates various aspects of data handling and analysis into a coherent workflow, facilitating efficient and accurate analysis of LC-ICP-MS data.

Key Components
--------------

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