#Simple script to download all districts 
#Author: Chris Cummings
#License: MIT

import requests
import os
import shutil
import json
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

#Date to download
MAP_DATE = "2022-05-01"

#Latest download url
MAP_URL = f"https://devblobs.shapevrcloud.com/infiniverse/public/{MAP_DATE}/map.json"

#data dir
DATA_DIR = os.path.abspath(f"data/{MAP_DATE}")

count = 0
num_districts = 0

#function to do a download
def download_district(district):
    global count
    district_rsp = requests.get(district['url'])
    if len(district_rsp.content) == 0:
        print("WHAT")
    with open(f"{DATA_DIR}/{district['code']}.json","wb") as f:
        f.write(district_rsp.content)

def done(arg):
    global count
    global num_districts
    count += 1
    print(f"Downloaded {count}/{num_districts}")

def main():
    global count 
    global num_districts

    #clear data
    if os.path.exists(DATA_DIR):
        shutil.rmtree(DATA_DIR, ignore_errors=True)
    os.makedirs(DATA_DIR)

    #download map
    map_rsp = requests.get(MAP_URL)
    map_text = map_rsp.text
    with open(f"{DATA_DIR}/map.json","w") as f:
        f.write(map_text)

    #load map 
    map_data = json.loads(map_text)

    #init counters
    num_districts = len(map_data['districts'])
    count = 0

    #async download districts
    with ThreadPoolExecutor(max_workers=128) as executor:
        for district in map_data['districts']:
            executor.submit(download_district, district).add_done_callback(done)
    #for district in map_data['districts']:
    #    download_district(district)
    #    done(None)

if __name__ == '__main__':
    main()