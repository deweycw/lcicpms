chroma-icpms
-------
BACKEND

src / 

	chroma-icpms / 

		io / 
			- read_raw_data
			- get_user_input
			- package_output

		utils / 
			- integrate
			- subtract_background

		dataset / 
			attributes:
				- sample_list
				- feature_list 

		raw_icpms_data (raw_data_file) /				# class 
			methods: 
				- load_data
				- export_data
				- parse_data
				- get_elements
				- get_intensities
				- get_times
			attributes:
				- dict(keys = elements, values = [intensities])
				- dict(keys = elements, values = [times])
				- max_time
				- min_time

		calibration_curve (element, icpms_lc_data) / 		# class
			methods:
				- build_curve
				- run_regression
				- load_curve
				- export_curve
			attributes:
				- element
				- m
				- b 
				- r2
				- rmse 
				- dict(stds, intensities)
				- dict(stds, concentrations)

		internal_std_normalization (reference_file, internal_std_element, internal_std_concentration) / 
			methods: 
				- get_signal
				- calc_sample_to_ref_ratio
			attributes:
				- internal_std_element
				- internal_std_concentration

		quantitation (time_range, element, calibration_curve, internal_std_normalize_flag) / 
			methods: 
				- subtract_background
				- integrate_signal
				- apply_calibration_curve
			attributes:
				- concentration
				- corrected_concentration

		chroma_feature (elements) /
			methods:
				- get_timerange
				- get_elements
				- get_concentrations
				- get_intensities
			attributes:
				- timerange
				- elements
				- concentrations
				- intensities 




