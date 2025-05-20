import pandas as pd

# Chargement des datasets
edos = pd.read_csv(r"C:\Users\ULTRABOOK DELL\OneDrive - UPEC\Bureau\Mémoire M2\DataSets\BERT\dataset.csv")

# Harmonisation du dataset edos
edos_harmonized = edos.rename(columns={"language": "langue"}).copy()
edos_harmonized["id"] = ["edos_" + str(i) for i in range(len(edos_harmonized))]
edos_harmonized = edos_harmonized[["id", "text", "label", "langue"]]

edos_harmonized.to_csv("edos_hate_speech.csv", index=False)
