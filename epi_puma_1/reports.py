import os
import json
import requests
import pandas as pd
from .analysis import *


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
    try:
        absolute_path = os.path.join(os.path.dirname(__file__), path)
        print(absolute_path)
    except Exception as e:
        message = "There was a problem related path of the report"
        return (None, None, message)

    covariables_list, summary_list, message = nbayes_analysis(target, covariables, 
        lim_inf_training, lim_sup_training, lim_inf_validation, lim_sup_validation, 
        modifier, type_analysis, lim_inf_first, lim_sup_first)

    df_covariables = pd.DataFrame(covariables_list)
    df_cells = pd.DataFrame(summary_list)

    df_covariables.to_csv(os.path.join(absolute_path, 'covars.csv'), index=False)
    df_cells.to_csv(os.path.join(absolute_path, 'cells.csv'), index=False)





