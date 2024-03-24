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
```
## Setup Anime Catalog

Create a file in this folder called `anime_list.yml`

This file uses YAML syntax.

Create an Anime Proyect adding the item name, it will require the following properties:

### *It will currently work with just the first anime on the list*

1. group: Name of the Release Group
2. name: Exact name of the anime to download, it is recommended that you do the search first manually to confirm the naming used
3. resolution: Horizontal resolution of the encoded videos, e.g: 1080p
4. dir: Path to the folder you want this anime to be stored in your PC. It will create the folder if it doesn't exists
5. (optional) season: Set this value to 1 if you want to download exclusively the first season of the show. If you want other seasons, add the necessary words in the name of the anime to filter the search, like "2nd Season"

---

### Example anime_list.yml:
```
- Mashle original:
    group: Erai-Raws
    name: Mashle
    resolution: 1080p
    dir: D:/MagicStorage/Anime/Mashle/
    season: 1
```