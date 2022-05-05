import os 
import json 
import requests
import downloader

#core settings used by all scripts

#----------------------------------------------------------------------
#Configurable settings
#----------------------------------------------------------------------

#Base url for infiniverse server data
CDN_URL = "https://devblobs.shapevrcloud.com/infiniverse/public"

#Date of map data to load
MAP_DATE = None

#Download latest version info
LATEST = requests.get(f"{CDN_URL}/latest.txt").text.splitlines()[0]

#read version text
if os.path.exists("data/version.txt"):
    with open("data/version.txt") as f:
        MAP_DATE = f.readline()

#check for mismatch that requires download
if MAP_DATE != LATEST:
    downloader.run(CDN_URL)

#----------------------------------------------------------------------
#Derived constants
#----------------------------------------------------------------------

#setup derived properties from map date
DATA_DIR = os.path.abspath(f"data/{MAP_DATE}")

#always try to load the map from disk or set to default value if doesn't exist
MAP = { 'districts': [] }
try:
    map_path = f"{DATA_DIR}/map.json"
    if os.path.exists(map_path):
        with open (map_path,"rb") as f:
            MAP = json.load(f)
except Exception as err:
    print(err)




