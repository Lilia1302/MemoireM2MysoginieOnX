import json
import pandas as pd

# Lire ligne par ligne, chaque ligne étant un tweet JSON
with open("tweets_twikit_multi_periods.json", encoding="utf-8") as f:
    data = [json.loads(line) for line in f]

# Créer un DataFrame avec pandas
df = pd.DataFrame(data)

# Sauvegarder en CSV
df.to_csv("tweets_lamanada.csv", index=False, encoding="utf-8")
