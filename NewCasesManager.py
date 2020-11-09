import pandas as pd
from datetime import datetime


class NewCasesManager:
    def __init__(self):
        self.cases = pd.read_csv(r'./data/cases.csv')

    def get_cases(self, voivodeship: str = None, date_from: str = None, date_to: str = None):
        cases = self.cases
        if voivodeship is not None:
            cases = cases[cases.voivodeship == voivodeship]
        if date_from is not None:
            cases = cases[cases.date >= date_from]
        if date_to is not None:
            cases = cases[cases.date <= date_to]
        return cases
