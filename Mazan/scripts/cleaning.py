import pandas as pd
import re

# === Étape 1 : Charger les fichiers JSON ===
fichiers_json = [
    r"C:\Users\ULTRABOOK DELL\OneDrive - UPEC\Bureau\Mémoire M2\DataSets\MISOGYNIE_MAZAN_2024-12-10_2024-12-20_tweets.json",
    r"C:\Users\ULTRABOOK DELL\OneDrive - UPEC\Bureau\Mémoire M2\DataSets\MISOGYNIE_MAZAN_2025-01-07_2025-01-15_tweets.json",
    r"C:\Users\ULTRABOOK DELL\OneDrive - UPEC\Bureau\Mémoire M2\DataSets\MISOGYNIE_MAZAN_2025-02-25_2025-03-05_tweets.json",
    r"C:\Users\ULTRABOOK DELL\OneDrive - UPEC\Bureau\Mémoire M2\DataSets\MAZAN_MENTIONS_2024-09-15_2025-03-15_tweets.json"
]

df_list = [pd.read_json(f, lines=True) for f in fichiers_json]
df = pd.concat(df_list, ignore_index=True)

# === Étape 2 : Supprimer les colonnes RGPD ===
colonnes_rgpd = ['username', 'user_id', 'location', 'id']
df = df.drop(columns=[col for col in colonnes_rgpd if col in df.columns], errors='ignore')

# === Étape 3 : Supprimer les tweets vides ===
df = df.dropna(subset=['text'])

# === Étape 4 : Nettoyage du texte ===
def clean_text(text):
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'#\S+', '', text)
    text = re.sub(r'[^a-zA-ZÀ-ÿ0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()

df['cleaned_text'] = df['text'].apply(clean_text)

# === Étape 5 : Détection de misogynie via mots-clés ===
mots_misogynes = [
    "pute", "pétasse", "sal*pe", "tapin", "viol collectif", "victime elle ment",
    "elle l’a cherché", "tournée comme une chienne", "grosse pute",
    "fausse victime", "méritait", "main au cul", "daronne", "enfant de viol"
]

def detect_misogyny(text):
    return any(mot in text for mot in mots_misogynes)

df['is_misogynistic'] = df['cleaned_text'].apply(detect_misogyny)

# === Étape 6 : Conversion des dates ===
df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')

# === Étape 7 : Réorganiser les colonnes ===
colonnes_finales = [
    'created_at', 'text', 'cleaned_text',
    'likes', 'retweets', 'period', 'label', 'is_misogynistic'
]
df = df[[col for col in colonnes_finales if col in df.columns]]

# === Étape 8 : Export final ===
df.to_csv("tweets_mazan_nettoyes_rgpd_misogynie.csv", index=False)

print("✅ Fichier final exporté : tweets_mazan_nettoyes_rgpd_misogynie.csv")
