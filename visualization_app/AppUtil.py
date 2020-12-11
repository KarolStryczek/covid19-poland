import json
from data_access import dao


def get_geojson():
    with open('visualization_app/voivodeships.json', 'r', encoding='utf-8') as outfile:
        voivodeships = json.load(outfile)

    voivodeship_map = dict()
    for voivodeship in voivodeships['features']:
        voivodeship_map[voivodeship['properties']['name']] = voivodeship['id']
    return voivodeships, voivodeship_map


def get_dates():
    cases = dao.get_cases_filtered()
    dates = cases['date'].unique()
    dates.sort()
    return dates


def get_cases(date_from, date_to, voivodeship_map):
    cases = dao.get_cases_grouped(date_from=date_from, date_to=date_to)
    cases = populate_cases_with_ids(cases, voivodeship_map)
    return cases


def populate_cases_with_ids(cases, id_map):
    cases['id'] = cases['voivodeship'].apply(lambda name: id_map[name])
    return cases
