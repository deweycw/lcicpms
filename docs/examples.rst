Examples
===========

.. code-block::

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