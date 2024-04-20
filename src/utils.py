import os
import requests
import qbittorrentapi
from time import sleep
from lxml import etree
from urllib.parse import unquote
from random import randrange
from datetime import datetime, timezone
from src.setup import downloaded_episodes, anime_dir, conn_info, args, qbt_client

MAX_SEEK_TIME = 150
MAX_DOWNLOAD_TIME = 30
today = datetime.now(timezone.utc)
EPS = []

def download_torrents(feed):
    # Collect magnet links
    magnets = []
    for entry in feed.entries:
        episode = get_episode_from(entry)
        if not (episode["title"] in downloaded_episodes):
            magnets.append(episode['magnet'])
            print(f"Downloading: '{episode['title']}'")
            EPS.append(episode['title'])

    # Download any torrent that is missing
    if magnets:
        # Pass the links to the qBitTorrent client to download the torrents
        path = anime_dir if conn_info["host"] == "localhost" else args.name
        with qbittorrentapi.Client(**conn_info) as qbt_client:
            if qbt_client.torrents_add(urls=magnets, save_path=path) != "Ok.":
                raise Exception("Failed to add torrent.")
        return True
    return False

def download_file(url, folder_path, filename="rss.xml"):
    full_path = os.path.join(folder_path, filename)
    response = requests.get(url)
    if response.status_code == 200:
        with open(full_path, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception("Failed to download file")
    return full_path

def get_episode_from(entry):
    html = etree.HTML(entry.content.value)
    magnet = html.xpath("//a[text()='Magnet']")[0].get('href')
    nzb_link = html.xpath("//a[text()='NZB']")[0].get('href')
    title = unquote(nzb_link).split('/')[-1].split('.')[0]
    ep = dict(magnet=magnet, title=title)
    return ep

def get_last_publish_date_from(feed):
    return max([entry.published for entry in feed.entries])

def is_from_today(publish_date):
    if os.getenv("SKIP") == "true":
        return True
    time_delta = today - publish_date
    seconds = time_delta.total_seconds()
    return (seconds / 3600) < publish_date.hour

def time_delta_since(date):
    now = datetime.now(timezone.utc)
    time_delta = now - date
    return time_delta.total_seconds()

def seeking():
    return (time_delta_since(today) / 60) < MAX_SEEK_TIME

def downloading(start):
    return (time_delta_since(start) / 60) < MAX_DOWNLOAD_TIME

def wait_until_torrents_download():
    start = datetime.now(timezone.utc)
    downloaded = False
    while downloading(start) and not downloaded:
        sleep(5)
        finished = []
        for torrent in qbt_client.torrents_info():
            # Make sure torrent is from the series
            finished.append(torrent.state == 'stalledUP')
        downloaded = all(finished)

def notify():
    topic = os.getenv("NTFY_TOPIC")
    if topic and EPS:
        text = ""
        EPS.sort()
        for ep in EPS:
            text += f"""-  {ep}
"""
        requests.post(f"https://ntfy.sh/{topic}", data=text.encode(encoding='utf-8'))