from selenium import webdriver
import yaml
import os
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import *

MAGNETS = []

# Utils
def get_episode_numbers(episode_names):
    episode_numbers = []
    for episode in episode_names:
        txt = re.sub(r'\[.*?\]', '', episode)
        txt = txt.replace(anime["name"], '').replace("-", '')
        words = txt.split()
        for i in range(len(words)):
            if re.match(r'^(S\d{1,2})?E?\d{1,3}$', words[i]):
                episode_numbers.append(words[i])
                break
    
    return episode_numbers

def get_episode_title_from_number(episode_names, ep_number):
    for i, name in enumerate(episode_names):
        txt = re.sub(r'\[.*?\]', '', name)
        txt = txt.replace(anime["name"], '').replace("-", '')
        txt = txt.replace("1080p", '').replace("2160p", '').replace("720p", '')
        txt = txt.replace("x265", '').replace("x264", '').replace("H264", '')
        txt = txt.replace("10bit", '').replace("AV1", '')
        if ep_number in txt:
            return episode_names[i]

# Main
with open("anime_list.yml", "+r") as yml_file:
    animes = yaml.safe_load(yml_file)

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)

anime = animes[0]["Solo Leveling"]

# Open Page
driver.get("https://animetosho.org/")
try:
    # Find Anime
    search_box = driver.find_element(By.XPATH, "//input[@placeholder='Search']")
    text = anime["group"] + " " + anime["name"]
    search_box.send_keys(text)
    search_box.send_keys(Keys.ENTER)

    # Get List of Episodes to Download
    wait.until(visibility_of_element_located((By.XPATH, "//h2[text()='Search Results']")))
    search_results = driver.find_elements(By.XPATH, "//div[contains(@class,'home_list_entry')]/div[@class='link']")
    available_episodes = [a.text for a in search_results]

    # Get List of Episodes already downloaded
    file_list = []
    for path in os.listdir(anime["dir"]):
        if os.path.isfile(os.path.join(anime["dir"], path)):
            file_list.append(path)

    # Compare both lists to get the missing episodes
    torrent_eps = get_episode_numbers(available_episodes)
    local_eps = get_episode_numbers(file_list)
    if torrent_eps:
        missing_eps = list(set(torrent_eps) - set(local_eps))
    else:
        raise Exception("Failed to get the list of episodes")
    
    # Download Torrent for each missing Episode
    for ep in missing_eps:
        title = get_episode_title_from_number(available_episodes, ep)
        driver.find_element(By.XPATH, f"//a[contains(text(),'{title}')]").click()
        wait.until(visibility_of_element_located((By.XPATH, "//a[text()='Magnet Link']")))
        link = driver.find_element(By.XPATH, "//a[text()='Magnet Link']").get_property("href")
        MAGNETS.append(link)
        driver.back()
except Exception as e:
    raise e
finally:
    driver.close()

print("Magnet Links to download:")
for link in MAGNETS:
    print("######")
    print(link)
