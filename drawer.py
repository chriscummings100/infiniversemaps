from ast import Str
from dis import dis
from enum import Enum
from locale import resetlocale
from math import dist
from typing import Tuple, List, Union
from PIL import Image, ImageDraw, ImageFont
from infiniverse import Color, DistrictInfo, FloorType, Map, Polygon, Vector2, loaddistrictinfo, loadmap
import settings
import math
import os

class BaseRenderer:

    scale: Vector2
    centre: Vector2
    dimensions: Vector2
    
    def __init__(self, dimensions: Vector2, scale: Vector2, centre: Vector2) -> None:
        self.scale = scale
        self.centre = centre
        self.dimensions = dimensions

    #helper that transforms a scaled point into image space
    def transformpoint(self, point: Vector2)->Vector2:
        res = (
            self.dimensions[0]*(0.5+(point[0]-self.centre[0])*self.scale[0]),
            self.dimensions[1]*(0.5+(point[1]-self.centre[1])*self.scale[1]),
        )
        return res

    #overridable function to draw a polygon
    def drawpoly(self, poly: Polygon, fill: Color | None, line: Color | None, width: float=1):
        raise NotImplementedError()

    def drawtext(self, text: str, pos: Vector2, size: float, color: Color, angle: float):
        raise NotImplementedError()


    #overridable function to save
    def save(name: Str):
        raise NotImplementedError()
  
def col2tuple(color: Color | None):
    if color:
        if isinstance(color,str):
            if not color.startswith("#"):
                raise NameError("Not web color")
            if len(color) == 7:
                return (int(color[1:3],16),int(color[3:5],16),int(color[5:7],16))
            elif len(color) == 9:
                return (int(color[1:3],16),int(color[3:5],16),int(color[5:7],16),int(color[7:9],16))
            else: 
                raise NameError("Invalid color")
        elif isinstance(color,tuple):
            return color 
        else:
            raise NameError("Invalid color")
    else:
        return None

class SVGRenderer(BaseRenderer):
    def __init__(self, dimensions: Vector2=(512,512), scale: Vector2=(1,1), centre: Vector2=(0,0)) -> None:
        super().__init__(dimensions,scale,centre)

class PixelRenderer(BaseRenderer):

    img: Image
    draw: ImageDraw
    font: ImageFont


    def __init__(self, dimensions: Vector2=(512,512), scale: Vector2=(1,1), centre: Vector2=(0,0)) -> None:        
        super().__init__(dimensions,(scale[0],-scale[1]),centre)
        self.img = Image.new("RGB", self.dimensions, (20, 20, 20))
        self.draw = ImageDraw.Draw(self.img)
        self.font = ImageFont.truetype('arial.ttf',40)

    def drawpoly(self, poly: Polygon, fill: Color | None, line: Color | None, width: float=1):
        if poly and len(poly) >= 3:
            transformed = [self.transformpoint(x) for x in poly]
            self.draw.polygon(transformed,col2tuple(fill), col2tuple(line), width)

    def drawtext(self, text: str, pos: Vector2, size: float, color: Color, angle: float):
        with Image.new("L", (512,512), 0) as text_mask:
            text_draw = ImageDraw.Draw(text_mask)         
            text_draw.text((256,256), text, 255, align='center', anchor='mm', font=self.font)

            #calculate resizing to apply to generated image to get value where size of 1 means text is 1m high
            resized = 512*size/40          
            resized = resized * self.scale[0] * self.dimensions[0]

            #transform pos to top left of target image + make it all integers
            pos = self.transformpoint(pos)
            pos = (pos[0]-resized/2, pos[1]-resized/2)
            pos = (int(pos[0]),int(pos[1]))
            resized = int(resized)

            with text_mask.resize((resized,resized), resample=Image.Resampling.BILINEAR) as resized_mask:
                with resized_mask.rotate(-angle, resample=Image.Resampling.BILINEAR) as rotated_mask:
                    self.img.paste(color,pos, rotated_mask)

    def save(self, name: str):
        self.img.save(name)
        #self.img.show()


class DrawMode(Enum):
    svg = 'svg',
    pixel = 'pixel'

class Drawer:
    renderer: BaseRenderer

    def __init__(self, mode: DrawMode, dimensions: Vector2=(512,512), scale: Vector2=(1,1), centre: Vector2=(0,0)) -> None:
        if mode == DrawMode.svg:
            self.renderer = SVGRenderer(dimensions,scale,centre)
        else:
            self.renderer = PixelRenderer(dimensions,scale,centre)        

    def _drawground(self, poly: Polygon, ground_type: FloorType):
        if poly and len(poly) >= 3:
            col = '#969696'
            if ground_type == FloorType.Grass:
                col ='#80B63A'
            elif ground_type == FloorType.Water:
                col =  '#68BAC8'
            self.renderer.drawpoly(poly, col, None)

    def drawDistrictBaseLayer(self, district: DistrictInfo) -> None:
        self.renderer.drawpoly(district.district.boundingpoly, '#646464', None)

        for subdistrict in district.subdistricts:
            self._drawground(subdistrict.curbpoly,'Curb')
            self._drawground(subdistrict.outerpoly,subdistrict.outerfloor)
            self._drawground(subdistrict.innerpoly,subdistrict.innerfloor)

        for building in district.buildings:
            self.renderer.drawpoly(building.boundingpoly, (200,200,200), None)

    def drawDistrictStreets(self, district: DistrictInfo) -> None:


        junctions = { x.code: x for x in district.junctions }
        for street in district.streets:
            #get the first+last junction ids from the street, then use to get the junctions and their positions
            junclist = street.junctions
            ja = junctions[junclist[0]]
            jb = junctions[junclist[-1]]
            japos = ja.pos
            jbpos = jb.pos

            #calculate centre of the street (average of start+end positions)
            centre = ((japos[0]+jbpos[0])*0.5, (japos[1]+jbpos[1])*0.5)

            #calculate vector from start to end, and use to work out orientation of street
            dx = jbpos[1]-japos[1]
            dy = jbpos[0]-japos[0]                    
            ang = math.degrees(math.atan2(dx,-dy))

            #if dy is > 0, text will end up right->left, so rotate 180 degrees
            if dy > 0:
                ang += 180

            #choose font size, doubling if both junctions start with 'VJ', meaning they are large 
            #district level junctions, rather than smaller inter-district junctions
            fs = 5
            if ja.code.startswith('VJ') and jb.code.startswith('VJ'):
                fs *= 2

            #draw the text
            self.renderer.drawtext(street.name, centre, fs, (255,255,255), ang )

    def drawRegion(self, map: Map):

        centre = self.renderer.centre
        size = 0.5/self.renderer.scale[0]

        todraw: List[DistrictInfo] = []
        for cell in map.districts:
            x = cell.centre[0]
            y = cell.centre[1]
            if  (x > (centre[0]-size-250)) and (x < (centre[0]+size+250)) and (y > (centre[1]-size-250)) and (y < (centre[1]+size+250)):
                fn = f"{settings.DATA_DIR}/{cell.code}.json"
                try:
                    print(f"Loading {fn}")
                    todraw.append(loaddistrictinfo(fn))
                    district = loaddistrictinfo(fn)
                    self.drawDistrictBaseLayer(district)
                except Exception as err:
                    print(f"Error {fn}: {err}")

        for district in todraw:
            try:
                print(f"Drawing base layer {district.district.code}")
                self.drawDistrictBaseLayer(district)
            except Exception as err:
                print(f"Error {district.district.code}")

        for district in todraw:
            try:
                print(f"Drawing streets {district.district.code}")
                self.drawDistrictStreets(district)
            except Exception as err:
                print(f"Error {district.district.code}")



    def save(self, name: str):
        self.renderer.save(name)    

if __name__ == "__main__":

    map = loadmap(f"{settings.DATA_DIR}/map.json")

    step = 32000
    while step < 40000:
        os.makedirs(f"map/{step}",exist_ok=True)
        max = step*math.ceil(10000/step)
        min = -max
        for x in range(min,max+step,step):
            for y in range(min,max+step,step):
                drawer = Drawer(DrawMode.pixel, (1024,1024), (1/step,1/step), (x,y))
                drawer.drawRegion(map)
                drawer.save(f"map/{step}/{x}_{y}.jpg")
        step *= 2