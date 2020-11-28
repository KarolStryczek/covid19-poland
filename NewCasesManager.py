import pandas as pd
from datetime import datetime


filepath = r'./data/cases.csv'


def get_cases(voivodeship: str = None, date_from: str = None, date_to: str = None):
    cases = pd.read_csv(filepath)
    if voivodeship is not None:
        cases = cases[cases.voivodeship == voivodeship]
    if date_from is not None:
        cases = cases[cases.date >= date_from]
    if date_to is not None:
        cases = cases[cases.date <= date_to]
    return cases


def get_cases_grouped(voivodeship: str = None, date_from: str = None, date_to: str = None):
    cases = get_cases(voivodeship, date_from, date_to)
    cases = cases.groupby('voivodeship').sum()
    cases.reset_index(inplace=True)
    return cases


def populate_cases_with_ids(cases, id_map):
    cases['id'] = cases['voivodeship'].apply(lambda name: id_map[name])
    return cases
