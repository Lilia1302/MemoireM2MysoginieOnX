import pandas as pd

# Chargement du fichier annoté automatiquement
df = pd.read_csv("sentiment_results.csv")

# Filtrage strict par valeur de la colonne 'case'
manada_df = df[df["case"] == "LaManada"]
mazan_df = df[df["case"] == "Mazan"]

# Vérification des quantités disponibles
print("Tweets LaManada disponibles :", len(manada_df))
print("Tweets Mazan disponibles :", len(mazan_df))

# Prélèvement aléatoire de 300 tweets dans chaque cas (ou moins si pas assez)
sample_manada = manada_df.sample(n=min(300, len(manada_df)), random_state=42)
sample_mazan = mazan_df.sample(n=min(300, len(mazan_df)), random_state=42)

# Fusion des échantillons
sample_df = pd.concat([sample_manada, sample_mazan]).reset_index(drop=True)

# Ajout d'une colonne vide pour l'annotation manuelle
sample_df["misogyny_label"] = ""

# Sauvegarde du fichier prêt à être annoté
sample_df.to_csv("sample_to_annotate.csv", index=False, sep=';')

print("Fichier 'tweets_a_annoter.csv' généré avec succès.")
