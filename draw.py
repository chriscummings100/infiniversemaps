#Experimental script to generate map images from downloaded scripts
#Author: Chris Cummings
#License: MIT

import sys
import json
import os
from PIL import Image, ImageDraw
import settings

#centre and scale at which to draw map
#The [-904,-484] coordinates are grand central
DRAW_SIZE = 1500
DRAW_CENTRE_X = -904
DRAW_CENTRE_Y = -484
IMAGE_SIZE = 4096

#these numbers roughly draw the whole map at 4k resolution
#DRAW_SIZE = 20000
#DRAW_CENTRE_X = 0
#DRAW_CENTRE_Y = 0
#IMAGE_SIZE = 4096



#transforms a point from Infiniverse coords to pixel position in image
def transformpoint(point, draw):
    res = (
        draw.im.size[0]*(0.5+(point[0]-DRAW_CENTRE_X)/DRAW_SIZE),
        draw.im.size[1]*(0.5+-(point[1]-DRAW_CENTRE_Y)/DRAW_SIZE),
    )
    return res

#draws a polygon from Infiniverse data to the image, applying correct transforms
def drawpoly(draw, poly, fill, line, width=1):
    if poly and len(poly) >= 3:
        transformed = [transformpoint(x,draw) for x in poly]
        draw.polygon(transformed, fill, line, width)

#draws a ground polygon with the correct colour + style
def drawground(draw, poly, ground_type):
    if poly and len(poly) >= 3:
        col = (150,150,150)
        if ground_type == 'Grass':
            col = (50,150,50)
        elif ground_type == 'Water':
            col = (75,75,200)
        drawpoly(draw, poly, col, None)

#loads a district and draws it into the image
def drawdistrict(code, draw):
    try:
        with open(f"{settings.DATA_DIR}/{code}.json","rb") as f:
            print("Drawing district" + code)

            district = json.load(f)

            bounding_poly = district['district']['boundingpoly']

            new_poly = [transformpoint(x,draw) for x in bounding_poly]

            #use first line to show white border to highlight cell edges
            #draw.polygon(new_poly, (100,100,100), (255,255,255))
            draw.polygon(new_poly, (100,100,100), None)

            for subdistrict in district['subdistricts']:
                drawground(draw,subdistrict['curbpoly'],'Curb')
                drawground(draw,subdistrict['outerpoly'],subdistrict['outerfloor'])
                drawground(draw,subdistrict['innerpoly'],subdistrict['innerfloor'])

            for building in district['buildings']:
                drawpoly(draw, building['boundingpoly'], (200,200,200), None)

    except Exception as err:
        print(err)

#create a new image
with Image.new("RGB", (IMAGE_SIZE, IMAGE_SIZE), (255, 255, 255)) as im:
    draw = ImageDraw.Draw(im)

    #iterate over all districts and draw any that are within 500m of draw rectangle (a district is never more
    # than 300m in size so this is a nice safe bound)
    for district in settings.MAP['districts']:
        x = district['centre'][0]
        y = district['centre'][1]
        if  (x > (DRAW_CENTRE_X-DRAW_SIZE-500)) and (x < (DRAW_CENTRE_X+DRAW_SIZE+500)) and (y > (DRAW_CENTRE_Y-DRAW_SIZE-500)) and (y < (DRAW_CENTRE_Y+DRAW_SIZE+500)):
            drawdistrict(district['code'],draw)

    #save and draw the image
    im.save("image.jpg")
    im.show()
