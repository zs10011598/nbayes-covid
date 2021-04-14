import os
import json
import requests
import pandas as pd


def get_cells_name(resolution='mun'):
    '''
        Description: This function returns names and codes of cells

        Args:
            - resolution: "state"or "mun"

        Rteurns:
            - List of objects which represents cells
    '''
    try:
        with open('conf.json', 'r') as f:
            content_file = f.read()
            json_parsed = json.loads(content_file)
            url = json_parsed['urlApiEP1.0']
    except Exception as e:
        message = "There was a problem related with config file: URL Epi Puma 1.0"
        return (None, None, message)

    url = url + 'niche/especie/getColumnsGrid'
    body = {'gridids':[]}
    
    body['grid_resolution'] = resolution

    if resolution == 'mun':
        body['columns'] = ["NOM_MUN","NOM_ENT", "CVE_MUN", "CVE_ENT"]
    elif resolution == 'state':
        body['columns'] = ["NOM_ENT", "CVE_ENT"]

    res = requests.post(url, json=body).json()
    res = res['data']

    return res
