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
ballondor_df = pd.read_csv("ballondor_all_ranked.csv")
merged_df = ballondor_df.merge(players_df, on="Player", how="left")

all_stats = []

def save_data(stats, headers):
    """Save stats to CSV."""
    if stats:
        temp_df = pd.DataFrame(stats, columns=headers)
        temp_df.to_csv("player_stats_all_years.csv", mode='a', index=False, header=False)

for idx, row in merged_df.iterrows():
    year = row["Year"]
    player_name = row["Player"]
    player_id = row["PlayerID"]
    url = row["URL"]
    
    # go to website for specific player
    matchlog_url = f"https://fbref.com/en/players/{player_id}/matchlogs/{year - 1}-{year}/{player_name.replace(' ', '-')}-Match-Logs"
    print(f"Fetching URL: {matchlog_url}")
    
    try:
        driver.get(matchlog_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "matchlogs_all")))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table", {"id": "matchlogs_all"})
        if table:
            if 'stats_headers' not in locals():
                headers_row = table.find("thead").find_all("tr")[1]  # Skipping "grouping" row since theyre causing problems
                stats_headers = ["", "Year", "Player"] + [header.get_text() for header in headers_row.find_all("th")] 
                pd.DataFrame(columns=stats_headers).to_csv("player_stats_all_years.csv", index=False)
            
            # we care about the aggregate row on the bottom
            footer = table.find("tfoot")
            if footer:
                agg_row = footer.find("tr")
                data = [td.get_text(strip=True) or None for td in agg_row.find_all("td")]
                
                # added extra col for now, i might remove
                data.insert(0, None)
                data.insert(1, year)
                data.insert(2, player_name)
                
                # padding if needed
                if len(data) < len(stats_headers):
                    data.extend([None] * (len(stats_headers) - len(data)))
                all_stats.append(data)
                save_data([data], stats_headers) #save after each in case it crashes
            else:
                print(f"no footer womp {player_name} ({year})")
        else:
            print(f"womp womp no table {player_name} ({year})")
    except Exception as e:
        print(f"nothing works nice {player_name} ({year}): {e}")
    
    # random wait
    wait_time = random.uniform(5, 15)
    time.sleep(wait_time)

driver.quit()