import pandas as pd

df = pd.read_parquet('./data/data.parquet')
df.reset_index(drop=True, inplace=True)
print(df.info())
print(df.head())
df.to_csv('./data/data.csv', index=False)