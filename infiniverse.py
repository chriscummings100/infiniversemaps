
import json
from typing import List, Tuple
from enum import Enum
import settings
import os

Vector2 = Tuple[float]
Vector3 = Tuple[float]
Color = Tuple[float] | str
Polygon = List[Vector2]

class FloorType(Enum):
    NoFloor = "None"
    Concrete = "Concrete"
    Grass = "Grass"
    Water = "Water"

class BuildingType(Enum):
    SkyScraper = "skyscraper"
    TowerBlock = "towerblock"

def readFloorType(input: str)->FloorType:
    if input:
        return FloorType(input)
    else:
        return None

def readVector2(input: List[float])->Vector2:
    if input:
        return (input[0],input[1])
    else:
        return None

def readVector3(input: List[float])->Vector3:
    return (input[0],input[1],input[2])

def readPolygon2(input: List[List[float]])->Polygon:
    if input:
        return [readVector2(x) for x in input]
    else:
        return None


class Junction:
    code: str
    pos: Vector2

    def __init__(self, input) -> None:
        self.code = input['code']
        self.pos = readVector2(input['pos'])  

class Street:
    code: str 
    name: str 
    junctions: List[str]

    def __init__(self, input) -> None:
        self.code = input['code']
        self.name = input['name']
        self.junctions = input['junctions']

class BaseNode:
    cellx: int 
    celly: int 
    code: str 

    def __init__(self, input) -> None:
        self.cellx = input['cellx']
        self.celly = input['celly']
        self.code = input['code']
      

class Slot(BaseNode):
    subdistrictid: int 
    buildingid: int 
    slot: int 
    owner: str 
    location: str
    domain: str
    destination: str 
    iconurl: str 

    def __init__(self, input) -> None:
        super().__init__(input)
        self.subdistrictid = input['subdistrictid']
        self.buildingid = input['buildingid']
        self.slot = input['slot']
        self.owner = input['owner']
        self.location = input['location']
        self.domain = input['domain']
        self.destination = input['destination']
        self.iconurl = input['iconurl']


class Building(BaseNode):
    centre: Vector2
    subdistrictid: int 
    buildingid: int 
    buildingstyle: BuildingType
    name: str
    doorcentre: Vector2
    doordir: Vector2
    storefront: bool
    street: str
    street_number: int
    boundingpoly: Polygon

    def __init__(self, input) -> None:
        super().__init__(input)
        self.centre = readVector2(input['centre'])
        self.subdistrictid = input['subdistrictid']
        self.buildingid = input['buildingid']
        self.buildingstyle = BuildingType(input['buildingstyle'])
        self.name = input['name']
        self.doorcentre = readVector2(input['doorcentre'])
        self.doordir = readVector2(input['doorcentre'])
        self.storefront = input['storefront']
        self.street = input['street']
        self.street_number = input['street_number']
        self.boundingpoly = readPolygon2(input['boundingpoly'])

class Subdistrict(BaseNode):
    centre: Vector2
    subdistrictid: int 
    innerfloor: FloorType
    outerfloor: FloorType
    innerpoly: Polygon
    outerpoly: Polygon
    curbpoly: Polygon

    def __init__(self, input) -> None:
        super().__init__(input)
        self.centre = readVector2(input['centre'])
        self.subdistrictid = input['subdistrictid']
        self.innerfloor = readFloorType(input['innerfloor'])
        self.outerfloor = readFloorType(input['outerfloor'])
        self.innerpoly = readPolygon2(input['innerpoly'])
        self.outerpoly = readPolygon2(input['outerpoly'])
        self.curbpoly = readPolygon2(input['curbpoly'])

class District(BaseNode):
    centre: Vector2
    boundingpoly: Polygon

    def __init__(self, input) -> None:
        super().__init__(input)
        self.centre = readVector2(input['centre'])
        self.boundingpoly = readPolygon2(input['boundingpoly'])

class DistrictInfo:
    district: District
    subdistricts: List[Subdistrict]
    buildings: List[Building]
    slots: List[Slot]
    streets: List[Street]
    junctions: List[Junction]

    def __init__(self,input) -> None:
        self.district = District(input['district'])
        self.subdistricts = [Subdistrict(x) for x in input['subdistricts']]
        self.buildings = [Building(x) for x in input['buildings']]
        self.slots = [Slot(x) for x in input['slots']]
        self.streets = [Street(x) for x in input['streets']]
        self.junctions = [Junction(x) for x in input['junctions']]

class MapRecord:
    cellx: int 
    celly: int 
    code: str 
    centre: Vector2
    url: str

    def __init__(self, input) -> None:
        self.cellx = input['cellx']
        self.celly = input['celly']
        self.code = input['code']
        self.centre = readVector2(input['centre'])
        self.url = input['url']

class Map:
    districts: List[MapRecord]

    def __init__(self, input) -> None:
        self.districts = [MapRecord(x) for x in input['districts']]

def parsemap(text: str)->Map:
    return Map(json.loads(text))

def loadmap(fn: str)->Map:
    with open(fn,"rb") as f:
        return parsemap(f.read())

def parsedistrictinfo(text: str)->Map:
    return DistrictInfo(json.loads(text))

def loaddistrictinfo(fn: str)->Map:
    with open(fn,"rb") as f:
        return parsedistrictinfo(f.read())

if __name__ == "__main__":

    map = loadmap(f"{settings.DATA_DIR}/map.json")
    for district in map.districts:
        fn = f"{settings.DATA_DIR}/{district.code}.json"
        if os.path.exists(fn):
            print(f"Load {fn}")
            loaddistrictinfo(fn)
        else:
            print(f"Missing {fn}")


#

#### ROOT
#* districts: [ MapDistrictRecord ]
#
#### MapDistrictRecord
#* cellx: x id of cell
#* celly: y id of cell
#* centrex: x position of district cell centre
#* centrey: y position of district cell centre
#* code: zip code of district (based on x and y id)
#* url: download url of district info
#
### district file
#Each district has an associated json file whose url is found in map.json
#
#### ROOT
#* district: District
#* subdistricts: [ SubDistrict ]
#* buildings: [ Building ]
#* slots: [ Slot ]
#* streets: [ Street ]
#* junctions: [ Junction ]
#
#### Common properties to district/subdistrict/building/slot
#* cellx: x id of containing cell
#* celly: y id of containing cell
#* centre: Vector2, centre of node
#* code: zip code
#
#### District
#* boundingpoly: Polygon, outer polygon covered by district
#
#### Subdistrict
#* subdistrictid: numeric id of subdistrict inside district
#* innerfloor: FloorType, interior floor type
#* outerfloor: FloorType, exterior floor type
#* innerpoly: Polygon, interior floor polygon
#* outerpoly: Polygon, exterior floor polygon
#* curbpoly: Polygon, curb polygon
#
#### Building
#* subdistrictid: numeric id of containing subdistrict
#* buildingid: numeric id of building inside subdistrict
#* buildingstyle: BuildingType, type of building
#* name: human readable building name
#* doorcentre: Vector2, centre of door 
#* doordir: Vector2, direction door faces
#* storefront: Boolean, does building have storefront
#* street: Street zip code
#* street_number: Number of building on street
#* boundingpoly: Polygon, Boundary of building structure
#
#### Slot
#* subdistrictid: numeric id of containing subdistrict
#* buildingid: numeric id of containing building
#* slot: slot index (0 = penthouse, 65538 = storefront)
#* owner: Owner name
#* location: Target location name
#* domain: Target location metaverse name
#* destination: Target location url
#
#### Street
#* code: zip code
#* name: street name
#* junctions: [ junction zip code ]
#
#### Junction
#* code: zip code
#* pos: Vector2
#
#### Polygon
#* [ Vector2 ]
#
#### Vector2
#* [ x coord, y coord]
#
#### FloorType (enum)
#* [ Concrete | Grass | Water ]