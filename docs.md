# Documentation

## Description

This repository is divided by modules. Each module contains functions 
to do specific tasks.

## Modules

### Epi-Puma 1.0

This module has functions which use endpoints of Epi-Puma API 1.0 to
generate their results. Functions of this modules are in the folder
called `./epi_puma_1`

#### File `./epi_puma_1/analysis.py`

* `nbayes_epi_puma_v1(target, covariables, lim_inf_training, 
	lim_sup_training, lim_inf_validation, lim_sup_validation, modifier
	=None type_analysis=None, lim_inf_first=None, lim_sup_first=None)`: This
	function calculates score, epsilon and presence cells of covariables
	and provides a summary of cells which containas epsilon, best drivers,
	worst drivers, etc.

	- Args: 

		1.  `target` is a sublist of `["COVID-19 CONFIRMADO", 
		"COVID-19 FALLECIDO", "COVID-19 NEGATIVO"]`
		2. `covariables` is a sublist of `['Demograficos', 'Pobreza', 
		'Movilidad', 'Infraestructura-Salud', 'Vulnerabilidad', 
		'Worldclim', 'CCA-Climaticas', 'CCA-Contaminacion']`
		3. `lim_inf_training` and `lim_sup_training` are dates which 
		define the training period. All dates must be written in format 
		yyyy-MM-dd.
		4. `lim_inf_validation` and `lim_sup_validation` are dates which 
		define the validation period.All dates must be written in format 
		yyyy-MM-dd.
		5. `modifier` modify the target, taking top decil "cases", "incidence", 
		"prevalence" or "lethality"
		6. `type_analysis` defines if the analysis will be improvement 
		(`green`), deterioration (`red`) or profiling (`none`).
		7. (Optional) `lim_inf_first` and `lim_sup_first` are dates 
		which define the first period. All dates must be written in 
		format yyyy-MM-dd.

	- Returns:

		1. An array of objects, each object represents a covariable
		2. An array of objects, each object represents a cell
		3. A string which represents the reason why something was bad 
