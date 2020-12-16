import json
from data_access import dao
import pandas as pd
from typing import Tuple, Dict, List, Union
import datetime as dt


any_date = Union[dt.datetime, str]


def get_geojson() -> Tuple[Dict, Dict]:
    with open('visualization_app/voivodeships.json', 'r', encoding='utf-8') as outfile:
        voivodeships = json.load(outfile)

    voivodeship_map = dict()
    for voivodeship in voivodeships['features']:
        voivodeship_map[voivodeship['properties']['name']] = voivodeship['id']
    return voivodeships, voivodeship_map


def get_unique_dates() -> List[str]:
    cases = dao.get_cases_filtered()
    dates = cases['date'].unique()
    dates.sort()
    return dates.tolist()


def get_cases_and_voivodeships(date_from: any_date, date_to: any_date) -> Tuple[pd.DataFrame, Dict]:
    voivodeships, voivodeship_map = get_geojson()
    cases = dao.get_cases_grouped(date_from=date_from, date_to=date_to)
    cases = populate_cases_with_ids(cases, voivodeship_map)
    return cases, voivodeships


def populate_cases_with_ids(cases: pd.DataFrame, id_map: Dict) -> pd.DataFrame:
    cases['id'] = cases['voivodeship'].apply(lambda name: id_map[name])
    return cases


def count_cases(cases: pd.DataFrame) -> int:
    return cases['cases'].sum()
