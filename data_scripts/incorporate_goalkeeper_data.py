import pandas as pd

# This file takes the scraped gk data, picks the relevant features from post and pre 2018
# keeping both the important general player data AND specific goalkeeper data
# then we add them to our general player list of stats for pre and post 2018.

# PRE 2018 DATA

general_stats = pd.read_csv("general_stats_pre2018.csv")
cleaned_data = pd.read_csv("pre_2018_cleanedv2.csv")
keeper_stats = pd.read_csv("keeper_stats_pre2018.csv")

general_columns_to_keep = ["Year", "Player", "Result", "Min", "Gls", "Ast", "PK", "Sh", "SoT", "CrdY", "CrdR", "Int", "TklW"]
keeper_columns_to_keep = [
    'Year', 'Player', 'SoTA', 'GA', 'Saves', 'Save%', 'CS'
]
general_stats = general_stats[general_columns_to_keep]
keeper_stats = keeper_stats[keeper_columns_to_keep]
merged_stats = general_stats.merge(keeper_stats, on=['Year', 'Player'], how='left')

merged_data = pd.merge(cleaned_data, keeper_stats[['Year', 'Player', 'SoTA', 'GA', 'Saves', 'Save%', 'CS']], on=['Year', 'Player'], how='left')

goalkeeper_features = ['SoTA', 'GA', 'Saves', 'Save%', 'CS']
merged_data[goalkeeper_features] = merged_data[goalkeeper_features].fillna(0)

columns = [col for col in merged_data.columns if col != 'is_goalkeeper'] + ['is_goalkeeper']
merged_data = merged_data[columns]

merged_data.to_csv("final_pre2018_combined_stats.csv", index=False)


# POST 2018 DATA
general_stats = pd.read_csv("general_stats_post2018.csv")
keeper_stats = pd.read_csv("keeper_stats_post2018.csv")
cleaned_data = pd.read_csv("post_2018_cleanedv2.csv")

general_columns_to_keep = [
    'Year', 'Player', 'Result', 'Min', 'Gls', 'Ast', 'PK', 'Sh', 'SoT', 'CrdY', 'CrdR', 'Int', 'Tkl', 
    'xG', 'xAG', 'SCA', 'GCA'
]

keeper_columns_to_keep = [
    'Year', 'Player', 'SoTA', 'GA', 'Saves', 'Save%', 'CS'
]

# filter
general_stats = general_stats[general_columns_to_keep]
keeper_stats = keeper_stats[keeper_columns_to_keep]

merged_stats = general_stats.merge(keeper_stats, on=['Year', 'Player'], how='left')

# merge with the clean data
merged_data = pd.merge(cleaned_data, merged_stats[['Year', 'Player', 'SoTA', 'GA', 'Saves', 'Save%', 'CS']], on=['Year', 'Player'], how='left')
goalkeeper_features = ['SoTA', 'GA', 'Saves', 'Save%', 'CS']
merged_data[goalkeeper_features] = merged_data[goalkeeper_features].fillna(0)
# reorder
columns = [col for col in merged_data.columns if col != 'is_goalkeeper'] + ['is_goalkeeper']
#merge
merged_data = merged_data[columns]
merged_data.to_csv("final_post2018_combined_stats.csv", index=False)

