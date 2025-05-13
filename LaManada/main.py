import asyncio
from twikit import Client, TooManyRequests
import json
from datetime import datetime
from configparser import ConfigParser
from random import randint
import httpx
import os

MINIMUM_TWEETS = 1000
# Périodes à scraper
QUERY_PERIODS = [
    ("La Manada", "2016-07-08", "2016-07-09"),
    ("La Manada", "2017-11-15", "2017-11-30"),
    ("La Manada", "2018-04-01", "2018-06-30"),
    ("La Manada", "2019-06-01", "2019-06-30"),
]

# Hashtags et expressions clés à surveiller
KEYWORDS = [
    "#LaManada", "#lamanada", "#Stopfeminazism", "#stopradicalfeminism", "#yonotecreo", "\"La Manada\""
]
async def get_tweets(tweets, query, since, until):
    search_query = f"({' OR '.join(KEYWORDS)}) {query} -filter:retweets lang:es since:{since} until:{until}"
    
    if tweets is None:
        print(f'{datetime.now()} - Getting tweets for {since} to {until}...')
        try:
            tweets = await client.search_tweet(search_query, product='Latest')
        except Exception as e:
            print(f"Error fetching initial tweets: {e}")
            return None
    else:
        wait_time = randint(15, 30)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...')
        await asyncio.sleep(wait_time)
        try:
            tweets = await tweets.next()
        except Exception as e:
            print(f"Error fetching next tweets: {e}")
            return None

    return tweets

#download config
config = ConfigParser()
config.read(r"C:\Users\ULTRABOOK DELL\OneDrive - UPEC\Bureau\Mémoire M2\DataSets\LaManada\config.ini")
username = config['X']['username']
email = config['X']['email']
password = config['X']['password']

client = Client(language='fr-FR')

#continuous saving
def save_tweets_to_file(tweets, filename='tweets_twikit_multi_periods_part2.json'):
    try:
        with open(filename, 'a', encoding='utf-8') as json_file:
            for tweet in tweets:
                json.dump(tweet, json_file, ensure_ascii=False)
                json_file.write("\n")
        print(f"{len(tweets)} tweets saved to {filename}")
    except Exception as e:
        print(f"Error saving tweets: {e}")

async def main():
    print('Logged in')
    client.load_cookies(r"C:\Users\ULTRABOOK DELL\OneDrive - UPEC\Bureau\Mémoire M2\DataSets\LaManada\cookies.json")

    for query, since, until in QUERY_PERIODS:
        tweet_count = 0
        tweets = None
        period_tweets = []

        while tweet_count < MINIMUM_TWEETS:
            try:
                tweets = await get_tweets(tweets, query, since, until)
                if not tweets:
                    print(f'{datetime.now()} - No more tweets found for {since} to {until}')
                    break

                for tweet in tweets:
                    tweet_count += 1
                    try:
                        created_at = datetime.strptime(tweet.created_at, "%Y-%m-%dT%H:%M:%S.%fZ").isoformat()
                    except ValueError:
                        created_at = tweet.created_at

                    tweet_data = {
                        "id": tweet.id,
                        "count": tweet_count,
                        "username": tweet.user.name,
                        "text": tweet.text.replace("\n", " "),
                        "created_at": created_at,
                        "retweets": tweet.retweet_count,
                        "likes": tweet.favorite_count,
                        "location": tweet.user.location if tweet.user.location else "Unknown",
                        "period": f"{since} to {until}"
                    }
                    period_tweets.append(tweet_data)

                    if tweet_count % 100 == 0:
                        print(f"{tweet_count} tweets collected. Saving progress...")
                        save_tweets_to_file(period_tweets)
                        period_tweets.clear()

            except TooManyRequests as e:
                rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
                print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
                wait_time = (rate_limit_reset - datetime.now()).total_seconds()
                await asyncio.sleep(wait_time)
            except httpx.ConnectTimeout:
                print(f'{datetime.now()} - Connection timeout. Retrying in 60 seconds...')
                await asyncio.sleep(60)
            except Exception as e:
                print(f"Unexpected error: {e}")
                await asyncio.sleep(30)

        if period_tweets:
            save_tweets_to_file(period_tweets)

    print(f'{datetime.now()} - Done!')


asyncio.run(main())