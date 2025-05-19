import json
from ntscraper import Nitter


scraper = Nitter(log_level=1, skip_instance_check=False)
def fetch_tweets(query, mode, total_tweets, filename):
    all_tweets = []
    remaining = total_tweets
    batch_size = 50

    while remaining > 0:
        print(f"🔍 Fetching batch of {min(batch_size, remaining)} tweets for: {query}")
        try:
            tweets = scraper.get_tweets(query, mode=mode, number=min(batch_size, remaining))
            if 'tweets' in tweets and tweets['tweets']:
                all_tweets.extend(tweets['tweets'])
                remaining -= len(tweets['tweets'])
                print(f"✅ Fetched {len(tweets['tweets'])} tweets. Remaining: {remaining}")
            else:
                print("⚠️ No more tweets found.")
                break
        except Exception as e:
            print(f"❌ Error fetching tweets: {e}")
            break

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_tweets, f, ensure_ascii=False, indent=4)
    print(f"📁 Saved {len(all_tweets)} tweets to {filename}")

# ----------------------
# UTILISATION AVEC mode='hashtag'
# ----------------------

# Par exemple : tweets contenant le hashtag #Mazan
fetch_tweets("Mazan", mode='hashtag', total_tweets=100, filename='mazan_hashtag_tweets.json')

# OU : un autre exemple en mode 'term' (si tu veux des tweets qui mentionnent un mot)
# fetch_tweets("viol Mazan", mode='term', total_tweets=100, filename='mazan_term_tweets.json')