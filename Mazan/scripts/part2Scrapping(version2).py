import asyncio
from twikit import Client, TooManyRequests
import json
from datetime import datetime
from configparser import ConfigParser
from random import randint
import httpx

MINIMUM_TWEETS = 500

QUERY_GROUPS = {
    "mazan_misogynie": [
        '("mazan" OR "gisèle pelicot") ("pute" OR "sal*pe" OR "elle ment" OR "viol collectif" OR "femmes menteuses" OR "justice pour les hommes" OR "c’est faux" OR "elles exagèrent" OR "elle l’a cherché" OR "faut arrêter de croire les femmes") lang:fr'
    ]
}

PERIODS = [
    ("2024-12-01", "2025-05-29")
]

config = ConfigParser()
config.read(r"C:\Users\ULTRABOOK DELL\OneDrive - UPEC\Bureau\Mémoire M2\DataSets\LaManada\config.ini")
client = Client(language='fr-FR')

async def get_tweets(query, since, until):
    search_query = f"{query} since:{since} until:{until}"
    print(f"{datetime.now()} - Searching: {search_query}")
    try:
        tweets = await client.search_tweet(search_query, product='Latest')
        return tweets
    except Exception as e:
        print(f"⛔ Erreur initiale de recherche : {e}")
        return None

def save_tweets(tweets, filename):
    try:
        with open(filename, 'a', encoding='utf-8') as json_file:
            for tweet in tweets:
                json.dump(tweet, json_file, ensure_ascii=False)
                json_file.write("\n")
        print(f"✅ {len(tweets)} tweets enregistrés dans {filename}")
    except Exception as e:
        print(f"⛔ Erreur enregistrement fichier : {e}")

async def main():
    print('🔐 Connexion à X...')
    client.load_cookies(r"C:\Users\ULTRABOOK DELL\OneDrive - UPEC\Bureau\Mémoire M2\DataSets\LaManada\cookies.json")

    for label, queries in QUERY_GROUPS.items():
        for since, until in PERIODS:
            for query in queries:
                tweet_count = 0
                tweets = await get_tweets(query, since, until)
                period_tweets = []
                file_label = f"{label.upper()}_{since}_{until}_tweets.json"

                while tweets and tweet_count < MINIMUM_TWEETS:
                    try:
                        for tweet in tweets:
                            text = tweet.text.lower()
                            # Sécurité : le texte doit contenir une mention claire de l'affaire
                            if "mazan" in text or "gisèle pelicot" in text:
                                tweet_json = {
                                    "id": tweet.id,
                                    "count": tweet_count,
                                    "username": tweet.user.name,
                                    "text": tweet.text.replace("\n", " "),
                                    "created_at": tweet.created_at,
                                    "retweets": tweet.retweet_count,
                                    "likes": tweet.favorite_count,
                                    "location": tweet.user.location if tweet.user.location else "Unknown",
                                    "period": f"{since} to {until}",
                                    "label": label
                                }

                                period_tweets.append(tweet_json)
                                tweet_count += 1

                                if tweet_count % 100 == 0:
                                    print(f"{tweet_count} tweets collectés... sauvegarde temporaire.")
                                    save_tweets(period_tweets, file_label)
                                    period_tweets.clear()

                        wait = randint(10, 30)
                        print(f"⏳ Attente {wait}s avant la page suivante...")
                        await asyncio.sleep(wait)
                        tweets = await tweets.next()

                    except TooManyRequests as e:
                        wait_time = (datetime.fromtimestamp(e.rate_limit_reset) - datetime.now()).total_seconds()
                        print(f"⚠️ Rate limit atteint. Attente {wait_time:.0f}s...")
                        await asyncio.sleep(wait_time)
                    except httpx.ConnectTimeout:
                        print(f"🌐 Timeout réseau. Reconnexion dans 60s...")
                        await asyncio.sleep(60)
                    except Exception as e:
                        print(f"⚠️ Erreur inattendue : {e}")
                        await asyncio.sleep(30)
                        break

                if period_tweets:
                    save_tweets(period_tweets, file_label)

    print(f"{datetime.now()} ✅ Fin de la collecte.")

asyncio.run(main())
