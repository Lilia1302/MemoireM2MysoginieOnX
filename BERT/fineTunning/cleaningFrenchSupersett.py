import pandas as pd

# Charger le dataset
df =pd.read_csv(
    r"C:\Users\ULTRABOOK DELL\OneDrive - UPEC\Bureau\Mémoire M2\DataSets\BERT\fr_hf.csv")

fr_hf_filtered = df[df["target"] == "women"].copy()
fr_hf_filtered["label"] = fr_hf_filtered["labels"]
fr_hf_filtered["langue"] = "fr"
fr_hf_harmonized = fr_hf_filtered[["text", "label", "langue"]].copy()
fr_hf_harmonized["id"] = ["frhf_" + str(i) for i in range(len(fr_hf_harmonized))]
fr_hf_harmonized = fr_hf_harmonized[["id", "text", "label", "langue"]]

fr_hf_harmonized.to_csv("clean_french_hate_speech.csv", index=False)
