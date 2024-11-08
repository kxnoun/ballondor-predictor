import pandas as pd
import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-software-rasterizer")


driver = webdriver.Chrome()
driver.get("https://www.google.com/")
players_df = pd.read_csv("players_with_urls_and_ids.csv")
ballondor_df = pd.read_csv("post_2018_cleanedv2.csv") # CHANGE TO PRE_2018 FOR gk stats before 2018

merged_df = ballondor_df.merge(players_df, on="Player", how="left")

keeper_stats = []
general_stats = []

def save_data(stats, headers, filename):
    """Save stats to CSV."""
    if stats:
        temp_df = pd.DataFrame(stats, columns=headers)
        temp_df.to_csv(filename, mode='a', index=False, header=False)

for idx, row in merged_df.iterrows():
    if row["is_goalkeeper"] == 1:  # only process gk
        year = row["Year"]
        player_name = row["Player"]
        player_id = row["PlayerID"]
        
        # get URLS for both regular player data for gk and GK specific data.
        keeper_url = f"https://fbref.com/en/players/{player_id}/matchlogs/{year - 1}-{year}/keeper/{player_name.replace(' ', '-')}-Match-Logs"
        general_url = f"https://fbref.com/en/players/{player_id}/matchlogs/{year - 1}-{year}/summary/{player_name.replace(' ', '-')}-Match-Logs"
        
        try:
            driver.get(keeper_url) # first we start with gk specific stats
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "matchlogs_all")))
            soup = BeautifulSoup(driver.page_source, "html.parser")
            table = soup.find("table", {"id": "matchlogs_all"})
            if table:
                if 'keeper_headers' not in locals():
                    headers_row = table.find("thead").find_all("tr")[1]
                    keeper_headers = ["", "Year", "Player"] + [header.get_text() for header in headers_row.find_all("th")]
                    pd.DataFrame(columns=keeper_headers).to_csv("keeper_stats_post2018.csv", index=False)
                
                footer = table.find("tfoot")
                if footer:
                    agg_row = footer.find("tr")
                    data = [td.get_text(strip=True) or None for td in agg_row.find_all("td")]
                    data.insert(0, None)  # empty col
                    data.insert(1, year)
                    data.insert(2, player_name)
                    if len(data) < len(keeper_headers):
                        data.extend([None] * (len(keeper_headers) - len(data)))
                    keeper_stats.append(data)
                    save_data([data], keeper_headers, "keeper_stats_post2018.csv") # change to pre2018 if wanted
                else:
                    print(f"womp womp no keeper footer {player_name} ({year})")

            # now we do general stats
            driver.get(general_url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "matchlogs_all")))
            soup = BeautifulSoup(driver.page_source, "html.parser")
            table = soup.find("table", {"id": "matchlogs_all"})
            if table:
                if 'general_headers' not in locals():
                    headers_row = table.find("thead").find_all("tr")[1]
                    general_headers = ["", "Year", "Player"] + [header.get_text() for header in headers_row.find_all("th")]
                    pd.DataFrame(columns=general_headers).to_csv("general_stats_post2018.csv", index=False)
                
                footer = table.find("tfoot")
                if footer:
                    agg_row = footer.find("tr")
                    data = [td.get_text(strip=True) or None for td in agg_row.find_all("td")]
                    data.insert(0, None)  # empty col again
                    data.insert(1, year)
                    data.insert(2, player_name)
                    if len(data) < len(general_headers):
                        data.extend([None] * (len(general_headers) - len(data)))
                    general_stats.append(data)
                    save_data([data], general_headers, "general_stats_post2018.csv") # change to pre2018 if wanted
                else:
                    print(f"womp womp no general footer {player_name} ({year})")
        
        except Exception as e:
            print(f"womp womp nothing works {player_name} ({year}): {e}")
        
        wait_time = random.uniform(5, 15)
        time.sleep(wait_time)

driver.quit()