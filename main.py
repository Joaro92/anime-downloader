from selenium import webdriver
import yaml
import os
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import *

with open("anime_list.yml", "+r") as yml_file:
    animes = yaml.safe_load(yml_file)

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)

# Open Page
driver.get("https://animetosho.org/")

anime = animes[0]["Solo Leveling"]

# Find Anime
search_box = driver.find_element(By.XPATH, "//input[@placeholder='Search']")
text = anime["group"] + " " + anime["name"]
search_box.send_keys(text)
search_box.send_keys(Keys.ENTER)

# Get List of Episodes
wait.until(visibility_of_element_located((By.XPATH, "//h2[text()='Search Results']")))
search_results = driver.find_elements(By.XPATH, "//div[contains(@class,'home_list_entry')]/div[@class='link']")
episodes_list = [a.text for a in search_results]
episodes_number = []
for episode in episodes_list:
    txt = re.sub(r'\[.*?\]', '', episode)
    txt = txt.replace(anime["name"], '')
    txt = txt.replace("-", '')
    words = txt.split()
    episodes_number.append(words[0])


# Compare against folder
file_list = []
for path in os.listdir(anime["dir"]):
    if os.path.isfile(os.path.join(anime["dir"], path)):
        file_list.append(path)
missing_eps = []
for episode in episodes_list:
    if any([f.startswith(episode) for f in file_list]):
        missing_eps(episode)

# Download the ones that are missing
driver.close()