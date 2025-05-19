import pandas as pd

# Charger le fichier (détection automatique du séparateur)
metwo = pd.read_csv(
    r"C:\Users\ULTRABOOK DELL\OneDrive - UPEC\Bureau\Mémoire M2\DataSets\BERT\MeTwoText.csv",
    sep=None, engine="python"
)

# Renommer les colonnes utiles
metwo_clean = metwo.rename(columns={
    "status_id": "id",
    "categoria": "label"
})

# Binariser la colonne label : SEXISM = 1, NO-SEXISM et DOUBTFUL = 0
metwo_clean["label"] = metwo_clean["label"].apply(lambda x: 1 if x == "SEXISM" else 0)

# Ajouter la colonne "langue"
metwo_clean["langue"] = "es"

# Garder uniquement les colonnes souhaitées
metwo_clean = metwo_clean[["id", "text", "label", "langue"]]

# Sauvegarder le fichier nettoyé
metwo_clean.to_csv("MeTwoText_clean.csv", index=False, encoding="utf-8")

print("✅ Dataset MeTwo nettoyé, label binarisé, et sauvegardé sous 'MeTwoText_clean.csv'")
