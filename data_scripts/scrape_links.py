import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

# load players, make sure unique since you have duplicates from diff years
ballondor_players = pd.read_csv("ballondor_all_ranked.csv")
unique_players = ballondor_players["Player"].unique()

player_data = {}

for player_name in unique_players:
    # use google
    query = f"site:fbref.com {player_name} \"Match Logs\""
    g_url = f"https://www.google.com/search?q={query}"
    
    print(f"search url: {g_url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    }
    response = requests.get(g_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # find links
        found_fbref_link = False
        for link in soup.find_all("a", href=True):
            href = link["href"]
            # look for specific link style
            if "fbref.com/en/players" in href:
                p_url = href
                p_id = p_url.split("/")[4]
                # save
                player_data[player_name] = {
                    "PlayerID": p_id,
                    "URL": p_url
                }
                found_fbref_link = True
                break
        
        if not found_fbref_link:
            print("cant find")
    else:
        print(f"womp womp status: {response.status_code})")
    
    # add delay bc rate limiter... prolly have to make it random lol
    # lets see if this even works
    time.sleep(2)

df = pd.DataFrame.from_dict(player_data, orient="index")
df.to_csv("ballondor_player_ids.csv", index_label="Player")
