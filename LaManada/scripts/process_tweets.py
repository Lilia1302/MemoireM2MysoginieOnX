import json
import pandas as pd

with open("tweets_twikit_multi_periods.json", encoding="utf-8") as f:
    data = [json.loads(line) for line in f]

#create a DataFrame with pandas
df = pd.DataFrame(data)

#transform into csv
df.to_csv("tweets_lamanada.csv", index=False, encoding="utf-8")
