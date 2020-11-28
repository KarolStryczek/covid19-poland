import json
import pandas as pd


def get_geojson():
    with open('./data/voivodeships.json', 'r', encoding='utf-8') as outfile:
        voivodeships = json.load(outfile)

    voivodeship_map = dict()
    for voivodeship in voivodeships['features']:
        voivodeship_map[voivodeship['properties']['name']] = voivodeship['id']
    return voivodeships, voivodeship_map


def get_dates():
    cases = pd.read_csv(r'./data/cases.csv')
    dates = cases['date'].unique()
    dates.sort()
    return dates
