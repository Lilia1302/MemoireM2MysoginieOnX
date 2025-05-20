import pandas as pd

df = pd.read_csv(
    r"C:\Users\ULTRABOOK DELL\OneDrive - UPEC\Bureau\Mémoire M2\DataSets\BERT\es_hf_102024.csv")
df = df[["text", "labels"]]

# Renommer les colonnes
df = df.rename(columns={"labels": "label"})

# Ajouter la langue
df["langue"] = "es"

# Sauvegarder
df.to_csv("clean_spanish_hate_speech.csv", index=False)