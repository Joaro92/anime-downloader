import argparse
import os
import qbittorrentapi

# Python parser Setup
parser = argparse.ArgumentParser(description='Homemade Anime Downloader.')
parser.add_argument('name', help="Folder name that will be used to download the files")
parser.add_argument('aniID', help="AniDB ID to search specifically the correct season")
parser.add_argument('group', help="Release Group that provide the subtitles")
parser.add_argument('--HEVC', action='store_const', dest='encoding', const=' HEVC', default='',
                    help='Filter episodes by HEVC Encoding')
group = parser.add_mutually_exclusive_group()
group.add_argument('--480p', action='store_const', dest='resolution', const=' 480p', default='',
                    help='Filter episodes by 480p resolution')
group.add_argument('--720p', action='store_const', dest='resolution', const=' 720p', default='',
                    help='Filter episodes by 720p resolution')
group.add_argument('--1080p', action='store_const', dest='resolution', const=' 1080p', default='',
                    help='Filter episodes by 1080p resolution')

args = parser.parse_args()

# qBitTorrent Setup
conn_info = dict(
    host = "localhost" if not os.getenv("QBITTORRENT_IP") else os.getenv("QBITTORRENT_IP"),
    port = 8080 if not os.getenv("QBITTORRENT_PORT") else os.getenv("QBITTORRENT_PORT"),
    username = "admin" if not os.getenv("QBITTORRENT_USER") else os.getenv("QBITTORRENT_USER"),
    password = os.getenv("QBITTORRENT_PASS"),
)
qbt_client = qbittorrentapi.Client(**conn_info)
try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)

# Path Folder Setup
main_path = os.getenv("DOWNLOAD_FOLDER")
if not os.path.isdir(main_path):
    raise f"'{main_path}' is not a valid destination folder. Set the DOWNLOAD_FOLDER env variable correctly"
anime_dir = os.path.join(main_path, args.name)
if not os.path.exists(anime_dir):
    os.mkdir(anime_dir)

# Read Downloaded Episodes
downloaded_episodes = []
for path in os.listdir(anime_dir):
    if not (".xml" in path or ".nfo" in path) and os.path.isfile(os.path.join(anime_dir, path)):
        downloaded_episodes.append(path.split('.')[0])