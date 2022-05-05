#Simple script to download all districts 
#Author: Chris Cummings
#License: MIT

import requests
import os
import shutil
import json
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

count = 0
num_districts = 0

#function to do a download
def download_district(district, data_dir):
    global count
    district_rsp = requests.get(district['url'])
    with open(f"{data_dir}/{district['code']}.json","wb") as f:
        f.write(district_rsp.content)

def done(arg):
    global count
    global num_districts
    count += 1
    print(f"Downloaded {count}/{num_districts}")

def run(cdn_url):
    global count 
    global num_districts

    #download
    latest_rsp = requests.get(f"{cdn_url}/latest.txt")
    latest = latest_rsp.text.splitlines()[0]

    #choose data dir
    data_dir = f"data/{latest}"

    #clear data
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir, ignore_errors=True)
    os.makedirs(data_dir)

    #download map
    map_rsp = requests.get(f"{cdn_url}/{latest}/map.json")
    map_text = map_rsp.text
    with open(f"{data_dir}/map.json","w") as f:
        f.write(map_text)

    #load map 
    map_data = json.loads(map_text)

    #init counters
    num_districts = len(map_data['districts'])
    count = 0

    #async download districts
    with ThreadPoolExecutor(max_workers=128) as executor:
        for district in map_data['districts']:
            executor.submit(download_district, district, data_dir).add_done_callback(done)
    #for district in map_data['districts']:
    #    download_district(district)
    #    done(None)

    with open(f"data/version.txt","wt") as f:
        f.write(latest)
