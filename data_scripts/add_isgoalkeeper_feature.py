import pandas as pd
# HERE WE ADD GK LABELS

# currently pre2018 and post2018 are seperate due to differences in data columns (post 2018 has more descriptive data)

# Pre 2018
data = pd.read_csv('pre_2018_cleaned.csv')

gk_names = [
    "Manuel Neuer", "Gianluigi Buffon", "Dida", "Fabien Barthez",
    "Francesco Toldo", "Iker Casillas", "Jens Lehmann", "Oliver Kahn",
    "Petr Čech", "Rui Patrício"
]

data['is_gk'] = data['Player'].apply(lambda x: 1 if x in gk_names else 0)
data.to_csv('pre_2018_cleanedv2.csv', index=False)

# Post 2018
data = pd.read_csv('post_2018_cleaned.csv')
gkeeper_names = [
    "Alisson", "Emiliano Martínez", "Gianluigi Donnarumma", "Thibaut Courtois", "Yassine Bounou"
]
data['is_goalkeeper'] = data['Player'].apply(lambda x: 1 if x in gkeeper_names else 0)
data.to_csv('post_2018_cleanedv2.csv', index=False)