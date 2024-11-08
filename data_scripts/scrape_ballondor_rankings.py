import requests
from bs4 import BeautifulSoup
import pandas as pd

start_year = 1998
end_year = 2024

years = []
ranks = []
players = []

for year in range(start_year, end_year + 1):
    if year == 2020: # no ballondor this year
        continue
    if 2010 <= year <= 2015: # special case
        url = f'https://en.wikipedia.org/wiki/{year}_FIFA_Ballon_d%27Or'
    else:
        url = f'https://en.wikipedia.org/wiki/{year}_Ballon_d%27Or'
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"error cant retrieve {year}")
        continue
    soup = BeautifulSoup(response.text, 'html.parser')
    
    #wikitable
    tables = soup.find_all('table', {'class': 'wikitable'})
    
    # parse rows
    for table in tables:
        for row in table.find_all('tr')[1:]:  # skip header
            cells = row.find_all('td')
            
            # check min length
            if len(cells) >= 2:
                rank = cells[0].text.strip()  # first col is rank
                player = cells[1].text.strip()  # second col is player

                # check
                if rank.isdigit() and "%" not in player:
                    years.append(year)
                    ranks.append(rank)
                    players.append(player)

df = pd.DataFrame({
    'Year': years,
    'Rank': ranks,
    'Player': players
})

df.to_csv('ballondor_all_ranked.csv', index=False)
