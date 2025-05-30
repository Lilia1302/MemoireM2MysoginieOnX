import json

INPUT_FILE = "C:\Users\ULTRABOOK DELL\OneDrive - UPEC\Bureau\Mémoire M2\DataSets\MAZAN_REACTIONS_2024-09-15_2025-03-15_tweets.json"
OUTPUT_FILE = "tweets_mazan_affaire_filtrés.json"

# Mots-clés indiquant qu’un tweet parle de l’affaire judiciaire (et pas de la ville)
keywords = [
    "gisele pelicot", "gisèle pelicot", "viols", "viol collectif",
    "procès", "procès mazan", "condamnation", "jugement", "victime", "témoignage",
    "dominique pelicot", "caroline darian", "soumission chimique", "accusés"
]

# Mots-clés à exclure (liés à la ville ou hors contexte)
exclude_keywords = [
    "carrière à ciel ouvert", "usine", "big band", "concert", "plâtre", "industrie", "jazz"
]

filtered = []

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        tweet = json.loads(line)
        text = tweet["text"].lower()
        if any(kw in text for kw in keywords) and not any(kw in text for kw in exclude_keywords):
            filtered.append(tweet)

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    for tweet in filtered:
        json.dump(tweet, f, ensure_ascii=False)
        f.write('\n')

print(f"✅ {len(filtered)} tweets filtrés sur l'affaire Mazan sauvegardés dans {OUTPUT_FILE}")
