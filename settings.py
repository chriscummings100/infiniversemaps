import os 
import json 

#core settings used by all scripts

#----------------------------------------------------------------------
#Configurable settings
#----------------------------------------------------------------------

#Base url for infiniverse server data
CDN_URL = "https://devblobs.shapevrcloud.com/infiniverse/public"

#Date of map data to load
MAP_DATE = None

#read version text
if os.path.exists("data/version.txt"):
    with open("data/version.txt") as f:
        MAP_DATE = f.readline()

#----------------------------------------------------------------------
#Derived constants
#----------------------------------------------------------------------
MAP_URL = ""
DATA_DIR = ""
MAP_PATH = ""
MAP = { 'districts': [] }

def init():
    global MAP_URL
    global DATA_DIR
    global MAP_PATH
    global MAP

    if MAP_DATE:
        #setup derived properties from map date
        MAP_URL = f"{CDN_URL}/{MAP_DATE}/map.json"
        DATA_DIR = os.path.abspath(f"data/{MAP_DATE}")
        MAP_PATH = f"{DATA_DIR}/map.json"

        #always try to load the map from disk or set to default value if doesn't exist
        try:
            if os.path.exists(MAP_PATH):
                with open (f"{DATA_DIR}/map.json","rb") as f:
                    MAP = json.load(f)
        except Exception as err:
            print(err)

init()



