import json
import pandas as pd
from acquisition_app import NewCasesManager


def get_geojson():
    with open('data/voivodeships.json', 'r', encoding='utf-8') as outfile:
        voivodeships = json.load(outfile)

    voivodeship_map = dict()
    for voivodeship in voivodeships['features']:
        voivodeship_map[voivodeship['properties']['name']] = voivodeship['id']
    return voivodeships, voivodeship_map


def get_dates():
    cases = pd.read_csv(r'data/cases.csv')
    dates = cases['date'].unique()
    dates.sort()
    return dates


def get_cases(date_from, date_to, voivodeship_map):
    cases = NewCasesManager.get_cases_grouped(date_from=date_from, date_to=date_to)
    cases = NewCasesManager.populate_cases_with_ids(cases, voivodeship_map)
    return cases
