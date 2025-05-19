import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
from tqdm import tqdm

# Charger le CSV
df = pd.read_csv("merged_tweets.csv")

# Filtrer les lignes avec texte lemmatisé non vide
df_valid = df[df["lemmatized_text"].notna() & df["lemmatized_text"].str.strip().ne("")].copy()

# Modèle
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Prédiction
results = []
for text in tqdm(df_valid["lemmatized_text"].astype(str)):
    try:
        output = sentiment_pipeline(text[:512])[0]
        results.append(output)
    except Exception as e:
        results.append({"label": "ERROR", "score": 0.0})

# Ajouter les résultats
df_valid["sentiment_label"] = [r["label"] for r in results]
df_valid["sentiment_score"] = [r["score"] for r in results]

# Fusion avec le DataFrame original
df = df.merge(df_valid[["lemmatized_text", "sentiment_label", "sentiment_score"]], on="lemmatized_text", how="left")

# Export
df.to_csv("sentiment_results.csv", index=False, encoding="utf-8")
print("✅ Sentiment analysis done and saved.")
