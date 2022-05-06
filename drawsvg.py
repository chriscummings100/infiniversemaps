# Experimental script to generate map images from downloaded scripts
# Author: Chris Cummings / Andrea Benvenuti
# License: MIT
import argparse
import sys
import json
import os
import drawSvg
import settings
import math

# centre and scale at which to drawPIL map
# The [-904,-484] coordinates are grand central
DRAW_SIZE = 1000
DRAW_CENTRE_X = -904
DRAW_CENTRE_Y = -484
IMAGE_SIZE = 512

FONT_SIZE = 8 * IMAGE_SIZE / DRAW_SIZE

# transforms a point from Infiniverse coords to pixel position in image
def transformpoint(point, d):
    res = (
        d.width * (0.5 + (point[0] - DRAW_CENTRE_X) / DRAW_SIZE),
        d.height * (0.5 + (point[1] - DRAW_CENTRE_Y) / DRAW_SIZE),
    )
    return res

# draws a polygon from Infiniverse data to the image, applying correct transforms
def drawpoly(draw, poly, fill, line, width=1):
    if poly and len(poly) >= 3:
        transformed = [transformpoint(x, draw) for x in poly]
        #flatten array to list of values
        out = [item for t in transformed for item in t]
        #duplicate first point at end, so stroke border goes whole way round 
        out.append(out[0])
        out.append(out[1])
        d.append(drawSvg.Lines(*out, fill=fill, stroke=line, stroke_width=width))

#draws a ground polygon with the correct colour + style
def drawground(draw, poly, ground_type):
    if poly and len(poly) >= 3:
        col = '#969696'
        if ground_type == 'Grass':
            col ='#80B63A'
        elif ground_type == 'Water':
            col =  '#68BAC8'
        drawpoly(draw, poly, col, None)

# loads a district and draws it into the image
def drawdistrict(code, draw):
    with open(f"{settings.DATA_DIR}/{code}.json", "rb") as f:
        # print("Drawing district" + code)

        district = json.load(f)
        junctions = { x['code']: x for x in district['junctions'] }

        bounding_poly = district['district']['boundingpoly']

        new_poly = [transformpoint(x, draw) for x in bounding_poly]
        item = new_poly.pop(0)

        sx = item[0]
        sy = item[1]
        out = [item for t in new_poly for item in t]

        # use first line to show white border to highlight cell edges
        # drawPIL.polygon(new_poly, (100,100,100), (255,255,255))
        draw.append(drawSvg.Lines(sx,sy, *out, fill='#646464', stroke=None))

        for subdistrict in district['subdistricts']:
            drawground(draw,subdistrict['curbpoly'],'Curb')
            drawground(draw,subdistrict['outerpoly'],subdistrict['outerfloor'])
            drawground(draw,subdistrict['innerpoly'],subdistrict['innerfloor'])

        for building in district['buildings']:
            drawpoly(draw, building['boundingpoly'], '#68BAC8', None)


        for street in district['streets']:
            junclist = street['junctions']
            ja = junctions[junclist[0]]
            jb = junctions[junclist[-1]]
            japos = ja['pos']
            jbpos = jb['pos']

            centre = transformpoint( [(japos[0]+jbpos[0])*0.5, (japos[1]+jbpos[1])*0.5], draw)

            dx = jbpos[1]-japos[1]
            dy = jbpos[0]-japos[0]
            
            ang = math.degrees(math.atan2(dx,-dy))
            if dy > 0:
                ang += 180

            fs = FONT_SIZE

            if ja['code'].startswith('VJ') and jb['code'].startswith('VJ'):
                fs *= 2

            draw.append(drawSvg.Text(street['name'], fs, centre[0], centre[1], fill='black', font_weight="bold", text_anchor="middle", valign="middle",
                transform=f'rotate({ang},{centre[0]},{-centre[1]})'))

            

            pass


# create a new image


d = drawSvg.Drawing(IMAGE_SIZE, IMAGE_SIZE)

# iterate over all districts and drawPIL any that are within 500m of drawPIL rectangle (a district is never more
# than 300m in size so this is a nice safe bound)
for district in settings.MAP['districts']:
    x = district['centre'][0]
    y = district['centre'][1]
    if (x > (DRAW_CENTRE_X - DRAW_SIZE - 500)) and (x < (DRAW_CENTRE_X + DRAW_SIZE + 500)) and (
            y > (DRAW_CENTRE_Y - DRAW_SIZE - 500)) and (y < (DRAW_CENTRE_Y + DRAW_SIZE + 500)):
        drawdistrict(district['code'], d)

# save and draw the image
d.setPixelScale(1)  # Set number of pixels per geometry unit
d.saveSvg('image.svg')

