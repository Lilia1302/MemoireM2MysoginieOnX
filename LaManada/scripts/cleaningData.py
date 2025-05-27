import pandas as pd
import re

# === Charger le fichier ===
df = pd.read_json(r"C:\Users\ULTRABOOK DELL\OneDrive - UPEC\Bureau\Mémoire M2\DataSets\LaManada\results\tweets_twikit_multi_periods_part2.json", lines=True)

# === Supprimer les colonnes RGPD ===
colonnes_rgpd = ['username', 'user_id', 'location', 'id']
df = df.drop(columns=[col for col in colonnes_rgpd if col in df.columns], errors='ignore')

# === Supprimer les tweets vides ===
df = df.dropna(subset=['text'])

# === Nettoyage du texte ===
def clean_text(text):
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'#\S+', '', text)
    text = re.sub(r'[^a-zA-ZÀ-ÿ0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()

df['cleaned_text'] = df['text'].apply(clean_text)

# === Détection de misogynie ===
mots_misogynes = [
    "puta", "zorra", "feminazi", "se lo buscó", "ella miente", "puta feminista",
    "violación falsa", "es mentira", "merecía", "prostituta", "les violen"
]

def detect_misogyny(text):
    return any(mot in text for mot in mots_misogynes)

df['is_misogynistic'] = df['cleaned_text'].apply(detect_misogyny)

# === Détection de tweets de soutien ===
mots_soutien = [
    "yo sí te creo", "fue violación", "sentencia injusta", "cultura de la violación",
    "justicia patriarcal", "no es abuso es violación", "apoyo a la víctima",
    "no olvidamos", "no es no", "solidaridad con la víctima"
]

def detect_support(text):
    return any(mot in text for mot in mots_soutien)

df['is_supportive'] = df['cleaned_text'].apply(detect_support)

# === Convertir les dates ===
df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')

# === Réorganiser les colonnes ===
colonnes_finales = [
    'created_at', 'text', 'cleaned_text', 'likes', 'retweets', 'period',
    'is_misogynistic', 'is_supportive'
]
df = df[[col for col in colonnes_finales if col in df.columns]]

# === Sauvegarder le résultat ===
df.to_csv("tweets_twikit_cleaned_classified.csv", index=False)
print("✅ Fichier exporté avec misogynie et soutien détectés.")
