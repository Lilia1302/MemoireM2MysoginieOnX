import json
from ntscraper import Nitter

scraper = Nitter(log_level=1, skip_instance_check=False)

def fetch_tweets_in_batches(query, mode='hashtag', total_tweets=2000, batch_size=50):
    all_tweets = []
    remaining_tweets = total_tweets

    try:
        while remaining_tweets > 0:
            num_to_fetch = min(batch_size, remaining_tweets)
            print(f"Fetching {num_to_fetch} tweets...")
            
            try:
                tweets = scraper.get_tweets(query, mode=mode, number=num_to_fetch)
                
                if 'tweets' in tweets and tweets['tweets']:
                    all_tweets.extend(tweets['tweets'])
                    remaining_tweets -= len(tweets['tweets'])
                    print(f"✅ Fetched {len(tweets['tweets'])} tweets. Remaining: {remaining_tweets}")
                else:
                    print("❗ No more tweets found.")
                    break
            except IndexError as e:
                print(f"IndexError: {e}. Skipping to the next batch.")
                continue

        # Save to JSON
        with open('tweets.json', 'w', encoding='utf-8') as f:
            json.dump(all_tweets, f, ensure_ascii=False, indent=4)
        print("✅ Tweets successfully saved to 'tweets.json'.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function
fetch_tweets_in_batches("Mazan", total_tweets=2000)
