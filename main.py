from selenium import webdriver
import yaml
import os
import re
import time
from random import randrange
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

def has_duplicates(nums):
    return len(nums) != len(set(nums))

def random_sleep():
    rng = randrange(0, 600, 1)
    time.sleep(0.222 + (rng / 1000))

# Main
with open("anime_list.yml", "+r") as yml_file:
    animes = yaml.safe_load(yml_file)

random_sleep()
driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)

anime = animes[0][list(animes[0].keys())[0]]

# Open Page
driver.get("https://animetosho.org/")
try:
    # Find Anime
    search_box = driver.find_element(By.XPATH, "//input[@placeholder='Search']")
    text = anime["group"] + " " + anime["name"] + " " + anime["resolution"]
    search_box.send_keys(text)
    search_box.send_keys(Keys.ENTER)

    # Get List of Episodes to Download
    wait.until(visibility_of_element_located((By.XPATH, "//h2[text()='Search Results']")))
    search_results = driver.find_elements(By.XPATH, "//div[contains(@class,'home_list_entry')]//span[contains(@class, 'icon_filesize')]/../../div[@class='link']")
    available_episodes = [a.text for a in search_results]

    # Get simplified list of episodes if possible
    if any(['HEVC' in a for a in available_episodes]):
        print("Found HEVC encoded episodes")
        available_episodes = list(filter(lambda x: 'HEVC' in x.replace(anime["name"], ''), available_episodes))

    # Filter original Season if specified
    if anime.get("season") == 1:
        available_episodes = list(filter(lambda x: 'Season' not in x.replace(anime["name"], ''), available_episodes))

    # Get List of Episodes already downloaded
    file_list = []
    if not os.path.exists(anime["dir"]):
        os.mkdir(anime["dir"])
    for path in os.listdir(anime["dir"]):
        if os.path.isfile(os.path.join(anime["dir"], path)):
            file_list.append(path)

    # Compare both lists to get the missing episodes
    torrent_eps = get_episode_numbers(available_episodes)
    local_eps = get_episode_numbers(file_list)
    if torrent_eps:
        if has_duplicates(torrent_eps):
            raise Exception("Found duplicate episode numbers in the search result")
        missing_eps = list(set(torrent_eps) - set(local_eps))
    else:
        raise Exception("Failed to get the list of episodes")
    
    # Download Torrent for each missing Episode
    for ep in missing_eps:
        title = get_episode_title_from_number(available_episodes, ep)
        element = driver.find_element(By.XPATH, f"//div[@class='link' and contains(normalize-space(),'{title}')]")
        driver.execute_script("arguments[0].scrollIntoView();", element)
        element.click()
        wait.until(visibility_of_element_located((By.XPATH, "//a[text()='Magnet Link']")))
        link = driver.find_element(By.XPATH, "//a[text()='Magnet Link']").get_property("href")
        MAGNETS.append(link)
        driver.back()
        random_sleep()

# except Exception as e:
#     raise e
finally:
    driver.close()

print("Magnet Links to download:")
print("-------------------------")
for link in MAGNETS:
    print(link + "\n")
