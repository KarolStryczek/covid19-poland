import tweepy
from tweepy.models import Status
import os
import re


class MinistryOfHealthTwitter:
    HEALTH_MINISTRY_TWITTER = "MZ_GOV_PL"
    PATTERN = re.compile(r".*Mamy [\d|\s]+ now.+ przypadk.+ zakażenia #*koronawirus.+", re.IGNORECASE)

    def __init__(self):
        auth = tweepy.OAuthHandler(os.getenv('TWITTER_API_KEY'), os.getenv('TWITTER_API_KEY_SECRET'))
        auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'), os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))
        self.api = tweepy.API(auth)
        self.tweets = list()

    def get_tweets_cursor(self, **kwargs) -> tweepy.Cursor:
        return tweepy.Cursor(self.api.user_timeline, id=self.HEALTH_MINISTRY_TWITTER, tweet_mode="extended", **kwargs)

    def get_new_cases_tweets(self, count: int = 100, **kwargs):
        new_cases_tweets = list()
        previous_tweets = list()
        for tweet in self.get_tweets_cursor(**kwargs).items(count):
            if self.is_new_cases_start_tweet(tweet):
                new_case = [tweet]
                for i in range(len(previous_tweets)-1, -1, -1):
                    if previous_tweets[i].in_reply_to_status_id == new_case[-1].id:
                        new_case.append(previous_tweets[i])
                    else:
                        previous_tweets = list()
                        break
                new_cases_tweets.append(new_case)
            else:
                previous_tweets.append(tweet)
        return new_cases_tweets

    def is_new_cases_start_tweet(self, tweet: Status) -> bool:
        return self.PATTERN.match(tweet.full_text) is not None
