import pandas as pd

pre2018 = pd.read_csv("final_pre2018_combined_stats.csv")
post2018 = pd.read_csv("final_post2018_combined_stats.csv")

# add missing columns from pre 2018 w value of 0
for col in ['xG', 'xAG', 'SCA', 'GCA']:
    pre2018[col] = 0

# since these are both similar, we proxy them by combining them.
pre2018 = pre2018.rename(columns={'TklW': 'Tkl'})

# ensure columns aligned + add
pre2018 = pre2018[post2018.columns] 
combined_data = pd.concat([pre2018, post2018], ignore_index=True)
combined_data.to_csv("final_combined_stats.csv", index=False)