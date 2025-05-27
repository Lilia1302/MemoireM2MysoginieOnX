import pandas as pd
import re

# Fonction de nettoyage du texte
def clean_text(text):
    text = str(text)
    text = re.sub(r"http\S+", "", text)            # Supprimer les URLs
    text = re.sub(r"@\w+", "", text)               # Supprimer les mentions
    text = re.sub(r"#\w+", "", text)               # Supprimer les hashtags
    text = re.sub(r"[^\w\s.,!?]", "", text)        # Supprimer caractères spéciaux sauf ponctuation basique
    text = re.sub(r"\s+", " ", text)               # Réduire les espaces multiples
    return text.strip()

# Charger les 4 fichiers harmonisés
df_metwo = pd.read_csv(r"C:\Users\ULTRABOOK DELL\OneDrive - UPEC\Bureau\Mémoire M2\DataSets\BERT\fineTunning\cleanedDatasets\MeTwoText_clean.csv")
df_spanish = pd.read_csv(r"C:\Users\ULTRABOOK DELL\OneDrive - UPEC\Bureau\Mémoire M2\DataSets\BERT\fineTunning\cleanedDatasets\clean_spanish_hate_speech.csv")
df_fr_hf = pd.read_csv(r"C:\Users\ULTRABOOK DELL\OneDrive - UPEC\Bureau\Mémoire M2\DataSets\BERT\fineTunning\cleanedDatasets\clean_french_hate_speech.csv")
df_edos = pd.read_csv(r"C:\Users\ULTRABOOK DELL\OneDrive - UPEC\Bureau\Mémoire M2\DataSets\BERT\fineTunning\cleanedDatasets\edos_hate_speech.csv")

# Vérification : ils doivent tous avoir les colonnes ['text', 'label', 'langue']
colonnes_attendues = ["text", "label", "langue"]
for name, df in zip(["MeToo", "Spanish", "fr_hf", "EDOS"], [df_metwo, df_spanish, df_fr_hf, df_edos]):
    if not all(col in df.columns for col in colonnes_attendues):
        raise ValueError(f"Le dataset {name} ne contient pas toutes les colonnes requises : {colonnes_attendues}")

# Concaténer les datasets
df_total = pd.concat([df_metwo, df_spanish, df_fr_hf, df_edos], ignore_index=True)

# Nettoyer les textes
df_total["text"] = df_total["text"].apply(clean_text)

# Sauvegarder dans un fichier CSV
df_total.to_csv("dataset_total_harmonised.csv", index=False)
print("✅ Fusion et nettoyage terminés : dataset_total_harmonised.csv")
