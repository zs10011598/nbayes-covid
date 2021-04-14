import os
import json
import requests
import pandas as pd
from .analysis import *
from .utils import *


def nbayes_report(path, target, covariables, lim_inf_training, lim_sup_training, 
          lim_inf_validation, lim_sup_validation, modifier=None, 
          type_analysis=None, lim_inf_first=None, lim_sup_first=None):
    '''
        Description: This function makes a request to Epi-Puma API 1.0
    
        Args:
            - path: relative path for the reports to be created
            - target: A list with some of the following variables
                "COVID-19 CONFIRMADO", "COVID-19 NEGATIVO", "COVID-19 FALLECIDO".
            - covariables: A list with some of the following variables "Demograficos", 
                "Pobreza", "Movilidad",  "Infraestructura-salud", "Vulnerabilidad",
                "Worldclim",
            - lim_inf_training and lim_sup_training: define the training interval.
            - lim_inf_validation and lim_inf_validation: define the validation 
                interval
            - modifier: "cases", "incidence", "prevalence" or "lethality"
            - type_analysis: "green", "red" or None
            - lim_inf_first and lim_sup_first: define the first interval (before than
                training interval)
            - path: 
        Returns: 
            - absolute path covariables report 
            - absolute path cells report 
            - message
    '''

    covariable_filename = 'COVARIABLES::'
    cells_filename = 'CELLS::'

    try:
        absolute_path = os.path.join(os.path.dirname(__file__), '../')
        absolute_path = os.path.join(absolute_path, path)
        print(absolute_path)
    except Exception as e:
        message = "There was a problem related path of the report"
        return (None, None, message)

    covariables_list, summary_list, message = nbayes_analysis(target, covariables, 
        lim_inf_training, lim_sup_training, lim_inf_validation, lim_sup_validation, 
        modifier, type_analysis, lim_inf_first, lim_sup_first)


    covariable_filename += 'target:' 
    cells_filename += 'target:'
    for t in target:
        covariable_filename += t + ';'
        cells_filename += t + ';'

    covariable_filename += ';'
    cells_filename += ';'

    covariable_filename += 'covariables:' 
    cells_filename += 'covariables:' 
    for c in covariables:
        covariable_filename += c + ';'
        cells_filename += c + ';'

    covariable_filename += ';'
    cells_filename += ';'

    covariable_filename += 'training:' + lim_inf_training + '_to_' + lim_sup_training + ';'
    cells_filename += 'training:' + lim_inf_training + '_to_' + lim_sup_training + ';'

    covariable_filename += 'validation:' + lim_inf_validation + '_to_' + lim_sup_validation + ';' 
    cells_filename += 'validation:' + lim_inf_validation + '_to_' + lim_sup_validation + ';'

    if type_analysis == None:
        covariable_filename += 'type:profiling;'
        cells_filename += 'type:profiling;'
    else:
        covariable_filename += 'type:' + type_analysis + ';'
        cells_filename += 'type:' + type_analysis + ';'

    if modifier != None:
        covariable_filename += 'modifier:' + modifier + ';'
        cells_filename += 'modifier:' + modifier + ';'

    covariable_filename += '.csv'
    cells_filename += '.csv'

    df_covariables = pd.DataFrame(covariables_list)
    df_cells = pd.DataFrame(summary_list)

    cell_names = get_cells_name()
    df_names = pd.DataFrame(cell_names)

    df_cells = df_cells.merge(df_names, how='left', left_on='gridid', right_on='gridid_munkm') 

    df_covariables.to_csv(os.path.join(absolute_path, covariable_filename), index=False)
    df_cells.to_csv(os.path.join(absolute_path, cells_filename), index=False)





