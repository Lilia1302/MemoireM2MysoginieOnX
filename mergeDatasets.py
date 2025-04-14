import pandas as pd

# 🔹 Charger les datasets
df_lamanada = pd.read_csv("LaManada/results/tweets_avec_lemmas.csv")
df_mazan = pd.read_csv("Mazan/results/tweets_avec_lemmas.csv")

# 🔁 Sélection et renommage des colonnes
df_lamanada = df_lamanada[["cleaned_text", "lemmatized_text", "created_at", "username", "location"]]
df_mazan = df_mazan[["cleaned_text", "lemmatized_text", "date", "user_username"]]

# Harmoniser les noms de colonnes
df_mazan = df_mazan.rename(columns={
    "date": "created_at",
    "user_username": "username"
})

# ➕ Ajouter colonne "location" vide pour Mazan
df_mazan["location"] = None

# ➕ Ajouter colonne "case"
df_lamanada["case"] = "LaManada"
df_mazan["case"] = "Mazan"

# 🔗 Fusion
df_combined = pd.concat([df_lamanada, df_mazan], ignore_index=True)

# 💾 Sauvegarder
df_combined.to_csv("merged_tweets.csv", index=False, encoding="utf-8")

print("✅ Merged dataset created with shape:", df_combined.shape)
