import json
import pandas as pd

with open('tweets.json', 'r', encoding='utf-8') as file:
    data = file.read()


if data.startswith('[') and data.endswith(']'):
    data = data[1:-1]  #deleate brakets 


data = data.replace("}\n{", "},\n{") #replace /n by , 

#add back brackets 
data = f"[{data}]"


try:
    tweets = json.loads(data)
    print("Fichier JSON chargé avec succès.")
except json.JSONDecodeError as e:
    print(f"Erreur de décodage JSON: {e}")

df = pd.json_normalize(tweets, sep='_')

df.to_csv('tweets_cleaned.csv', index=False)
print("Données sauvegardées en CSV.")

