import pandas as pd
from typing import Tuple
import datetime as dt
from data_access import dao
import re
from typing import List
from tweepy import Status


def parse_new_cases(new_cases: List[Status]) -> None:
    first_tweet = new_cases[0]
    tweet_text = first_tweet.full_text + ' ' + new_cases[1].full_text
    new_cases_data = parse_tweet_text(tweet_text)
    if sum(new_cases_data.cases.values) > 0:
        new_cases_with_date, date = populate_new_cases_with_date(new_cases_data, first_tweet.created_at)
        dao.save_new_cases(new_cases_with_date)


def parse_tweet_text(tweet_text: str) -> pd.DataFrame:
    voivodeships = dao.get_voivodeships()
    new_cases_table = list()
    for voivodeship_genitive_name in voivodeships['name_genitive'].values:
        regex_pattern = re.compile(rf'[\n|\s]{voivodeship_genitive_name} \(\d+')
        matched_object = regex_pattern.search(tweet_text)
        name = voivodeships[voivodeships['name_genitive'] == voivodeship_genitive_name]['name'].values[0]
        if matched_object is not None:
            name_genitive, value = matched_object.group().strip().replace('(', '').split(' ')
        else:
            value = 0
        new_cases_table.append([name, int(value)])
    return pd.DataFrame(new_cases_table, columns=['voivodeship', 'cases'])


def populate_new_cases_with_date(new_cases: pd.DataFrame, date_time: dt.datetime) -> Tuple[pd.DataFrame, str]:
    date = date_time.strftime('%Y-%m-%d')
    new_cases.insert(1, 'date', [date] * len(new_cases))
    return new_cases, date

