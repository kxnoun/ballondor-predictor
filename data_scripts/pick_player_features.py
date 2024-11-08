import pandas as pd

# Pre 2018
df = pd.read_csv('pre_2018.csv')
important_features = ["Year", "Player", "Result", "Min", "Gls", "Ast", "PK", "Sh", "SoT", "CrdY", "CrdR", "Int", "TklW"]
df_filtered = df[important_features]
df_filtered.to_csv('pre_2018_cleaned.csv', index=False)

# Post 2018
df = pd.read_csv('post_2018.csv')
important_features = [
    'Year', 'Player', 'Result', 'Min', 'Gls', 'Ast', 'PK', 'Sh', 'SoT', 'CrdY', 'CrdR', 'Int', 'Tkl', 
    'xG', 'xAG', 'SCA', 'GCA'
]

df_filtered = df[important_features]
df_filtered.to_csv('post_2018_cleaned.csv', index=False)