import pandas as pd

url = 'https://drive.google.com/file/d/19xYEAqI0r1aCKNpVsLza1_NDjBpyhhnP/view?usp=sharing'
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
df = pd.read_csv(path, nrows=20000)
print(df.head(5))