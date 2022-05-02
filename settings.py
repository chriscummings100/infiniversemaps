import os 
import json 

#core settings used by all scripts

#----------------------------------------------------------------------
#Configurable settings
#----------------------------------------------------------------------

#Base url for infiniverse server data
CDN_URL = "https://devblobs.shapevrcloud.com/infiniverse/public"

#Date of map data to load
MAP_DATE = "2022-05-01"

#----------------------------------------------------------------------
#Derived constants
#----------------------------------------------------------------------
MAP_URL = f"{CDN_URL}/{MAP_DATE}/map.json"
DATA_DIR = os.path.abspath(f"data/{MAP_DATE}")

MAP_PATH = f"{DATA_DIR}/map.json"

#always try to load the map from disk or set to default value if doesn't exist
if os.path.exists(MAP_PATH):
    with open (f"{DATA_DIR}/map.json","rb") as f:
        MAP = json.load(f)
else:
    MAP = { 'districts': [] }
