#Read all store fronts and dump to CSV
#Author: Chris Cummings
#License: MIT

import sys
import json
import os

#Date to download
MAP_DATE = "2022-05-01"
DATA_DIR = os.path.abspath(f"data/{MAP_DATE}")

#load map file
with open (f"{DATA_DIR}/map.json","rb") as f:
    MAP = json.load(f)

#json for a storefront slot
#    {
#      "code": "S2-W3-19-0-65538",
#      "cellx": 2147483644,
#      "celly": 2147483645,
#      "subdistrictid": 19,
#      "buildingid": 0,
#      "slot": 65538,
#      "owner": "OllyR-FTL",
#      "location": "1 Mink Mews",
#      "domain": "OllyR-FTL",
#      "iconurl": ""
#      "destination": ""
#    },

COLUMNS = ['code','owner','domain','location','destination','iconurl']

#Output CSV
with open("stores.csv","wt") as outf:
    txt = ','.join(COLUMNS) 
    outf.write(txt + "\n")
    for district_record in MAP['districts']:
        with open(f"{DATA_DIR}/{district_record['code']}.json","rb") as f:
            district = json.load(f)
            for slot in district['slots']:
                if slot['slot'] == 65538:  #65538 is the magic number for a store!
                    txt = ",".join([slot.get(x,"") for x in COLUMNS])
                    outf.write(txt + "\n")

#Dirty copy and paste to generate TABSV instead
with open("stores.tab","wt") as outf:
    txt = '\t'.join(COLUMNS) 
    outf.write(txt + "\n")
    for district_record in MAP['districts']:
        with open(f"{DATA_DIR}/{district_record['code']}.json","rb") as f:
            district = json.load(f)
            for slot in district['slots']:
                if slot['slot'] == 65538:  #65538 is the magic number for a store!
                    txt = "\t".join([slot.get(x,"") for x in COLUMNS])
                    outf.write(txt + "\n")
