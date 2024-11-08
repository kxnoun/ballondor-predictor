import pandas as pd
from sklearn.impute import SimpleImputer

data = pd.read_csv("final_combined_stats.csv")

# fix data issue with numbers (3,624) -> (3624)
data['Min'] = data['Min'].replace(',', '', regex=True).astype(float)

# impute using mean first
key_cols = ['Min', 'Gls', 'Ast', 'SoT']
mean_imputer = SimpleImputer(strategy='mean')
data[key_cols] = mean_imputer.fit_transform(data[key_cols])

# MAKE SOME PROXIES!
pre_2018_mask = data['Year'] < 2018

#xG, basically number of goals per 90 mins.
data.loc[pre_2018_mask, 'xG'] = (data.loc[pre_2018_mask, 'Gls'] / data.loc[pre_2018_mask, 'Min']) * 90
#xAG, basically number of assists per 90 mins
data.loc[pre_2018_mask, 'xAG'] = (data.loc[pre_2018_mask, 'Ast'] / data.loc[pre_2018_mask, 'Min']) * 90
#SCA basically the number of shots on target every 90 mins
data.loc[pre_2018_mask, 'SCA'] = (data.loc[pre_2018_mask, 'SoT'] / data.loc[pre_2018_mask, 'Min']) * 90
#GCA, goal creating chances, thats basically assists...kinda
data.loc[pre_2018_mask, 'GCA'] = data.loc[pre_2018_mask, 'Ast']

# for goalkeepers, we use median, just better imo.
goalkeepers = data[data['is_goalkeeper'] == 1]
median_values = goalkeepers[['SoTA', 'GA', 'Saves', 'Save%']].median()

# and the median vals need to be used for only gk players, dont count the 0s from outfield players.
for col in ['SoTA', 'GA', 'Saves', 'Save%']:
    data.loc[(data['is_goalkeeper'] == 1) & (data[col].isna()), col] = median_values[col]

zero_cols = ['CrdY', 'CrdR', 'CS', 'is_goalkeeper']
mode_cols = ['Result']
data[zero_cols] = data[zero_cols].fillna(0)

# mode for category here.
mode_imputer = SimpleImputer(strategy='most_frequent')
data[mode_cols] = mode_imputer.fit_transform(data[mode_cols])

# final dataset, almost.
data.to_csv("final_combined_imputed_with_proxies.csv", index=False)

rankings = pd.read_csv("ballondor_all_ranked.csv")
final_data = pd.merge(data, rankings, on=['Year', 'Player'], how='left')

# final dataset!
final_data.to_csv("final_combined_with_labels.csv", index=False)