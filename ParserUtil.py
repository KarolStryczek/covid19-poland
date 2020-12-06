import pandas as pd
from typing import Dict, Tuple
import os.path
from datetime import datetime


def parse_new_cases(new_cases_dict: Dict) -> pd.DataFrame:
    first_tweet = new_cases_dict['first_tweet']
    first_tweet_data = first_tweet.full_text.split(': ')[1]
    second_tweet_data = new_cases_dict['other_tweets'][0].full_text.split('.')[0]
    voivodeships_data = first_tweet_data.split(', ') + second_tweet_data.split(', ')
    voivodeships_cases = dict()
    for voivodeship_data in voivodeships_data:
        try:
            parsed_data = parse_voivodeship_data(voivodeship_data)
            voivodeships_cases.update(parsed_data)
        except Exception:
            print(first_tweet.created_at)
    new_cases = pd.DataFrame(voivodeships_cases.items(), columns=['voivodeship', 'cases'])
    new_cases_with_date, date = populate_new_cases_with_date(new_cases, first_tweet.created_at)
    save_new_cases(new_cases_with_date, date)
    return new_cases_with_date


def parse_voivodeship_data(voivodeship_data: str) -> Dict[str, int]:
    voivodeships = pd.read_csv(r'./data/voivodeships.csv')
    voivodeship_data = voivodeship_data.strip()
    voivodeship_genitive_name = voivodeship_data[:voivodeship_data.find(' ')]
    voivodeship_cases_str = voivodeship_data[voivodeship_data.find('(') + 1: voivodeship_data.find(')')]
    voivodeship_cases = int(voivodeship_cases_str.replace(' ', ''))
    voivodeship_name = voivodeships[voivodeships.name_genitive == voivodeship_genitive_name].name.values[0]
    return {voivodeship_name: voivodeship_cases}


def populate_new_cases_with_date(new_cases: pd.DataFrame, date_time: datetime) -> Tuple[pd.DataFrame, str]:
    date = date_time.strftime('%Y-%m-%d')
    new_cases.insert(1, 'date', [date] * len(new_cases))
    return new_cases, date


def save_new_cases(new_cases: pd.DataFrame, date: str) -> None:
    filepath = r'./data/cases.csv'
    save_to_daily_file(new_cases, date)
    if not os.path.isfile(filepath):
        new_cases.to_csv(filepath, index=False)
    else:
        cases = pd.read_csv(filepath)
        if len(cases[cases.date == date]) == 0:
            new_cases.to_csv(filepath, index=False, header=False, mode='a')


def save_to_daily_file(new_cases: pd.DataFrame, date:str) -> None:
    filepath = rf'./data/daily/{date}.csv'
    if not os.path.isfile(filepath):
        new_cases.to_csv(filepath, index=False)
