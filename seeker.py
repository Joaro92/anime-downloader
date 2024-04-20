import atoma
from time import sleep
from src.utils import *
from src.setup import args, qbt_client, anime_dir

# Download RSS Feed
url = f"https://feed.animetosho.org/atom?q={args.group}&aids={args.aniID}"
atom_file = download_file(url, anime_dir)
feed = atoma.parse_atom_file(atom_file)

# Download any not present episode
download_torrents(feed)

# Find if seek mode is required
last_published = get_last_publish_date_from(feed)
if not is_from_today(last_published):
    downloaded = False
    while seeking() and not downloaded:
        sleep(120)
        atom_file = download_file(url, anime_dir)
        feed = atoma.parse_atom_file(atom_file)
        downloaded = download_torrents(feed)

# Wait for all torrents to finish downloading
wait_until_torrents_download()

# Logout of qBitTorrent client
qbt_client.auth_log_out()

# Notify user
notify()