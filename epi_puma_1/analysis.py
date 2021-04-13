import os
import json
import requests


def nbayes_epi_puma_v1(target, covariables, lim_inf_training, lim_sup_training, 
          lim_inf_validation, lim_sup_validation, modifier=None, 
          type_analysis=None, lim_inf_first=None, lim_sup_first=None):
    '''
        Description: This function makes a request to Epi-Puma API 1.0
    
        Args:
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
        Returns: 
            - List of covariables
            - List of municipalities 
            - A message - 
    '''
    available_targets = ["COVID-19 CONFIRMADO", "COVID-19 FALLECIDO", 
                         "COVID-19 NEGATIVO"]

    available_covariables = {
                             'Demograficos': {'name': 'Demograficos', 'biotic': True, 'merge_vars': [{'rank': 'kingdom', 'value': 'Demográficos', "type":0, 'level': 'species'}]}, 
                             'Pobreza': {'name': 'Pobreza', 'biotic': True, 'merge_vars': [{'rank': 'kingdom', 'value': 'Pobreza', 'level': 'species'}]}, 
                             'Movilidad': {'name': 'Movilidad', 'biotic': True, 'merge_vars': [{'rank': 'kingdom', 'value': 'Movilidad', 'level': 'species'}]}, 
                             'Infraestructura-Salud': {'name': 'Infraestructura-Salud', 'biotic': True, 'merge_vars': [{'rank': 'kingdom', 'value': 'infraestructura_salud', 'level': 'species'}]}, 
                             'Vulnerabilidad': {'name': 'Vulnerabilidad', 'biotic': True, 'merge_vars': [{'rank': 'genus', 'value': 'Vulnerabilidad', 'level': 'species'}]},
                             'Worldclim': {'name': 'Worldclim', 'biotic': True, 'merge_vars': [{'rank': 'type', 'value': 13, 'level': 'bid'}]}, 
                             'CCA-Climaticas': {'name': 'CCA-Climaticas', 'biotic': True, 'merge_vars': [{'rank': 'type', 'value': 12, 'level': 'bid'}]},
                             'CCA-Contaminacion': {'name': 'CCA-Contaminacion', 'biotic': True, 'merge_vars': [{'rank': 'type', 'value': 14, 'level': 'bid'}]}
                             }

    available_modifiers = ["cases", "incidence", "prevalence", "lethality"]
    analysis_types = ['red', 'green', 'none']
    url = ''
    covariables_response = []
    cells = []
    message = 'Everything is OK'
    try:
        with open('conf.json', 'r') as f:
            content_file = f.read()
            json_parsed = json.loads(content_file)
            url = json_parsed['urlApiEP1.0']
    except Exception as e:
        message = "There was a problem related with config file: URL Epi Puma 1.0"
        return (None, None, message)

    ## Target validation
    for t in target:
        if not t in available_targets:
            message = 'There was a problem related with target: {} not found'.format(t)
            return (None, None, message)

    for c in covariables:
        if not c in available_covariables.keys():
            message = 'There was a problem related with covariables: {} not found'.format(c)
            return (None, None, message)

    if lim_inf_training == None or lim_sup_training == None:
        message = 'There was a problem related training period: dates are nulls'
        return (None, None, message)

    if lim_sup_training < lim_inf_training:
        message = 'There was a problem related training period: interval is incorrect'
        return (None, None, message)

    if lim_inf_validation == None or lim_sup_validation == None:
        message = 'There was a problem related validation period: dates are nulls'
        return (None, None, message)

    if lim_sup_validation < lim_inf_validation:
        message = 'There was a problem related validation period: interval is incorrect'
        return (None, None, message)

    if type_analysis == None:
        type_analysis = 'none'

    if not type_analysis in analysis_types:
        message = 'There was a problem related analysis type: {} isn\'t an analysis type'.format(type_analysis)
        return (None, None, message)

    if modifier != None and not modifier in available_modifiers:
        message = 'There was a problem related with target: {} isn\'t an available modifier type'.format(modifier)
        return (None, None, message)        

    ## Body construction
    body_ = '{"min_cells":1,"fosil":false,"date":false,"grid_resolution":"mun","region":1,"get_grid_species":false,"with_data_score_cell":true,"with_data_freq":true,"with_data_freq_cell":true,"with_data_score_decil":true,"excluded_cells":[],"target_name":"targetGroup"}'
    body_ = json.loads(body_)

    if lim_inf_first != None and lim_sup_first !=None:
        body_['lim_inf_first'] = lim_inf_first
        body_['lim_sup_first'] = lim_sup_first
    
    body_['lim_inf'] = lim_inf_training
    body_['lim_sup'] = lim_sup_training
    body_['lim_inf_validation'] = lim_inf_validation
    body_['lim_sup_validation'] = lim_sup_validation

    body_['target_taxons'] = []

    for t in target:
        body_['target_taxons'].append({"taxon_rank":"species","value":t})

    body_['covariables'] = []

    for c in covariables:
        body_['covariables'].append(available_covariables[c])   

    #print(body_['covariables'])
    ## Request to API
    if modifier != None:
        body_['modifier'] = modifier
        url = url + 'niche/generateTarget'
    else:
        url = url + 'niche/countsTaxonsGroupTimeValidation'

    print(url)
    response = requests.post(url, json=body_)
    response = response.json()

    ## Extract data from response
    covariables_response = response['data']
    cells = response['cell_summary']
    return (covariables_response, cells, message)