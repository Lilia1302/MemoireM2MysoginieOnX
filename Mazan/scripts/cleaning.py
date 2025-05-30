import json
import pandas as pd
import re
import string

# === 1. Charger le fichier JSONL ===
input_path = "C:/Users/ULTRABOOK DELL/OneDrive - UPEC/Bureau/Mémoire M2/DataSets/Mazan/results/Mazan_Tweets_part2.json"

with open(input_path, "r", encoding="utf-8") as f:
    tweets = [json.loads(line) for line in f if line.strip()]  # JSONL : 1 tweet par ligne

# === 2. Créer un DataFrame ===
df = pd.DataFrame(tweets)

# === 3. Supprimer les doublons basés sur la colonne "text" ===
if "text" in df.columns:
    df = df.drop_duplicates(subset="text")

# === 4. Nettoyer le texte pour BERT/RoBERTa ===
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)                     # supprimer les liens
    text = re.sub(r"@\w+", "", text)                         # supprimer les mentions @
    text = re.sub(r"#", "", text)                            # enlever '#' mais garder le mot
    text = text.translate(str.maketrans("", "", string.punctuation))  # enlever ponctuation
    text = re.sub(r"\s+", " ", text).strip()                # enlever espaces multiples
    return text

if "text" in df.columns:
    df["clean_text"] = df["text"].apply(clean_text)

# === 5. Supprimer les colonnes inutiles si elles existent ===
colonnes_a_supprimer = ["user", "quoted-post", "replying-to", "pictures", "videos", "gifs", "link"]
colonnes_existantes = [col for col in colonnes_a_supprimer if col in df.columns]
if colonnes_existantes:
    df = df.drop(columns=colonnes_existantes)

# === 6. Exporter en CSV ===
output_path = "C:/Users/ULTRABOOK DELL/OneDrive - UPEC/Bureau/Mémoire M2/DataSets/Mazan/results/mazan_part2_cleaned.csv"
df.to_csv(output_path, index=False, encoding="utf-8")

print(f"{len(df)} tweets nettoyés et enregistrés dans {output_path}")
