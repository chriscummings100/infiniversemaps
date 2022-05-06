#Read all store fronts and dump to CSV
#Author: Chris Cummings
#License: MIT

import sys
import json
import os
import settings

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
    for district_record in settings.MAP['districts']:
        try:
            with open(f"{settings.DATA_DIR}/{district_record['code']}.json","rb") as f:
                district = json.load(f)
                for slot in district['slots']:
                    if slot['slot'] == 65538:  #65538 is the magic number for a store!
                        txt = ",".join([str(slot.get(x,"")) for x in COLUMNS])
                        outf.write(txt + "\n")
        except Exception as err:
            print(f"Error loading {district_record['code']}: {err}")

#Dirty copy and paste to generate TABSV instead
with open("stores.tab","wt") as outf:
    txt = '\t'.join(COLUMNS) 
    outf.write(txt + "\n")
    for district_record in settings.MAP['districts']:
        try:
            with open(f"{settings.DATA_DIR}/{district_record['code']}.json","rb") as f:
                district = json.load(f)
                for slot in district['slots']:
                    if slot['slot'] == 65538:  #65538 is the magic number for a store!
                        txt = "\t".join([str(slot.get(x,"")) for x in COLUMNS])
                        outf.write(txt + "\n")
        except Exception as err:
            print(f"Error loading {district_record['code']}: {err}")
