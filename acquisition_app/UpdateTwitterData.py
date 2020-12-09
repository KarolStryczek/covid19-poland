from acquisition_app import MinistryOfHealthTwitter, ParserUtil
import pandas as pd


def update_data():
    updates_filepath = r'../data/update.csv'
    updates = pd.read_csv(updates_filepath)
    last_id = None
    if len(updates) > 0:
        last_id = max(updates['last_id'])

    twitter = MinistryOfHealthTwitter.MinistryOfHealthTwitter()
    new_cases = twitter.get_new_cases_tweets(since_id=last_id)
    if len(new_cases) > 0:
        new_last_id = new_cases[0][0].id
        new_date = new_cases[0][0].created_at.strftime('%Y-%m-%d')
        new_update = pd.DataFrame([[new_date, new_last_id]], columns=['date', 'last_id'])
        new_update.to_csv(updates_filepath, index=False, header=False, mode='a')
        for new_case in new_cases:
            ParserUtil.parse_new_cases(new_case)


if __name__ == "__main__":
    update_data()
