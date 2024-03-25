# anime-downloader

## How to use

For first time users, Install dependencies with the following command:
`pip install -r requirements.txt`

This application utilizes the 'animetosho.org' site to retrieve the .torrent links

To make this work, it is necessary to specify as much as possible on the search results to avoid 'duplicates' of the same episode, it will fail otherwise.

## Setup environment

You will need to set as environment variables the connection strings to connect to your qBitTorrent Client.

These are the necessary environment variables to set:
```
 - QBITTORRENT_IP: Defaults as 'localhost' if you are running the bitTorrent Client in the same PC
 - QBITTORRENT_PORT: Defaults as 8080
 - QBITTORRENT_USER: Username to connect to the bitTorrent client
 - QBITTORRENT_PASS: Password used by the previous username
 - DOWNLOAD_FOLDER: Main Directory to download all the animes, it will create a folder by the title name in the yaml file. *WARNING: Try not to use any special characters that are no allowed as folder's names*
```

In case of connecting to an external qBitTorrent Client, please set up the default download folder the same as the environment variable on your client's configuration. Then, it will try to create the folders for each series following this path.

### GUIDE: Setup Environment Variables in PowerShell

```https://www.tutorialspoint.com/how-to-set-environment-variables-using-powershell```

## Python Arguments

You can pass ```--headless``` to the end of the python command in your terminal console to enable Headless Browser searching

To execute the python script you can run:
```
python main.py
```
Or in Headless mode with:
```
python main.py --headless
```

## Setup Anime Catalog

Create a file in this folder called `anime_list.yml`

This file uses YAML syntax.

Create an Anime Proyect adding the item name, it will require the following properties:

### *It will currently work with just the first anime on the list*

1. group: Name of the Release Group
2. name: Exact name of the anime to download, it is recommended that you do the search first manually to confirm the naming used
3. resolution: Horizontal resolution of the encoded videos, e.g: 1080p
4. (optional) season: Set this value to 1 if you want to download exclusively the first season of the show. If you want other seasons, add the necessary words in the name of the anime to filter the search, like "2nd Season"

---

### Example anime_list.yml:
```
- Mashle original:
    group: Erai-Raws
    name: Mashle
    resolution: 1080p
    season: 1
```