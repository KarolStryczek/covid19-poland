import pandas as pd
from typing import Dict, Tuple
import os.path
from datetime import datetime
import re


# def parse_new_cases(new_cases_data) -> pd.DataFrame:
#     first_tweet = new_cases_data[0]
#     first_tweet_text = first_tweet.full_text.split(':')[1].replace(' i ', ', ').replace(' ', '')
#     second_tweet_text = new_cases_data[1].full_text.split('.')[0].replace(' i ', ', ').replace(' ', '')
#     voivodeships_data = first_tweet_text.split(',') + second_tweet_text.split(',')
#     voivodeships_cases = dict()
#     for voivodeship_data in list(filter(None, voivodeships_data)):
#         try:
#             parsed_data = parse_voivodeship_data(voivodeship_data)
#             voivodeships_cases.update(parsed_data)
#         except Exception:
#             print(f'{first_tweet.created_at}: {voivodeships_data}')
#     new_cases_data = pd.DataFrame(voivodeships_cases.items(), columns=['voivodeship', 'cases'])
#     new_cases_with_date, date = populate_new_cases_with_date(new_cases_data, first_tweet.created_at)
#     save_new_cases(new_cases_with_date, date)
#     return new_cases_with_date


def parse_new_cases(new_cases) -> pd.DataFrame:
    voivodeships = pd.read_csv(r'../data/voivodeships.csv')
    first_tweet = new_cases[0]
    tweets_text = first_tweet.full_text + new_cases[1].full_text
    new_cases_table = list()
    for voivodeship_genitive_name in voivodeships['name_genitive'].values:
        regex_pattern = re.compile(rf'{voivodeship_genitive_name} \(\d+')
        matched_object = regex_pattern.search(tweets_text)
        if matched_object is not None:
            name_genitive, value = matched_object.group().replace('(', '').split(' ')
            name = voivodeships[voivodeships['name_genitive'] == voivodeship_genitive_name]['name'].values[0]
            new_cases_table.append([name, value])
        else:
            print(f'Date: {first_tweet.created_at}, voivodeship: {voivodeship_genitive_name}, text: {tweets_text}')
    new_cases_data = pd.DataFrame(new_cases_table, columns=['voivodeship', 'cases'])
    new_cases_with_date, date = populate_new_cases_with_date(new_cases_data, first_tweet.created_at)
    save_new_cases(new_cases_with_date, date)
    return new_cases_with_date


# def parse_voivodeship_data(voivodeship_data: str) -> Dict[str, int]:
#     voivodeships = pd.read_csv(r'./data/voivodeships.csv')
#     voivodeship_data = voivodeship_data.strip()
#     voivodeship_name_end_index = voivodeship_data.find('(')
#     voivodeship_genitive_name = voivodeship_data[:voivodeship_name_end_index]
#     voivodeship_cases = int(voivodeship_data[voivodeship_name_end_index + 1:-1])
#     voivodeship_name = voivodeships[voivodeships.name_genitive == voivodeship_genitive_name].name.values[0]
#     return {voivodeship_name: voivodeship_cases}


def populate_new_cases_with_date(new_cases: pd.DataFrame, date_time: datetime) -> Tuple[pd.DataFrame, str]:
    date = date_time.strftime('%Y-%m-%d')
    new_cases.insert(1, 'date', [date] * len(new_cases))
    return new_cases, date


def save_new_cases(new_cases: pd.DataFrame, date: str) -> None:
    filepath = r'../data/cases.csv'
    # save_to_daily_file(new_cases, date)
    if not os.path.isfile(filepath):
        new_cases.to_csv(filepath, index=False)
    else:
        cases = pd.read_csv(filepath)
        if len(cases[cases.date == date]) == 0:
            new_cases.to_csv(filepath, index=False, header=False, mode='a')


# def save_to_daily_file(new_cases: pd.DataFrame, date:str) -> None:
#     filepath = rf'./data/daily/{date}.csv'
#     if not os.path.isfile(filepath):
#         new_cases.to_csv(filepath, index=False)
