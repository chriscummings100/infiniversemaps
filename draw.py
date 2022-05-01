#Experimental script to generate map images from downloaded scripts
#Author: Chris Cummings
#License: MIT

import sys
import json
import os
from PIL import Image, ImageDraw


#Date to download
MAP_DATE = "2022-05-01"
DATA_DIR = os.path.abspath(f"data/{MAP_DATE}")

#load map file
with open (f"{DATA_DIR}/map.json","rb") as f:
    MAP = json.load(f)

#centre and scale at which to draw map
DRAW_SIZE = 1000
DRAW_CENTRE_X = 0
DRAW_CENTRE_Y = 0

#transforms a point from Infiniverse coords to pixel position in image
def transformpoint(point, draw):
    res = (
        draw.im.size[0]*(0.5+(point[0]-DRAW_CENTRE_X)/DRAW_SIZE),
        draw.im.size[1]*(0.5+(point[1]-DRAW_CENTRE_Y)/DRAW_SIZE),
    )
    return res

#draws a polygon from Infiniverse data to the image, applying correct transforms
def drawpoly(draw, poly, fill, line, width=1):
    if poly and len(poly) >= 3:
        transformed = [transformpoint(x,draw) for x in poly]
        draw.polygon(transformed, fill, line, width)

#loads a district and draws it into the image
def drawdistrict(code, draw):
    with open(f"{DATA_DIR}/{code}.json","rb") as f:
        print("Drawing district" + code)

        district = json.load(f)

        bounding_poly = district['district']['boundingpoly']

        new_poly = [transformpoint(x,draw) for x in bounding_poly]

        draw.polygon(new_poly, (100,100,100), (255,255,255))

        for subdistrict in district['subdistricts']:
            drawpoly(draw, subdistrict['innerpoly'], (150,150,150), None)

        for building in district['buildings']:
            drawpoly(draw, building['boundingpoly'], (200,200,200), (0,0,0))


#create a new image
with Image.new("RGB", (512, 512), (255, 255, 255)) as im:
    draw = ImageDraw.Draw(im)

    #iterate over all districts and draw any that are within 500m of draw rectangle (a district is never more
    # than 300m in size so this is a nice safe bound)
    for district in MAP['districts']:
        x = district['centre'][0]
        y = district['centre'][1]
        if  (x > (DRAW_CENTRE_X-DRAW_SIZE-500)) and (x < (DRAW_CENTRE_X+DRAW_SIZE+500)) and (y > (DRAW_CENTRE_Y-DRAW_SIZE-500)) and (y < (DRAW_CENTRE_Y+DRAW_SIZE+500)):
            drawdistrict(district['code'],draw)

    #save and draw the image
    im.save("image.jpg")
    im.show()
