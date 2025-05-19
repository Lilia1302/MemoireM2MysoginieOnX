import pandas as pd

df_lamanada = pd.read_csv("LaManada/results/tweets_avec_lemmas.csv")
df_mazan = pd.read_csv("Mazan/results/tweets_avec_lemmas.csv")

#select the columns that we want to keep
df_lamanada = df_lamanada[["cleaned_text", "lemmatized_text", "created_at", "username", "location"]]
df_mazan = df_mazan[["cleaned_text", "lemmatized_text", "date", "user_username"]]

#Harmonize the columns
df_mazan = df_mazan.rename(columns={
    "date": "created_at",
    "user_username": "username"
})


df_mazan["location"] = None

#add a 'case' column
df_lamanada["case"] = "LaManada"
df_mazan["case"] = "Mazan"

#combine both files
df_combined = pd.concat([df_lamanada, df_mazan], ignore_index=True)

df_combined.to_csv("merged_tweets.csv", index=False, encoding="utf-8")

print("Merged dataset created ")
